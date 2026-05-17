"""Phase 3C.2 St Andrews validation-candidate audit utilities."""

from __future__ import annotations

import csv
import json
import math
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from eternity.registry import load_registry

REQUIRED_METRICS = [
    "mean_absolute_error",
    "root_mean_square_error",
    "max_absolute_residual",
    "dip_wavelength_offset",
    "shape_correlation_minmax",
]


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


def _minmax(values: list[float]) -> list[float]:
    low = min(values)
    high = max(values)
    if math.isclose(high, low):
        return [0.0 for _ in values]
    span = high - low
    return [(value - low) / span for value in values]


def _pearson(left_values: list[float], right_values: list[float]) -> float | None:
    if len(left_values) != len(right_values) or len(left_values) < 2:
        return None
    mean_left = sum(left_values) / len(left_values)
    mean_right = sum(right_values) / len(right_values)
    numerator = sum(
        (left - mean_left) * (right - mean_right)
        for left, right in zip(left_values, right_values, strict=True)
    )
    denom_left = math.sqrt(sum((left - mean_left) ** 2 for left in left_values))
    denom_right = math.sqrt(sum((right - mean_right) ** 2 for right in right_values))
    if math.isclose(denom_left, 0.0) or math.isclose(denom_right, 0.0):
        return None
    return numerator / (denom_left * denom_right)


def _dip(values: list[float], wavelengths: list[float]) -> dict[str, float]:
    index = min(range(len(values)), key=values.__getitem__)
    return {"wavelength_nm": wavelengths[index], "value": values[index]}


def _comparison_diagnostics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    wavelengths = [row["wavelength_nm"] for row in rows]
    predictions = [row["prediction"] for row in rows]
    measurements = [row["measurement"] for row in rows]
    prediction_norm = _minmax(predictions)
    measurement_norm = _minmax(measurements)
    prediction_dip = _dip(predictions, wavelengths)
    measurement_dip = _dip(measurements, wavelengths)
    return {
        "points": len(rows),
        "wavelength_window_nm": [min(wavelengths), max(wavelengths)],
        "prediction_dip": prediction_dip,
        "measurement_dip": measurement_dip,
        "dip_wavelength_offset_nm": (
            prediction_dip["wavelength_nm"] - measurement_dip["wavelength_nm"]
        ),
        "shape_correlation_minmax": _pearson(prediction_norm, measurement_norm),
    }


def _build_future_threshold_policy(
    run_dir: Path,
    resolved_spec: dict[str, Any],
) -> dict[str, Any]:
    validation = resolved_spec.get("validation", {})
    return {
        "phase_id": "Phase 3C.2",
        "policy": "future_threshold_policy",
        "status": "pending_pro_or_user_lock_before_clean_run",
        "created_at": datetime.now(tz=UTC).isoformat(),
        "applies_to_existing_run": False,
        "residuals_inspected_before_policy": True,
        "residuals_inspected_run_refs": [str(run_dir)],
        "policy_may_promote_calibrated_evidence": False,
        "requires_clean_run_after_policy_lock": True,
        "wavelength_window_nm": {"min_nm": 400.0, "max_nm": 1000.0},
        "primary_channel": {
            "kind": "reflectance",
            "measurement_ref": validation.get("holdout_measurement_ref"),
            "use": "candidate_holdout_for_future_clean_run",
        },
        "auxiliary_channels": [
            {
                "kind": "transmittance",
                "measurement_ref": measurement_ref,
                "use": "diagnostic_only",
            }
            for measurement_ref in validation.get("auxiliary_measurement_refs", [])
        ],
        "required_metrics": [
            {"name": name, "threshold": None, "status": "pending"}
            for name in REQUIRED_METRICS
        ],
        "approval": {
            "approver": None,
            "approved_at": None,
            "locked_before_run": False,
            "thresholds_ref": None,
        },
        "forbidden_uses": [
            "using_run_42fe0ad6dd295019_residuals_to_tune_cutoffs",
            "retroactive_promotion_of_existing_run",
            "serious_core_evidence_before_clean_run",
            "calibrated_linear_evidence_without_predeclared_thresholds",
        ],
    }


def validate_phase3c2_future_policy(
    policy: dict[str, Any],
    run_created_at: str | None = None,
) -> dict[str, Any]:
    """Validate that a Phase 3C.2 threshold policy remains future-only."""

    blocking_reasons: list[str] = []
    if policy.get("phase_id") != "Phase 3C.2":
        blocking_reasons.append("wrong_phase_id")
    if policy.get("status") != "pending_pro_or_user_lock_before_clean_run":
        blocking_reasons.append("policy_not_pending")
    if policy.get("applies_to_existing_run") is not False:
        blocking_reasons.append("policy_applies_to_existing_run")
    if policy.get("policy_may_promote_calibrated_evidence") is not False:
        blocking_reasons.append("policy_claims_promotion_authority")
    if policy.get("residuals_inspected_before_policy") is not True:
        blocking_reasons.append("residual_inspection_status_not_recorded")

    metric_names = {metric.get("name") for metric in policy.get("required_metrics", [])}
    missing_metrics = [name for name in REQUIRED_METRICS if name not in metric_names]
    if missing_metrics:
        blocking_reasons.append("missing_required_metrics:" + ",".join(missing_metrics))

    approval = policy.get("approval", {})
    if policy.get("policy_may_promote_calibrated_evidence") and (
        not approval.get("approver")
        or not approval.get("approved_at")
        or approval.get("locked_before_run") is not True
    ):
        blocking_reasons.append("promotion_without_pre_run_approval")

    created_at = policy.get("created_at")
    if run_created_at and created_at:
        try:
            policy_time = datetime.fromisoformat(created_at)
            run_time = datetime.fromisoformat(run_created_at)
        except ValueError:
            blocking_reasons.append("unparseable_policy_or_run_timestamp")
        else:
            if policy_time > run_time:
                blocking_reasons.append("policy_created_after_existing_run")

    return {
        "status": "future_only_ready" if not blocking_reasons else "blocked_for_existing_run",
        "existing_run_promotion_allowed": False,
        "future_clean_run_required": True,
        "blocking_reasons": blocking_reasons,
    }


def build_phase3c2_audit(
    run_dir: Path,
    pairing_json: Path,
    registry_path: Path = Path("lab_data/registry.yaml"),
) -> dict[str, Any]:
    pairing = _load_json(pairing_json)
    claim_status = _load_json(run_dir / "claim_status.json")
    validation_summary = _load_json(run_dir / "validation_summary.json")
    resolved_spec = _load_json(run_dir / "resolved_spec.json")
    provenance = _load_json(run_dir / "provenance.json")
    thresholds_gate = _load_json(
        run_dir / "validation_gates" / "thresholds_predeclared.json"
    )
    normalization_gate = _load_json(run_dir / "validation_gates" / "normalization_gate.json")
    no_fit_leakage = _load_json(run_dir / "validation_gates" / "no_fit_leakage.json")
    comparison_rows = _load_comparison_table(run_dir / "comparison_table.csv")
    registry = load_registry(registry_path)

    validation = resolved_spec.get("validation", {})
    split_ref = validation.get("split_ref")
    if split_ref not in registry.splits:
        raise ValueError(f"split not found in registry: {split_ref}")

    pairing_status = pairing.get("selected_pairing", {}).get(
        "pairing_status",
        pairing.get("decision", {}).get("status"),
    )
    pairing_gate = {
        "status": (
            "pass"
            if pairing_status == "candidate_supported_reflectance_only"
            else "blocked"
        ),
        "pairing_status": pairing_status,
    }
    claim_ceiling_gate = {
        "status": (
            "pass"
            if claim_status.get("status") == "weak_within_dataset_holdout"
            and claim_status.get("can_feed_serious_core") is False
            else "blocked"
        ),
        "claim_status": claim_status.get("status"),
        "can_feed_serious_core": claim_status.get("can_feed_serious_core"),
    }

    future_policy = _build_future_threshold_policy(run_dir, resolved_spec)
    policy_validation = validate_phase3c2_future_policy(
        future_policy,
        run_created_at=provenance.get("created_at"),
    )

    blocking_reasons = [
        "existing_residuals_inspected_before_policy",
        "policy_does_not_apply_to_existing_run",
        "next_clean_run_required",
    ]
    if thresholds_gate.get("status") != "pass":
        blocking_reasons.append("thresholds_predeclared_gate_blocked")
    if normalization_gate.get("status") != "pass":
        blocking_reasons.append("normalization_gate_blocked")
    if no_fit_leakage.get("status") != "pass":
        blocking_reasons.append("no_fit_leakage_gate_failed")
    if pairing_gate["status"] != "pass":
        blocking_reasons.append("pairing_gate_blocked")
    if claim_ceiling_gate["status"] != "pass":
        blocking_reasons.append("claim_status_ceiling_gate_blocked")

    return {
        "phase_id": "Phase 3C.2",
        "title": "St Andrews Candidate Run Audit + Future-Only Threshold Policy",
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "inputs": {
            "run_dir": str(run_dir),
            "pairing_json": str(pairing_json),
            "registry_path": str(registry_path),
            "comparison_table": str(run_dir / "comparison_table.csv"),
            "run_created_at": provenance.get("created_at"),
            "split_ref": split_ref,
        },
        "decision": {
            "status": "candidate_run_audited_future_policy_prepared",
            "can_feed_serious_core": False,
            "can_promote_calibrated_linear_evidence": False,
            "existing_run_promotable": False,
            "next_clean_run_required": True,
            "claim_status_ceiling": "weak_within_dataset_holdout",
            "blocking_reasons": blocking_reasons,
        },
        "run": {
            "claim_status": claim_status,
            "validation_summary": validation_summary,
            "historical_residual_metrics": validation_summary.get("metrics", {}),
            "comparison_diagnostics": _comparison_diagnostics(comparison_rows),
        },
        "gates": {
            "pairing_gate": pairing_gate,
            "thresholds_predeclared": thresholds_gate,
            "normalization_gate": normalization_gate,
            "no_fit_leakage": no_fit_leakage,
            "claim_status_ceiling": claim_ceiling_gate,
            "future_threshold_policy": policy_validation,
        },
        "future_threshold_policy": future_policy,
        "interpretation_boundary": (
            "Phase 3C.2 may prepare a future policy, but the existing St Andrews "
            "run remains historical because residuals were inspected first."
        ),
    }


def _audit_markdown(audit: dict[str, Any]) -> str:
    decision = audit["decision"]
    metrics = audit["run"]["historical_residual_metrics"]
    diagnostics = audit["run"]["comparison_diagnostics"]
    return "\n".join(
        [
            "# Phase 3C.2 - St Andrews Candidate Run Audit",
            "",
            "## Decision",
            "",
            f"- Status: `{decision['status']}`",
            f"- Can feed serious core: `{decision['can_feed_serious_core']}`",
            f"- Existing run promotable: `{decision['existing_run_promotable']}`",
            f"- Next clean run required: `{decision['next_clean_run_required']}`",
            f"- Claim-status ceiling: `{decision['claim_status_ceiling']}`",
            "",
            "## Historical Residual Context",
            "",
            f"- Points: `{metrics.get('validation_points')}`",
            f"- Mean absolute residual: `{metrics.get('validation_mean_abs_residual')}`",
            f"- RMSE: `{metrics.get('validation_rmse')}`",
            f"- Max absolute residual: `{metrics.get('validation_max_abs_residual')}`",
            f"- Dip wavelength offset: `{diagnostics['dip_wavelength_offset_nm']}` nm",
            f"- Shape correlation: `{diagnostics['shape_correlation_minmax']}`",
            "",
            "These values are recorded as historical context only. They must not",
            "be used to tune pass/fail cutoffs for this already-inspected run.",
            "",
            "## Future Policy",
            "",
            "- Policy status: `pending_pro_or_user_lock_before_clean_run`",
            "- Applies to existing run: `false`",
            "- Primary channel: `reflectance`",
            "- Auxiliary channel: `transmittance`, diagnostic only",
            "",
            "## Boundary",
            "",
            audit["interpretation_boundary"],
            "",
        ]
    )


def _policy_yaml(policy: dict[str, Any]) -> str:
    return yaml.safe_dump(policy, sort_keys=False)


def write_phase3c2_audit(output_dir: Path, audit: dict[str, Any]) -> tuple[Path, Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase3c2_standrews_run_audit.json"
    md_path = output_dir / "phase3c2_standrews_run_audit.md"
    policy_path = output_dir / "phase3c2_future_threshold_policy.yaml"
    json_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(_audit_markdown(audit), encoding="utf-8")
    policy_path.write_text(_policy_yaml(audit["future_threshold_policy"]), encoding="utf-8")
    return json_path, md_path, policy_path
