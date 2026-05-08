"""Typer commands for local research-memory records."""

from __future__ import annotations

import json
from pathlib import Path

import typer
from pydantic import ValidationError

from eternity.research_memory.digest import write_digest
from eternity.research_memory.radar.cli import app as radar_app
from eternity.research_memory.search import search_records
from eternity.research_memory.store import DEFAULT_RECORD_DIR, load_records, resolve_record

app = typer.Typer(help="Research memory commands for reviewable local records.")
app.add_typer(radar_app, name="radar")
SHOW_DIR_OPTION = typer.Option(DEFAULT_RECORD_DIR, "--dir")


def _load_or_exit(path: Path):
    try:
        return load_records(path)
    except (FileNotFoundError, ValueError, ValidationError) as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(1) from error


@app.command("validate")
def validate_memory(path: Path) -> None:
    """Validate one research-memory file or a directory of records."""

    loaded = _load_or_exit(path)
    typer.echo(f"valid research memory records: {len(loaded)}")


@app.command("list")
def list_memory(
    directory: Path,
    record_type: str | None = typer.Option(None, "--record-type"),
    tag: str | None = typer.Option(None, "--tag"),
) -> None:
    """List local research-memory records."""

    loaded = _load_or_exit(directory)
    records = [item.record for item in loaded]
    if record_type is not None:
        records = [record for record in records if record.record_type == record_type]
    if tag is not None:
        records = [record for record in records if tag in record.tags]

    for record in sorted(records, key=lambda item: item.record_id or ""):
        tags = ",".join(record.tags)
        typer.echo(
            f"{record.record_id} {record.title} "
            f"type={record.record_type} evidence={record.evidence_state} tags={tags}"
        )


@app.command("show")
def show_memory(
    record_id_or_path: str,
    directory: Path = SHOW_DIR_OPTION,
    output_json: bool = typer.Option(False, "--json"),
) -> None:
    """Show one research-memory record by path or deterministic id."""

    try:
        loaded = resolve_record(record_id_or_path, directory=directory)
    except (FileNotFoundError, ValueError, ValidationError) as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(1) from error

    payload = loaded.record.model_dump(mode="json", exclude_none=True)
    if output_json:
        typer.echo(json.dumps(payload, indent=2, sort_keys=True))
        return

    record = loaded.record
    typer.echo(f"# {record.title}")
    typer.echo(f"id: {record.record_id}")
    typer.echo(f"type: {record.record_type}")
    typer.echo(f"evidence: {record.evidence_state}")
    typer.echo(f"tags: {', '.join(record.tags)}")
    typer.echo("")
    typer.echo(record.summary)


@app.command("search")
def search_memory(
    directory: Path,
    query: str,
    limit: int = typer.Option(10, "--limit", min=1),
) -> None:
    """Search local research-memory records with deterministic lexical scoring."""

    loaded = _load_or_exit(directory)
    results = search_records([item.record for item in loaded], query, limit=limit)
    if not results:
        typer.echo("no matching research memory records")
        return

    for result in results:
        record = result.record
        tags = ",".join(record.tags)
        typer.echo(
            f"{record.record_id} {record.title} "
            f"type={record.record_type} evidence={record.evidence_state} tags={tags} "
            f"score={result.score}"
        )
        typer.echo(f"snippet={result.snippet}")


@app.command("digest")
def digest_memory(
    directory: Path,
    project_area: str | None = typer.Option(None, "--project-area"),
) -> None:
    """Write a conservative Markdown digest for local records."""

    loaded = _load_or_exit(directory)
    output_path = write_digest(
        [item.record for item in loaded],
        project_area=project_area,
    )
    typer.echo(output_path)
