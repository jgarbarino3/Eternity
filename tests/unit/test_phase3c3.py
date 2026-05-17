import json
from pathlib import Path

import yaml

from eternity.phase3c3 import (
    PHASE3C2_HISTORICAL_RUN_ID,
    build_phase3c3_evaluation,
    phase3c3_policy_allows_reflectance_normalization,
    validate_phase3c3_policy_for_run,
    write_phase3c3_evaluation,
)


def _policy(created_at: str = "2026-05-17T19:00:00+00:00") -> dict:
    return {
        "phase_id": "Phase 3C.3",
        "policy": "standrews_threshold_policy",
        "status": "locked_for_future_clean_run",
        "created_at": created_at,
        "applies_to_existing_runs": False,
        "excluded_run_refs": [f"results/runs/{PHASE3C2_HISTORICAL_RUN_ID}"],
        "excluded_run_ids": [PHASE3C2_HISTORICAL_RUN_ID],
        "normalization_basis": {
            "status": "absolute_fraction_accepted_for_reflectance",
        },
        "primary_channel": {
            "kind": "reflectance",
            "measurement_ref": "public_standrews_tin_50nm_reflectance_measurement",
        },
        "auxiliary_channels": [
            {
                "kind": "transmittance",
                "measurement_ref": "public_standrews_tin_50nm_transmittance_measurement",
                "use": "diagnostic_only",
            }
        ],
        "required_metrics": [
            {"name": "mean_absolute_error", "comparator": "less_equal", "threshold": 0.04},
            {
                "name": "root_mean_square_error",
                "comparator": "less_equal",
                "threshold": 0.06,
            },
            {
                "name": "max_absolute_residual",
                "comparator": "less_equal",
                "threshold": 0.15,
            },
            {
                "name": "dip_wavelength_offset_nm",
                "comparator": "abs_less_equal",
                "threshold": 40.0,
            },
            {
                "name": "shape_correlation_minmax",
                "comparator": "greater_equal",
                "threshold": 0.90,
            },
        ],
        "approval": {
            "approver": "user_phase3c3_plan_request",
            "approved_at": created_at,
            "locked_before_run": True,
        },
    }


def _write_run(tmp_path: Path, residuals: list[float]) -> Path:
    run_dir = tmp_path / "results" / "runs" / "run_clean"
    gates_dir = run_dir / "validation_gates"
    gates_dir.mkdir(parents=True)
    rows = ["wavelength_nm,prediction,measurement,residual,measurement_ref"]
    measurements = [0.5, 0.2, 0.7]
    wavelengths = [400.0, 540.0, 1000.0]
    for wavelength, measurement, residual in zip(wavelengths, measurements, residuals, strict=True):
        rows.append(
            f"{wavelength},{measurement + residual},{measurement},{residual},"
            "public_standrews_tin_50nm_reflectance_measurement"
        )
    (run_dir / "comparison_table.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")
    (run_dir / "provenance.json").write_text(
        json.dumps({"created_at": "2026-05-17T20:00:00+00:00"}),
        encoding="utf-8",
    )
    (run_dir / "claim_status.json").write_text(
        json.dumps({"status": "weak_within_dataset_holdout", "can_feed_serious_core": False}),
        encoding="utf-8",
    )
    (run_dir / "resolved_spec.json").write_text(
        json.dumps(
            {
                "validation": {
                    "holdout_measurement_ref": (
                        "public_standrews_tin_50nm_reflectance_measurement"
                    )
                }
            }
        ),
        encoding="utf-8",
    )
    (gates_dir / "thresholds_predeclared.json").write_text(
        json.dumps({"status": "pass", "thresholds_ref": "docs/policy.yaml"}),
        encoding="utf-8",
    )
    (gates_dir / "normalization_gate.json").write_text(
        json.dumps({"status": "pass"}),
        encoding="utf-8",
    )
    (gates_dir / "no_fit_leakage.json").write_text(
        json.dumps({"status": "pass"}),
        encoding="utf-8",
    )
    return run_dir


def test_phase3c3_policy_rejects_phase3c2_historical_run() -> None:
    result = validate_phase3c3_policy_for_run(
        _policy(),
        Path(f"results/runs/{PHASE3C2_HISTORICAL_RUN_ID}"),
        "2026-05-17T20:00:00+00:00",
        "candidate_supported_reflectance_only",
        "public_standrews_tin_50nm_reflectance_measurement",
    )

    assert result["status"] == "blocked"
    assert "run_excluded_by_policy" in result["blocking_reasons"]
    assert "historical_phase3c2_run_not_promotable" in result["blocking_reasons"]


def test_phase3c3_policy_date_must_precede_clean_run() -> None:
    result = validate_phase3c3_policy_for_run(
        _policy(created_at="2026-05-17T21:00:00+00:00"),
        Path("results/runs/run_clean"),
        "2026-05-17T20:00:00+00:00",
        "candidate_supported_reflectance_only",
        "public_standrews_tin_50nm_reflectance_measurement",
    )

    assert result["status"] == "blocked"
    assert "policy_created_after_run" in result["blocking_reasons"]


def test_phase3c3_requires_all_five_metrics() -> None:
    policy = _policy()
    policy["required_metrics"] = policy["required_metrics"][:-1]

    result = validate_phase3c3_policy_for_run(
        policy,
        Path("results/runs/run_clean"),
        "2026-05-17T20:00:00+00:00",
        "candidate_supported_reflectance_only",
        "public_standrews_tin_50nm_reflectance_measurement",
    )

    assert result["status"] == "blocked"
    assert "missing_required_metrics:shape_correlation_minmax" in result["blocking_reasons"]


def test_phase3c3_reflectance_normalization_and_transmittance_boundary() -> None:
    policy = _policy()

    assert phase3c3_policy_allows_reflectance_normalization(
        policy,
        "public_standrews_tin_50nm_reflectance_measurement",
    )
    assert not phase3c3_policy_allows_reflectance_normalization(
        policy,
        "public_standrews_tin_50nm_transmittance_measurement",
    )
    assert policy["auxiliary_channels"][0]["use"] == "diagnostic_only"


def test_phase3c3_failed_thresholds_emit_failed_validation(tmp_path: Path) -> None:
    run_dir = _write_run(tmp_path, residuals=[0.2, -0.2, 0.2])
    policy_path = tmp_path / "policy.yaml"
    policy_path.write_text(yaml.safe_dump(_policy(), sort_keys=False), encoding="utf-8")
    pairing_json = tmp_path / "pairing.json"
    pairing_json.write_text(
        json.dumps(
            {
                "selected_pairing": {
                    "pairing_status": "candidate_supported_reflectance_only"
                }
            }
        ),
        encoding="utf-8",
    )

    evaluation = build_phase3c3_evaluation(run_dir, policy_path, pairing_json)

    assert evaluation["decision"]["status"] == "clean_run_failed_thresholds"
    assert evaluation["decision"]["claim_status_decision"] == "failed_validation"
    assert evaluation["decision"]["can_feed_serious_core"] is False
    assert evaluation["threshold_evaluation"]["status"] == "fail"

    json_path, md_path = write_phase3c3_evaluation(tmp_path / "out", evaluation)
    assert json.loads(json_path.read_text())["decision"]["status"] == "clean_run_failed_thresholds"
    assert "Phase 3C.3" in md_path.read_text()
