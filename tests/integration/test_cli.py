import json
from pathlib import Path

from typer.testing import CliRunner

from eternity.cli import app

runner = CliRunner()


def test_validate_command_accepts_toy_spec() -> None:
    result = runner.invoke(app, ["validate", "experiments/examples/linear_ito_toy.yaml"])

    assert result.exit_code == 0, result.output
    assert "valid" in result.output


def test_validate_command_accepts_tabulated_tion_spec() -> None:
    result = runner.invoke(app, ["validate", "experiments/examples/linear_tion_48_tabulated.yaml"])

    assert result.exit_code == 0, result.output
    assert "valid: linear_tion_48_tabulated_001" in result.output


def test_validate_command_accepts_phase3a_validation_candidate_spec() -> None:
    result = runner.invoke(
        app,
        ["validate", "experiments/examples/linear_tin_sio2_d10nm_validation_candidate.yaml"],
    )

    assert result.exit_code == 0, result.output
    assert "valid: linear_tin_sio2_d10nm_validation_candidate_001" in result.output


def test_memory_subcommand_is_registered_without_breaking_v0_cli() -> None:
    result = runner.invoke(app, ["memory", "--help"])

    assert result.exit_code == 0, result.output
    assert "Research memory" in result.output


def test_run_command_creates_expected_artifacts() -> None:
    result = runner.invoke(app, ["run", "experiments/examples/linear_ito_toy.yaml"])

    assert result.exit_code == 0, result.output
    run_dir = Path(result.output.strip().splitlines()[-1])

    assert (run_dir / "resolved_spec.json").exists()
    assert (run_dir / "provenance.json").exists()
    assert (run_dir / "metrics.json").exists()
    assert (run_dir / "warnings.json").exists()
    assert (run_dir / "report.md").exists()
    assert (run_dir / "plots" / "epsilon.png").exists()
    assert (run_dir / "plots" / "nk.png").exists()
    assert (run_dir / "plots" / "tra.png").exists()


def test_energy_bookkeeping_and_rerun_determinism() -> None:
    first = runner.invoke(app, ["run", "experiments/examples/linear_ito_toy.yaml"])
    second = runner.invoke(app, ["run", "experiments/examples/linear_ito_toy.yaml"])
    first_dir = Path(first.output.strip().splitlines()[-1])
    second_dir = Path(second.output.strip().splitlines()[-1])

    assert first_dir == second_dir
    metrics = (first_dir / "metrics.json").read_text()
    assert '"max_energy_error"' in metrics
    assert '"spec_hash"' in metrics


def test_hash_artifact_command_outputs_digest() -> None:
    result = runner.invoke(
        app,
        ["hash-artifact", "lab_data/raw/synthetic_v0/transmission_fixture.csv"],
    )

    assert result.exit_code == 0, result.output
    assert len(result.output.strip()) == 64


def test_validate_registry_command_accepts_fixture_registry() -> None:
    result = runner.invoke(app, ["validate-registry", "lab_data/registry.yaml"])

    assert result.exit_code == 0, result.output
    assert "valid registry" in result.output


def test_run_writes_claim_status_and_gate_artifacts() -> None:
    result = runner.invoke(app, ["run", "experiments/examples/linear_ito_toy.yaml"])
    assert result.exit_code == 0, result.output
    run_dir = Path(result.output.strip().splitlines()[-1])

    assert (run_dir / "input_manifest.json").exists()
    assert (run_dir / "claim_status.json").exists()
    assert (run_dir / "artifact_hashes.json").exists()
    assert (run_dir / "validation_gates" / "input_integrity.json").exists()
    assert (run_dir / "validation_gates" / "split_integrity.json").exists()

    report = (run_dir / "report.md").read_text()
    assert "## Claim Status" in report
    assert "synthetic_software_fixture" in report


def test_tabulated_run_writes_v1_grounding_artifacts() -> None:
    result = runner.invoke(app, ["run", "experiments/examples/linear_tion_48_tabulated.yaml"])
    assert result.exit_code == 0, result.output
    run_dir = Path(result.output.strip().splitlines()[-1])

    assert (run_dir / "registry_snapshot.json").exists()
    assert (run_dir / "registry_snapshot.sha256").exists()
    assert (run_dir / "raw_artifacts.json").exists()
    assert (run_dir / "material_model.json").exists()
    assert (run_dir / "prediction_table.csv").exists()
    assert (run_dir / "rt_provenance_audit.json").exists()
    assert (run_dir / "provenance_gaps.json").exists()

    claim_status = (run_dir / "claim_status.json").read_text()
    assert "calibration_only_no_holdout" in claim_status
    assert "calibrated_linear_evidence" not in claim_status


def test_phase3a_run_writes_fail_closed_validation_candidate_artifacts() -> None:
    result = runner.invoke(
        app,
        ["run", "experiments/examples/linear_tin_sio2_d10nm_validation_candidate.yaml"],
    )
    assert result.exit_code == 0, result.output
    run_dir = Path(result.output.strip().splitlines()[-1])

    assert (run_dir / "comparison_table.csv").exists()
    assert (run_dir / "holdout_residuals.csv").exists()
    assert (run_dir / "validation_summary.json").exists()
    assert (run_dir / "validation_gates" / "stack_mapping.json").exists()
    assert (run_dir / "validation_gates" / "normalization_gate.json").exists()
    assert (run_dir / "validation_gates" / "thresholds_predeclared.json").exists()

    claim_status = (run_dir / "claim_status.json").read_text()
    assert "weak_within_dataset_holdout" in claim_status
    assert "calibrated_linear_evidence" not in claim_status
    normalization_gate = (run_dir / "validation_gates" / "normalization_gate.json").read_text()
    assert "blocked" in normalization_gate
    no_fit_leakage = json.loads((run_dir / "validation_gates" / "no_fit_leakage.json").read_text())
    assert no_fit_leakage["status"] == "pass"
    assert no_fit_leakage["leaked_measurement_refs"] == []
    assert no_fit_leakage["leaked_raw_artifact_refs"] == []
    assert "phase3a_30_20_10_reflectance_measurement" not in no_fit_leakage[
        "forbidden_measurement_refs"
    ]
    stack_mapping = json.loads((run_dir / "validation_gates" / "stack_mapping.json").read_text())
    assert stack_mapping["status"] == "pass"
    assert "Figure 4.1" in stack_mapping["source"]
    manifest = json.loads((run_dir / "manifest.json").read_text())
    assert manifest["artifacts"]["comparison_table.csv"]["role"] == "holdout"
    assert manifest["artifacts"]["comparison_table.csv"]["kind"] == "validation_comparison_table"
    assert manifest["artifacts"]["material_model.json"]["role"] == "calibration"
    assert manifest["artifacts"]["artifact_hashes.json"]["kind"] == "artifact_hash_index"


def test_phase3a1_audit_reports_blocked_existing_run(tmp_path: Path) -> None:
    run_result = runner.invoke(
        app,
        ["run", "experiments/examples/linear_tin_sio2_d10nm_validation_candidate.yaml"],
    )
    assert run_result.exit_code == 0, run_result.output
    run_dir = Path(run_result.output.strip().splitlines()[-1])

    audit_result = runner.invoke(
        app,
        [
            "phase3a1-audit",
            "--run-dir",
            str(run_dir),
            "--output-dir",
            str(tmp_path),
        ],
    )

    assert audit_result.exit_code == 0, audit_result.output
    assert (tmp_path / "phase3a1_audit.json").exists()
    assert (tmp_path / "phase3a1_audit.md").exists()
    audit = json.loads((tmp_path / "phase3a1_audit.json").read_text())
    assert audit["status"] == "blocked_existing_run"
    assert audit["promotion"]["existing_run_allowed"] is False
    assert "normalization_gate_blocked" in audit["promotion"]["blocking_reasons"]


def test_phase3a7_recovery_command_writes_artifacts(tmp_path: Path) -> None:
    source_root = tmp_path / "sources"
    source_root.mkdir()
    (source_root / "candidate.SE").write_text(
        "CompleteEASE reflectance intensity quartz 3 layer cap test",
        encoding="utf-8",
    )
    thesis_pdf = tmp_path / "thesis.pdf"
    thesis_pdf.write_text("3L2 Figure 4.1", encoding="utf-8")
    d10_initial = tmp_path / "d_10nm_initial.txt"
    d10_initial.write_text("Wavelength\tIntensity\n", encoding="utf-8")
    d10_12v = tmp_path / "d_10nm_12V.txt"
    d10_12v.write_text("Wavelength\tIntensity\n", encoding="utf-8")
    ps_intensity = tmp_path / "30_20_10 p_s intensity.txt"
    ps_intensity.write_text("Wavelength\tp-Intensity\ts-Intensity\n", encoding="utf-8")
    reflectance = tmp_path / "30_20_10 reflectance.txt"
    reflectance.write_text("Wavelength\tIntensity\n", encoding="utf-8")

    result = runner.invoke(
        app,
        [
            "phase3a7-recovery",
            "--source-root",
            str(source_root),
            "--thesis-pdf",
            str(thesis_pdf),
            "--d10-initial",
            str(d10_initial),
            "--d10-12v",
            str(d10_12v),
            "--candidate-ps-intensity",
            str(ps_intensity),
            "--candidate-reflectance",
            str(reflectance),
            "--output-dir",
            str(tmp_path / "out"),
        ],
    )

    assert result.exit_code == 0, result.output
    recovery = json.loads(
        (tmp_path / "out" / "phase3a7_completeease_source_recovery.json").read_text()
    )
    assert recovery["decision"]["can_promote_calibrated_linear_evidence"] is False
    assert (tmp_path / "out" / "phase3a7_completeease_source_recovery.md").exists()


def test_phase3a8_triage_command_writes_artifacts(tmp_path: Path) -> None:
    recovery_json = tmp_path / "phase3a7.json"
    recovery_json.write_text(
        json.dumps(
            {
                "phase_id": "Phase 3A.7",
                "title": "CompleteEASE Source Recovery + 3L2 Provenance Lock",
                "decision": {
                    "exact_source_identity_status": "not_found",
                    "absolute_reflectance_status": "absolute_reflectance_blocked",
                },
                "candidate_sources": [
                    {
                        "path": "/tmp/quartz 10nm SiO2 cap pulsed.SEsnap",
                        "kind": "sesnap",
                        "sha256": "quartz",
                        "score": 40,
                        "match_reasons": ["mentions_quartz", "mentions_10nm_or_11nm"],
                        "absolute_reflectance_proof": False,
                        "evidence_snippets": ["CompleteEASE quartz 10nm SiO2 cap pulsed"],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "phase3a8-triage",
            "--recovery-json",
            str(recovery_json),
            "--output-dir",
            str(tmp_path / "out"),
        ],
    )

    assert result.exit_code == 0, result.output
    triage = json.loads((tmp_path / "out" / "phase3a8_source_candidate_triage.json").read_text())
    assert triage["decision"]["final_decision"] == "pivot_to_relative_only_diagnostic"
    assert triage["decision"]["can_feed_serious_core"] is False
    assert (tmp_path / "out" / "phase3a8_source_candidate_triage.md").exists()
    assert (tmp_path / "out" / "phase3a8_relative_only_diagnostic_policy.yaml").exists()


def test_phase3a9_diagnostic_command_writes_artifacts(tmp_path: Path) -> None:
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
        json.dumps({"status": "blocked_from_calibrated_promotion", "metrics": {}}),
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
                "forbidden_uses:",
                "  - serious_core_evidence",
                "  - calibrated_linear_evidence",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "phase3a9-diagnostic",
            "--run-dir",
            str(run_dir),
            "--policy",
            str(policy_path),
            "--output-dir",
            str(tmp_path / "out"),
        ],
    )

    assert result.exit_code == 0, result.output
    packet = json.loads(
        (tmp_path / "out" / "phase3a9_relative_only_diagnostic_packet.json").read_text()
    )
    assert packet["decision"]["status"] == "relative_only_diagnostic_packet_ready"
    assert packet["decision"]["can_feed_serious_core"] is False
    assert (tmp_path / "out" / "phase3a9_relative_only_diagnostic_packet.md").exists()
    assert (tmp_path / "out" / "phase3a9_relative_only_diagnostic_table.csv").exists()


def test_phase3a10_decision_command_writes_artifacts(tmp_path: Path) -> None:
    triage_json = tmp_path / "phase3a8.json"
    triage_json.write_text(
        json.dumps(
            {
                "phase_id": "Phase 3A.8",
                "categories": {
                    "manual_followup_priority": [
                        {
                            "path": "/tmp/quartz 10nm pulsed.SEsnap",
                            "sha256": "abc",
                            "triage_priority_score": 86,
                            "score": 40,
                            "triage_rationale": "matches quartz dynamic",
                        }
                    ]
                },
            }
        ),
        encoding="utf-8",
    )
    diagnostic_json = tmp_path / "phase3a9.json"
    diagnostic_json.write_text(
        json.dumps(
            {
                "phase_id": "Phase 3A.9",
                "decision": {"status": "relative_only_diagnostic_packet_ready"},
                "diagnostics": {
                    "shape_correlation_minmax": 0.986,
                    "trend_direction_agreement": True,
                },
            }
        ),
        encoding="utf-8",
    )
    registry = tmp_path / "registry.yaml"
    registry.write_text(
        "\n".join(
            [
                "raw_artifacts:",
                "  tion_48_0p8pa_epsilon: {}",
                "  tion_49_1p0pa_epsilon: {}",
                "measurements:",
                "  tion_48_0p8pa_epsilon_measurement:",
                "    sample_ref: tion_48_40nm_0p8pa",
                "    kind: epsilon_table",
                "    y_quantity: complex_dielectric_function",
                "material_models:",
                "  tion_48_0p8pa_epsilon_model: {}",
                "  tion_49_1p0pa_epsilon_model: {}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "phase3a10-decision",
            "--triage-json",
            str(triage_json),
            "--diagnostic-json",
            str(diagnostic_json),
            "--registry",
            str(registry),
            "--output-dir",
            str(tmp_path / "out"),
        ],
    )

    assert result.exit_code == 0, result.output
    packet = json.loads((tmp_path / "out" / "phase3a10_branch_decision.json").read_text())
    assert packet["decision"]["selected_branch"] == "limited_manual_source_followup_first"
    assert packet["decision"]["can_feed_serious_core"] is False
    assert (tmp_path / "out" / "phase3a10_branch_decision.md").exists()


def test_phase3a11_packet_command_writes_artifacts(tmp_path: Path) -> None:
    decision_json = tmp_path / "phase3a10.json"
    decision_json.write_text(
        json.dumps(
            {
                "phase_id": "Phase 3A.10",
                "decision": {"selected_branch": "limited_manual_source_followup_first"},
                "manual_source_followup": {
                    "targets": [
                        {
                            "path": "/tmp/quartz 10nm pulsed.SEsnap",
                            "sha256": "abc",
                            "priority": 86,
                            "score": 40,
                            "rationale": "matches quartz dynamic",
                        }
                    ]
                },
            }
        ),
        encoding="utf-8",
    )
    triage_json = tmp_path / "phase3a8.json"
    triage_json.write_text(
        json.dumps(
            {
                "phase_id": "Phase 3A.8",
                "categories": {
                    "manual_followup_priority": [
                        {
                            "path": "/tmp/quartz 10nm pulsed.SEsnap",
                            "sha256": "abc",
                            "member_path": "archive/candidate.SEsnap",
                            "container_path": "/tmp/source.zip",
                            "inner_ise_entries": ["candidate.iSE"],
                            "evidence_snippets": ["60.0 0.0 F -5.0 5.0 F '60.0deg'"],
                            "absolute_reflectance_proof": False,
                        }
                    ]
                },
            }
        ),
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "phase3a11-packet",
            "--decision-json",
            str(decision_json),
            "--triage-json",
            str(triage_json),
            "--output-dir",
            str(tmp_path / "out"),
        ],
    )

    assert result.exit_code == 0, result.output
    packet = json.loads(
        (tmp_path / "out" / "phase3a11_manual_source_followup_packet.json").read_text()
    )
    assert packet["phase_id"] == "Phase 3A.11"
    assert packet["decision"]["can_feed_serious_core"] is False
    assert (tmp_path / "out" / "phase3a11_manual_source_followup_packet.md").exists()
