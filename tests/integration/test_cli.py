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

    result = runner.invoke(app, ["validate", "experiments/examples/linear_tion_49_tabulated.yaml"])

    assert result.exit_code == 0, result.output
    assert "valid: linear_tion_49_tabulated_001" in result.output


def test_validate_command_accepts_phase3a_validation_candidate_spec() -> None:
    result = runner.invoke(
        app,
        ["validate", "experiments/examples/linear_tin_sio2_d10nm_validation_candidate.yaml"],
    )

    assert result.exit_code == 0, result.output
    assert "valid: linear_tin_sio2_d10nm_validation_candidate_001" in result.output


def test_validate_command_accepts_standrews_validation_candidate_spec() -> None:
    result = runner.invoke(
        app,
        ["validate", "experiments/examples/linear_standrews_tin_50nm_validation_candidate.yaml"],
    )

    assert result.exit_code == 0, result.output
    assert "valid: linear_standrews_tin_50nm_validation_candidate_001" in result.output


def test_validate_command_accepts_standrews_threshold_locked_clean_run_spec() -> None:
    result = runner.invoke(
        app,
        [
            "validate",
            "experiments/examples/linear_standrews_tin_50nm_threshold_locked_clean_run.yaml",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "valid: linear_standrews_tin_50nm_threshold_locked_clean_run_001" in result.output


def test_memory_subcommand_is_registered_without_breaking_v0_cli() -> None:
    result = runner.invoke(app, ["memory", "--help"])

    assert result.exit_code == 0, result.output
    assert "Research memory" in result.output


def test_phase3e1_scaffold_command_writes_gate_artifacts(tmp_path: Path) -> None:
    result = runner.invoke(app, ["phase3e1-scaffold", "--output-dir", str(tmp_path)])

    assert result.exit_code == 0, result.output
    assert (tmp_path / "phase3e1_public_dataset_gate_assistant_scaffold.json").exists()
    assert (tmp_path / "phase3e1_public_dataset_gate_assistant_scaffold.md").exists()
    assert (tmp_path / "phase3e1_claim_status_summary.json").exists()

    summary = json.loads((tmp_path / "phase3e1_claim_status_summary.json").read_text())
    assert summary["can_open_phase4_now"] is False
    assert summary["can_feed_serious_core_now"] is False
    assert summary["phase4_candidate_ids"] == []


def test_phase3e2a_wang_intake_command_writes_artifacts(tmp_path: Path) -> None:
    result = runner.invoke(app, ["phase3e2a-wang-intake", "--output-dir", str(tmp_path)])

    assert result.exit_code == 0, result.output
    assert (tmp_path / "phase3e2a_wang_wo3_baseline_intake.json").exists()
    assert (tmp_path / "phase3e2a_wang_wo3_baseline_intake.md").exists()

    packet = json.loads((tmp_path / "phase3e2a_wang_wo3_baseline_intake.json").read_text())
    assert packet["decision"]["phase4_enz_ready"] is False
    assert packet["decision"]["claim_status_ceiling"] == "non_enz_planar_tmm_baseline_candidate"


def test_phase3e2bcd_wang_commands_write_artifacts(tmp_path: Path) -> None:
    result = runner.invoke(app, ["phase3e2b-wang-semantics", "--output-dir", str(tmp_path)])

    assert result.exit_code == 0, result.output
    assert (tmp_path / "phase3e2b_wang_fig2f_semantics_audit.json").exists()
    assert (tmp_path / "phase3e2b_wang_fig2f_semantics_audit.md").exists()

    result = runner.invoke(app, ["phase3e2c-wang-fixture", "--output-dir", str(tmp_path)])

    assert result.exit_code == 0, result.output
    assert (tmp_path / "phase3e2c_wang_deoffset_reproduction_fixture.json").exists()
    assert (tmp_path / "phase3e2c_wang_deoffset_reproduction_fixture.md").exists()
    assert (tmp_path / "phase3e2c_wang_deoffset_reproduction_fixture.csv").exists()

    result = runner.invoke(app, ["phase3e2d-wang-handoff", "--output-dir", str(tmp_path)])

    assert result.exit_code == 0, result.output
    assert (tmp_path / "phase3e2d_wang_claim_boundary_handoff.json").exists()
    assert (tmp_path / "phase3e2d_wang_claim_boundary_handoff.md").exists()


def test_phase3f1_simulator_validation_scout_command_writes_artifacts(
    tmp_path: Path,
) -> None:
    result = runner.invoke(
        app,
        ["phase3f1-simulator-validation-scout", "--output-dir", str(tmp_path)],
    )

    assert result.exit_code == 0, result.output
    json_path = tmp_path / "phase3f1_simulator_validation_scout.json"
    assert json_path.exists()
    assert (tmp_path / "phase3f1_simulator_validation_scout.md").exists()

    packet = json.loads(json_path.read_text(encoding="utf-8"))
    assert packet["decision"]["phase3f2_intake_allowed"] is False
    assert packet["decision"]["residual_modeling_performed"] is False


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


def test_standrews_run_writes_fail_closed_validation_candidate_artifacts() -> None:
    result = runner.invoke(
        app,
        ["run", "experiments/examples/linear_standrews_tin_50nm_validation_candidate.yaml"],
    )
    assert result.exit_code == 0, result.output
    run_dir = Path(result.output.strip().splitlines()[-1])

    assert (run_dir / "comparison_table.csv").exists()
    assert (run_dir / "holdout_residuals.csv").exists()
    assert (run_dir / "validation_summary.json").exists()
    assert (run_dir / "validation_gates" / "normalization_gate.json").exists()
    assert (run_dir / "validation_gates" / "thresholds_predeclared.json").exists()
    assert (run_dir / "validation_gates" / "no_fit_leakage.json").exists()

    claim_status = json.loads((run_dir / "claim_status.json").read_text())
    assert claim_status["status"] == "weak_within_dataset_holdout"
    assert claim_status["can_feed_serious_core"] is False
    normalization_gate = json.loads(
        (run_dir / "validation_gates" / "normalization_gate.json").read_text()
    )
    assert normalization_gate["status"] == "blocked"
    threshold_gate = json.loads(
        (run_dir / "validation_gates" / "thresholds_predeclared.json").read_text()
    )
    assert threshold_gate["status"] == "blocked"
    no_fit_leakage = json.loads((run_dir / "validation_gates" / "no_fit_leakage.json").read_text())
    assert no_fit_leakage["status"] == "pass"
    assert no_fit_leakage["leaked_measurement_refs"] == []
    assert "public_standrews_tin_50nm_reflectance_measurement" in no_fit_leakage[
        "forbidden_measurement_refs"
    ]
    assert "public_standrews_tin_50nm_transmittance" in no_fit_leakage[
        "forbidden_raw_artifact_refs"
    ]


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


def test_phase3a12_result_command_writes_artifacts(tmp_path: Path) -> None:
    review_input = tmp_path / "phase3a12_review.json"
    review_input.write_text(
        json.dumps(
            {
                "phase_id": "Phase 3A.12",
                "source_packet": "docs/phase3a11_manual_source_followup_packet.json",
                "reviewed_candidates": [
                    {
                        "candidate_id": "phase3a11_candidate_1",
                        "sha256": "abc",
                        "path": "/tmp/candidate.SEsnap",
                        "positive_evidence": ["FitLog line 216 records 60.0 degrees"],
                        "negative_evidence": [
                            "No FitLog hits for 3L2 or absolute reflectance."
                        ],
                        "proof_gate_results": {
                            "exact_3l2_quartz_identity": "failed",
                            "stack_30nm_tin_10nm_sio2_20nm_tin": "failed",
                            "s_polarized_or_te_reflectance_channel": "unresolved",
                            "sixty_degree_incidence": "passed",
                            "absolute_reflectance_units_or_calibration_state": "failed",
                            "export_or_source_lineage_to_d10nm_text_trace": "failed",
                        },
                        "candidate_decision": "related_but_not_source_identity",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "phase3a12-result",
            "--review-input",
            str(review_input),
            "--output-dir",
            str(tmp_path / "out"),
        ],
    )

    assert result.exit_code == 0, result.output
    packet = json.loads(
        (tmp_path / "out" / "phase3a12_manual_source_review_result.json").read_text()
    )
    assert packet["decision"]["status"] == "manual_source_followup_exhausted"
    assert packet["decision"]["can_feed_serious_core"] is False
    assert (tmp_path / "out" / "phase3a12_manual_source_review_result.md").exists()


def test_phase3c1_intake_command_writes_artifacts(tmp_path: Path) -> None:
    raw_dir = tmp_path / "raw"
    output_dir = tmp_path / "out"

    result = runner.invoke(
        app,
        [
            "phase3c1-intake",
            "--zip-path",
            "lab_data/raw/public_st_andrews_tin_2025/TiN-data_Pure.zip",
            "--raw-output-dir",
            str(raw_dir),
            "--output-dir",
            str(output_dir),
        ],
    )

    assert result.exit_code == 0, result.output
    packet = json.loads((output_dir / "phase3c1_standrews_tin_pairing.json").read_text())
    assert packet["selected_pairing"]["pairing_status"] == "candidate_supported_reflectance_only"
    assert packet["decision"]["can_feed_serious_core"] is False
    assert (output_dir / "phase3c1_standrews_tin_pairing.md").exists()
    assert (raw_dir / "standrews_tin_50nm_reflectance.csv").exists()
    assert (raw_dir / "standrews_tin_50nm_transmittance.csv").exists()
    assert (raw_dir / "standrews_tin_50nm_50c_epsilon.txt").exists()


def test_phase3c2_audit_command_writes_future_only_policy(tmp_path: Path) -> None:
    run_result = runner.invoke(
        app,
        ["run", "experiments/examples/linear_standrews_tin_50nm_validation_candidate.yaml"],
    )
    assert run_result.exit_code == 0, run_result.output
    run_dir = Path(run_result.output.strip().splitlines()[-1])

    result = runner.invoke(
        app,
        [
            "phase3c2-audit",
            "--run-dir",
            str(run_dir),
            "--pairing-json",
            "docs/phase3c1_standrews_tin_pairing.json",
            "--output-dir",
            str(tmp_path / "out"),
        ],
    )

    assert result.exit_code == 0, result.output
    audit = json.loads((tmp_path / "out" / "phase3c2_standrews_run_audit.json").read_text())
    assert audit["decision"]["existing_run_promotable"] is False
    assert audit["decision"]["next_clean_run_required"] is True
    assert audit["decision"]["can_feed_serious_core"] is False
    assert audit["future_threshold_policy"]["applies_to_existing_run"] is False
    assert audit["gates"]["no_fit_leakage"]["status"] == "pass"
    assert (tmp_path / "out" / "phase3c2_standrews_run_audit.md").exists()
    policy_text = (tmp_path / "out" / "phase3c2_future_threshold_policy.yaml").read_text()
    assert "pending_pro_or_user_lock_before_clean_run" in policy_text


def test_phase3c3_evaluate_command_writes_clean_run_decision(tmp_path: Path) -> None:
    run_result = runner.invoke(
        app,
        ["run", "experiments/examples/linear_standrews_tin_50nm_threshold_locked_clean_run.yaml"],
    )
    assert run_result.exit_code == 0, run_result.output
    run_dir = Path(run_result.output.strip().splitlines()[-1])
    assert run_dir.name != "run_42fe0ad6dd295019"

    claim_status = json.loads((run_dir / "claim_status.json").read_text())
    assert claim_status["can_feed_serious_core"] is False
    threshold_gate = json.loads(
        (run_dir / "validation_gates" / "thresholds_predeclared.json").read_text()
    )
    normalization_gate = json.loads(
        (run_dir / "validation_gates" / "normalization_gate.json").read_text()
    )
    assert threshold_gate["status"] == "pass"
    assert normalization_gate["status"] == "pass"

    result = runner.invoke(
        app,
        [
            "phase3c3-evaluate",
            "--run-dir",
            str(run_dir),
            "--policy",
            "docs/phase3c3_standrews_threshold_policy.yaml",
            "--pairing-json",
            "docs/phase3c1_standrews_tin_pairing.json",
            "--output-dir",
            str(tmp_path / "out"),
        ],
    )

    assert result.exit_code == 0, result.output
    evaluation = json.loads((tmp_path / "out" / "phase3c3_clean_run_evaluation.json").read_text())
    assert evaluation["decision"]["status"] in {
        "clean_run_failed_thresholds",
        "clean_run_passed_thresholds_ready_for_phase4_review",
    }
    assert evaluation["decision"]["can_feed_serious_core"] is False
    assert evaluation["gates"]["no_fit_leakage"]["status"] == "pass"
    assert evaluation["gates"]["normalization_gate"]["status"] == "pass"
    assert "public_standrews_tin_50nm_transmittance_measurement" in (
        evaluation["gates"]["no_fit_leakage"]["forbidden_measurement_refs"]
    )
    assert (tmp_path / "out" / "phase3c3_clean_run_evaluation.md").exists()
