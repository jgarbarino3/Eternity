import json
import zipfile
from pathlib import Path

from eternity.phase3c4 import build_phase3c4_triage, write_phase3c4_triage


def _write_phase3c4_inputs(tmp_path: Path) -> tuple[Path, Path, Path]:
    run_dir = tmp_path / "results" / "runs" / "run_failed"
    run_dir.mkdir(parents=True)
    (run_dir / "comparison_table.csv").write_text(
        "\n".join(
            [
                "wavelength_nm,prediction,measurement,residual,measurement_ref",
                "400,0.2,0.8,-0.6,public_standrews_tin_50nm_reflectance_measurement",
                "500,0.25,0.3,-0.05,public_standrews_tin_50nm_reflectance_measurement",
                "600,0.3,0.32,-0.02,public_standrews_tin_50nm_reflectance_measurement",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (run_dir / "claim_status.json").write_text(
        json.dumps({"status": "weak_within_dataset_holdout", "can_feed_serious_core": False}),
        encoding="utf-8",
    )
    (run_dir / "sample_stack.json").write_text(
        json.dumps({"stack": {"layers": [{"material": "TiN"}]}}),
        encoding="utf-8",
    )
    (run_dir / "resolved_spec.json").write_text(
        json.dumps({"geometry": {"substrate": "glass", "polarization": "TE"}}),
        encoding="utf-8",
    )

    evaluation_json = tmp_path / "phase3c3_clean_run_evaluation.json"
    evaluation_json.write_text(
        json.dumps(
            {
                "decision": {"status": "clean_run_failed_thresholds"},
                "metrics": {
                    "validation_points": 3,
                    "wavelength_window_nm": [400.0, 600.0],
                    "mean_absolute_error": 0.223333,
                    "root_mean_square_error": 0.347754,
                    "max_absolute_residual": 0.6,
                    "dip_wavelength_offset_nm": -100.0,
                    "shape_correlation_minmax": -0.5,
                },
                "threshold_evaluation": {
                    "failed_metrics": [
                        "mean_absolute_error",
                        "root_mean_square_error",
                        "max_absolute_residual",
                        "dip_wavelength_offset_nm",
                        "shape_correlation_minmax",
                    ],
                    "metrics": [
                        {
                            "name": "mean_absolute_error",
                            "comparator": "less_equal",
                            "threshold": 0.04,
                        },
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
                            "threshold": 0.9,
                        },
                    ],
                },
            }
        ),
        encoding="utf-8",
    )

    archive_path = tmp_path / "standrews.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        archive.writestr(
            "TiN-data_Pure/Ellipsometry/50nm-MTiN-50c.txt",
            "\n".join(
                [
                    "All Layer Optical Constants",
                    "300 2.0 3.0",
                    "400 1.0 3.0",
                    "500 0.5 4.0",
                    "600 -0.5 5.0",
                    "700 -1.0 6.0",
                ]
            ),
        )
    pairing_json = tmp_path / "pairing.json"
    pairing_json.write_text(
        json.dumps(
            {
                "source_archive": {"path": str(archive_path)},
                "selected_pairing": {
                    "selected_material_member": "TiN-data_Pure/Ellipsometry/50nm-MTiN-50c.txt"
                },
                "candidate_epsilon_tables": [
                    {
                        "member": "TiN-data_Pure/Ellipsometry/50nm-MTiN-50c.txt",
                        "enz_wavelengths_nm": [550.0],
                        "passivity_check": "pass",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return run_dir, evaluation_json, pairing_json


def test_phase3c4_triages_failure_without_promotion(tmp_path: Path) -> None:
    run_dir, evaluation_json, pairing_json = _write_phase3c4_inputs(tmp_path)

    packet = build_phase3c4_triage(run_dir, evaluation_json, pairing_json)

    assert packet["phase_id"] == "Phase 3C.4"
    assert packet["decision"]["status"] == "failure_triaged_no_promotion"
    assert packet["decision"]["can_feed_serious_core"] is False
    assert packet["decision"]["phase4_ready"] is False
    assert packet["dominant_failure_windows"][0]["window_nm"] == [400.0, 450.0]
    assert packet["diagnostic_sweeps"]["alternate_material_tables"][0]["threshold_status"][
        "status"
    ] == "fail"


def test_phase3c4_writes_report_artifacts(tmp_path: Path) -> None:
    run_dir, evaluation_json, pairing_json = _write_phase3c4_inputs(tmp_path)
    packet = build_phase3c4_triage(run_dir, evaluation_json, pairing_json)

    json_path, md_path, csv_path = write_phase3c4_triage(tmp_path / "out", packet)

    assert json.loads(json_path.read_text())["phase_id"] == "Phase 3C.4"
    assert "St Andrews Failure Triage" in md_path.read_text()
    assert "alternate_material_tables" in csv_path.read_text()
