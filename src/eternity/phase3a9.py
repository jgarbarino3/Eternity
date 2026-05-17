"""Phase 3A.9 relative-only diagnostic packet utilities."""

from __future__ import annotations

import csv
import json
import math
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_phase3a8_relative_policy(path: Path) -> dict[str, Any]:
    policy = yaml.safe_load(path.read_text(encoding="utf-8"))
    if policy.get("phase_id") != "Phase 3A.8":
        raise ValueError("Phase 3A.9 requires a Phase 3A.8 relative-only policy")
    if policy.get("policy") != "relative_only_diagnostic":
        raise ValueError("Phase 3A.9 requires policy: relative_only_diagnostic")
    if policy.get("can_feed_serious_core") is not False:
        raise ValueError("Phase 3A.9 policy must keep can_feed_serious_core false")
    return policy


def _load_comparison_table(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError("comparison table is empty")

    parsed = []
    for row in rows:
        measurement = row.get("measurement", row.get("holdout"))
        if measurement is None:
            raise ValueError("comparison table must include measurement or holdout column")
        parsed.append(
            {
                "wavelength_nm": float(row["wavelength_nm"]),
                "prediction": float(row["prediction"]),
                "measurement": float(measurement),
                "residual": float(row["residual"]),
                "measurement_ref": row.get("measurement_ref", ""),
            }
        )
    return parsed


def _minmax(values: list[float]) -> list[float]:
    low = min(values)
    high = max(values)
    if math.isclose(high, low):
        return [0.0 for _ in values]
    span = high - low
    return [(value - low) / span for value in values]


def _pearson(a_values: list[float], b_values: list[float]) -> float | None:
    if len(a_values) != len(b_values) or len(a_values) < 2:
        return None
    mean_a = sum(a_values) / len(a_values)
    mean_b = sum(b_values) / len(b_values)
    numerator = sum(
        (a - mean_a) * (b - mean_b) for a, b in zip(a_values, b_values, strict=True)
    )
    denom_a = math.sqrt(sum((a - mean_a) ** 2 for a in a_values))
    denom_b = math.sqrt(sum((b - mean_b) ** 2 for b in b_values))
    if math.isclose(denom_a, 0.0) or math.isclose(denom_b, 0.0):
        return None
    return numerator / (denom_a * denom_b)


def _trend_direction(values: list[float]) -> str:
    delta = values[-1] - values[0]
    if math.isclose(delta, 0.0, abs_tol=1e-12):
        return "flat"
    if delta > 0:
        return "increasing"
    return "decreasing"


def _dip(values: list[float], wavelengths: list[float]) -> dict[str, float]:
    index = min(range(len(values)), key=values.__getitem__)
    return {"wavelength_nm": wavelengths[index], "value": values[index]}


def _diagnostic_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    predictions = [row["prediction"] for row in rows]
    measurements = [row["measurement"] for row in rows]
    prediction_norm = _minmax(predictions)
    measurement_norm = _minmax(measurements)
    output = []
    for row, pred_norm, meas_norm in zip(rows, prediction_norm, measurement_norm, strict=True):
        output.append(
            {
                "wavelength_nm": row["wavelength_nm"],
                "prediction": row["prediction"],
                "measurement": row["measurement"],
                "prediction_minmax": pred_norm,
                "measurement_minmax": meas_norm,
                "relative_shape_delta": pred_norm - meas_norm,
                "measurement_ref": row["measurement_ref"],
            }
        )
    return output


def build_phase3a9_packet(run_dir: Path, policy_path: Path) -> dict[str, Any]:
    policy = load_phase3a8_relative_policy(policy_path)
    comparison_rows = _load_comparison_table(run_dir / "comparison_table.csv")
    claim_status = _load_json(run_dir / "claim_status.json")
    validation_summary = _load_json(run_dir / "validation_summary.json")

    wavelengths = [row["wavelength_nm"] for row in comparison_rows]
    predictions = [row["prediction"] for row in comparison_rows]
    measurements = [row["measurement"] for row in comparison_rows]
    prediction_norm = _minmax(predictions)
    measurement_norm = _minmax(measurements)
    prediction_trend = _trend_direction(prediction_norm)
    measurement_trend = _trend_direction(measurement_norm)
    prediction_dip = _dip(predictions, wavelengths)
    measurement_dip = _dip(measurements, wavelengths)
    shape_delta = [
        pred - meas for pred, meas in zip(prediction_norm, measurement_norm, strict=True)
    ]
    mean_abs_shape_delta = sum(abs(value) for value in shape_delta) / len(shape_delta)
    max_abs_shape_delta = max(abs(value) for value in shape_delta)

    return {
        "phase_id": "Phase 3A.9",
        "title": "Relative-Only Diagnostic Run Packet",
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "inputs": {
            "run_dir": str(run_dir),
            "policy_path": str(policy_path),
            "comparison_table": str(run_dir / "comparison_table.csv"),
            "source_claim_status": claim_status.get("status"),
            "source_validation_status": validation_summary.get("status"),
        },
        "decision": {
            "status": "relative_only_diagnostic_packet_ready",
            "normalization_basis": "relative_intensity_only",
            "can_feed_serious_core": False,
            "can_promote_calibrated_linear_evidence": False,
            "claim_status_ceiling": "weak_within_dataset_holdout",
            "existing_run_promotion": "forbidden",
            "historical_run": run_dir.name,
        },
        "allowed_diagnostics": policy.get("allowed_diagnostics", []),
        "forbidden_uses": policy.get("forbidden_uses", []),
        "diagnostics": {
            "wavelength_window_nm": [min(wavelengths), max(wavelengths)],
            "points": len(comparison_rows),
            "shape_correlation_minmax": _pearson(prediction_norm, measurement_norm),
            "mean_abs_relative_shape_delta": mean_abs_shape_delta,
            "max_abs_relative_shape_delta": max_abs_shape_delta,
            "prediction_dip": prediction_dip,
            "measurement_dip": measurement_dip,
            "dip_offset_nm": prediction_dip["wavelength_nm"] - measurement_dip["wavelength_nm"],
            "prediction_trend_direction": prediction_trend,
            "measurement_trend_direction": measurement_trend,
            "trend_direction_agreement": prediction_trend == measurement_trend,
        },
        "historical_residual_context": validation_summary.get("metrics", {}),
        "interpretation_boundary": (
            "These diagnostics compare relative spectral shape only. They are not "
            "absolute-reflectance validation, pass/fail thresholds, or calibrated evidence."
        ),
        "table": _diagnostic_rows(comparison_rows),
    }


def diagnostic_table_csv(packet: dict[str, Any]) -> str:
    rows = packet["table"]
    fieldnames = [
        "wavelength_nm",
        "prediction",
        "measurement",
        "prediction_minmax",
        "measurement_minmax",
        "relative_shape_delta",
        "measurement_ref",
    ]
    output = []
    output.append(",".join(fieldnames))
    for row in rows:
        output.append(
            ",".join(
                [
                    f"{row['wavelength_nm']:.9g}",
                    f"{row['prediction']:.9g}",
                    f"{row['measurement']:.9g}",
                    f"{row['prediction_minmax']:.9g}",
                    f"{row['measurement_minmax']:.9g}",
                    f"{row['relative_shape_delta']:.9g}",
                    str(row["measurement_ref"]),
                ]
            )
        )
    return "\n".join(output) + "\n"


def diagnostic_markdown(packet: dict[str, Any]) -> str:
    decision = packet["decision"]
    diagnostics = packet["diagnostics"]
    return "\n".join(
        [
            "# Phase 3A.9 Relative-Only Diagnostic Run Packet",
            "",
            "## Decision",
            "",
            f"- Status: `{decision['status']}`",
            f"- Normalization basis: `{decision['normalization_basis']}`",
            f"- Can feed serious core: `{decision['can_feed_serious_core']}`",
            (
                "- Can promote calibrated evidence: "
                f"`{decision['can_promote_calibrated_linear_evidence']}`"
            ),
            f"- Claim-status ceiling: `{decision['claim_status_ceiling']}`",
            f"- Existing run promotion: `{decision['existing_run_promotion']}`",
            "",
            "## Relative Diagnostics",
            "",
            f"- Wavelength window: `{diagnostics['wavelength_window_nm'][0]}` to "
            f"`{diagnostics['wavelength_window_nm'][1]}` nm",
            f"- Points: `{diagnostics['points']}`",
            f"- Min-max shape correlation: `{diagnostics['shape_correlation_minmax']}`",
            f"- Mean absolute relative-shape delta: "
            f"`{diagnostics['mean_abs_relative_shape_delta']}`",
            f"- Max absolute relative-shape delta: `{diagnostics['max_abs_relative_shape_delta']}`",
            f"- Prediction dip: `{diagnostics['prediction_dip']['wavelength_nm']}` nm",
            f"- Measurement dip: `{diagnostics['measurement_dip']['wavelength_nm']}` nm",
            f"- Dip offset: `{diagnostics['dip_offset_nm']}` nm",
            f"- Prediction trend: `{diagnostics['prediction_trend_direction']}`",
            f"- Measurement trend: `{diagnostics['measurement_trend_direction']}`",
            f"- Trend agreement: `{diagnostics['trend_direction_agreement']}`",
            "",
            "## Boundary",
            "",
            packet["interpretation_boundary"],
            "",
            "Allowed diagnostics: "
            + ", ".join(f"`{item}`" for item in packet["allowed_diagnostics"])
            + ".",
            "",
            "Forbidden uses: "
            + ", ".join(f"`{item}`" for item in packet["forbidden_uses"])
            + ".",
            "",
        ]
    )


def write_phase3a9_packet(output_dir: Path, packet: dict[str, Any]) -> tuple[Path, Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase3a9_relative_only_diagnostic_packet.json"
    md_path = output_dir / "phase3a9_relative_only_diagnostic_packet.md"
    csv_path = output_dir / "phase3a9_relative_only_diagnostic_table.csv"
    json_packet = dict(packet)
    json_packet.pop("table", None)
    json_path.write_text(json.dumps(json_packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(diagnostic_markdown(packet), encoding="utf-8")
    csv_path.write_text(diagnostic_table_csv(packet), encoding="utf-8")
    return json_path, md_path, csv_path
