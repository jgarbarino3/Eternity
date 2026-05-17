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
