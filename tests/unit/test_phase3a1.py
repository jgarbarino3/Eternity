import json
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from eternity.phase3a1 import (
    Phase3A1GatePolicy,
    build_phase3a1_audit,
    load_phase3a1_gate_policy,
)


def test_phase3a1_blocked_policy_loads() -> None:
    policy = load_phase3a1_gate_policy(Path("docs/phase3a1_threshold_policy.yaml"))

    assert policy.phase_id == "Phase 3A.1"
    assert policy.status == "blocked_pending_pro_checkpoint"
    assert policy.normalization_basis == "unknown"
    assert policy.policy_may_promote_calibrated_evidence is False


def test_phase3a1_approved_policy_requires_decision_fields() -> None:
    with pytest.raises(ValidationError, match="approved_for_future_runs policy is missing"):
        Phase3A1GatePolicy.model_validate(
            {
                "phase_id": "Phase 3A.1",
                "status": "approved_for_future_runs",
                "normalization_basis": "unknown",
                "residuals_inspected_before_policy": False,
            }
        )


def test_phase3a1_approved_future_policy_parses(tmp_path: Path) -> None:
    policy_path = tmp_path / "approved_policy.yaml"
    policy_path.write_text(
        yaml.safe_dump(
            {
                "phase_id": "Phase 3A.1",
                "status": "approved_for_future_runs",
                "normalization_basis": "absolute_reflectance_confirmed",
                "normalization_evidence_refs": ["thesis_page_or_source_note"],
                "thresholds_ref": "docs/phase3a1_threshold_policy.md",
                "wavelength_window_nm": {"min_nm": 450.0, "max_nm": 850.0},
                "metrics": [
                    {
                        "name": "rmse",
                        "comparator": "<=",
                        "threshold": 0.05,
                        "unit": "reflectance_fraction",
                    }
                ],
                "approver": "user",
                "approved_at": "2026-05-16",
                "residuals_inspected_before_policy": False,
                "applies_to_existing_run": False,
                "policy_may_promote_calibrated_evidence": True,
            }
        ),
        encoding="utf-8",
    )

    policy = load_phase3a1_gate_policy(policy_path)

    assert policy.status == "approved_for_future_runs"
    assert policy.policy_may_promote_calibrated_evidence is True
    assert policy.metrics[0].name == "rmse"


def test_phase3a1_audit_keeps_existing_run_blocked(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    gates_dir = run_dir / "validation_gates"
    gates_dir.mkdir(parents=True)
    (run_dir / "claim_status.json").write_text(
        json.dumps(
            {
                "status": "weak_within_dataset_holdout",
                "can_feed_serious_core": False,
            }
        ),
        encoding="utf-8",
    )
    (run_dir / "validation_summary.json").write_text(
        json.dumps(
            {
                "blocking_gates": ["thresholds_predeclared", "normalization_gate"],
                "metrics": {"validation_rmse": 0.28},
            }
        ),
        encoding="utf-8",
    )
    (gates_dir / "normalization_gate.json").write_text(
        json.dumps({"status": "blocked"}),
        encoding="utf-8",
    )
    (gates_dir / "thresholds_predeclared.json").write_text(
        json.dumps({"status": "blocked"}),
        encoding="utf-8",
    )
    (gates_dir / "no_fit_leakage.json").write_text(
        json.dumps({"status": "pass"}),
        encoding="utf-8",
    )

    audit = build_phase3a1_audit(
        Path("experiments/examples/linear_tin_sio2_d10nm_validation_candidate.yaml"),
        run_dir,
        Path("docs/phase3a1_threshold_policy.yaml"),
    )

    assert audit["status"] == "blocked_existing_run"
    assert audit["promotion"]["existing_run_allowed"] is False
    assert "normalization_gate_blocked" in audit["promotion"]["blocking_reasons"]
    assert "thresholds_predeclared_gate_blocked" in audit["promotion"]["blocking_reasons"]
