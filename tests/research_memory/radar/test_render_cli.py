from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from eternity.cli import app
from eternity.research_memory.radar.models import RadarCandidate
from eternity.research_memory.radar.render import build_radar_markdown
from eternity.research_memory.radar.scoring import grade_candidate

runner = CliRunner()


def test_radar_markdown_includes_required_eternity_fields() -> None:
    ranked = grade_candidate(
        RadarCandidate(
            source_id="fixture",
            source_type="arxiv_query",
            title="Bayesian experimental design for self-driving ultrafast spectroscopy",
            abstract="Closed-loop experiment design for autonomous spectroscopy.",
        )
    )

    markdown = build_radar_markdown([ranked], dry_run=True)

    assert "Why this matters for Eternity" in markdown
    assert "Possible experiment" in markdown
    assert "Possible code module" in markdown
    assert "Risk / limitation" in markdown
    assert "Should we act now" in markdown
    assert "not validated evidence" in markdown


def test_radar_cli_scan_dry_run_writes_no_research_records(tmp_path: Path) -> None:
    output_root = tmp_path / "radar"
    record_dir = tmp_path / "records"

    result = runner.invoke(
        app,
        [
            "memory",
            "radar",
            "scan",
            "--config",
            "/Users/joegarbarino/Desktop/Eternity/config/research_radar.example.yaml",
            "--output-root",
            str(output_root),
            "--dry-run",
        ],
    )

    assert result.exit_code == 0, result.output
    run_dir = Path(result.output.strip())
    assert (run_dir / "manifest.json").exists()
    assert not record_dir.exists()
    manifest = json.loads((run_dir / "manifest.json").read_text())
    assert manifest["dry_run"] is True
    assert manifest["raw_candidate_count"] >= 1


def test_radar_cli_digest_renders_markdown_from_run(tmp_path: Path) -> None:
    output_root = tmp_path / "radar"
    scan_result = runner.invoke(
        app,
        [
            "memory",
            "radar",
            "scan",
            "--config",
            "/Users/joegarbarino/Desktop/Eternity/config/research_radar.example.yaml",
            "--output-root",
            str(output_root),
            "--dry-run",
        ],
    )
    run_dir = Path(scan_result.output.strip())

    digest_result = runner.invoke(
        app,
        ["memory", "radar", "digest", "--run-dir", str(run_dir)],
    )

    assert digest_result.exit_code == 0, digest_result.output
    digest_path = Path(digest_result.output.strip())
    assert digest_path == run_dir / "digest.md"
    assert "Eternity Weekly Research Radar" in digest_path.read_text()
    assert (output_root / "latest.md").exists()
