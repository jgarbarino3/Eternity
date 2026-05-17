"""Phase 3A.10 branch-decision utilities."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

DECISIONS = {
    "limited_manual_source_followup_first",
    "return_to_phase3b_evidence_gathering",
    "request_clean_export_or_measurement",
}


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_registry(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _tion_status(registry: dict[str, Any]) -> dict[str, Any]:
    raw_artifacts = registry.get("raw_artifacts", {})
    measurements = registry.get("measurements", {})
    material_models = registry.get("material_models", {})
    tion_artifacts = [
        artifact_id
        for artifact_id in raw_artifacts
        if artifact_id.startswith("tion_48") or artifact_id.startswith("tion_49")
    ]
    tion_models = [
        model_id
        for model_id in material_models
        if model_id.startswith("tion_48") or model_id.startswith("tion_49")
    ]
    rt_measurements = []
    for measurement_id, measurement in measurements.items():
        sample_ref = str(measurement.get("sample_ref", "")).lower()
        kind = str(measurement.get("kind", "")).lower()
        quantity = str(measurement.get("y_quantity", "")).lower()
        if "tion" not in sample_ref:
            continue
        if "reflect" in kind or "transmission" in kind or "reflect" in quantity:
            rt_measurements.append(measurement_id)
    return {
        "optical_constants_registered": sorted(tion_artifacts),
        "material_models_registered": sorted(tion_models),
        "raw_rt_measurements_registered": sorted(rt_measurements),
        "phase3b_ready_for_calibrated_evidence": bool(rt_measurements),
        "blockers": [
            "TiON_48/TiON_49 raw R/T spectra are not registered.",
            "Attached TiON plots remain plot-level provenance unless digitized and registered.",
            "FROG labels remain unmapped to TiON_48/TiON_49.",
        ],
    }


def _manual_candidates(triage: dict[str, Any]) -> list[dict[str, Any]]:
    candidates = triage.get("categories", {}).get("manual_followup_priority", [])
    return [
        {
            "path": candidate.get("path"),
            "sha256": candidate.get("sha256"),
            "priority": candidate.get("triage_priority_score"),
            "score": candidate.get("score"),
            "rationale": candidate.get("triage_rationale"),
        }
        for candidate in candidates
    ]


def _select_decision(
    manual_candidates: list[dict[str, Any]],
    diagnostic: dict[str, Any],
    tion_status: dict[str, Any],
) -> str:
    diagnostics = diagnostic.get("diagnostics", {})
    shape_correlation = diagnostics.get("shape_correlation_minmax")
    trend_agreement = diagnostics.get("trend_direction_agreement") is True
    strong_relative_clue = (
        isinstance(shape_correlation, int | float) and shape_correlation >= 0.95 and trend_agreement
    )
    if manual_candidates and strong_relative_clue:
        return "limited_manual_source_followup_first"
    if tion_status["phase3b_ready_for_calibrated_evidence"]:
        return "return_to_phase3b_evidence_gathering"
    if not manual_candidates:
        return "request_clean_export_or_measurement"
    return "return_to_phase3b_evidence_gathering"


def build_phase3a10_decision(
    triage: dict[str, Any],
    diagnostic: dict[str, Any],
    registry: dict[str, Any],
) -> dict[str, Any]:
    if triage.get("phase_id") != "Phase 3A.8":
        raise ValueError("Phase 3A.10 requires Phase 3A.8 triage input")
    if diagnostic.get("phase_id") != "Phase 3A.9":
        raise ValueError("Phase 3A.10 requires Phase 3A.9 diagnostic input")

    manual = _manual_candidates(triage)
    tion = _tion_status(registry)
    decision = _select_decision(manual, diagnostic, tion)
    if decision not in DECISIONS:
        raise ValueError(f"invalid Phase 3A.10 decision: {decision}")
    return {
        "phase_id": "Phase 3A.10",
        "title": "Manual Source Follow-Up vs Phase 3B Return Decision",
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "decision": {
            "selected_branch": decision,
            "can_feed_serious_core": False,
            "can_promote_calibrated_linear_evidence": False,
            "normalization_basis": "relative_intensity_only",
            "claim_status_ceiling": "weak_within_dataset_holdout",
            "requires_pro_checkpoint_before_thresholds": True,
        },
        "inputs": {
            "triage_phase_id": triage.get("phase_id"),
            "diagnostic_phase_id": diagnostic.get("phase_id"),
            "diagnostic_status": diagnostic.get("decision", {}).get("status"),
            "diagnostic_shape_correlation_minmax": diagnostic.get("diagnostics", {}).get(
                "shape_correlation_minmax"
            ),
            "diagnostic_trend_agreement": diagnostic.get("diagnostics", {}).get(
                "trend_direction_agreement"
            ),
        },
        "manual_source_followup": {
            "status": "bounded_followup_recommended" if manual else "no_candidates",
            "candidate_count": len(manual),
            "targets": manual[:3],
            "stop_after": "the listed top-three candidates unless the user adds new evidence",
            "success_condition": (
                "Find source-backed channel name, units, calibration state, angle, "
                "polarization, and exact 3L2/Quartz identity."
            ),
            "failure_action": (
                "Keep Phase 3A relative-only and use Phase 3A.6 clean export/new "
                "measurement packet or return to Phase 3B."
            ),
        },
        "phase3b_return": {
            "status": "parked_not_calibrated",
            "tion_status": tion,
            "recommended_if_manual_followup_fails": True,
            "first_actions": [
                "Keep TiON_48/TiON_49 as optical-constants-only material models.",
                "Register raw sample-matched R/T if it appears.",
                "If using grower plots, digitize them explicitly as plot-derived evidence.",
                "Do not use TiON optical constants alone as calibrated evidence.",
            ],
        },
        "branch_order": [
            "bounded manual source follow-up on the top quartz dynamic candidates",
            "Phase 3A.6 clean export or new measurement if absolute reflectance is required",
            "Phase 3B TiON evidence gathering if no Phase 3A source proof appears",
        ],
        "forbidden_uses": [
            "serious_core_evidence",
            "calibrated_linear_evidence",
            "absolute_reflectance_claim",
            "retroactive_threshold_tuning",
        ],
    }


def build_phase3a10_decision_from_paths(
    triage_path: Path,
    diagnostic_path: Path,
    registry_path: Path,
) -> dict[str, Any]:
    return build_phase3a10_decision(
        _load_json(triage_path),
        _load_json(diagnostic_path),
        _load_registry(registry_path),
    )


def decision_markdown(packet: dict[str, Any]) -> str:
    decision = packet["decision"]
    manual = packet["manual_source_followup"]
    phase3b = packet["phase3b_return"]
    lines = [
        "# Phase 3A.10 Branch Decision",
        "",
        "## Decision",
        "",
        f"- Selected branch: `{decision['selected_branch']}`",
        f"- Can feed serious core: `{decision['can_feed_serious_core']}`",
        (
            "- Can promote calibrated evidence: "
            f"`{decision['can_promote_calibrated_linear_evidence']}`"
        ),
        f"- Normalization basis: `{decision['normalization_basis']}`",
        f"- Claim-status ceiling: `{decision['claim_status_ceiling']}`",
        (
            "- Pro checkpoint before thresholds: "
            f"`{decision['requires_pro_checkpoint_before_thresholds']}`"
        ),
        "",
        "## Manual Source Follow-Up",
        "",
        f"- Status: `{manual['status']}`",
        f"- Candidate count: `{manual['candidate_count']}`",
        f"- Stop after: {manual['stop_after']}",
        f"- Success condition: {manual['success_condition']}",
        f"- Failure action: {manual['failure_action']}",
        "",
        "| Priority | Score | SHA-256 | Path |",
        "| ---: | ---: | --- | --- |",
    ]
    for target in manual["targets"]:
        lines.append(
            "| "
            f"{target.get('priority')} | {target.get('score')} | "
            f"`{target.get('sha256')}` | `{target.get('path')}` |"
        )
    if not manual["targets"]:
        lines.append("| - | - | - | No manual candidates. |")

    tion = phase3b["tion_status"]
    lines.extend(
        [
            "",
            "## Phase 3B Return",
            "",
            f"- Status: `{phase3b['status']}`",
            "- TiON optical constants registered: "
            + ", ".join(f"`{item}`" for item in tion["optical_constants_registered"]),
            "- TiON raw R/T measurements registered: "
            + (
                ", ".join(f"`{item}`" for item in tion["raw_rt_measurements_registered"])
                if tion["raw_rt_measurements_registered"]
                else "`none`"
            ),
            f"- Ready for calibrated evidence: `{tion['phase3b_ready_for_calibrated_evidence']}`",
            "",
            "First actions:",
        ]
    )
    lines.extend(f"- {item}" for item in phase3b["first_actions"])
    lines.extend(
        [
            "",
            "## Branch Order",
            "",
        ]
    )
    lines.extend(f"{index}. {item}" for index, item in enumerate(packet["branch_order"], start=1))
    lines.extend(
        [
            "",
            "Forbidden uses: " + ", ".join(f"`{item}`" for item in packet["forbidden_uses"]) + ".",
            "",
        ]
    )
    return "\n".join(lines)


def write_phase3a10_decision(output_dir: Path, packet: dict[str, Any]) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase3a10_branch_decision.json"
    md_path = output_dir / "phase3a10_branch_decision.md"
    json_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(decision_markdown(packet), encoding="utf-8")
    return json_path, md_path
