"""Command-line interface for Eternity V0."""

from __future__ import annotations

import json
from pathlib import Path

import typer
from pydantic import ValidationError

from eternity.artifacts import sha256_file
from eternity.phase3a1 import build_phase3a1_audit, write_phase3a1_audit
from eternity.registry import load_registry, validate_registry_integrity
from eternity.research_memory.cli import app as memory_app
from eternity.runner import load_spec, run_experiment

app = typer.Typer(help="Run reproducible Eternity ENZ toy experiments.")
app.add_typer(memory_app, name="memory")

DEFAULT_PHASE3A1_SPEC_PATH = Path(
    "experiments/examples/linear_tin_sio2_d10nm_validation_candidate.yaml"
)
DEFAULT_PHASE3A1_RUN_DIR = Path("results/runs/run_f35a15cef565fb15")
DEFAULT_PHASE3A1_POLICY_PATH = Path("docs/phase3a1_threshold_policy.yaml")
PHASE3A1_SPEC_OPTION = typer.Option(
    DEFAULT_PHASE3A1_SPEC_PATH,
    "--spec",
    help="Phase 3A validation-candidate spec to audit.",
)
PHASE3A1_RUN_DIR_OPTION = typer.Option(
    DEFAULT_PHASE3A1_RUN_DIR,
    "--run-dir",
    help="Existing Phase 3A run directory to audit.",
)
PHASE3A1_POLICY_OPTION = typer.Option(
    DEFAULT_PHASE3A1_POLICY_PATH,
    "--policy",
    help="Machine-readable Phase 3A.1 gate policy.",
)
PHASE3A1_OUTPUT_DIR_OPTION = typer.Option(
    None,
    "--output-dir",
    help="Optional directory for JSON and Markdown audit artifacts.",
)


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


@app.command("phase3a1-audit")
def phase3a1_audit(
    spec_path: Path = PHASE3A1_SPEC_OPTION,
    run_dir: Path = PHASE3A1_RUN_DIR_OPTION,
    policy_path: Path = PHASE3A1_POLICY_OPTION,
    output_dir: Path | None = PHASE3A1_OUTPUT_DIR_OPTION,
) -> None:
    """Audit Phase 3A.1 normalization and threshold gates."""

    try:
        audit = build_phase3a1_audit(spec_path, run_dir, policy_path)
    except (FileNotFoundError, ValidationError, ValueError) as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(1) from error

    if output_dir is not None:
        json_path, md_path = write_phase3a1_audit(output_dir, audit)
        typer.echo(f"wrote {json_path}")
        typer.echo(f"wrote {md_path}")
        return

    typer.echo(json.dumps(audit, indent=2, sort_keys=True))


if __name__ == "__main__":
    app()
