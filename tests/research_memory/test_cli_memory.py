from __future__ import annotations

from typer.testing import CliRunner

from eternity.cli import app

runner = CliRunner()


def test_memory_validate_cli_accepts_examples() -> None:
    result = runner.invoke(app, ["memory", "validate", "research_memory/examples"])

    assert result.exit_code == 0, result.output
    assert "valid research memory records" in result.output


def test_memory_list_cli_includes_evidence_state() -> None:
    result = runner.invoke(app, ["memory", "list", "research_memory/examples", "--tag", "frog"])

    assert result.exit_code == 0, result.output
    assert "evidence=" in result.output
    assert "rm_" in result.output


def test_memory_search_cli_includes_uncertainty_metadata() -> None:
    result = runner.invoke(
        app,
        ["memory", "search", "research_memory/examples", "scalar GDD TiN FROG"],
    )

    assert result.exit_code == 0, result.output
    assert "evidence=observed_lab" in result.output
    assert "snippet=" in result.output


def test_memory_show_cli_resolves_record_id() -> None:
    list_result = runner.invoke(app, ["memory", "list", "research_memory/examples"])
    record_id = next(
        line.split()[0] for line in list_result.output.splitlines() if line.startswith("rm_")
    )

    result = runner.invoke(
        app,
        ["memory", "show", record_id, "--dir", "research_memory/examples", "--json"],
    )

    assert result.exit_code == 0, result.output
    assert f'"record_id": "{record_id}"' in result.output


def test_memory_digest_cli_writes_artifact() -> None:
    with runner.isolated_filesystem():
        result = runner.invoke(
            app,
            [
                "memory",
                "digest",
                "/Users/joegarbarino/Desktop/Eternity/research_memory/examples",
                "--project-area",
                "tin_frog",
            ],
        )

        assert result.exit_code == 0, result.output
        assert "results/research_memory/digests" in result.output
