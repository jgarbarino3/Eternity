"""Run orchestration for V0 experiments."""

from __future__ import annotations

import json
import platform
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from eternity.artifacts import sha256_file
from eternity.claim_status import ClaimStatus
from eternity.ids import deterministic_hash, run_id_for_spec
from eternity.reporting import write_plots, write_report
from eternity.simulation import run_linear_tmm, write_tables
from eternity.specs import ExperimentSpec


def load_spec(path: Path) -> ExperimentSpec:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return ExperimentSpec.model_validate(payload)


def resolved_spec_payload(spec: ExperimentSpec) -> dict[str, Any]:
    return spec.model_dump(mode="json")


def git_value(args: list[str]) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            check=True,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return result.stdout.strip()


def provenance(spec_path: Path, spec_hash: str) -> dict[str, Any]:
    dirty = git_value(["status", "--short"])
    return {
        "created_at": datetime.now(UTC).isoformat(),
        "spec_path": str(spec_path),
        "spec_hash": spec_hash,
        "python_version": sys.version,
        "platform": platform.platform(),
        "git_commit": git_value(["rev-parse", "HEAD"]),
        "git_dirty": bool(dirty),
        "git_branch": git_value(["branch", "--show-current"]),
        "command": f"eternity run {spec_path}",
    }


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_experiment(spec_path: Path, results_root: Path = Path("results/runs")) -> Path:
    spec = load_spec(spec_path)
    resolved = resolved_spec_payload(spec)
    spec_hash = deterministic_hash(resolved)
    run_id = run_id_for_spec(resolved)
    run_dir = results_root / run_id
    plots_dir = run_dir / "plots"
    tables_dir = run_dir / "tables"
    run_dir.mkdir(parents=True, exist_ok=True)

    result = run_linear_tmm(spec)
    table_path = write_tables(result, tables_dir)
    plot_paths = write_plots(result, plots_dir)
    report_path = write_report(spec, result, run_dir, spec_hash, plot_paths)

    metrics = dict(result.metrics)
    metrics["spec_hash"] = spec_hash
    metrics["run_id"] = run_id

    write_json(run_dir / "resolved_spec.json", resolved)
    write_json(run_dir / "provenance.json", provenance(spec_path, spec_hash))
    write_json(run_dir / "metrics.json", metrics)
    write_json(run_dir / "warnings.json", result.warnings)
    write_json(
        run_dir / "manifest.json",
        {
            "run_id": run_id,
            "spec_hash": spec_hash,
            "artifacts": {
                "table": str(table_path.relative_to(run_dir)),
                "plots": [str(path.relative_to(run_dir)) for path in plot_paths],
                "report": str(report_path.relative_to(run_dir)),
            },
        },
    )
    gates_dir = run_dir / "validation_gates"
    gates_dir.mkdir(exist_ok=True)
    write_json(
        run_dir / "input_manifest.json",
        {
            "claim_scope": "synthetic V0 run",
            "source_type": "synthetic",
            "measurements": [],
            "registry_snapshot_sha256": None,
        },
    )
    write_json(
        run_dir / "claim_status.json",
        {
            "status": ClaimStatus.SYNTHETIC_SOFTWARE_FIXTURE.value,
            "can_feed_serious_core": False,
            "reason": "Synthetic fixture only; no measured or holdout data were used.",
        },
    )
    write_json(
        gates_dir / "input_integrity.json",
        {"status": "pass", "scope": "synthetic inline V0 inputs"},
    )
    write_json(
        gates_dir / "split_integrity.json",
        {"status": "not_applicable", "reason": "No calibration or holdout split in V0."},
    )

    artifact_hashes = {}
    for artifact_path in sorted(run_dir.rglob("*")):
        if artifact_path.is_file() and artifact_path.name != "artifact_hashes.json":
            artifact_hashes[str(artifact_path.relative_to(run_dir))] = sha256_file(artifact_path)
    write_json(run_dir / "artifact_hashes.json", artifact_hashes)
    return run_dir
