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
    manifest = json.loads((run_dir / "manifest.json").read_text())
    assert manifest["artifacts"]["comparison_table.csv"]["role"] == "holdout"
    assert manifest["artifacts"]["comparison_table.csv"]["kind"] == "validation_comparison_table"
    assert manifest["artifacts"]["material_model.json"]["role"] == "calibration"
    assert manifest["artifacts"]["artifact_hashes.json"]["kind"] == "artifact_hash_index"
