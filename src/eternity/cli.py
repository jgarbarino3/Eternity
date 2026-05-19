"""Command-line interface for Eternity V0."""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

import typer
import yaml
from pydantic import ValidationError

from eternity.artifacts import sha256_file
from eternity.phase3a1 import build_phase3a1_audit, write_phase3a1_audit
from eternity.phase3a7 import (
    DEFAULT_302010_PS_INTENSITY,
    DEFAULT_302010_REFLECTANCE,
    DEFAULT_D10_12V,
    DEFAULT_D10_INITIAL,
    DEFAULT_SOURCE_ROOT,
    DEFAULT_THESIS_PDF,
    RecoveryInputs,
    build_phase3a7_recovery,
    write_phase3a7_recovery,
)
from eternity.phase3a8 import (
    build_phase3a8_triage,
    load_phase3a7_recovery,
    write_phase3a8_triage,
)
from eternity.phase3a9 import build_phase3a9_packet, write_phase3a9_packet
from eternity.phase3a10 import (
    build_phase3a10_decision_from_paths,
    write_phase3a10_decision,
)
from eternity.phase3a11 import (
    build_phase3a11_packet_from_paths,
    write_phase3a11_packet,
)
from eternity.phase3a12 import (
    build_phase3a12_result_from_path,
    write_phase3a12_result,
)
from eternity.phase3b1 import build_phase3b1_packet, write_phase3b1_packet
from eternity.phase3c1 import build_phase3c1_packet_from_paths, write_phase3c1_packet
from eternity.phase3c2 import build_phase3c2_audit, write_phase3c2_audit
from eternity.phase3c3 import build_phase3c3_evaluation, write_phase3c3_evaluation
from eternity.phase3c4 import build_phase3c4_triage, write_phase3c4_triage
from eternity.phase3c5 import build_phase3c5_parity_packet, write_phase3c5_parity_packet
from eternity.phase3c6 import build_phase3c6_packet, write_phase3c6_packet
from eternity.phase3d1b import build_phase3d1b_packet_from_paths, write_phase3d1b_packet
from eternity.phase3d1c import build_phase3d1c_packet, write_phase3d1c_packet
from eternity.phase3d2 import build_phase3d2_packet, write_phase3d2_packet
from eternity.phase3e1 import build_phase3e1_scaffold, write_phase3e1_scaffold
from eternity.phase3e2a import (
    DEFAULT_METADATA_PATH as DEFAULT_PHASE3E2A_METADATA_PATH,
)
from eternity.phase3e2a import (
    DEFAULT_RAW_DIR as DEFAULT_PHASE3E2A_RAW_DIR,
)
from eternity.phase3e2a import (
    build_phase3e2a_packet,
    write_phase3e2a_packet,
)
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
PHASE3A7_SOURCE_ROOT_OPTION = typer.Option(
    DEFAULT_SOURCE_ROOT,
    "--source-root",
    help="Read-only root containing candidate CompleteEASE/Woollam .SE/.SEsnap/.iSE files.",
)
PHASE3A7_OUTPUT_DIR_OPTION = typer.Option(
    None,
    "--output-dir",
    help="Optional directory for JSON and Markdown recovery artifacts.",
)
PHASE3A7_THESIS_PDF_OPTION = typer.Option(DEFAULT_THESIS_PDF, "--thesis-pdf")
PHASE3A7_D10_INITIAL_OPTION = typer.Option(DEFAULT_D10_INITIAL, "--d10-initial")
PHASE3A7_D10_12V_OPTION = typer.Option(DEFAULT_D10_12V, "--d10-12v")
PHASE3A7_CANDIDATE_PS_INTENSITY_OPTION = typer.Option(
    DEFAULT_302010_PS_INTENSITY,
    "--candidate-ps-intensity",
)
PHASE3A7_CANDIDATE_REFLECTANCE_OPTION = typer.Option(
    DEFAULT_302010_REFLECTANCE,
    "--candidate-reflectance",
)
PHASE3A8_RECOVERY_JSON_OPTION = typer.Option(
    Path("docs/phase3a7_completeease_source_recovery.json"),
    "--recovery-json",
    help="Phase 3A.7 recovery JSON to triage without rescanning local source files.",
)
PHASE3A8_OUTPUT_DIR_OPTION = typer.Option(
    None,
    "--output-dir",
    help="Optional directory for JSON, Markdown, and policy triage artifacts.",
)
PHASE3A9_RUN_DIR_OPTION = typer.Option(
    DEFAULT_PHASE3A1_RUN_DIR,
    "--run-dir",
    help="Existing Phase 3A run directory with comparison_table.csv.",
)
PHASE3A9_POLICY_OPTION = typer.Option(
    Path("docs/phase3a8_relative_only_diagnostic_policy.yaml"),
    "--policy",
    help="Phase 3A.8 relative-only diagnostic policy.",
)
PHASE3A9_OUTPUT_DIR_OPTION = typer.Option(
    None,
    "--output-dir",
    help="Optional directory for JSON, Markdown, and CSV diagnostic artifacts.",
)
PHASE3A10_TRIAGE_OPTION = typer.Option(
    Path("docs/phase3a8_source_candidate_triage.json"),
    "--triage-json",
    help="Phase 3A.8 source-candidate triage JSON.",
)
PHASE3A10_DIAGNOSTIC_OPTION = typer.Option(
    Path("docs/phase3a9_relative_only_diagnostic_packet.json"),
    "--diagnostic-json",
    help="Phase 3A.9 relative-only diagnostic packet JSON.",
)
PHASE3A10_REGISTRY_OPTION = typer.Option(
    Path("lab_data/registry.yaml"),
    "--registry",
    help="Registry used to inspect Phase 3B TiON readiness.",
)
PHASE3A10_OUTPUT_DIR_OPTION = typer.Option(
    None,
    "--output-dir",
    help="Optional directory for JSON and Markdown branch-decision artifacts.",
)
PHASE3A11_DECISION_OPTION = typer.Option(
    Path("docs/phase3a10_branch_decision.json"),
    "--decision-json",
    help="Phase 3A.10 branch-decision JSON.",
)
PHASE3A11_TRIAGE_OPTION = typer.Option(
    Path("docs/phase3a8_source_candidate_triage.json"),
    "--triage-json",
    help="Phase 3A.8 source-candidate triage JSON.",
)
PHASE3A11_OUTPUT_DIR_OPTION = typer.Option(
    None,
    "--output-dir",
    help="Optional directory for JSON and Markdown manual follow-up artifacts.",
)
PHASE3A12_REVIEW_INPUT_OPTION = typer.Option(
    Path("docs/phase3a12_manual_source_review_input.json"),
    "--review-input",
    help="Phase 3A.12 manual source review input JSON.",
)
PHASE3A12_OUTPUT_DIR_OPTION = typer.Option(
    None,
    "--output-dir",
    help="Optional directory for JSON and Markdown manual source review results.",
)
PHASE3B1_REGISTRY_OPTION = typer.Option(
    Path("lab_data/registry.yaml"),
    "--registry",
    help="Registry used to inspect TiON evidence readiness.",
)
PHASE3B1_REPO_ROOT_OPTION = typer.Option(
    Path("."),
    "--repo-root",
    help="Repository root to scan for TiON plot candidates.",
)
PHASE3B1_OUTPUT_DIR_OPTION = typer.Option(
    None,
    "--output-dir",
    help="Optional directory for JSON and Markdown TiON evidence reality-check artifacts.",
)
PHASE3C1_ZIP_OPTION = typer.Option(
    Path("lab_data/raw/public_st_andrews_tin_2025/TiN-data_Pure.zip"),
    "--zip-path",
    help="St Andrews TiN dataset zip snapshot.",
)
PHASE3C1_RAW_OUTPUT_DIR_OPTION = typer.Option(
    Path("lab_data/raw/public_st_andrews_tin_2025"),
    "--raw-output-dir",
    help="Directory for canonical extracted raw-member snapshots.",
)
PHASE3C1_OUTPUT_DIR_OPTION = typer.Option(
    None,
    "--output-dir",
    help="Optional directory for JSON and Markdown Phase 3C.1 pairing artifacts.",
)
PHASE3C2_RUN_DIR_OPTION = typer.Option(
    Path("results/runs/run_42fe0ad6dd295019"),
    "--run-dir",
    help="Existing St Andrews validation-candidate run directory to audit.",
)
PHASE3C2_PAIRING_JSON_OPTION = typer.Option(
    Path("docs/phase3c1_standrews_tin_pairing.json"),
    "--pairing-json",
    help="Phase 3C.1 pairing JSON.",
)
PHASE3C2_REGISTRY_OPTION = typer.Option(
    Path("lab_data/registry.yaml"),
    "--registry",
    help="Registry containing the St Andrews validation split.",
)
PHASE3C2_OUTPUT_DIR_OPTION = typer.Option(
    None,
    "--output-dir",
    help="Optional directory for JSON, Markdown, and policy audit artifacts.",
)
PHASE3C3_RUN_DIR_OPTION = typer.Option(
    None,
    "--run-dir",
    help="Threshold-locked St Andrews clean-run directory to evaluate.",
)
PHASE3C3_POLICY_OPTION = typer.Option(
    Path("docs/phase3c3_standrews_threshold_policy.yaml"),
    "--policy",
    help="Locked Phase 3C.3 threshold policy.",
)
PHASE3C3_PAIRING_JSON_OPTION = typer.Option(
    Path("docs/phase3c1_standrews_tin_pairing.json"),
    "--pairing-json",
    help="Phase 3C.1 pairing JSON.",
)
PHASE3C3_OUTPUT_DIR_OPTION = typer.Option(
    None,
    "--output-dir",
    help="Optional directory for JSON and Markdown clean-run evaluation artifacts.",
)
PHASE3C4_RUN_DIR_OPTION = typer.Option(
    Path("results/runs/run_f6ea582618328f44"),
    "--run-dir",
    help="Threshold-locked St Andrews clean-run directory to triage.",
)
PHASE3C4_EVALUATION_JSON_OPTION = typer.Option(
    Path("docs/phase3c3_clean_run_evaluation.json"),
    "--evaluation-json",
    help="Phase 3C.3 clean-run evaluation JSON.",
)
PHASE3C4_PAIRING_JSON_OPTION = typer.Option(
    Path("docs/phase3c1_standrews_tin_pairing.json"),
    "--pairing-json",
    help="Phase 3C.1 pairing JSON with St Andrews source archive metadata.",
)
PHASE3C4_OUTPUT_DIR_OPTION = typer.Option(
    None,
    "--output-dir",
    help="Optional directory for JSON, Markdown, and CSV triage artifacts.",
)
PHASE3C5_TRIAGE_JSON_OPTION = typer.Option(
    Path("docs/phase3c4_standrews_failure_triage.json"),
    "--triage-json",
    help="Phase 3C.4 failure-triage JSON.",
)
PHASE3C5_PAIRING_JSON_OPTION = typer.Option(
    Path("docs/phase3c1_standrews_tin_pairing.json"),
    "--pairing-json",
    help="Phase 3C.1 pairing JSON with St Andrews source archive metadata.",
)
PHASE3C5_RUN_DIR_OPTION = typer.Option(
    Path("results/runs/run_f6ea582618328f44"),
    "--run-dir",
    help="Threshold-locked St Andrews clean-run directory used for parity context.",
)
PHASE3C5_OUTPUT_DIR_OPTION = typer.Option(
    None,
    "--output-dir",
    help="Optional directory for JSON and Markdown source-model parity artifacts.",
)
PHASE3C6_PARITY_JSON_OPTION = typer.Option(
    Path("docs/phase3c5_standrews_source_model_parity.json"),
    "--parity-json",
    help="Phase 3C.5 source-model parity JSON.",
)
PHASE3C6_PAIRING_JSON_OPTION = typer.Option(
    Path("docs/phase3c1_standrews_tin_pairing.json"),
    "--pairing-json",
    help="Phase 3C.1 pairing JSON with the selected St Andrews source archive.",
)
PHASE3C6_RUN_DIR_OPTION = typer.Option(
    Path("results/runs/run_f6ea582618328f44"),
    "--run-dir",
    help="Threshold-locked St Andrews clean-run directory used for parity variants.",
)
PHASE3C6_OUTPUT_DIR_OPTION = typer.Option(
    None,
    "--output-dir",
    help="Optional directory for JSON, Markdown, and CSV source-model parity artifacts.",
)
PHASE3D1B_ZIP_OPTION = typer.Option(
    Path("lab_data/raw/public_exeter_bohn_ito_2021/OpenData.zip"),
    "--zip-path",
    help="Exeter/Bohn ITO OpenData.zip snapshot.",
)
PHASE3D1B_RAW_OUTPUT_DIR_OPTION = typer.Option(
    Path("lab_data/raw/public_exeter_bohn_ito_2021"),
    "--raw-output-dir",
    help="Directory for canonical Exeter/Bohn extracted CSV artifacts.",
)
PHASE3D1B_OUTPUT_DIR_OPTION = typer.Option(
    None,
    "--output-dir",
    help="Optional directory for JSON, Markdown, and YAML split-lock artifacts.",
)
PHASE3D1C_STATIC_R0_OPTION = typer.Option(
    Path("lab_data/raw/public_exeter_bohn_ito_2021/exeter_bohn_fig2_static_r0.csv"),
    "--static-r0",
    help="Phase 3D.1B canonical Exeter/Bohn static R0 surface.",
)
PHASE3D1C_SPLIT_LOCK_OPTION = typer.Option(
    Path("docs/phase3d1b_exeter_bohn_split_lock.yaml"),
    "--split-lock",
    help="Phase 3D.1B split-lock YAML.",
)
PHASE3D1C_OUTPUT_DIR_OPTION = typer.Option(
    None,
    "--output-dir",
    help="Optional directory for JSON, Markdown, and CSV no-fit reconstruction artifacts.",
)
PHASE3D2_METADATA_OPTION = typer.Option(
    Path("lab_data/raw/public_saha_tin_azo_2023/figshare_article_23734116.json"),
    "--metadata",
    help="Saha TiN/AZO Figshare API metadata snapshot.",
)
PHASE3D2_RAW_DIR_OPTION = typer.Option(
    Path("lab_data/raw/public_saha_tin_azo_2023"),
    "--raw-dir",
    help="Directory containing downloaded Saha TiN/AZO OPJU source-data files.",
)
PHASE3D2_OUTPUT_DIR_OPTION = typer.Option(
    None,
    "--output-dir",
    help="Optional directory for JSON and Markdown source-data intake artifacts.",
)
PHASE3E1_REGISTRY_OPTION = typer.Option(
    Path("docs/phase3e1_dataset_candidate_registry.yaml"),
    "--registry",
    help="Phase 3E.1 public dataset candidate registry.",
)
PHASE3E1_OUTPUT_DIR_OPTION = typer.Option(
    None,
    "--output-dir",
    help="Optional directory for JSON, Markdown, and claim-summary artifacts.",
)
PHASE3E2A_METADATA_OPTION = typer.Option(
    DEFAULT_PHASE3E2A_METADATA_PATH,
    "--metadata",
    help="Wang W/WO3 Figshare API metadata snapshot.",
)
PHASE3E2A_RAW_DIR_OPTION = typer.Option(
    DEFAULT_PHASE3E2A_RAW_DIR,
    "--raw-dir",
    help="Directory containing selected Wang W/WO3 source-data spreadsheets.",
)
PHASE3E2A_OUTPUT_DIR_OPTION = typer.Option(
    None,
    "--output-dir",
    help="Optional directory for JSON and Markdown Wang baseline intake artifacts.",
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


@app.command("phase3a7-recovery")
def phase3a7_recovery(
    source_root: Path = PHASE3A7_SOURCE_ROOT_OPTION,
    thesis_pdf: Path = PHASE3A7_THESIS_PDF_OPTION,
    d10_initial: Path = PHASE3A7_D10_INITIAL_OPTION,
    d10_12v: Path = PHASE3A7_D10_12V_OPTION,
    candidate_ps_intensity: Path = PHASE3A7_CANDIDATE_PS_INTENSITY_OPTION,
    candidate_reflectance: Path = PHASE3A7_CANDIDATE_REFLECTANCE_OPTION,
    output_dir: Path | None = PHASE3A7_OUTPUT_DIR_OPTION,
) -> None:
    """Recover Phase 3A.7 CompleteEASE/Woollam source provenance."""

    try:
        recovery = build_phase3a7_recovery(
            RecoveryInputs(
                source_root=source_root,
                thesis_pdf=thesis_pdf,
                d10_initial=d10_initial,
                d10_12v=d10_12v,
                candidate_ps_intensity=candidate_ps_intensity,
                candidate_reflectance=candidate_reflectance,
            )
        )
    except FileNotFoundError as error:
        typer.echo(f"Phase 3A.7 input not found: {error}", err=True)
        raise typer.Exit(1) from error

    if output_dir is not None:
        json_path, md_path = write_phase3a7_recovery(output_dir, recovery)
        typer.echo(f"wrote {json_path}")
        typer.echo(f"wrote {md_path}")
        return

    typer.echo(json.dumps(recovery, indent=2, sort_keys=True))


@app.command("phase3a8-triage")
def phase3a8_triage(
    recovery_json: Path = PHASE3A8_RECOVERY_JSON_OPTION,
    output_dir: Path | None = PHASE3A8_OUTPUT_DIR_OPTION,
) -> None:
    """Triage Phase 3A.7 source candidates without fresh source scanning."""

    try:
        recovery = load_phase3a7_recovery(recovery_json)
        triage = build_phase3a8_triage(recovery)
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as error:
        typer.echo(f"Phase 3A.8 triage failed: {error}", err=True)
        raise typer.Exit(1) from error

    if output_dir is not None:
        json_path, md_path, policy_path = write_phase3a8_triage(output_dir, triage)
        typer.echo(f"wrote {json_path}")
        typer.echo(f"wrote {md_path}")
        typer.echo(f"wrote {policy_path}")
        return

    typer.echo(json.dumps(triage, indent=2, sort_keys=True))


@app.command("phase3a9-diagnostic")
def phase3a9_diagnostic(
    run_dir: Path = PHASE3A9_RUN_DIR_OPTION,
    policy_path: Path = PHASE3A9_POLICY_OPTION,
    output_dir: Path | None = PHASE3A9_OUTPUT_DIR_OPTION,
) -> None:
    """Write a Phase 3A.9 relative-only diagnostic packet for an existing run."""

    try:
        packet = build_phase3a9_packet(run_dir, policy_path)
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as error:
        typer.echo(f"Phase 3A.9 diagnostic failed: {error}", err=True)
        raise typer.Exit(1) from error

    if output_dir is not None:
        json_path, md_path, csv_path = write_phase3a9_packet(output_dir, packet)
        typer.echo(f"wrote {json_path}")
        typer.echo(f"wrote {md_path}")
        typer.echo(f"wrote {csv_path}")
        return

    packet_without_table = dict(packet)
    packet_without_table.pop("table", None)
    typer.echo(json.dumps(packet_without_table, indent=2, sort_keys=True))


@app.command("phase3a10-decision")
def phase3a10_decision(
    triage_json: Path = PHASE3A10_TRIAGE_OPTION,
    diagnostic_json: Path = PHASE3A10_DIAGNOSTIC_OPTION,
    registry_path: Path = PHASE3A10_REGISTRY_OPTION,
    output_dir: Path | None = PHASE3A10_OUTPUT_DIR_OPTION,
) -> None:
    """Decide whether Phase 3A should do manual source follow-up or return to Phase 3B."""

    try:
        packet = build_phase3a10_decision_from_paths(
            triage_json,
            diagnostic_json,
            registry_path,
        )
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as error:
        typer.echo(f"Phase 3A.10 decision failed: {error}", err=True)
        raise typer.Exit(1) from error

    if output_dir is not None:
        json_path, md_path = write_phase3a10_decision(output_dir, packet)
        typer.echo(f"wrote {json_path}")
        typer.echo(f"wrote {md_path}")
        return

    typer.echo(json.dumps(packet, indent=2, sort_keys=True))


@app.command("phase3a11-packet")
def phase3a11_packet(
    decision_json: Path = PHASE3A11_DECISION_OPTION,
    triage_json: Path = PHASE3A11_TRIAGE_OPTION,
    output_dir: Path | None = PHASE3A11_OUTPUT_DIR_OPTION,
) -> None:
    """Build the bounded Phase 3A.11 manual source follow-up packet."""

    try:
        packet = build_phase3a11_packet_from_paths(decision_json, triage_json)
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as error:
        typer.echo(f"Phase 3A.11 packet failed: {error}", err=True)
        raise typer.Exit(1) from error

    if output_dir is not None:
        json_path, md_path = write_phase3a11_packet(output_dir, packet)
        typer.echo(f"wrote {json_path}")
        typer.echo(f"wrote {md_path}")
        return

    typer.echo(json.dumps(packet, indent=2, sort_keys=True))


@app.command("phase3a12-result")
def phase3a12_result(
    review_input: Path = PHASE3A12_REVIEW_INPUT_OPTION,
    output_dir: Path | None = PHASE3A12_OUTPUT_DIR_OPTION,
) -> None:
    """Build the Phase 3A.12 bounded manual source review result."""

    try:
        result = build_phase3a12_result_from_path(review_input)
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as error:
        typer.echo(f"Phase 3A.12 result failed: {error}", err=True)
        raise typer.Exit(1) from error

    if output_dir is not None:
        json_path, md_path = write_phase3a12_result(output_dir, result)
        typer.echo(f"wrote {json_path}")
        typer.echo(f"wrote {md_path}")
        return

    typer.echo(json.dumps(result, indent=2, sort_keys=True))


@app.command("phase3b1-reality-check")
def phase3b1_reality_check(
    registry_path: Path = PHASE3B1_REGISTRY_OPTION,
    repo_root: Path = PHASE3B1_REPO_ROOT_OPTION,
    output_dir: Path | None = PHASE3B1_OUTPUT_DIR_OPTION,
) -> None:
    """Build the Phase 3B.1 TiON evidence reality-check packet."""

    try:
        packet = build_phase3b1_packet(registry_path, repo_root)
    except (FileNotFoundError, yaml.YAMLError, KeyError, ValueError) as error:
        typer.echo(f"Phase 3B.1 reality check failed: {error}", err=True)
        raise typer.Exit(1) from error

    if output_dir is not None:
        json_path, md_path = write_phase3b1_packet(output_dir, packet)
        typer.echo(f"wrote {json_path}")
        typer.echo(f"wrote {md_path}")
        return

    typer.echo(json.dumps(packet, indent=2, sort_keys=True))


@app.command("phase3c1-intake")
def phase3c1_intake(
    zip_path: Path = PHASE3C1_ZIP_OPTION,
    raw_output_dir: Path = PHASE3C1_RAW_OUTPUT_DIR_OPTION,
    output_dir: Path | None = PHASE3C1_OUTPUT_DIR_OPTION,
) -> None:
    """Extract and report Phase 3C.1 St Andrews TiN pairing artifacts."""

    try:
        packet = build_phase3c1_packet_from_paths(zip_path, raw_output_dir)
    except (FileNotFoundError, KeyError, ValueError) as error:
        typer.echo(f"Phase 3C.1 intake failed: {error}", err=True)
        raise typer.Exit(1) from error

    if output_dir is not None:
        json_path, md_path = write_phase3c1_packet(output_dir, packet)
        typer.echo(f"wrote {json_path}")
        typer.echo(f"wrote {md_path}")
        return

    typer.echo(json.dumps(packet, indent=2, sort_keys=True))


@app.command("phase3c2-audit")
def phase3c2_audit(
    run_dir: Path = PHASE3C2_RUN_DIR_OPTION,
    pairing_json: Path = PHASE3C2_PAIRING_JSON_OPTION,
    registry_path: Path = PHASE3C2_REGISTRY_OPTION,
    output_dir: Path | None = PHASE3C2_OUTPUT_DIR_OPTION,
) -> None:
    """Audit Phase 3C.2 St Andrews candidate run and future threshold policy."""

    try:
        audit = build_phase3c2_audit(run_dir, pairing_json, registry_path)
    except (FileNotFoundError, json.JSONDecodeError, ValueError, ValidationError) as error:
        typer.echo(f"Phase 3C.2 audit failed: {error}", err=True)
        raise typer.Exit(1) from error

    if output_dir is not None:
        json_path, md_path, policy_path = write_phase3c2_audit(output_dir, audit)
        typer.echo(f"wrote {json_path}")
        typer.echo(f"wrote {md_path}")
        typer.echo(f"wrote {policy_path}")
        return

    typer.echo(json.dumps(audit, indent=2, sort_keys=True))


@app.command("phase3c3-evaluate")
def phase3c3_evaluate(
    run_dir: Path | None = PHASE3C3_RUN_DIR_OPTION,
    policy: Path = PHASE3C3_POLICY_OPTION,
    pairing_json: Path = PHASE3C3_PAIRING_JSON_OPTION,
    output_dir: Path | None = PHASE3C3_OUTPUT_DIR_OPTION,
) -> None:
    """Evaluate Phase 3C.3 St Andrews threshold-locked clean run."""

    if run_dir is None:
        typer.echo("Phase 3C.3 evaluation failed: --run-dir is required", err=True)
        raise typer.Exit(1)

    try:
        evaluation = build_phase3c3_evaluation(run_dir, policy, pairing_json)
    except (FileNotFoundError, json.JSONDecodeError, KeyError, ValueError) as error:
        typer.echo(f"Phase 3C.3 evaluation failed: {error}", err=True)
        raise typer.Exit(1) from error

    if output_dir is not None:
        json_path, md_path = write_phase3c3_evaluation(output_dir, evaluation)
        typer.echo(f"wrote {json_path}")
        typer.echo(f"wrote {md_path}")
        return

    typer.echo(json.dumps(evaluation, indent=2, sort_keys=True))


@app.command("phase3c4-triage")
def phase3c4_triage(
    run_dir: Path = PHASE3C4_RUN_DIR_OPTION,
    evaluation_json: Path = PHASE3C4_EVALUATION_JSON_OPTION,
    pairing_json: Path = PHASE3C4_PAIRING_JSON_OPTION,
    output_dir: Path | None = PHASE3C4_OUTPUT_DIR_OPTION,
) -> None:
    """Triage the failed Phase 3C.3 St Andrews clean run."""

    try:
        packet = build_phase3c4_triage(run_dir, evaluation_json, pairing_json)
    except (FileNotFoundError, json.JSONDecodeError, KeyError, ValueError) as error:
        typer.echo(f"Phase 3C.4 triage failed: {error}", err=True)
        raise typer.Exit(1) from error

    if output_dir is not None:
        json_path, md_path, csv_path = write_phase3c4_triage(output_dir, packet)
        typer.echo(f"wrote {json_path}")
        typer.echo(f"wrote {md_path}")
        typer.echo(f"wrote {csv_path}")
        return

    typer.echo(json.dumps(packet, indent=2, sort_keys=True))


@app.command("phase3c5-parity")
def phase3c5_parity(
    triage_json: Path = PHASE3C5_TRIAGE_JSON_OPTION,
    pairing_json: Path = PHASE3C5_PAIRING_JSON_OPTION,
    run_dir: Path = PHASE3C5_RUN_DIR_OPTION,
    output_dir: Path | None = PHASE3C5_OUTPUT_DIR_OPTION,
) -> None:
    """Record St Andrews raw Woollam source-model parity gaps."""

    try:
        packet = build_phase3c5_parity_packet(triage_json, pairing_json, run_dir)
    except (FileNotFoundError, json.JSONDecodeError, KeyError, ValueError) as error:
        typer.echo(f"Phase 3C.5 parity failed: {error}", err=True)
        raise typer.Exit(1) from error

    if output_dir is not None:
        json_path, md_path = write_phase3c5_parity_packet(output_dir, packet)
        typer.echo(f"wrote {json_path}")
        typer.echo(f"wrote {md_path}")
        return

    typer.echo(json.dumps(packet, indent=2, sort_keys=True))


@app.command("phase3c6-parity")
def phase3c6_parity(
    parity_json: Path = PHASE3C6_PARITY_JSON_OPTION,
    pairing_json: Path = PHASE3C6_PAIRING_JSON_OPTION,
    run_dir: Path = PHASE3C6_RUN_DIR_OPTION,
    output_dir: Path | None = PHASE3C6_OUTPUT_DIR_OPTION,
) -> None:
    """Run bounded St Andrews source-model parity variants."""

    try:
        packet = build_phase3c6_packet(parity_json, pairing_json, run_dir)
    except (FileNotFoundError, json.JSONDecodeError, KeyError, ValueError) as error:
        typer.echo(f"Phase 3C.6A parity failed: {error}", err=True)
        raise typer.Exit(1) from error

    if output_dir is not None:
        json_path, md_path, csv_path = write_phase3c6_packet(output_dir, packet)
        typer.echo(f"wrote {json_path}")
        typer.echo(f"wrote {md_path}")
        typer.echo(f"wrote {csv_path}")
        return

    typer.echo(json.dumps(packet, indent=2, sort_keys=True))


@app.command("phase3d1b-extract")
def phase3d1b_extract(
    zip_path: Path = PHASE3D1B_ZIP_OPTION,
    raw_output_dir: Path = PHASE3D1B_RAW_OUTPUT_DIR_OPTION,
    output_dir: Path | None = PHASE3D1B_OUTPUT_DIR_OPTION,
) -> None:
    """Extract Exeter/Bohn Figure 1 epsilon and Figure 2 static R0 artifacts."""

    try:
        packet = build_phase3d1b_packet_from_paths(zip_path, raw_output_dir)
    except (FileNotFoundError, KeyError, ValueError, zipfile.BadZipFile) as error:
        typer.echo(f"Phase 3D.1B extraction failed: {error}", err=True)
        raise typer.Exit(1) from error

    if output_dir is not None:
        json_path, md_path, split_path = write_phase3d1b_packet(output_dir, packet)
        typer.echo(f"wrote {json_path}")
        typer.echo(f"wrote {md_path}")
        typer.echo(f"wrote {split_path}")
        return

    typer.echo(json.dumps(packet, indent=2, sort_keys=True))


@app.command("phase3d1c-reconstruct")
def phase3d1c_reconstruct(
    static_r0_path: Path = PHASE3D1C_STATIC_R0_OPTION,
    split_lock_path: Path = PHASE3D1C_SPLIT_LOCK_OPTION,
    output_dir: Path | None = PHASE3D1C_OUTPUT_DIR_OPTION,
) -> None:
    """Run the Exeter/Bohn package-constant no-fit static reconstruction."""

    try:
        packet = build_phase3d1c_packet(static_r0_path, split_lock_path)
    except (FileNotFoundError, KeyError, ValueError, yaml.YAMLError) as error:
        typer.echo(f"Phase 3D.1C reconstruction failed: {error}", err=True)
        raise typer.Exit(1) from error

    if output_dir is not None:
        json_path, md_path, csv_path = write_phase3d1c_packet(output_dir, packet)
        typer.echo(f"wrote {json_path}")
        typer.echo(f"wrote {md_path}")
        typer.echo(f"wrote {csv_path}")
        return

    packet_without_table = dict(packet)
    packet_without_table.pop("table", None)
    typer.echo(json.dumps(packet_without_table, indent=2, sort_keys=True))


@app.command("phase3d2-intake")
def phase3d2_intake(
    metadata_path: Path = PHASE3D2_METADATA_OPTION,
    raw_dir: Path = PHASE3D2_RAW_DIR_OPTION,
    output_dir: Path | None = PHASE3D2_OUTPUT_DIR_OPTION,
) -> None:
    """Audit the Saha TiN/AZO Figshare OPJU source-data package."""

    try:
        packet = build_phase3d2_packet(metadata_path, raw_dir)
    except (FileNotFoundError, KeyError, ValueError, json.JSONDecodeError) as error:
        typer.echo(f"Phase 3D.2 intake failed: {error}", err=True)
        raise typer.Exit(1) from error

    if output_dir is not None:
        json_path, md_path = write_phase3d2_packet(output_dir, packet)
        typer.echo(f"wrote {json_path}")
        typer.echo(f"wrote {md_path}")
        return

    typer.echo(json.dumps(packet, indent=2, sort_keys=True))


@app.command("phase3e1-scaffold")
def phase3e1_scaffold(
    registry_path: Path = PHASE3E1_REGISTRY_OPTION,
    output_dir: Path | None = PHASE3E1_OUTPUT_DIR_OPTION,
) -> None:
    """Build the Phase 3E.1 public-dataset gate and assistant scaffold."""

    try:
        packet = build_phase3e1_scaffold(registry_path)
    except (FileNotFoundError, yaml.YAMLError, ValueError) as error:
        typer.echo(f"Phase 3E.1 scaffold failed: {error}", err=True)
        raise typer.Exit(1) from error

    if output_dir is not None:
        json_path, md_path, summary_path = write_phase3e1_scaffold(output_dir, packet)
        typer.echo(f"wrote {json_path}")
        typer.echo(f"wrote {md_path}")
        typer.echo(f"wrote {summary_path}")
        return

    typer.echo(json.dumps(packet, indent=2, sort_keys=True))


@app.command("phase3e2a-wang-intake")
def phase3e2a_wang_intake(
    metadata_path: Path = PHASE3E2A_METADATA_OPTION,
    raw_dir: Path = PHASE3E2A_RAW_DIR_OPTION,
    output_dir: Path | None = PHASE3E2A_OUTPUT_DIR_OPTION,
) -> None:
    """Audit the Wang W/WO3 non-ENZ baseline source-data package."""

    try:
        packet = build_phase3e2a_packet(metadata_path, raw_dir)
    except (
        FileNotFoundError,
        KeyError,
        ValueError,
        json.JSONDecodeError,
        zipfile.BadZipFile,
    ) as error:
        typer.echo(f"Phase 3E.2A Wang intake failed: {error}", err=True)
        raise typer.Exit(1) from error

    if output_dir is not None:
        json_path, md_path = write_phase3e2a_packet(output_dir, packet)
        typer.echo(f"wrote {json_path}")
        typer.echo(f"wrote {md_path}")
        return

    typer.echo(json.dumps(packet, indent=2, sort_keys=True))


if __name__ == "__main__":
    app()
