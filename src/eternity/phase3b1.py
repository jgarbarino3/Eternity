"""Phase 3B.1 TiON evidence reality-check utilities."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

TION_SAMPLE_IDS = {"tion_48_40nm_0p8pa", "tion_49_40nm_1p0pa"}
TION_MODEL_IDS = {"tion_48_0p8pa_epsilon_model", "tion_49_1p0pa_epsilon_model"}
PLOT_SUFFIXES = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".svg", ".pdf"}
EXCLUDED_SCAN_PARTS = {".git", ".venv", "__pycache__", "results", "build"}


def _load_registry(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _is_tion_ref(value: Any) -> bool:
    text = str(value).lower()
    return "tion" in text or "tion_48" in text or "tion_49" in text


def _raw_artifacts(registry: dict[str, Any]) -> list[dict[str, Any]]:
    records = []
    for artifact_id, artifact in registry.get("raw_artifacts", {}).items():
        if artifact_id.startswith("tion_48") or artifact_id.startswith("tion_49"):
            records.append(
                {
                    "id": artifact_id,
                    "kind": artifact.get("kind"),
                    "path": artifact.get("path"),
                    "source_type": artifact.get("source_type"),
                    "source_notes": artifact.get("source_notes"),
                    "sha256": artifact.get("sha256"),
                }
            )
    return sorted(records, key=lambda item: item["id"])


def _measurements(registry: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    epsilon = []
    rt = []
    for measurement_id, measurement in registry.get("measurements", {}).items():
        if not _is_tion_ref(measurement.get("sample_ref")):
            continue
        record = {
            "id": measurement_id,
            "kind": measurement.get("kind"),
            "sample_ref": measurement.get("sample_ref"),
            "raw_artifact_ref": measurement.get("raw_artifact_ref"),
            "stack_ref": measurement.get("stack_ref"),
            "geometry_polarization": measurement.get("geometry_polarization"),
            "instrument_or_source_notes": measurement.get("instrument_or_source_notes"),
        }
        kind = str(measurement.get("kind", "")).lower()
        quantity = str(measurement.get("y_quantity", "")).lower()
        if "epsilon" in kind:
            epsilon.append(record)
        elif "reflect" in kind or "transmission" in kind or "reflect" in quantity:
            rt.append(record)
    return (
        sorted(epsilon, key=lambda item: item["id"]),
        sorted(rt, key=lambda item: item["id"]),
    )


def _material_models(registry: dict[str, Any]) -> list[dict[str, Any]]:
    records = []
    for model_id, model in registry.get("material_models", {}).items():
        if model_id not in TION_MODEL_IDS:
            continue
        records.append(
            {
                "id": model_id,
                "sample_ref": model.get("sample_ref"),
                "kind": model.get("kind"),
                "source_type": model.get("source_type"),
                "raw_artifact_ref": model.get("raw_artifact_ref"),
                "enz_wavelengths_nm": model.get("enz_wavelengths_nm", []),
                "wavelength_min_nm": model.get("wavelength_min_nm"),
                "wavelength_max_nm": model.get("wavelength_max_nm"),
                "passivity_check": model.get("passivity_check"),
                "limitations": model.get("limitations", []),
            }
        )
    return sorted(records, key=lambda item: item["id"])


def _sample_records(registry: dict[str, Any]) -> list[dict[str, Any]]:
    records = []
    for sample_id, sample in registry.get("samples", {}).items():
        if sample_id not in TION_SAMPLE_IDS:
            continue
        records.append(
            {
                "id": sample_id,
                "material": sample.get("material"),
                "nominal_thickness": sample.get("nominal_thickness"),
                "composition": sample.get("composition"),
                "process_notes": sample.get("process_notes", []),
                "provenance_refs": sample.get("provenance_refs", []),
            }
        )
    return sorted(records, key=lambda item: item["id"])


def _find_tion_plot_candidates(root: Path) -> list[str]:
    candidates: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in EXCLUDED_SCAN_PARTS for part in path.parts):
            continue
        if path.suffix.lower() not in PLOT_SUFFIXES:
            continue
        lower_name = path.name.lower()
        if "tion" not in lower_name:
            continue
        candidates.append(str(path.relative_to(root)))
    return sorted(candidates)


def build_phase3b1_packet(
    registry_path: Path,
    repo_root: Path,
) -> dict[str, Any]:
    registry = _load_registry(registry_path)
    epsilon_measurements, rt_measurements = _measurements(registry)
    plot_candidates = _find_tion_plot_candidates(repo_root)
    material_models = _material_models(registry)
    calibration_examples = [
        {
            "sample": "TiON_48",
            "spec": "experiments/examples/linear_tion_48_tabulated.yaml",
            "status": "available",
            "claim_status": "calibration_only_no_holdout",
        },
        {
            "sample": "TiON_49",
            "spec": "experiments/examples/linear_tion_49_tabulated.yaml",
            "status": (
                "available"
                if (repo_root / "experiments/examples/linear_tion_49_tabulated.yaml").exists()
                else "missing"
            ),
            "claim_status": "calibration_only_no_holdout",
        },
    ]
    no_rt = not rt_measurements
    no_plots = not plot_candidates
    next_external = no_rt and no_plots
    return {
        "phase_id": "Phase 3B.1",
        "title": "TiON Evidence Reality Check / Digitized Plot Intake",
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "inputs": {
            "registry_path": str(registry_path),
            "repo_root": str(repo_root),
        },
        "hard_constraints": {
            "completeease_available": False,
            "completeease_contact_available": False,
            "st_andrews_author_contact_available": False,
            "tion_raw_rt_available": bool(rt_measurements),
            "notes": [
                (
                    "Unavailable CompleteEASE/export paths are treated as hard blockers, "
                    "not active tasks."
                ),
                "Unavailable TiON raw R/T is treated as a hard validation blocker.",
                "St Andrews remains parked unless new source evidence appears externally.",
            ],
        },
        "evidence_inventory": {
            "samples": _sample_records(registry),
            "raw_artifacts": _raw_artifacts(registry),
            "epsilon_measurements": epsilon_measurements,
            "rt_measurements": rt_measurements,
            "material_models": material_models,
            "repo_plot_candidates": plot_candidates,
            "calibration_only_examples": calibration_examples,
        },
        "decision": {
            "status": (
                "local_validation_data_exhausted_literature_or_external_data_needed"
                if next_external
                else "local_followup_available_under_weak_evidence"
            ),
            "can_feed_serious_core": False,
            "can_promote_calibrated_linear_evidence": False,
            "phase4_ready": False,
            "plot_digitization_ready": bool(plot_candidates),
            "calibration_only_modeling_ready": bool(material_models),
            "validation_ready": bool(rt_measurements),
            "recommended_next_phase": (
                "Phase 3D - literature/data search for validation datasets"
                if next_external
                else "Phase 3B.2 - explicit plot-derived TiON intake"
            ),
        },
        "allowed_now": [
            "Run calibration-only TiON_48/TiON_49 TMM examples from frozen epsilon tables.",
            "Use TiON optical constants for model exploration and mechanism planning.",
            (
                "Register plot-derived evidence only if actual plot files with usable axes "
                "are supplied."
            ),
            (
                "Search literature/public repositories for a validation dataset with optical "
                "constants plus R/T."
            ),
        ],
        "forbidden_now": [
            "Treat TiON optical constants alone as calibrated validation evidence.",
            "Treat unavailable raw R/T or unavailable CompleteEASE exports as active next tasks.",
            "Keep iterating St Andrews source-model parity without new external source evidence.",
            "Map FROG or pump-probe labels to TiON_48/TiON_49 without authoritative evidence.",
        ],
        "stop_condition": (
            "Local repo evidence is exhausted for calibrated validation if no TiON R/T "
            "or digitizable plot candidates are present. The next meaningful validation "
            "step is a literature/public-data search for a new dataset."
        ),
    }


def _bool(value: bool) -> str:
    return "true" if value else "false"


def phase3b1_markdown(packet: dict[str, Any]) -> str:
    decision = packet["decision"]
    inventory = packet["evidence_inventory"]
    lines = [
        "# Phase 3B.1 - TiON Evidence Reality Check / Digitized Plot Intake",
        "",
        "## Decision",
        "",
        f"- Status: `{decision['status']}`",
        f"- Can feed serious core: `{_bool(decision['can_feed_serious_core'])}`",
        "- Can promote calibrated evidence: "
        f"`{_bool(decision['can_promote_calibrated_linear_evidence'])}`",
        f"- Phase 4 ready: `{_bool(decision['phase4_ready'])}`",
        f"- Plot digitization ready: `{_bool(decision['plot_digitization_ready'])}`",
        "- Calibration-only modeling ready: "
        f"`{_bool(decision['calibration_only_modeling_ready'])}`",
        f"- Validation ready: `{_bool(decision['validation_ready'])}`",
        f"- Recommended next phase: `{decision['recommended_next_phase']}`",
        "",
        "## Hard Constraints",
        "",
    ]
    for name, value in packet["hard_constraints"].items():
        if name == "notes":
            continue
        lines.append(f"- `{name}`: `{_bool(value)}`")
    lines.extend(f"- {note}" for note in packet["hard_constraints"]["notes"])
    lines.extend(["", "## TiON Evidence Inventory", ""])
    lines.append(f"- Samples: `{len(inventory['samples'])}`")
    lines.append(f"- Raw TiON artifacts: `{len(inventory['raw_artifacts'])}`")
    lines.append(f"- TiON epsilon measurements: `{len(inventory['epsilon_measurements'])}`")
    lines.append(f"- TiON R/T measurements: `{len(inventory['rt_measurements'])}`")
    lines.append(f"- TiON material models: `{len(inventory['material_models'])}`")
    lines.append(f"- Repo plot candidates: `{len(inventory['repo_plot_candidates'])}`")
    lines.extend(["", "### Material Models", ""])
    lines.extend(
        (
            f"- `{model['id']}`: ENZ `{model['enz_wavelengths_nm']}` nm, "
            f"range `{model['wavelength_min_nm']}`-`{model['wavelength_max_nm']}` nm, "
            f"passivity `{model['passivity_check']}`"
        )
        for model in inventory["material_models"]
    )
    lines.extend(["", "### Calibration-Only Examples", ""])
    lines.extend(
        f"- `{example['spec']}`: `{example['status']}`, `{example['claim_status']}`"
        for example in inventory["calibration_only_examples"]
    )
    lines.extend(["", "## Allowed Now", ""])
    lines.extend(f"- {item}" for item in packet["allowed_now"])
    lines.extend(["", "## Forbidden Now", ""])
    lines.extend(f"- {item}" for item in packet["forbidden_now"])
    lines.extend(["", "## Stop Condition", "", packet["stop_condition"], ""])
    return "\n".join(lines)


def write_phase3b1_packet(output_dir: Path, packet: dict[str, Any]) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase3b1_tion_evidence_reality_check.json"
    md_path = output_dir / "phase3b1_tion_evidence_reality_check.md"
    json_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(phase3b1_markdown(packet), encoding="utf-8")
    return json_path, md_path
