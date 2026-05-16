"""Run orchestration for V0 experiments."""

from __future__ import annotations

import json
import platform
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
import yaml

from eternity.artifacts import sha256_file
from eternity.claim_status import ClaimStatus
from eternity.ids import deterministic_hash, run_id_for_spec
from eternity.optical_data import load_reflectance_spectrum
from eternity.registry import (
    LabDataRegistry,
    artifact_path,
    load_registry,
    validate_registry_integrity,
)
from eternity.reporting import write_plots, write_report
from eternity.simulation import SimulationResult, run_linear_tmm, write_tables
from eternity.specs import ExperimentSpec, ValidationComparisonSpec


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


def _write_text(path: Path, value: str) -> None:
    path.write_text(value, encoding="utf-8")


def _registry_payloads(
    registry: LabDataRegistry,
    registry_path: Path,
    spec: ExperimentSpec,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    layer_model_refs = [layer.material_model_ref for layer in spec.sample.layers]
    if layer_model_refs:
        material_models = {
            model_ref: registry.material_models[model_ref].model_dump(mode="json")
            for model_ref in layer_model_refs
        }
        raw_artifact_refs = [
            registry.material_models[model_ref].raw_artifact_ref for model_ref in layer_model_refs
        ]
        source_measurement_refs = [
            registry.material_models[model_ref].source_measurement_ref
            for model_ref in layer_model_refs
        ]
    else:
        model_ref = spec.sample.material_model.material_model_ref
        if model_ref is None:
            raise ValueError("tabulated_epsilon spec requires material_model_ref")
        material_models = {model_ref: registry.material_models[model_ref].model_dump(mode="json")}
        raw_artifact_refs = [registry.material_models[model_ref].raw_artifact_ref]
        source_measurement_refs = [registry.material_models[model_ref].source_measurement_ref]

    sample = registry.samples.get(spec.sample.sample_id)
    stack = registry.stacks.get(spec.sample.stack_ref or "")
    if stack is None and material_models:
        first_model = registry.material_models[next(iter(material_models))]
        stack = next(
            (
                candidate
                for candidate in registry.stacks.values()
                if candidate.sample_ref == first_model.sample_ref
            ),
            None,
        )

    material_payload: dict[str, Any] = (
        {"layer_material_models": material_models}
        if layer_model_refs
        else next(iter(material_models.values()))
    )
    sample_stack = {
        "sample": sample.model_dump(mode="json") if sample else None,
        "stack": stack.model_dump(mode="json") if stack else None,
        "spec_layers": [layer.model_dump(mode="json") for layer in spec.sample.layers],
    }
    source_provenance = {
        "registry_path": str(registry_path),
        "layer_material_model_refs": layer_model_refs,
        "material_model_ref": spec.sample.material_model.material_model_ref,
        "raw_artifact_refs": [ref for ref in raw_artifact_refs if ref is not None],
        "source_measurement_refs": [ref for ref in source_measurement_refs if ref is not None],
        "source_type": "lab",
    }
    return material_payload, sample_stack, source_provenance


def _manifest_artifact_kind(relative_path: str) -> str:
    if relative_path.startswith("validation_gates/"):
        return "validation_gate"
    if relative_path.startswith("plots/"):
        return "plot"
    if relative_path.startswith("tables/"):
        return "spectrum_table"
    known_kinds = {
        "artifact_hashes.json": "artifact_hash_index",
        "assumptions.json": "assumptions",
        "claim_status.json": "claim_status",
        "comparison_table.csv": "validation_comparison_table",
        "data_splits.json": "data_split_snapshot",
        "environment.json": "environment",
        "fit_diagnostics.json": "fit_diagnostics",
        "fit_plan.json": "fit_plan",
        "fit_result.json": "fit_result",
        "holdout_residuals.csv": "holdout_residual_table",
        "input_manifest.json": "input_manifest",
        "material_model.json": "material_model",
        "metrics.json": "metrics",
        "prediction_table.csv": "prediction_table",
        "provenance.json": "run_provenance",
        "provenance_gaps.json": "provenance_gaps",
        "raw_artifacts.json": "raw_artifact_snapshot",
        "registry_snapshot.json": "registry_snapshot",
        "registry_snapshot.sha256": "registry_snapshot_hash",
        "report.md": "human_report",
        "resolved_spec.json": "resolved_spec",
        "rt_provenance_audit.json": "rt_provenance_audit",
        "sample_stack.json": "sample_stack",
        "source_provenance.json": "source_provenance",
        "validation_summary.json": "validation_summary",
        "validity_envelope.json": "validity_envelope",
        "warnings.json": "warnings",
    }
    return known_kinds.get(relative_path, "artifact")


def _manifest_artifact_role(relative_path: str) -> str:
    if relative_path in {
        "material_model.json",
        "fit_plan.json",
        "fit_result.json",
        "fit_diagnostics.json",
        "source_provenance.json",
    }:
        return "calibration"
    if (
        relative_path in {"comparison_table.csv", "holdout_residuals.csv"}
        or relative_path.startswith("validation_gates/")
        or relative_path == "validation_summary.json"
    ):
        return "holdout"
    return "neither"


def _write_validation_candidate_artifacts(
    spec: ExperimentSpec,
    validation: ValidationComparisonSpec,
    result: SimulationResult,
    registry: LabDataRegistry,
    registry_path: Path,
    run_dir: Path,
    gates_dir: Path,
) -> dict[str, float | str]:
    measurement = registry.measurements[validation.holdout_measurement_ref]
    artifact = registry.raw_artifacts[measurement.raw_artifact_ref]
    spectrum = load_reflectance_spectrum(artifact_path(artifact, registry_path))

    lower = max(validation.wavelength_window.min, float(result.wavelengths_nm.min()))
    upper = min(validation.wavelength_window.max, float(result.wavelengths_nm.max()))
    mask = (spectrum.wavelengths_nm >= lower) & (spectrum.wavelengths_nm <= upper)
    if not np.any(mask):
        raise ValueError("validation wavelength window has no overlap with holdout measurement")

    measured_wavelengths = spectrum.wavelengths_nm[mask]
    measured = spectrum.intensity[mask]
    predicted = np.interp(measured_wavelengths, result.wavelengths_nm, result.reflection)
    residual = predicted - measured
    rows = ["wavelength_nm,prediction,measurement,residual,measurement_ref"]
    rows.extend(
        (
            f"{wavelength:.9g},{prediction:.9g},{measurement_value:.9g},"
            f"{residual_value:.9g},{validation.holdout_measurement_ref}"
        )
        for wavelength, prediction, measurement_value, residual_value in zip(
            measured_wavelengths,
            predicted,
            measured,
            residual,
            strict=True,
        )
    )
    _write_text(run_dir / "comparison_table.csv", "\n".join(rows) + "\n")
    _write_text(
        run_dir / "holdout_residuals.csv",
        (run_dir / "comparison_table.csv").read_text(encoding="utf-8").replace(
            "measurement,",
            "holdout,",
            1,
        ),
    )

    split = registry.splits[validation.split_ref]
    metrics = {
        "validation_points": float(measured_wavelengths.size),
        "validation_window_min_nm": float(lower),
        "validation_window_max_nm": float(upper),
        "validation_mean_abs_residual": float(np.mean(np.abs(residual))),
        "validation_rmse": float(np.sqrt(np.mean(residual**2))),
        "validation_max_abs_residual": float(np.max(np.abs(residual))),
    }
    stack = registry.stacks[measurement.stack_ref]
    stack_mapping_status = (
        "blocked"
        if stack.notes
        and any(
            term in stack.notes.lower()
            for term in ("unresolved", "not source-confirmed", "filename-level")
        )
        else "pass"
    )
    write_json(
        gates_dir / "stack_mapping.json",
        {
            "status": stack_mapping_status,
            "sample_ref": measurement.sample_ref,
            "stack_ref": measurement.stack_ref,
            "geometry_incidence_angle": measurement.geometry_incidence_angle.model_dump(
                mode="json"
            ),
            "geometry_polarization": measurement.geometry_polarization,
            "source": stack.notes,
        },
    )
    forbidden_refs = [
        validation.holdout_measurement_ref,
        *validation.auxiliary_measurement_refs,
    ]
    forbidden_raw_refs = [
        registry.measurements[measurement_ref].raw_artifact_ref
        for measurement_ref in forbidden_refs
    ]
    used_material_model_refs = [layer.material_model_ref for layer in spec.sample.layers]
    used_measurement_refs = [
        registry.material_models[model_ref].source_measurement_ref
        for model_ref in used_material_model_refs
    ]
    used_raw_refs = [
        registry.material_models[model_ref].raw_artifact_ref
        for model_ref in used_material_model_refs
    ]
    leaked_measurement_refs = sorted(set(used_measurement_refs) & set(forbidden_refs))
    leaked_raw_artifact_refs = sorted(set(used_raw_refs) & set(forbidden_raw_refs))
    leakage_pass = (
        not split.fitting_may_access_holdout_y
        and not leaked_measurement_refs
        and not leaked_raw_artifact_refs
    )
    write_json(
        gates_dir / "no_fit_leakage.json",
        {
            "status": "pass" if leakage_pass else "fail",
            "forbidden_measurement_refs": forbidden_refs,
            "forbidden_raw_artifact_refs": forbidden_raw_refs,
            "used_material_model_refs": used_material_model_refs,
            "used_measurement_refs": used_measurement_refs,
            "used_raw_artifact_refs": used_raw_refs,
            "leaked_measurement_refs": leaked_measurement_refs,
            "leaked_raw_artifact_refs": leaked_raw_artifact_refs,
            "fitting_may_access_holdout_y": split.fitting_may_access_holdout_y,
            "reason": (
                "Frozen material inputs do not reference forbidden holdout or auxiliary data."
                if leakage_pass
                else "Forbidden holdout or auxiliary data leaked into fit/material inputs."
            ),
        },
    )
    write_json(
        gates_dir / "thresholds_predeclared.json",
        {
            "status": "blocked" if validation.thresholds_ref is None else "pass",
            "thresholds_ref": validation.thresholds_ref,
            "reason": (
                "No Pro/user-approved residual thresholds were predeclared."
                if validation.thresholds_ref is None
                else "Threshold policy was declared before residual inspection."
            ),
        },
    )
    write_json(
        gates_dir / "normalization_gate.json",
        {
            "status": "blocked",
            "reason": (
                "The holdout export is labeled Intensity/arb; it has not yet been proven "
                "to be directly comparable to absolute TMM reflectance."
            ),
        },
    )
    write_json(
        gates_dir / "claim_status_gate.json",
        {
            "status": "pass",
            "status_ceiling": validation.status_ceiling,
            "can_feed_serious_core": False,
        },
    )
    write_json(
        run_dir / "validation_summary.json",
        {
            "status": "blocked_from_calibrated_promotion",
            "claim_status_ceiling": validation.status_ceiling,
            "holdout_measurement_ref": validation.holdout_measurement_ref,
            "auxiliary_measurement_refs": validation.auxiliary_measurement_refs,
            "metrics": metrics,
            "blocking_gates": [
                *([] if stack_mapping_status == "pass" else ["stack_mapping"]),
                "thresholds_predeclared",
                "normalization_gate",
            ],
        },
    )
    return metrics


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
    prediction_table_path = run_dir / "prediction_table.csv"
    prediction_table_path.write_text(table_path.read_text(encoding="utf-8"), encoding="utf-8")
    plot_paths = write_plots(result, plots_dir)
    report_path = write_report(spec, result, run_dir, spec_hash, plot_paths)
    is_registry_backed = spec.sample.material_model.type in {
        "tabulated_epsilon",
        "registry_multilayer_stack",
    }
    is_validation_candidate = spec.validation is not None

    metrics = dict(result.metrics)
    metrics["spec_hash"] = spec_hash
    metrics["run_id"] = run_id

    write_json(run_dir / "resolved_spec.json", resolved)
    write_json(run_dir / "provenance.json", provenance(spec_path, spec_hash))
    write_json(run_dir / "metrics.json", metrics)
    write_json(run_dir / "warnings.json", result.warnings)
    gates_dir = run_dir / "validation_gates"
    gates_dir.mkdir(exist_ok=True)

    registry_snapshot_sha256 = None
    registry_measurements: list[str] = []
    claim_status = ClaimStatus.SYNTHETIC_SOFTWARE_FIXTURE
    claim_reason = "Synthetic fixture only; no measured or holdout data were used."
    source_type = "synthetic"

    if is_registry_backed:
        registry_path = Path(spec.sample.material_model.registry_path or "lab_data/registry.yaml")
        registry = load_registry(registry_path)
        integrity = validate_registry_integrity(registry, registry_path)
        if not integrity.ok:
            raise ValueError("registry integrity failed: " + "; ".join(integrity.issues))

        registry_measurements = sorted(registry.measurements)
        material_model_payload, sample_stack_payload, source_provenance = _registry_payloads(
            registry,
            registry_path,
            spec,
        )
        source_type = source_provenance["source_type"]
        if is_validation_candidate:
            claim_status = ClaimStatus.WEAK_WITHIN_DATASET_HOLDOUT
            claim_reason = (
                "A Phase 3A measured-reflectance comparison was prepared, but calibrated "
                "promotion is blocked by threshold and normalization gates."
            )
        else:
            claim_status = ClaimStatus.CALIBRATION_ONLY_NO_HOLDOUT
            claim_reason = (
                "Registry-backed tabulated optical constants were used, but no independent "
                "measured R/T holdout was validated."
            )

        write_json(run_dir / "registry_snapshot.json", registry.model_dump(mode="json"))
        registry_snapshot_sha256 = sha256_file(run_dir / "registry_snapshot.json")
        _write_text(run_dir / "registry_snapshot.sha256", registry_snapshot_sha256 + "\n")
        write_json(
            run_dir / "raw_artifacts.json",
            {key: value.model_dump(mode="json") for key, value in registry.raw_artifacts.items()},
        )
        write_json(
            run_dir / "data_splits.json",
            {key: value.model_dump(mode="json") for key, value in registry.splits.items()},
        )
        write_json(run_dir / "material_model.json", material_model_payload)
        write_json(run_dir / "sample_stack.json", sample_stack_payload)
        write_json(run_dir / "source_provenance.json", source_provenance)
        write_json(
            run_dir / "fit_plan.json",
            {
                "status": "not_applicable",
                "reason": "tabulated epsilon stack was loaded, not fitted",
            },
        )
        write_json(
            run_dir / "fit_result.json",
            {
                "status": "not_applicable",
                "used_data": source_provenance["raw_artifact_refs"],
            },
        )
        write_json(
            run_dir / "fit_diagnostics.json",
            {"status": "not_applicable", "reason": "no optimizer was run"},
        )
        validation_metrics: dict[str, float | str] = {}
        if spec.validation is not None:
            validation_metrics = _write_validation_candidate_artifacts(
                spec,
                spec.validation,
                result,
                registry,
                registry_path,
                run_dir,
                gates_dir,
            )
            metrics.update(validation_metrics)
            write_json(run_dir / "metrics.json", metrics)
        else:
            _write_text(
                run_dir / "comparison_table.csv",
                "wavelength_nm,prediction,measurement,residual,measurement_ref\n",
            )
            _write_text(
                run_dir / "holdout_residuals.csv",
                "wavelength_nm,prediction,holdout,residual,holdout_measurement_ref\n",
            )
        write_json(
            run_dir / "rt_provenance_audit.json",
            {
                "status": "candidate" if is_validation_candidate else "blocked",
                "reason": (
                    "Phase 3A TiN/SiO2 measured-reflectance comparison is prepared, "
                    "but calibrated promotion remains gate-blocked."
                    if is_validation_candidate
                    else "No independent R/T holdout is registered for this TiN/TiON run."
                ),
                "required_next_evidence": [
                    "sample-matched reflection or transmission spectrum",
                    "geometry, polarization, normalization, and substrate notes",
                    "predeclared calibration/holdout split",
                ],
            },
        )
        write_json(
            run_dir / "provenance_gaps.json",
            {
                "gaps": [
                    "TiON_48/TiON_49 raw R/T spectra are not registered.",
                    "FROG labels are not authoritatively mapped to TiON_48/TiON_49.",
                    "No independent holdout residual threshold has been approved.",
                    "Thesis intensity normalization is not yet proven as absolute reflectance.",
                ]
            },
        )

    write_json(
        run_dir / "input_manifest.json",
        {
            "claim_scope": (
                "V1 real-data grounding run" if is_registry_backed else "synthetic V0 run"
            ),
            "source_type": source_type,
            "measurements": registry_measurements,
            "registry_snapshot_sha256": registry_snapshot_sha256,
        },
    )
    write_json(
        run_dir / "claim_status.json",
        {
            "status": claim_status.value,
            "can_feed_serious_core": False,
            "reason": claim_reason,
        },
    )
    write_json(
        gates_dir / "input_integrity.json",
        {
            "status": "pass",
            "scope": (
                "registry-backed inputs"
                if is_registry_backed
                else "synthetic inline V0 inputs"
            ),
        },
    )
    write_json(
        gates_dir / "split_integrity.json",
        (
            {
                "status": "pass",
                "reason": (
                    "Phase 3A split declares calibration material inputs and "
                    "holdout spectra."
                ),
            }
            if is_validation_candidate
            else
            {
                "status": "blocked",
                "reason": "No independent holdout is registered for this grounding run.",
            }
            if is_registry_backed
            else {"status": "not_applicable", "reason": "No calibration or holdout split in V0."}
        ),
    )
    write_json(run_dir / "assumptions.json", result.assumptions)
    write_json(run_dir / "validity_envelope.json", spec.validity_envelope.model_dump(mode="json"))
    write_json(
        run_dir / "environment.json",
        {
            "python_version": sys.version,
            "platform": platform.platform(),
            "git_commit": git_value(["rev-parse", "HEAD"]),
        },
    )

    artifact_hashes = {}
    for artifact_file in sorted(run_dir.rglob("*")):
        if artifact_file.is_file() and artifact_file.name not in {
            "artifact_hashes.json",
            "manifest.json",
        }:
            artifact_hashes[str(artifact_file.relative_to(run_dir))] = sha256_file(
                artifact_file
            )
    write_json(run_dir / "artifact_hashes.json", artifact_hashes)
    manifest_hashes = {
        **artifact_hashes,
        "artifact_hashes.json": sha256_file(run_dir / "artifact_hashes.json"),
    }
    write_json(
        run_dir / "manifest.json",
        {
            "run_id": run_id,
            "spec_hash": spec_hash,
            "primary_table": str(table_path.relative_to(run_dir)),
            "primary_plots": [str(path.relative_to(run_dir)) for path in plot_paths],
            "primary_report": str(report_path.relative_to(run_dir)),
            "artifacts": {
                relative_path: {
                    "sha256": digest,
                    "kind": _manifest_artifact_kind(relative_path),
                    "role": _manifest_artifact_role(relative_path),
                }
                for relative_path, digest in sorted(manifest_hashes.items())
            },
        },
    )
    return run_dir
