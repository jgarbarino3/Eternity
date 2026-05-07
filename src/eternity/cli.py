"""Command-line interface for Eternity V0."""

from __future__ import annotations

from pathlib import Path

import typer
from pydantic import ValidationError

from eternity.runner import load_spec, run_experiment

app = typer.Typer(help="Run reproducible Eternity ENZ toy experiments.")


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


if __name__ == "__main__":
    app()
