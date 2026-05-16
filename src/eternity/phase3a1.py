"""Phase 3A.1 normalization and threshold gate audit utilities."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator

from eternity.specs import ExperimentSpec

NormalizationBasis = Literal[
    "absolute_reflectance_confirmed",
    "relative_intensity_only",
    "unknown",
]
ThresholdPolicyStatus = Literal[
    "blocked_pending_pro_checkpoint",
    "approved_for_future_runs",
]


class WavelengthWindowPolicy(BaseModel):
    min_nm: float
    max_nm: float

    model_config = ConfigDict(extra="forbid")


class ThresholdMetricPolicy(BaseModel):
    name: str
    comparator: Literal["<="] = "<="
    threshold: float
    unit: str = "reflectance_fraction"

    model_config = ConfigDict(extra="forbid")


class Phase3A1GatePolicy(BaseModel):
    phase_id: Literal["Phase 3A.1"]
    status: ThresholdPolicyStatus
    normalization_basis: NormalizationBasis
    normalization_evidence_refs: list[str] = Field(default_factory=list)
    thresholds_ref: str | None = None
    wavelength_window_nm: WavelengthWindowPolicy | None = None
    metrics: list[ThresholdMetricPolicy] = Field(default_factory=list)
    approver: str | None = None
    approved_at: str | None = None
    residuals_inspected_before_policy: bool
    applies_to_existing_run: bool = False
    policy_may_promote_calibrated_evidence: bool = False

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def validate_approval_fields(self) -> Phase3A1GatePolicy:
        if (
            self.policy_may_promote_calibrated_evidence
            and self.status != "approved_for_future_runs"
        ):
            raise ValueError("promotion-capable policy must be approved_for_future_runs")
        if self.status == "approved_for_future_runs":
            missing = []
            if self.normalization_basis != "absolute_reflectance_confirmed":
                missing.append("absolute_reflectance_confirmed normalization_basis")
            if self.thresholds_ref is None:
                missing.append("thresholds_ref")
            if self.wavelength_window_nm is None:
                missing.append("wavelength_window_nm")
            if not self.metrics:
                missing.append("metrics")
            if self.approver is None:
                missing.append("approver")
            if self.approved_at is None:
                missing.append("approved_at")
            if missing:
                raise ValueError(
                    "approved_for_future_runs policy is missing: " + ", ".join(missing)
                )
        if self.applies_to_existing_run and self.residuals_inspected_before_policy:
            raise ValueError(
                "policy cannot apply to an existing run after residuals were inspected"
            )
        return self


def load_phase3a1_gate_policy(path: Path) -> Phase3A1GatePolicy:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return Phase3A1GatePolicy.model_validate(payload)


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_spec(path: Path) -> ExperimentSpec:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return ExperimentSpec.model_validate(payload)


def build_phase3a1_audit(
    spec_path: Path,
    run_dir: Path,
    policy_path: Path,
) -> dict[str, Any]:
    spec = _load_spec(spec_path)
    if spec.validation is None:
        raise ValueError("Phase 3A.1 audit requires a validation candidate spec")

    policy = load_phase3a1_gate_policy(policy_path)
    claim_status = _load_json(run_dir / "claim_status.json")
    validation_summary = _load_json(run_dir / "validation_summary.json")
    normalization_gate = _load_json(run_dir / "validation_gates" / "normalization_gate.json")
    stack_mapping = _load_json(run_dir / "validation_gates" / "stack_mapping.json")
    thresholds_gate = _load_json(
        run_dir / "validation_gates" / "thresholds_predeclared.json"
    )
    no_fit_leakage = _load_json(run_dir / "validation_gates" / "no_fit_leakage.json")

    existing_run_allowed = (
        policy.applies_to_existing_run
        and policy.policy_may_promote_calibrated_evidence
        and normalization_gate.get("status") == "pass"
        and stack_mapping.get("status") == "pass"
        and thresholds_gate.get("status") == "pass"
        and no_fit_leakage.get("status") == "pass"
        and claim_status.get("status") == "calibrated_linear_evidence"
    )
    future_policy_ready = (
        policy.status == "approved_for_future_runs"
        and policy.policy_may_promote_calibrated_evidence
        and policy.normalization_basis == "absolute_reflectance_confirmed"
    )

    blocking_reasons = []
    if not policy.applies_to_existing_run:
        blocking_reasons.append("policy_does_not_apply_to_existing_run")
    if policy.residuals_inspected_before_policy:
        blocking_reasons.append("current_residuals_inspected_before_policy")
    if normalization_gate.get("status") != "pass":
        blocking_reasons.append("normalization_gate_blocked")
    if stack_mapping.get("status") != "pass":
        blocking_reasons.append("stack_mapping_gate_blocked")
    if thresholds_gate.get("status") != "pass":
        blocking_reasons.append("thresholds_predeclared_gate_blocked")
    if policy.status != "approved_for_future_runs":
        blocking_reasons.append("policy_not_approved")

    return {
        "phase_id": "Phase 3A.1",
        "status": "blocked_existing_run"
        if not existing_run_allowed
        else "calibrated_promotion_allowed",
        "spec": {
            "path": str(spec_path),
            "experiment_id": spec.experiment_id,
            "status_ceiling": spec.validation.status_ceiling,
            "thresholds_ref": spec.validation.thresholds_ref,
        },
        "run": {
            "path": str(run_dir),
            "claim_status": claim_status.get("status"),
            "can_feed_serious_core": claim_status.get("can_feed_serious_core"),
            "blocking_gates": validation_summary.get("blocking_gates", []),
            "metrics": validation_summary.get("metrics", {}),
        },
        "policy": policy.model_dump(mode="json"),
        "gates": {
            "stack_mapping": stack_mapping,
            "normalization_gate": normalization_gate,
            "thresholds_predeclared": thresholds_gate,
            "no_fit_leakage": no_fit_leakage,
        },
        "promotion": {
            "existing_run_allowed": existing_run_allowed,
            "future_policy_ready": future_policy_ready,
            "blocking_reasons": blocking_reasons,
        },
    }


def audit_markdown(audit: dict[str, Any]) -> str:
    metrics = audit["run"]["metrics"]
    reasons = ", ".join(audit["promotion"]["blocking_reasons"]) or "none"
    return "\n".join(
        [
            "# Phase 3A.1 Gate Audit",
            "",
            f"- Status: `{audit['status']}`",
            f"- Existing run promotion allowed: `{audit['promotion']['existing_run_allowed']}`",
            f"- Future policy ready: `{audit['promotion']['future_policy_ready']}`",
            f"- Claim status: `{audit['run']['claim_status']}`",
            f"- Normalization basis: `{audit['policy']['normalization_basis']}`",
            f"- Policy status: `{audit['policy']['status']}`",
            f"- Blocking reasons: `{reasons}`",
            "",
            "## Historical Residual Context",
            "",
            f"- Points: `{metrics.get('validation_points')}`",
            f"- Mean absolute residual: `{metrics.get('validation_mean_abs_residual')}`",
            f"- RMSE: `{metrics.get('validation_rmse')}`",
            f"- Max absolute residual: `{metrics.get('validation_max_abs_residual')}`",
            "",
            "These residuals are historical context only. They must not be used to choose",
            "a threshold for this already-inspected run.",
            "",
        ]
    )


def write_phase3a1_audit(output_dir: Path, audit: dict[str, Any]) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase3a1_audit.json"
    md_path = output_dir / "phase3a1_audit.md"
    json_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(audit_markdown(audit), encoding="utf-8")
    return json_path, md_path
