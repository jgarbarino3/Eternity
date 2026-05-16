"""Command-line interface for Eternity V0."""

from __future__ import annotations

from pathlib import Path

import typer
from pydantic import ValidationError

from eternity.artifacts import sha256_file
from eternity.registry import load_registry, validate_registry_integrity
from eternity.research_memory.cli import app as memory_app
from eternity.runner import load_spec, run_experiment

app = typer.Typer(help="Run reproducible Eternity ENZ toy experiments.")
app.add_typer(memory_app, name="memory")


@app.command()
def validate(spec_path: Path) -> None:
    """Validate an experiment specification."""

    try:
        spec = load_spec(spec_path)
    except FileNotFoundError:
        typer.echo(f"Spec not found: {spec_path}", err=True)
        raise typer.Exit(1) from None
    except ValidationError as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(1) from error

    typer.echo(f"valid: {spec.experiment_id}")


@app.command()
def run(spec_path: Path) -> None:
    """Run an experiment specification."""

    try:
        run_dir = run_experiment(spec_path)
    except FileNotFoundError:
        typer.echo(f"Spec not found: {spec_path}", err=True)
        raise typer.Exit(1) from None
    except ValidationError as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(1) from error

    typer.echo("run complete")
    typer.echo(run_dir)


@app.command("hash-artifact")
def hash_artifact(path: Path) -> None:
    """Print the SHA-256 digest for an artifact."""

    if not path.exists():
        typer.echo(f"Artifact not found: {path}", err=True)
        raise typer.Exit(1)
    typer.echo(sha256_file(path))


@app.command("validate-registry")
def validate_registry(path: Path) -> None:
    """Validate the lab-data registry."""

    try:
        registry = load_registry(path)
    except FileNotFoundError:
        typer.echo(f"Registry not found: {path}", err=True)
        raise typer.Exit(1) from None
    except ValidationError as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(1) from error

    integrity = validate_registry_integrity(registry, path)
    if not integrity.ok:
        for issue in integrity.issues:
            typer.echo(f"integrity issue: {issue}", err=True)
        raise typer.Exit(1)
    for warning in integrity.warnings:
        typer.echo(f"integrity warning: {warning}", err=True)

    typer.echo(
        "valid registry: "
        f"{len(registry.raw_artifacts)} artifacts, "
        f"{len(registry.measurements)} measurements, "
        f"{len(registry.splits)} splits"
    )


if __name__ == "__main__":
    app()
