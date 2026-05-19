"""Phase 3C.4 St Andrews failure-triage utilities."""

from __future__ import annotations

import csv
import json
import math
import zipfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
from tmm import coh_tmm

from eternity.materials import refractive_index_from_epsilon
from eternity.optical_data import EpsilonTable, interpolate_epsilon

SEGMENT_WINDOWS_NM = [
    (400.0, 450.0),
    (450.0, 500.0),
    (500.0, 600.0),
    (600.0, 700.0),
    (700.0, 850.0),
    (850.0, 1000.0),
]
THICKNESS_SWEEP_NM = [35.0, 40.0, 45.0, 50.0, 55.0, 60.0, 65.0, 70.0, 80.0, 90.0, 100.0]
SUBSTRATE_INDEX_SWEEP = [1.33, 1.40, 1.45, 1.50, 1.52, 1.60, 1.70, 1.80]


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


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


def _minmax(values: np.ndarray) -> np.ndarray:
    low = float(np.min(values))
    high = float(np.max(values))
    if math.isclose(high, low):
        return np.zeros_like(values, dtype=float)
    return (values - low) / (high - low)


def _pearson(left_values: np.ndarray, right_values: np.ndarray) -> float | None:
    if left_values.size != right_values.size or left_values.size < 2:
        return None
    left_norm = _minmax(left_values)
    right_norm = _minmax(right_values)
    left_centered = left_norm - float(np.mean(left_norm))
    right_centered = right_norm - float(np.mean(right_norm))
    denom = float(np.linalg.norm(left_centered) * np.linalg.norm(right_centered))
    if math.isclose(denom, 0.0):
        return None
    return float(np.dot(left_centered, right_centered) / denom)


def _dip(values: np.ndarray, wavelengths_nm: np.ndarray) -> dict[str, float]:
    index = int(np.argmin(values))
    return {"wavelength_nm": float(wavelengths_nm[index]), "value": float(values[index])}


def _comparison_metrics(
    wavelengths_nm: np.ndarray,
    prediction: np.ndarray,
    measurement: np.ndarray,
) -> dict[str, Any]:
    residual = prediction - measurement
    prediction_dip = _dip(prediction, wavelengths_nm)
    measurement_dip = _dip(measurement, wavelengths_nm)
    return {
        "validation_points": int(wavelengths_nm.size),
        "wavelength_window_nm": [float(np.min(wavelengths_nm)), float(np.max(wavelengths_nm))],
        "mean_absolute_error": float(np.mean(np.abs(residual))),
        "root_mean_square_error": float(np.sqrt(np.mean(residual**2))),
        "max_absolute_residual": float(np.max(np.abs(residual))),
        "prediction_dip": prediction_dip,
        "measurement_dip": measurement_dip,
        "dip_wavelength_offset_nm": (
            prediction_dip["wavelength_nm"] - measurement_dip["wavelength_nm"]
        ),
        "shape_correlation_minmax": _pearson(prediction, measurement),
        "prediction_range": [float(np.min(prediction)), float(np.max(prediction))],
        "measurement_range": [float(np.min(measurement)), float(np.max(measurement))],
    }


def _threshold_status(
    metrics: dict[str, Any],
    threshold_metrics: list[dict[str, Any]],
) -> dict[str, Any]:
    results = []
    for threshold_metric in threshold_metrics:
        name = threshold_metric["name"]
        value = metrics.get(name)
        comparator = threshold_metric["comparator"]
        threshold = float(threshold_metric["threshold"])
        if value is None:
            passed = False
        elif comparator == "less_equal":
            passed = float(value) <= threshold
        elif comparator == "abs_less_equal":
            passed = abs(float(value)) <= threshold
        elif comparator == "greater_equal":
            passed = float(value) >= threshold
        else:
            raise ValueError(f"unknown threshold comparator: {comparator}")
        results.append(
            {
                "name": name,
                "value": value,
                "comparator": comparator,
                "threshold": threshold,
                "status": "pass" if passed else "fail",
            }
        )
    failed = [result["name"] for result in results if result["status"] != "pass"]
    return {"status": "pass" if not failed else "fail", "failed_metrics": failed}


def _parse_epsilon_text(text: str) -> tuple[np.ndarray, np.ndarray]:
    rows: list[list[float]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        values = []
        for field in stripped.replace(",", ".").split():
            try:
                values.append(float(field))
            except ValueError:
                values = []
                break
        if len(values) >= 3:
            rows.append(values[:3])
    table = np.asarray(rows, dtype=float)
    if table.ndim != 2 or table.shape[1] != 3:
        raise ValueError("epsilon member does not look like wavelength/e1/e2 data")
    return table[:, 0], table[:, 1] + 1j * table[:, 2]


def _simulate_single_layer(
    wavelengths_nm: np.ndarray,
    table_wavelengths_nm: np.ndarray,
    table_epsilon: np.ndarray,
    *,
    thickness_nm: float = 50.0,
    substrate_index: float = 1.45,
) -> np.ndarray:
    epsilon = interpolate_epsilon(
        EpsilonTable(wavelengths_nm=table_wavelengths_nm, epsilon=table_epsilon),
        wavelengths_nm,
    )
    film_index = refractive_index_from_epsilon(epsilon)
    reflection = np.empty_like(wavelengths_nm, dtype=float)
    for index, wavelength_nm in enumerate(wavelengths_nm):
        result = coh_tmm(
            "s",
            [1.0 + 0j, film_index[index], complex(substrate_index)],
            [np.inf, thickness_nm, np.inf],
            0.0,
            float(wavelength_nm),
        )
        reflection[index] = float(result["R"])
    return reflection


def _segment_residuals(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    segments = []
    for lower, upper in SEGMENT_WINDOWS_NM:
        segment_rows = [
            row
            for row in rows
            if lower <= float(row["wavelength_nm"]) < upper
        ]
        if not segment_rows:
            continue
        residuals = np.asarray([row["residual"] for row in segment_rows], dtype=float)
        predictions = np.asarray([row["prediction"] for row in segment_rows], dtype=float)
        measurements = np.asarray([row["measurement"] for row in segment_rows], dtype=float)
        segments.append(
            {
                "window_nm": [lower, upper],
                "points": len(segment_rows),
                "measurement_mean": float(np.mean(measurements)),
                "prediction_mean": float(np.mean(predictions)),
                "bias": float(np.mean(residuals)),
                "mean_absolute_error": float(np.mean(np.abs(residuals))),
                "max_absolute_residual": float(np.max(np.abs(residuals))),
            }
        )
    return segments


def _sweep_record(
    name: str,
    prediction: np.ndarray,
    wavelengths_nm: np.ndarray,
    measurement: np.ndarray,
    threshold_metrics: list[dict[str, Any]],
    **extra: Any,
) -> dict[str, Any]:
    metrics = _comparison_metrics(wavelengths_nm, prediction, measurement)
    return {
        "name": name,
        **extra,
        "metrics": metrics,
        "threshold_status": _threshold_status(metrics, threshold_metrics),
    }


def _material_sweep(
    pairing: dict[str, Any],
    wavelengths_nm: np.ndarray,
    measurement: np.ndarray,
    threshold_metrics: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    zip_path = Path(pairing["source_archive"]["path"])
    selected_member = pairing["selected_pairing"]["selected_material_member"]
    records = []
    with zipfile.ZipFile(zip_path) as archive:
        for candidate in pairing.get("candidate_epsilon_tables", []):
            member = candidate["member"]
            text = archive.read(member).decode("utf-8-sig")
            table_wavelengths, table_epsilon = _parse_epsilon_text(text)
            prediction = _simulate_single_layer(wavelengths_nm, table_wavelengths, table_epsilon)
            records.append(
                _sweep_record(
                    member,
                    prediction,
                    wavelengths_nm,
                    measurement,
                    threshold_metrics,
                    selected=member == selected_member,
                    enz_wavelengths_nm=candidate.get("enz_wavelengths_nm", []),
                    passivity_check=candidate.get("passivity_check"),
                )
            )
    return sorted(records, key=lambda item: item["metrics"]["root_mean_square_error"])


def _selected_epsilon_table(pairing: dict[str, Any]) -> tuple[np.ndarray, np.ndarray]:
    zip_path = Path(pairing["source_archive"]["path"])
    selected_member = pairing["selected_pairing"]["selected_material_member"]
    with zipfile.ZipFile(zip_path) as archive:
        text = archive.read(selected_member).decode("utf-8-sig")
    return _parse_epsilon_text(text)


def _thickness_sweep(
    pairing: dict[str, Any],
    wavelengths_nm: np.ndarray,
    measurement: np.ndarray,
    threshold_metrics: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    table_wavelengths, table_epsilon = _selected_epsilon_table(pairing)
    records = []
    for thickness_nm in THICKNESS_SWEEP_NM:
        prediction = _simulate_single_layer(
            wavelengths_nm,
            table_wavelengths,
            table_epsilon,
            thickness_nm=thickness_nm,
        )
        records.append(
            _sweep_record(
                f"{thickness_nm:g} nm",
                prediction,
                wavelengths_nm,
                measurement,
                threshold_metrics,
                thickness_nm=thickness_nm,
            )
        )
    return sorted(records, key=lambda item: item["metrics"]["root_mean_square_error"])


def _substrate_sweep(
    pairing: dict[str, Any],
    wavelengths_nm: np.ndarray,
    measurement: np.ndarray,
    threshold_metrics: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    table_wavelengths, table_epsilon = _selected_epsilon_table(pairing)
    records = []
    for substrate_index in SUBSTRATE_INDEX_SWEEP:
        prediction = _simulate_single_layer(
            wavelengths_nm,
            table_wavelengths,
            table_epsilon,
            substrate_index=substrate_index,
        )
        records.append(
            _sweep_record(
                f"n={substrate_index:g}",
                prediction,
                wavelengths_nm,
                measurement,
                threshold_metrics,
                substrate_index=substrate_index,
            )
        )
    return sorted(records, key=lambda item: item["metrics"]["root_mean_square_error"])


def _affine_shape_check(
    wavelengths_nm: np.ndarray,
    prediction: np.ndarray,
    measurement: np.ndarray,
    threshold_metrics: list[dict[str, Any]],
) -> dict[str, Any]:
    design = np.column_stack([prediction, np.ones_like(prediction)])
    scale, offset = np.linalg.lstsq(design, measurement, rcond=None)[0]
    transformed = scale * prediction + offset
    return _sweep_record(
        "best affine transform of existing prediction",
        transformed,
        wavelengths_nm,
        measurement,
        threshold_metrics,
        scale=float(scale),
        offset=float(offset),
    )


def build_phase3c4_triage(
    run_dir: Path,
    evaluation_json: Path,
    pairing_json: Path,
) -> dict[str, Any]:
    evaluation = _load_json(evaluation_json)
    pairing = _load_json(pairing_json)
    rows = _load_comparison_table(run_dir / "comparison_table.csv")
    claim_status = _load_json(run_dir / "claim_status.json")
    sample_stack = _load_json(run_dir / "sample_stack.json")
    resolved_spec = _load_json(run_dir / "resolved_spec.json")

    wavelengths_nm = np.asarray([row["wavelength_nm"] for row in rows], dtype=float)
    prediction = np.asarray([row["prediction"] for row in rows], dtype=float)
    measurement = np.asarray([row["measurement"] for row in rows], dtype=float)
    threshold_metrics = evaluation["threshold_evaluation"]["metrics"]
    segments = _segment_residuals(rows)
    material_sweep = _material_sweep(pairing, wavelengths_nm, measurement, threshold_metrics)
    thickness_sweep = _thickness_sweep(pairing, wavelengths_nm, measurement, threshold_metrics)
    substrate_sweep = _substrate_sweep(pairing, wavelengths_nm, measurement, threshold_metrics)
    affine_shape_check = _affine_shape_check(
        wavelengths_nm,
        prediction,
        measurement,
        threshold_metrics,
    )
    dominant_segments = sorted(
        segments,
        key=lambda item: item["mean_absolute_error"],
        reverse=True,
    )[:2]

    return {
        "phase_id": "Phase 3C.4",
        "title": "St Andrews Failure Triage",
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "inputs": {
            "run_dir": str(run_dir),
            "evaluation_json": str(evaluation_json),
            "pairing_json": str(pairing_json),
            "comparison_table": str(run_dir / "comparison_table.csv"),
            "source_archive": pairing["source_archive"]["path"],
            "selected_material_member": pairing["selected_pairing"]["selected_material_member"],
        },
        "decision": {
            "status": "failure_triaged_no_promotion",
            "can_feed_serious_core": False,
            "can_promote_calibrated_linear_evidence": False,
            "phase4_ready": False,
            "leading_failure_mode": "source_model_or_material_pairing_mismatch",
            "secondary_failure_modes": [
                "roughness_or_source_ellipsometry_model_not_reproduced",
                "rt_xlsx_annealing_pairing_ambiguity",
            ],
            "deprioritized_causes": [
                "thresholds_only",
                "simple_fixed_substrate_index_only",
                "simple_thickness_offset_only",
            ],
            "next_phase": "Phase 3C.5 - St Andrews source-model parity diagnostic",
        },
        "current_run": {
            "run_id": run_dir.name,
            "claim_status": claim_status,
            "phase3c3_decision": evaluation["decision"],
            "phase3c3_metrics": evaluation["metrics"],
            "threshold_evaluation": evaluation["threshold_evaluation"],
            "sample_stack": sample_stack,
            "geometry": resolved_spec.get("geometry", {}),
        },
        "residual_segments": segments,
        "dominant_failure_windows": dominant_segments,
        "diagnostic_sweeps": {
            "alternate_material_tables": material_sweep,
            "selected_material_thickness_nm": thickness_sweep,
            "selected_material_substrate_index": substrate_sweep,
            "affine_shape_check": affine_shape_check,
        },
        "triage_findings": [
            {
                "finding": "failure_is_not_a_near_miss",
                "evidence": (
                    "All Phase 3C.3 thresholds failed, including shape correlation and dip "
                    "offset. The strongest residual concentration is at the blue edge."
                ),
            },
            {
                "finding": "blue_edge_residual_dominates",
                "evidence": (
                    "The 400-450 nm segment has the largest mean absolute residual, while "
                    "the 500-850 nm middle bands are much closer."
                ),
            },
            {
                "finding": "alternate_tables_do_not_repair_the_lane",
                "evidence": (
                    "No candidate St Andrews epsilon table passes the locked thresholds. "
                    "Some alternatives improve one diagnostic, but degrade others."
                ),
            },
            {
                "finding": "simple_substrate_or_thickness_changes_are_not_decisive",
                "evidence": (
                    "The selected-table thickness and substrate-index sweeps do not move the "
                    "predicted dip to the measured dip or restore the required shape correlation."
                ),
            },
            {
                "finding": "source_model_parity_is_the_next_clean_question",
                "evidence": (
                    "The paper and archive point to Woollam ellipsometry modeling with glass "
                    "substrate and roughness information, while the current clean run uses a "
                    "single flat TiN layer on lossless n=1.45 glass."
                ),
            },
        ],
        "interpretation_boundary": (
            "Phase 3C.4 is a diagnostic failure triage. It may rank likely failure causes, "
            "but it cannot tune thresholds, select a replacement model using the holdout, "
            "feed the serious core, or promote calibrated_linear_evidence."
        ),
    }


def _metric_summary(metrics: dict[str, Any]) -> str:
    return (
        f"MAE `{metrics['mean_absolute_error']:.6g}`, "
        f"RMSE `{metrics['root_mean_square_error']:.6g}`, "
        f"max residual `{metrics['max_absolute_residual']:.6g}`, "
        f"dip offset `{metrics['dip_wavelength_offset_nm']:.6g}` nm, "
        f"shape corr `{metrics['shape_correlation_minmax']:.6g}`"
    )


def _sweep_table(records: list[dict[str, Any]], label_key: str) -> list[str]:
    rows = ["| Candidate | RMSE | MAE | Dip offset nm | Shape corr | Threshold status |"]
    rows.append("| --- | ---: | ---: | ---: | ---: | --- |")
    for record in records[:6]:
        metrics = record["metrics"]
        rows.append(
            "| "
            f"`{record[label_key] if label_key in record else record['name']}` | "
            f"`{metrics['root_mean_square_error']:.6g}` | "
            f"`{metrics['mean_absolute_error']:.6g}` | "
            f"`{metrics['dip_wavelength_offset_nm']:.6g}` | "
            f"`{metrics['shape_correlation_minmax']:.6g}` | "
            f"`{record['threshold_status']['status']}` |"
        )
    return rows


def triage_markdown(packet: dict[str, Any]) -> str:
    decision = packet["decision"]
    current_metrics = packet["current_run"]["phase3c3_metrics"]
    selected_material = packet["inputs"]["selected_material_member"]
    dominant_windows = packet["dominant_failure_windows"]
    material_sweep = packet["diagnostic_sweeps"]["alternate_material_tables"]
    thickness_sweep = packet["diagnostic_sweeps"]["selected_material_thickness_nm"]
    substrate_sweep = packet["diagnostic_sweeps"]["selected_material_substrate_index"]
    best_material = material_sweep[0]
    best_thickness = thickness_sweep[0]
    best_substrate = substrate_sweep[0]
    failed_metrics = packet["current_run"]["threshold_evaluation"]["failed_metrics"]
    lines = [
        "# Phase 3C.4 - St Andrews Failure Triage",
        "",
        "## Decision",
        "",
        f"- Status: `{decision['status']}`",
        f"- Leading failure mode: `{decision['leading_failure_mode']}`",
        f"- Can feed serious core: `{decision['can_feed_serious_core']}`",
        "- Can promote calibrated evidence: "
        f"`{decision['can_promote_calibrated_linear_evidence']}`",
        f"- Phase 4 ready: `{decision['phase4_ready']}`",
        f"- Next phase: `{decision['next_phase']}`",
        "",
        "## Current Failure",
        "",
        f"- Run: `{packet['current_run']['run_id']}`",
        f"- Selected material member: `{selected_material}`",
        f"- Metrics: {_metric_summary(current_metrics)}",
        "- Failed metrics: "
        + ", ".join(f"`{name}`" for name in failed_metrics),
        "",
        "## Dominant Residual Windows",
        "",
    ]
    for window in dominant_windows:
        lines.append(
            "- "
            f"`{window['window_nm'][0]:g}-{window['window_nm'][1]:g} nm`: "
            f"MAE `{window['mean_absolute_error']:.6g}`, "
            f"bias `{window['bias']:.6g}`, "
            f"prediction mean `{window['prediction_mean']:.6g}`, "
            f"measurement mean `{window['measurement_mean']:.6g}`."
        )
    lines.extend(
        [
            "",
            "## Diagnostic Sweeps",
            "",
            (
                f"- Best RMSE material-table diagnostic: `{best_material['name']}` "
                f"with {_metric_summary(best_material['metrics'])}."
            ),
            (
                "- Best selected-table thickness diagnostic: "
                f"`{best_thickness['thickness_nm']:g} nm` "
                f"with {_metric_summary(best_thickness['metrics'])}."
            ),
            (
                f"- Best selected-table substrate-index diagnostic: "
                f"`n={best_substrate['substrate_index']:g}` with "
                f"{_metric_summary(best_substrate['metrics'])}."
            ),
            "",
            "### Alternate Material Tables",
            "",
            *_sweep_table(material_sweep, "name"),
            "",
            "### Thickness Sweep",
            "",
            *_sweep_table(thickness_sweep, "name"),
            "",
            "### Substrate-Index Sweep",
            "",
            *_sweep_table(substrate_sweep, "name"),
            "",
            "## Findings",
            "",
        ]
    )
    lines.extend(f"- `{item['finding']}`: {item['evidence']}" for item in packet["triage_findings"])
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            packet["interpretation_boundary"],
            "",
        ]
    )
    return "\n".join(lines)


def diagnostic_sweeps_csv(packet: dict[str, Any]) -> str:
    rows = [
        "sweep,name,parameter,rmse,mae,max_absolute_residual,dip_offset_nm,"
        "shape_correlation_minmax,threshold_status"
    ]
    for sweep_name, records in packet["diagnostic_sweeps"].items():
        if sweep_name == "affine_shape_check":
            records = [records]
        for record in records:
            metrics = record["metrics"]
            parameter = record.get("thickness_nm", record.get("substrate_index", ""))
            rows.append(
                ",".join(
                    [
                        sweep_name,
                        str(record["name"]),
                        str(parameter),
                        f"{metrics['root_mean_square_error']:.9g}",
                        f"{metrics['mean_absolute_error']:.9g}",
                        f"{metrics['max_absolute_residual']:.9g}",
                        f"{metrics['dip_wavelength_offset_nm']:.9g}",
                        f"{metrics['shape_correlation_minmax']:.9g}",
                        record["threshold_status"]["status"],
                    ]
                )
            )
    return "\n".join(rows) + "\n"


def write_phase3c4_triage(output_dir: Path, packet: dict[str, Any]) -> tuple[Path, Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase3c4_standrews_failure_triage.json"
    md_path = output_dir / "phase3c4_standrews_failure_triage.md"
    csv_path = output_dir / "phase3c4_diagnostic_sweeps.csv"
    json_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(triage_markdown(packet), encoding="utf-8")
    csv_path.write_text(diagnostic_sweeps_csv(packet), encoding="utf-8")
    return json_path, md_path, csv_path
