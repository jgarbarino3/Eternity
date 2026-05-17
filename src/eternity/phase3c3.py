"""Phase 3C.3 St Andrews threshold-lock evaluation utilities."""

from __future__ import annotations

import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from eternity.claim_status import ClaimStatus

REQUIRED_METRICS = [
    "mean_absolute_error",
    "root_mean_square_error",
    "max_absolute_residual",
    "dip_wavelength_offset_nm",
    "shape_correlation_minmax",
]

STANDREWS_REFLECTANCE_MEASUREMENT_REF = "public_standrews_tin_50nm_reflectance_measurement"
STANDREWS_TRANSMITTANCE_MEASUREMENT_REF = (
    "public_standrews_tin_50nm_transmittance_measurement"
)
PHASE3C2_HISTORICAL_RUN_ID = "run_42fe0ad6dd295019"


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_phase3c3_policy(path: Path) -> dict[str, Any]:
    policy = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(policy, dict):
        raise ValueError("Phase 3C.3 threshold policy must be a mapping")
    return policy


def _parse_datetime(value: str | None) -> datetime | None:
    if value is None:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _load_comparison_table(path: Path) -> list[dict[str, float | str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError("comparison table is empty")

    parsed: list[dict[str, float | str]] = []
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
    return [(value - low) / (high - low) for value in values]


def _pearson(left_values: list[float], right_values: list[float]) -> float | None:
    if len(left_values) != len(right_values) or len(left_values) < 2:
        return None
    left_mean = sum(left_values) / len(left_values)
    right_mean = sum(right_values) / len(right_values)
    numerator = sum(
        (left - left_mean) * (right - right_mean)
        for left, right in zip(left_values, right_values, strict=True)
    )
    left_norm = math.sqrt(sum((left - left_mean) ** 2 for left in left_values))
    right_norm = math.sqrt(sum((right - right_mean) ** 2 for right in right_values))
    if math.isclose(left_norm, 0.0) or math.isclose(right_norm, 0.0):
        return None
    return numerator / (left_norm * right_norm)


def _dip(values: list[float], wavelengths: list[float]) -> dict[str, float]:
    index = min(range(len(values)), key=values.__getitem__)
    return {"wavelength_nm": wavelengths[index], "value": values[index]}


def comparison_metrics(rows: list[dict[str, float | str]]) -> dict[str, Any]:
    wavelengths = [float(row["wavelength_nm"]) for row in rows]
    predictions = [float(row["prediction"]) for row in rows]
    measurements = [float(row["measurement"]) for row in rows]
    residuals = [float(row["residual"]) for row in rows]
    prediction_dip = _dip(predictions, wavelengths)
    measurement_dip = _dip(measurements, wavelengths)
    return {
        "validation_points": len(rows),
        "wavelength_window_nm": [min(wavelengths), max(wavelengths)],
        "mean_absolute_error": sum(abs(value) for value in residuals) / len(residuals),
        "root_mean_square_error": math.sqrt(
            sum(value * value for value in residuals) / len(residuals)
        ),
        "max_absolute_residual": max(abs(value) for value in residuals),
        "prediction_dip": prediction_dip,
        "measurement_dip": measurement_dip,
        "dip_wavelength_offset_nm": (
            prediction_dip["wavelength_nm"] - measurement_dip["wavelength_nm"]
        ),
        "shape_correlation_minmax": _pearson(_minmax(predictions), _minmax(measurements)),
    }


def phase3c3_policy_allows_reflectance_normalization(
    policy: dict[str, Any],
    holdout_measurement_ref: str,
) -> bool:
    return (
        policy.get("phase_id") == "Phase 3C.3"
        and policy.get("status") == "locked_for_future_clean_run"
        and policy.get("normalization_basis", {}).get("status")
        == "absolute_fraction_accepted_for_reflectance"
        and policy.get("primary_channel", {}).get("measurement_ref") == holdout_measurement_ref
        and holdout_measurement_ref == STANDREWS_REFLECTANCE_MEASUREMENT_REF
    )


def _policy_thresholds(policy: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(item.get("name")): item
        for item in policy.get("required_metrics", [])
        if isinstance(item, dict)
    }


def validate_phase3c3_policy_for_run(
    policy: dict[str, Any],
    run_dir: Path,
    run_created_at: str | None,
    pairing_status: str | None,
    holdout_measurement_ref: str | None,
) -> dict[str, Any]:
    blocking_reasons: list[str] = []
    if policy.get("phase_id") != "Phase 3C.3":
        blocking_reasons.append("wrong_phase_id")
    if policy.get("status") != "locked_for_future_clean_run":
        blocking_reasons.append("policy_not_locked_for_future_clean_run")
    if policy.get("applies_to_existing_runs") is not False:
        blocking_reasons.append("policy_applies_to_existing_runs")

    run_id = run_dir.name
    excluded_run_ids = set(policy.get("excluded_run_ids", []))
    excluded_run_refs = {str(ref) for ref in policy.get("excluded_run_refs", [])}
    if run_id in excluded_run_ids or str(run_dir) in excluded_run_refs:
        blocking_reasons.append("run_excluded_by_policy")
    if run_id == PHASE3C2_HISTORICAL_RUN_ID:
        blocking_reasons.append("historical_phase3c2_run_not_promotable")

    policy_time = _parse_datetime(policy.get("created_at"))
    run_time = _parse_datetime(run_created_at)
    if policy_time is None:
        blocking_reasons.append("policy_created_at_missing")
    if run_time is None:
        blocking_reasons.append("run_created_at_missing")
    if policy_time is not None and run_time is not None and policy_time > run_time:
        blocking_reasons.append("policy_created_after_run")

    approval = policy.get("approval", {})
    if (
        not approval.get("approver")
        or not approval.get("approved_at")
        or approval.get("locked_before_run") is not True
    ):
        blocking_reasons.append("policy_not_approved_and_locked_before_run")

    thresholds = _policy_thresholds(policy)
    missing_metrics = [name for name in REQUIRED_METRICS if name not in thresholds]
    if missing_metrics:
        blocking_reasons.append("missing_required_metrics:" + ",".join(missing_metrics))

    if pairing_status != "candidate_supported_reflectance_only":
        blocking_reasons.append("pairing_status_below_candidate_supported_reflectance_only")

    primary = policy.get("primary_channel", {})
    if primary.get("kind") != "reflectance":
        blocking_reasons.append("primary_channel_not_reflectance")
    if primary.get("measurement_ref") != holdout_measurement_ref:
        blocking_reasons.append("primary_channel_not_holdout_measurement")
    if not phase3c3_policy_allows_reflectance_normalization(
        policy,
        holdout_measurement_ref or "",
    ):
        blocking_reasons.append("reflectance_normalization_not_approved")

    for channel in policy.get("auxiliary_channels", []):
        if (
            channel.get("measurement_ref") == STANDREWS_TRANSMITTANCE_MEASUREMENT_REF
            and channel.get("use") != "diagnostic_only"
        ):
            blocking_reasons.append("transmittance_not_diagnostic_only")

    return {
        "status": "pass" if not blocking_reasons else "blocked",
        "blocking_reasons": blocking_reasons,
        "run_id": run_id,
    }


def _evaluate_thresholds(
    policy: dict[str, Any],
    metrics: dict[str, Any],
) -> dict[str, Any]:
    thresholds = _policy_thresholds(policy)
    results = []
    for name in REQUIRED_METRICS:
        if name not in thresholds:
            results.append(
                {
                    "name": name,
                    "value": metrics.get(name),
                    "comparator": "missing",
                    "threshold": None,
                    "status": "fail",
                }
            )
            continue
        threshold_spec = thresholds[name]
        value = metrics.get(name)
        threshold = float(threshold_spec["threshold"])
        comparator = threshold_spec["comparator"]
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
    return {
        "status": "pass" if not failed else "fail",
        "failed_metrics": failed,
        "metrics": results,
    }


def build_phase3c3_evaluation(
    run_dir: Path,
    policy_path: Path,
    pairing_json: Path,
) -> dict[str, Any]:
    policy = load_phase3c3_policy(policy_path)
    pairing = _load_json(pairing_json)
    provenance = _load_json(run_dir / "provenance.json")
    claim_status = _load_json(run_dir / "claim_status.json")
    resolved_spec = _load_json(run_dir / "resolved_spec.json")
    threshold_gate = _load_json(run_dir / "validation_gates" / "thresholds_predeclared.json")
    normalization_gate = _load_json(run_dir / "validation_gates" / "normalization_gate.json")
    no_fit_leakage = _load_json(run_dir / "validation_gates" / "no_fit_leakage.json")
    comparison_rows = _load_comparison_table(run_dir / "comparison_table.csv")

    validation = resolved_spec.get("validation", {})
    pairing_status = pairing.get("selected_pairing", {}).get(
        "pairing_status",
        pairing.get("decision", {}).get("status"),
    )
    policy_gate = validate_phase3c3_policy_for_run(
        policy,
        run_dir,
        provenance.get("created_at"),
        pairing_status,
        validation.get("holdout_measurement_ref"),
    )
    metrics = comparison_metrics(comparison_rows)
    threshold_evaluation = _evaluate_thresholds(policy, metrics)

    gate_blockers = []
    if threshold_gate.get("status") != "pass":
        gate_blockers.append("thresholds_predeclared_gate_not_pass")
    if normalization_gate.get("status") != "pass":
        gate_blockers.append("normalization_gate_not_pass")
    if no_fit_leakage.get("status") != "pass":
        gate_blockers.append("no_fit_leakage_gate_not_pass")
    if claim_status.get("can_feed_serious_core") is not False:
        gate_blockers.append("claim_status_can_feed_serious_core")
    if policy_gate["status"] != "pass":
        gate_blockers.extend(policy_gate["blocking_reasons"])

    if gate_blockers:
        decision_status = "blocked_invalid_policy_or_run_order"
        clean_run_ready_for_phase4 = False
        claim_status_decision = ClaimStatus.WEAK_WITHIN_DATASET_HOLDOUT.value
    elif threshold_evaluation["status"] == "pass":
        decision_status = "clean_run_passed_thresholds_ready_for_phase4_review"
        clean_run_ready_for_phase4 = True
        claim_status_decision = ClaimStatus.WEAK_WITHIN_DATASET_HOLDOUT.value
    else:
        decision_status = "clean_run_failed_thresholds"
        clean_run_ready_for_phase4 = False
        claim_status_decision = ClaimStatus.FAILED_VALIDATION.value

    return {
        "phase_id": "Phase 3C.3",
        "title": "St Andrews Threshold Lock + Clean Run Decision",
        "generated_at": datetime.now().astimezone().isoformat(),
        "inputs": {
            "run_dir": str(run_dir),
            "policy": str(policy_path),
            "pairing_json": str(pairing_json),
            "run_created_at": provenance.get("created_at"),
            "historical_run_excluded": PHASE3C2_HISTORICAL_RUN_ID,
        },
        "decision": {
            "status": decision_status,
            "can_feed_serious_core": False,
            "existing_phase3c2_run_promotable": False,
            "clean_run_ready_for_phase4_review": clean_run_ready_for_phase4,
            "claim_status_decision": claim_status_decision,
            "next_step": (
                "Phase 4 promotion review"
                if clean_run_ready_for_phase4
                else "inspect pairing/material-model mismatch or park St Andrews as diagnostic"
            ),
        },
        "metrics": metrics,
        "threshold_evaluation": threshold_evaluation,
        "gates": {
            "policy_gate": policy_gate,
            "thresholds_predeclared": threshold_gate,
            "normalization_gate": normalization_gate,
            "no_fit_leakage": no_fit_leakage,
            "claim_status": claim_status,
        },
        "boundary": (
            "Phase 3C.3 may decide whether a clean run is ready for Phase 4 review, "
            "but it cannot feed the serious core or promote to calibrated_linear_evidence."
        ),
    }


def _evaluation_markdown(evaluation: dict[str, Any]) -> str:
    decision = evaluation["decision"]
    metrics = evaluation["metrics"]
    wavelength_window = metrics["wavelength_window_nm"]
    threshold_rows = [
        (
            f"| `{item['name']}` | `{item['value']}` | `{item['comparator']}` "
            f"| `{item['threshold']}` | `{item['status']}` |"
        )
        for item in evaluation["threshold_evaluation"]["metrics"]
    ]
    return "\n".join(
        [
            "# Phase 3C.3 - St Andrews Clean Run Evaluation",
            "",
            "## Decision",
            "",
            f"- Status: `{decision['status']}`",
            f"- Can feed serious core: `{decision['can_feed_serious_core']}`",
            f"- Claim-status decision: `{decision['claim_status_decision']}`",
            "- Clean run ready for Phase 4 review: "
            f"`{decision['clean_run_ready_for_phase4_review']}`",
            "",
            "## Metrics",
            "",
            f"- Points: `{metrics['validation_points']}`",
            f"- Wavelength window: `{wavelength_window[0]}`-`{wavelength_window[1]}` nm",
            f"- Dip offset: `{metrics['dip_wavelength_offset_nm']}` nm",
            f"- Shape correlation: `{metrics['shape_correlation_minmax']}`",
            "",
            "| Metric | Value | Comparator | Threshold | Status |",
            "| --- | --- | --- | --- | --- |",
            *threshold_rows,
            "",
            "## Boundary",
            "",
            evaluation["boundary"],
            "",
        ]
    )


def write_phase3c3_evaluation(
    output_dir: Path,
    evaluation: dict[str, Any],
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase3c3_clean_run_evaluation.json"
    md_path = output_dir / "phase3c3_clean_run_evaluation.md"
    json_path.write_text(
        json.dumps(evaluation, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(_evaluation_markdown(evaluation), encoding="utf-8")
    return json_path, md_path
