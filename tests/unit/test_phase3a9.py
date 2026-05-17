import json
from pathlib import Path

from eternity.phase3a9 import (
    build_phase3a9_packet,
    load_phase3a8_relative_policy,
    write_phase3a9_packet,
)


def _write_phase3a9_inputs(tmp_path: Path) -> tuple[Path, Path]:
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    (run_dir / "comparison_table.csv").write_text(
        "\n".join(
            [
                "wavelength_nm,prediction,measurement,residual,measurement_ref",
                "400,0.4,0.3,0.1,thesis_reflectance_d_10nm_initial_measurement",
                "500,0.2,0.1,0.1,thesis_reflectance_d_10nm_initial_measurement",
                "600,0.5,0.4,0.1,thesis_reflectance_d_10nm_initial_measurement",
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
                "metrics": {"validation_rmse": 0.1},
            }
        ),
        encoding="utf-8",
    )
    policy_path = tmp_path / "phase3a8_policy.yaml"
    policy_path.write_text(
        "\n".join(
            [
                "phase_id: Phase 3A.8",
                "policy: relative_only_diagnostic",
                "can_feed_serious_core: false",
                "allowed_diagnostics:",
                "  - spectral_shape",
                "  - dip_position",
                "  - trend_direction",
                "  - figure_provenance",
                "forbidden_uses:",
                "  - serious_core_evidence",
                "  - calibrated_linear_evidence",
                "  - absolute_reflectance_claim",
                "  - retroactive_threshold_tuning",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return run_dir, policy_path


def test_phase3a9_rejects_non_relative_policy(tmp_path: Path) -> None:
    policy_path = tmp_path / "bad.yaml"
    policy_path.write_text(
        "phase_id: Phase 3A.8\npolicy: calibrated_evidence\ncan_feed_serious_core: false\n",
        encoding="utf-8",
    )

    try:
        load_phase3a8_relative_policy(policy_path)
    except ValueError as error:
        assert "relative_only_diagnostic" in str(error)
    else:
        raise AssertionError("expected relative-only policy validation to fail")


def test_phase3a9_packet_reports_relative_diagnostics_without_promotion(tmp_path: Path) -> None:
    run_dir, policy_path = _write_phase3a9_inputs(tmp_path)

    packet = build_phase3a9_packet(run_dir, policy_path)

    assert packet["phase_id"] == "Phase 3A.9"
    assert packet["decision"]["status"] == "relative_only_diagnostic_packet_ready"
    assert packet["decision"]["can_feed_serious_core"] is False
    assert packet["decision"]["can_promote_calibrated_linear_evidence"] is False
    assert packet["diagnostics"]["prediction_dip"]["wavelength_nm"] == 500.0
    assert packet["diagnostics"]["measurement_dip"]["wavelength_nm"] == 500.0
    assert packet["diagnostics"]["dip_offset_nm"] == 0.0
    assert packet["diagnostics"]["trend_direction_agreement"] is True
    assert packet["historical_residual_context"]["validation_rmse"] == 0.1


def test_phase3a9_writes_packet_artifacts(tmp_path: Path) -> None:
    run_dir, policy_path = _write_phase3a9_inputs(tmp_path)
    packet = build_phase3a9_packet(run_dir, policy_path)

    json_path, md_path, csv_path = write_phase3a9_packet(tmp_path / "out", packet)

    written = json.loads(json_path.read_text())
    assert written["phase_id"] == "Phase 3A.9"
    assert "table" not in written
    assert "Relative-Only Diagnostic" in md_path.read_text()
    table = csv_path.read_text()
    assert "prediction_minmax" in table
    assert "relative_shape_delta" in table
