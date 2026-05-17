import json
from pathlib import Path

from eternity.phase3c2 import (
    build_phase3c2_audit,
    validate_phase3c2_future_policy,
    write_phase3c2_audit,
)


def _write_phase3c2_inputs(
    tmp_path: Path,
    pairing_status: str = "candidate_supported_reflectance_only",
) -> tuple[Path, Path]:
    run_dir = tmp_path / "run"
    gates_dir = run_dir / "validation_gates"
    gates_dir.mkdir(parents=True)
    (run_dir / "comparison_table.csv").write_text(
        "\n".join(
            [
                "wavelength_nm,prediction,measurement,residual,measurement_ref",
                "400,0.2,0.8,-0.6,public_standrews_tin_50nm_reflectance_measurement",
                "540,0.1,0.2,-0.1,public_standrews_tin_50nm_reflectance_measurement",
                "1000,0.7,0.6,0.1,public_standrews_tin_50nm_reflectance_measurement",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (run_dir / "claim_status.json").write_text(
        json.dumps({"status": "weak_within_dataset_holdout", "can_feed_serious_core": False}),
        encoding="utf-8",
    )
    (run_dir / "validation_summary.json").write_text(
        json.dumps(
            {
                "status": "blocked_from_calibrated_promotion",
                "blocking_gates": ["thresholds_predeclared", "normalization_gate"],
                "metrics": {
                    "validation_points": 3,
                    "validation_mean_abs_residual": 0.266,
                    "validation_rmse": 0.35,
                    "validation_max_abs_residual": 0.6,
                },
            }
        ),
        encoding="utf-8",
    )
    (run_dir / "resolved_spec.json").write_text(
        json.dumps(
            {
                "validation": {
                    "split_ref": "public_standrews_tin_50nm_50c_validation_candidate",
                    "holdout_measurement_ref": "public_standrews_tin_50nm_reflectance_measurement",
                    "auxiliary_measurement_refs": [
                        "public_standrews_tin_50nm_transmittance_measurement"
                    ],
                }
            }
        ),
        encoding="utf-8",
    )
    (run_dir / "provenance.json").write_text(
        json.dumps({"created_at": "2026-05-17T19:23:45+00:00"}),
        encoding="utf-8",
    )
    (gates_dir / "thresholds_predeclared.json").write_text(
        json.dumps({"status": "blocked", "thresholds_ref": None}),
        encoding="utf-8",
    )
    (gates_dir / "normalization_gate.json").write_text(
        json.dumps({"status": "blocked"}),
        encoding="utf-8",
    )
    (gates_dir / "no_fit_leakage.json").write_text(
        json.dumps(
            {
                "status": "pass",
                "leaked_measurement_refs": [],
                "leaked_raw_artifact_refs": [],
            }
        ),
        encoding="utf-8",
    )
    pairing_json = tmp_path / "pairing.json"
    pairing_json.write_text(
        json.dumps({"selected_pairing": {"pairing_status": pairing_status}}),
        encoding="utf-8",
    )
    return run_dir, pairing_json


def test_phase3c2_audit_rejects_existing_run_promotion(tmp_path: Path) -> None:
    run_dir, pairing_json = _write_phase3c2_inputs(tmp_path)

    audit = build_phase3c2_audit(run_dir, pairing_json)

    assert audit["decision"]["status"] == "candidate_run_audited_future_policy_prepared"
    assert audit["decision"]["existing_run_promotable"] is False
    assert audit["decision"]["next_clean_run_required"] is True
    assert audit["decision"]["can_feed_serious_core"] is False
    assert "thresholds_predeclared_gate_blocked" in audit["decision"]["blocking_reasons"]
    assert audit["future_threshold_policy"]["applies_to_existing_run"] is False
    assert audit["gates"]["no_fit_leakage"]["status"] == "pass"


def test_phase3c2_policy_cannot_promote_without_pre_run_approval(tmp_path: Path) -> None:
    run_dir, pairing_json = _write_phase3c2_inputs(tmp_path)
    audit = build_phase3c2_audit(run_dir, pairing_json)
    policy = dict(audit["future_threshold_policy"])
    policy["applies_to_existing_run"] = True
    policy["policy_may_promote_calibrated_evidence"] = True

    result = validate_phase3c2_future_policy(
        policy,
        run_created_at="2026-05-17T19:23:45+00:00",
    )

    assert result["existing_run_promotion_allowed"] is False
    assert "policy_applies_to_existing_run" in result["blocking_reasons"]
    assert "promotion_without_pre_run_approval" in result["blocking_reasons"]


def test_phase3c2_blocks_ambiguous_pairing(tmp_path: Path) -> None:
    run_dir, pairing_json = _write_phase3c2_inputs(tmp_path, pairing_status="blocked_ambiguous")

    audit = build_phase3c2_audit(run_dir, pairing_json)

    assert audit["gates"]["pairing_gate"]["status"] == "blocked"
    assert "pairing_gate_blocked" in audit["decision"]["blocking_reasons"]


def test_phase3c2_writes_audit_and_future_policy(tmp_path: Path) -> None:
    run_dir, pairing_json = _write_phase3c2_inputs(tmp_path)
    audit = build_phase3c2_audit(run_dir, pairing_json)

    json_path, md_path, policy_path = write_phase3c2_audit(tmp_path / "out", audit)

    written = json.loads(json_path.read_text())
    assert written["decision"]["existing_run_promotable"] is False
    assert "St Andrews Candidate Run Audit" in md_path.read_text()
    policy_text = policy_path.read_text()
    assert "applies_to_existing_run: false" in policy_text
    assert "pending_pro_or_user_lock_before_clean_run" in policy_text
