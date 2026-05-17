"""Phase 3A.8 source-candidate triage utilities."""

from __future__ import annotations

import json
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

TRIAGE_DECISIONS = {
    "continue_source_recovery_manual_review",
    "pivot_to_relative_only_diagnostic",
    "blocked_needs_new_export_or_measurement",
}

TRIAGE_CATEGORIES = (
    "manual_followup_priority",
    "related_but_not_source_identity",
    "wrong_substrate_or_control",
    "not_decisive_for_absolute_reflectance",
)


def load_phase3a7_recovery(path: Path) -> dict[str, Any]:
    """Load a Phase 3A.7 recovery artifact from disk."""

    with path.open(encoding="utf-8") as handle:
        recovery = json.load(handle)
    if recovery.get("phase_id") != "Phase 3A.7":
        raise ValueError("Phase 3A.8 triage requires a Phase 3A.7 recovery JSON")
    return recovery


def _candidate_text(candidate: dict[str, Any]) -> str:
    snippets = "\n".join(candidate.get("evidence_snippets", []))
    reasons = "\n".join(candidate.get("match_reasons", []))
    return "\n".join(
        [
            str(candidate.get("path", "")),
            str(candidate.get("member_path", "")),
            str(candidate.get("container_path", "")),
            snippets,
            reasons,
        ]
    ).lower()


def _dedupe_candidates(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_hash: dict[str, dict[str, Any]] = {}
    for candidate in candidates:
        key = str(candidate.get("sha256") or candidate.get("path"))
        candidate_copy = deepcopy(candidate)
        candidate_copy["duplicate_paths"] = [candidate_copy.get("path")]
        existing = by_hash.get(key)
        if existing is None:
            by_hash[key] = candidate_copy
            continue
        existing["duplicate_paths"].append(candidate_copy.get("path"))
        existing["score"] = max(int(existing.get("score", 0)), int(candidate_copy.get("score", 0)))
        existing_reasons = set(existing.get("match_reasons", []))
        existing_reasons.update(candidate_copy.get("match_reasons", []))
        existing["match_reasons"] = sorted(existing_reasons)
    return sorted(
        by_hash.values(),
        key=lambda item: (
            -_triage_priority(item),
            -int(item.get("score", 0)),
            item.get("path", ""),
        ),
    )


def _has(candidate: dict[str, Any], needle: str) -> bool:
    return needle in _candidate_text(candidate)


def _triage_priority(candidate: dict[str, Any]) -> int:
    text = _candidate_text(candidate)
    score = 0
    if "quartz" in text:
        score += 30
    if "10nm" in text or "10 nm" in text:
        score += 24
    if "pulsed" in text or "dynamic" in text or "0-12v" in text or "0-8v" in text:
        score += 20
    if "reflect" in text or "intensity" in text:
        score += 12
    if "3l2" in text or "30_20_10" in text or "30 20 10" in text:
        score += 40
    if "si 100" in text or "silicon" in text:
        score -= 28
    return score


def _classify_candidate(candidate: dict[str, Any]) -> tuple[str, str]:
    text = _candidate_text(candidate)
    path_text = str(candidate.get("path", "")).lower()
    exact_identity = "3l2" in text or "30_20_10" in text or "30 20 10" in text
    quartz = "quartz" in text
    ten_nm = "10nm" in text or "10 nm" in text
    dynamic = "pulsed" in text or "dynamic" in text or "0-12v" in text or "0-8v" in text
    path_si_control = "si 100" in path_text or "silicon" in path_text
    si_control = path_si_control or "si 100" in text or "silicon" in text

    if exact_identity:
        return (
            "manual_followup_priority",
            "mentions exact 3L2 or 30_20_10 identity and needs manual source review",
        )
    if path_si_control:
        return (
            "wrong_substrate_or_control",
            "file/member path names Si control/substrate context rather than 3L2/Quartz",
        )
    if quartz and (ten_nm or dynamic):
        return (
            "manual_followup_priority",
            "matches quartz plus 10 nm/dynamic-source clues but not exact thesis identity",
        )
    if si_control:
        return (
            "wrong_substrate_or_control",
            "mentions Si control/substrate context rather than thesis 3L2/Quartz identity",
        )
    if candidate.get("score", 0) >= 35 or quartz:
        return (
            "related_but_not_source_identity",
            "related CompleteEASE/Woollam cap-test provenance without exact thesis identity",
        )
    return (
        "not_decisive_for_absolute_reflectance",
        "low-specificity source hit and no calibrated absolute reflectance proof",
    )


def _category_buckets(candidates: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    buckets = {category: [] for category in TRIAGE_CATEGORIES}
    for candidate in candidates:
        category, rationale = _classify_candidate(candidate)
        triaged = deepcopy(candidate)
        triaged["triage_category"] = category
        triaged["triage_rationale"] = rationale
        triaged["triage_priority_score"] = _triage_priority(candidate)
        triaged["can_prove_absolute_reflectance"] = bool(
            candidate.get("absolute_reflectance_proof")
        )
        buckets[category].append(triaged)
    for category in buckets:
        buckets[category].sort(
            key=lambda item: (
                -int(item.get("triage_priority_score", 0)),
                -int(item.get("score", 0)),
                item.get("path", ""),
            )
        )
    return buckets


def _triage_decision(recovery: dict[str, Any], buckets: dict[str, list[dict[str, Any]]]) -> str:
    decision = recovery.get("decision", {})
    if not recovery.get("candidate_sources"):
        return "blocked_needs_new_export_or_measurement"
    if decision.get("exact_source_identity_status") == "candidate_found_needs_manual_review":
        return "continue_source_recovery_manual_review"
    manual_followup = buckets["manual_followup_priority"]
    if any(item.get("can_prove_absolute_reflectance") for item in manual_followup):
        return "continue_source_recovery_manual_review"
    return "pivot_to_relative_only_diagnostic"


def build_phase3a8_triage(recovery: dict[str, Any]) -> dict[str, Any]:
    """Build the Phase 3A.8 source-candidate triage packet."""

    candidates = _dedupe_candidates(recovery.get("candidate_sources", []))
    buckets = _category_buckets(candidates)
    final_decision = _triage_decision(recovery, buckets)
    if final_decision not in TRIAGE_DECISIONS:
        raise ValueError(f"invalid Phase 3A.8 decision: {final_decision}")
    return {
        "phase_id": "Phase 3A.8",
        "title": "Source Candidate Triage + Relative-Only Diagnostic Decision",
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "inputs": {
            "source_phase_id": recovery.get("phase_id"),
            "source_title": recovery.get("title"),
            "source_recovery_decision": recovery.get("decision", {}),
            "input_candidate_count": len(recovery.get("candidate_sources", [])),
            "deduped_candidate_count": len(candidates),
            "dedupe_key": "sha256",
        },
        "decision": {
            "final_decision": final_decision,
            "normalization_basis": "relative_intensity_only",
            "absolute_reflectance_status": "absolute_reflectance_blocked",
            "can_feed_serious_core": False,
            "can_promote_calibrated_linear_evidence": False,
            "claim_status_ceiling": "weak_within_dataset_holdout",
            "existing_run_promotion": "forbidden",
            "historical_run": "run_f35a15cef565fb15",
            "blocked_gates": ["normalization_gate", "thresholds_predeclared"],
        },
        "allowed_relative_only_diagnostics": [
            "spectral_shape",
            "dip_position",
            "trend_direction",
            "figure_provenance",
        ],
        "forbidden_uses": [
            "serious_core_evidence",
            "calibrated_linear_evidence",
            "absolute_reflectance_claim",
            "retroactive_threshold_tuning",
        ],
        "categories": buckets,
        "next_fork": {
            "manual_source_followup": (
                "Inspect the manual-followup candidates in CompleteEASE or with stronger "
                "source tooling if the user wants to keep provenance recovery alive."
            ),
            "relative_only_diagnostic": (
                "Proceed with shape/dip/trend diagnostics only, explicitly capped below "
                "calibrated evidence."
            ),
            "fresh_export_or_measurement": (
                "Use the Phase 3A.6 packet if absolute reflectance evidence is required."
            ),
        },
    }


def triage_markdown(triage: dict[str, Any]) -> str:
    decision = triage["decision"]
    lines = [
        "# Phase 3A.8 Source Candidate Triage",
        "",
        "## Decision",
        "",
        f"- Final decision: `{decision['final_decision']}`",
        f"- Normalization basis: `{decision['normalization_basis']}`",
        f"- Absolute reflectance status: `{decision['absolute_reflectance_status']}`",
        f"- Can feed serious core: `{decision['can_feed_serious_core']}`",
        (
            "- Can promote calibrated evidence: "
            f"`{decision['can_promote_calibrated_linear_evidence']}`"
        ),
        f"- Claim-status ceiling: `{decision['claim_status_ceiling']}`",
        f"- Historical run promotion: `{decision['existing_run_promotion']}`",
        "",
        "## Relative-Only Lane",
        "",
        "Allowed diagnostics: "
        + ", ".join(f"`{item}`" for item in triage["allowed_relative_only_diagnostics"])
        + ".",
        "",
        "Forbidden uses: " + ", ".join(f"`{item}`" for item in triage["forbidden_uses"]) + ".",
        "",
        "## Candidate Buckets",
        "",
    ]
    for category in TRIAGE_CATEGORIES:
        candidates = triage["categories"][category]
        lines.extend([f"### `{category}`", ""])
        if not candidates:
            lines.extend(["No candidates.", ""])
            continue
        lines.extend(
            [
                "| Priority | Score | SHA-256 | Rationale | Path |",
                "| ---: | ---: | --- | --- | --- |",
            ]
        )
        for candidate in candidates[:8]:
            sha = str(candidate.get("sha256", ""))
            rationale = candidate.get("triage_rationale", "")
            path = candidate.get("path", "")
            lines.append(
                "| "
                f"{candidate.get('triage_priority_score', 0)} | "
                f"{candidate.get('score', 0)} | "
                f"`{sha}` | "
                f"{rationale} | "
                f"`{path}` |"
            )
        lines.append("")
    lines.extend(
        [
            "## Consequence",
            "",
            "Phase 3A.8 keeps the strongest source candidates visible for manual",
            "follow-up, but it does not treat any candidate as exact `3L2/Quartz`",
            "source identity or calibrated absolute `%R` proof.",
            "",
            "`run_f35a15cef565fb15` remains historical and non-promotable. Future",
            "work may use the thesis traces for relative-only diagnostics, or use",
            "the Phase 3A.6 packet for a clean export/new measurement.",
            "",
        ]
    )
    return "\n".join(lines)


def relative_only_policy_yaml(triage: dict[str, Any]) -> str:
    decision = triage["decision"]
    allowed = "\n".join(f"  - {item}" for item in triage["allowed_relative_only_diagnostics"])
    forbidden = "\n".join(f"  - {item}" for item in triage["forbidden_uses"])
    return "\n".join(
        [
            "phase_id: Phase 3A.8",
            "policy: relative_only_diagnostic",
            f"decision: {decision['final_decision']}",
            "normalization_basis: relative_intensity_only",
            "absolute_reflectance_confirmed: false",
            "can_feed_serious_core: false",
            "can_promote_calibrated_linear_evidence: false",
            "claim_status_ceiling: weak_within_dataset_holdout",
            "existing_run_promotion: forbidden",
            "historical_run: run_f35a15cef565fb15",
            "allowed_diagnostics:",
            allowed,
            "forbidden_uses:",
            forbidden,
            "promotion_requires:",
            "  - source_backed_absolute_reflectance_export_or_new_measurement",
            "  - future_predeclared_thresholds",
            "  - no_residual_inspection_before_policy_approval",
            "  - passing_normalization_and_threshold_gates",
            "",
        ]
    )


def write_phase3a8_triage(output_dir: Path, triage: dict[str, Any]) -> tuple[Path, Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase3a8_source_candidate_triage.json"
    md_path = output_dir / "phase3a8_source_candidate_triage.md"
    policy_path = output_dir / "phase3a8_relative_only_diagnostic_policy.yaml"
    json_path.write_text(json.dumps(triage, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(triage_markdown(triage), encoding="utf-8")
    policy_path.write_text(relative_only_policy_yaml(triage), encoding="utf-8")
    return json_path, md_path, policy_path
