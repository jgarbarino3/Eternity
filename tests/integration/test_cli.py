from pathlib import Path

from typer.testing import CliRunner

from eternity.cli import app

runner = CliRunner()


def test_validate_command_accepts_toy_spec() -> None:
    result = runner.invoke(app, ["validate", "experiments/examples/linear_ito_toy.yaml"])

    assert result.exit_code == 0, result.output
    assert "valid" in result.output


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
