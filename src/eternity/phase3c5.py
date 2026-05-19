"""Phase 3C.5 St Andrews source-model parity utilities."""

from __future__ import annotations

import json
import re
import zipfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

NUMBER_PATTERN = re.compile(r"[-+]?\d+(?:\.\d+)?(?:E[-+]?\d+)?", re.IGNORECASE)


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _normalize_stem(value: str) -> str:
    return Path(value).stem.lower().replace(" ", "").replace("_", "-")


def _find_raw_members(zip_path: Path, selected_material_member: str) -> dict[str, str | None]:
    selected_stem = _normalize_stem(selected_material_member)
    raw_mod = None
    raw_se = None
    with zipfile.ZipFile(zip_path) as archive:
        for member in archive.namelist():
            if "/raw file/" not in member:
                continue
            if _normalize_stem(member) != selected_stem:
                continue
            suffix = Path(member).suffix.lower()
            if suffix == ".mod":
                raw_mod = member
            elif suffix == ".se":
                raw_se = member
    return {"mod_member": raw_mod, "se_member": raw_se}


def _archive_text(zip_path: Path, member: str) -> str:
    with zipfile.ZipFile(zip_path) as archive:
        return archive.read(member).decode("utf-8-sig", errors="ignore")


def _first_number(line: str) -> float | None:
    match = NUMBER_PATTERN.search(line)
    if match is None:
        return None
    return float(match.group())


def _value_for_label(text: str, label: str) -> float | None:
    for line in text.splitlines():
        if label in line:
            return _first_number(line)
    return None


def _extract_source_model(mod_text: str) -> dict[str, Any]:
    substrate = {
        "cauchy_A": _value_for_label(mod_text, "'A'"),
        "cauchy_B": _value_for_label(mod_text, "'B'"),
        "cauchy_C": _value_for_label(mod_text, "'C'"),
        "k_amplitude": _value_for_label(mod_text, "'k Amplitude'"),
        "exponent": _value_for_label(mod_text, "'Exponent'"),
    }
    thickness_raw = _value_for_label(mod_text, "'Thickness # 1'")
    return {
        "film_thickness_raw": thickness_raw,
        "film_thickness_possible_nm_if_raw_angstrom": (
            thickness_raw / 10.0 if thickness_raw is not None else None
        ),
        "film_thickness_raw_units": "unresolved_completeease_internal_units",
        "roughness_raw": _value_for_label(mod_text, "'Roughness'"),
        "roughness_raw_units": "unresolved_completeease_internal_units",
        "thickness_nonuniformity_percent": _value_for_label(
            mod_text,
            "'% Thickness Non-uniformity'",
        ),
        "back_reflections_count": _value_for_label(mod_text, "'# Back Reflections'"),
        "first_reflection_percent": _value_for_label(mod_text, "'% 1st Reflection'"),
        "substrate_model": {
            "kind": "Float Glass - Air (Cauchy)",
            **substrate,
        },
        "layer_model": "TIN 3 (Lorentz)" if "TIN 3 (Lorentz)" in mod_text else None,
        "source_mentions_surface_roughness": "Surface Roughness" in mod_text
        or "'Roughness'" in mod_text,
    }


def _build_parity_checks(
    source_model: dict[str, Any],
    clean_stack: dict[str, Any],
) -> list[dict[str, Any]]:
    clean_layers = clean_stack.get("stack", {}).get("layers", [])
    clean_film = next((layer for layer in clean_layers if layer.get("role") == "film"), {})
    clean_substrate = next(
        (layer for layer in clean_layers if layer.get("role") == "substrate"),
        {},
    )
    clean_thickness_nm = (
        clean_film.get("thickness", {}).get("value")
        if isinstance(clean_film.get("thickness"), dict)
        else None
    )
    possible_source_nm = source_model.get("film_thickness_possible_nm_if_raw_angstrom")

    checks = [
        {
            "name": "film_thickness",
            "status": "mismatch_or_unit_unresolved",
            "clean_run_value_nm": clean_thickness_nm,
            "source_model_raw": source_model.get("film_thickness_raw"),
            "source_model_possible_nm_if_raw_angstrom": possible_source_nm,
            "reason": (
                "The clean run uses the nominal registry thickness. The raw Woollam "
                "model exposes a different internal thickness-like value whose unit "
                "must be decoded before using it."
            ),
        },
        {
            "name": "substrate_model",
            "status": "mismatch",
            "clean_run": {
                "material": clean_substrate.get("material"),
                "model": "lossless fixed n=1.45",
            },
            "source_model": source_model.get("substrate_model"),
            "reason": (
                "The clean run uses a fixed lossless glass index, while the source "
                "model uses a Float Glass Cauchy substrate."
            ),
        },
        {
            "name": "roughness_model",
            "status": "missing_in_clean_run",
            "clean_run": "no roughness layer or effective-medium roughness model",
            "source_model_raw": source_model.get("roughness_raw"),
            "source_mentions_surface_roughness": source_model.get(
                "source_mentions_surface_roughness"
            ),
            "reason": (
                "The source model exposes roughness metadata, but the clean run is a "
                "single flat TiN layer on glass."
            ),
        },
        {
            "name": "back_reflection_settings",
            "status": "missing_or_not_modeled_in_clean_run",
            "clean_run": "semi-infinite substrate without source back-reflection settings",
            "source_model": {
                "back_reflections_count": source_model.get("back_reflections_count"),
                "first_reflection_percent": source_model.get("first_reflection_percent"),
            },
            "reason": (
                "The Woollam model includes back-reflection settings that are not "
                "represented in the current clean-run stack."
            ),
        },
    ]
    return checks


def build_phase3c5_parity_packet(
    triage_json: Path,
    pairing_json: Path,
    run_dir: Path,
) -> dict[str, Any]:
    triage = _load_json(triage_json)
    pairing = _load_json(pairing_json)
    clean_stack = _load_json(run_dir / "sample_stack.json")
    resolved_spec = _load_json(run_dir / "resolved_spec.json")

    zip_path = Path(pairing["source_archive"]["path"])
    selected_member = pairing["selected_pairing"]["selected_material_member"]
    raw_members = _find_raw_members(zip_path, selected_member)
    if raw_members["mod_member"] is None:
        raise ValueError(f"No raw .mod member found for selected material {selected_member}")
    mod_text = _archive_text(zip_path, raw_members["mod_member"])
    source_model = _extract_source_model(mod_text)
    parity_checks = _build_parity_checks(source_model, clean_stack)
    blocking_gaps = [check["name"] for check in parity_checks if check["status"] != "match"]

    return {
        "phase_id": "Phase 3C.5",
        "title": "St Andrews Source-Model Parity Diagnostic",
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "inputs": {
            "triage_json": str(triage_json),
            "pairing_json": str(pairing_json),
            "run_dir": str(run_dir),
            "source_archive": str(zip_path),
            "selected_material_member": selected_member,
            "raw_mod_member": raw_members["mod_member"],
            "raw_se_member": raw_members["se_member"],
        },
        "decision": {
            "status": "source_model_parity_gaps_recorded",
            "can_feed_serious_core": False,
            "can_promote_calibrated_linear_evidence": False,
            "phase4_ready": False,
            "source_model_revision_ready": False,
            "next_phase": "Phase 3C.6 - source-model parity implementation or lane park decision",
        },
        "phase3c4_context": {
            "decision": triage["decision"],
            "dominant_failure_windows": triage["dominant_failure_windows"],
        },
        "clean_run_model": {
            "run_id": run_dir.name,
            "geometry": resolved_spec.get("geometry", {}),
            "sample_stack": clean_stack,
            "modeled_limitations": [
                "single flat TiN layer",
                "lossless fixed n=1.45 glass substrate",
                "no source roughness layer",
                "no source back-reflection settings",
                "no detector or RT.xlsx acquisition model",
            ],
        },
        "source_model": source_model,
        "parity_checks": parity_checks,
        "blocking_parity_gaps": blocking_gaps,
        "interpretation_boundary": (
            "Phase 3C.5 records source-model parity gaps only. It must not use the "
            "holdout to tune a replacement model, change thresholds, feed the serious core, "
            "or promote calibrated_linear_evidence."
        ),
    }


def parity_markdown(packet: dict[str, Any]) -> str:
    decision = packet["decision"]
    inputs = packet["inputs"]
    source_model = packet["source_model"]
    lines = [
        "# Phase 3C.5 - St Andrews Source-Model Parity Diagnostic",
        "",
        "## Decision",
        "",
        f"- Status: `{decision['status']}`",
        f"- Can feed serious core: `{decision['can_feed_serious_core']}`",
        "- Can promote calibrated evidence: "
        f"`{decision['can_promote_calibrated_linear_evidence']}`",
        f"- Phase 4 ready: `{decision['phase4_ready']}`",
        f"- Source-model revision ready: `{decision['source_model_revision_ready']}`",
        f"- Next phase: `{decision['next_phase']}`",
        "",
        "## Source Members",
        "",
        f"- Selected epsilon table: `{inputs['selected_material_member']}`",
        f"- Raw model member: `{inputs['raw_mod_member']}`",
        f"- Raw SE member: `{inputs['raw_se_member']}`",
        "",
        "## Readable Source-Model Assumptions",
        "",
        f"- Film thickness raw value: `{source_model['film_thickness_raw']}`",
        "- Film thickness possible nm if raw value is Angstrom: "
        f"`{source_model['film_thickness_possible_nm_if_raw_angstrom']}`",
        f"- Roughness raw value: `{source_model['roughness_raw']}`",
        f"- Thickness non-uniformity percent: `{source_model['thickness_nonuniformity_percent']}`",
        f"- Back reflections count: `{source_model['back_reflections_count']}`",
        f"- First reflection percent: `{source_model['first_reflection_percent']}`",
        f"- Substrate model: `{source_model['substrate_model']['kind']}`",
        f"- Cauchy A/B/C: `{source_model['substrate_model']['cauchy_A']}`, "
        f"`{source_model['substrate_model']['cauchy_B']}`, "
        f"`{source_model['substrate_model']['cauchy_C']}`",
        f"- Layer model label: `{source_model['layer_model']}`",
        "",
        "## Parity Checks",
        "",
    ]
    for check in packet["parity_checks"]:
        lines.append(f"- `{check['name']}`: `{check['status']}`. {check['reason']}")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            packet["interpretation_boundary"],
            "",
        ]
    )
    return "\n".join(lines)


def write_phase3c5_parity_packet(
    output_dir: Path,
    packet: dict[str, Any],
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase3c5_standrews_source_model_parity.json"
    md_path = output_dir / "phase3c5_standrews_source_model_parity.md"
    json_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(parity_markdown(packet), encoding="utf-8")
    return json_path, md_path
