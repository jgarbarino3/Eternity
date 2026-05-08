"""Typer CLI for the weekly research radar."""

from __future__ import annotations

from pathlib import Path

import typer
from pydantic import ValidationError

from eternity.research_memory.radar.config import load_radar_config
from eternity.research_memory.radar.promote import promote_radar_run
from eternity.research_memory.radar.run import digest_radar_run, scan_radar

app = typer.Typer(help="Weekly research radar commands.")
CONFIG_OPTION = typer.Option(..., "--config")
OUTPUT_ROOT_OPTION = typer.Option(Path("results/research_memory/radar"), "--output-root")
DRY_RUN_OPTION = typer.Option(True, "--dry-run/--write")
RUN_DIR_OPTION = typer.Option(..., "--run-dir")
MIN_GRADE_OPTION = typer.Option("A", "--min-grade")
RECORD_DIR_OPTION = typer.Option(Path("data/research_memory/radar"), "--record-dir")


@app.command("validate-config")
def validate_config(config: Path) -> None:
    """Validate a research-radar config file."""

    try:
        loaded = load_radar_config(config)
    except (FileNotFoundError, ValueError, ValidationError) as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(1) from error
    enabled = [source.id for source in loaded.sources if source.enabled]
    typer.echo(
        f"valid research radar config: {len(loaded.recurring_queries)} queries, "
        f"{len(loaded.sources)} sources, enabled={len(enabled)}"
    )


@app.command("scan")
def scan(
    config: Path = CONFIG_OPTION,
    output_root: Path = OUTPUT_ROOT_OPTION,
    dry_run: bool = DRY_RUN_OPTION,
) -> None:
    """Scan configured public metadata sources and write a radar run directory."""

    try:
        run_dir = scan_radar(config_path=config, output_root=output_root, dry_run=dry_run)
    except (FileNotFoundError, ValueError, ValidationError) as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(1) from error
    typer.echo(run_dir)


@app.command("digest")
def digest(run_dir: Path = RUN_DIR_OPTION) -> None:
    """Render a Markdown digest from a radar run directory."""

    try:
        digest_path = digest_radar_run(run_dir)
    except (FileNotFoundError, ValueError, ValidationError) as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(1) from error
    typer.echo(digest_path)


@app.command("promote")
def promote(
    run_dir: Path = RUN_DIR_OPTION,
    min_grade: str = MIN_GRADE_OPTION,
    record_dir: Path = RECORD_DIR_OPTION,
) -> None:
    """Promote reviewed radar items into local paper_card records."""

    if min_grade.upper() not in {"A", "B", "C", "D", "E"}:
        typer.echo("--min-grade must be one of A, B, C, D, E", err=True)
        raise typer.Exit(1)
    try:
        written = promote_radar_run(
            run_dir=run_dir,
            min_grade=min_grade.upper(),
            record_dir=record_dir,
        )
    except (FileNotFoundError, ValueError, ValidationError) as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(1) from error
    if not written:
        typer.echo("no new radar records promoted")
        return
    for path in written:
        typer.echo(path)
