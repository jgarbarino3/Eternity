"""Phase 3A.11 bounded manual source follow-up packet utilities."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REQUIRED_PROOF_GATES = [
    "exact_3l2_quartz_identity",
    "stack_30nm_tin_10nm_sio2_20nm_tin",
    "s_polarized_or_te_reflectance_channel",
    "sixty_degree_incidence",
    "absolute_reflectance_units_or_calibration_state",
    "export_or_source_lineage_to_d10nm_text_trace",
]

REVIEW_QUESTIONS = [
    "Does the source file explicitly identify the sample as 3L2/Quartz or the thesis d_10nm stack?",
    "Does it state or encode the layer order 30 nm TiN / 10 nm SiO2 / 20 nm TiN on quartz?",
    "Does it identify the channel as S-polarized/TE reflectance rather than generic intensity?",
    "Does it preserve the 60 degree incidence geometry used by thesis Figure 4.1?",
    "Does it prove the exported values are calibrated absolute reflectance or percent reflectance?",
    "Can the source lineage be tied to the existing d_10nm_initial or d_10nm_12V text trace?",
]


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _triage_by_sha(triage: dict[str, Any]) -> dict[str, dict[str, Any]]:
    categories = triage.get("categories", {})
    by_sha: dict[str, dict[str, Any]] = {}
    for candidates in categories.values():
        if not isinstance(candidates, list):
            continue
        for candidate in candidates:
            sha = candidate.get("sha256")
            if isinstance(sha, str) and sha:
                by_sha.setdefault(sha, candidate)
    return by_sha


def _clip_snippets(snippets: list[Any], limit: int = 10) -> list[str]:
    clipped: list[str] = []
    for snippet in snippets:
        if not isinstance(snippet, str):
            continue
        clipped.append(snippet[:500])
        if len(clipped) >= limit:
            break
    return clipped


def _candidate_packet(
    target: dict[str, Any],
    triage_candidate: dict[str, Any] | None,
    index: int,
) -> dict[str, Any]:
    triage_candidate = triage_candidate or {}
    return {
        "candidate_id": f"phase3a11_candidate_{index}",
        "review_status": "pending_manual_review",
        "path": target.get("path"),
        "sha256": target.get("sha256"),
        "priority": target.get("priority"),
        "score": target.get("score"),
        "rationale": target.get("rationale"),
        "archive_member_path": triage_candidate.get("member_path"),
        "container_path": triage_candidate.get("container_path"),
        "size_bytes": triage_candidate.get("size_bytes"),
        "zip_crc32": triage_candidate.get("zip_crc32"),
        "zip_mtime": triage_candidate.get("zip_mtime"),
        "inner_ise_entries": triage_candidate.get("inner_ise_entries", []),
        "archive_entries": triage_candidate.get("archive_entries", []),
        "match_reasons": triage_candidate.get("match_reasons", []),
        "evidence_snippets": _clip_snippets(triage_candidate.get("evidence_snippets", [])),
        "current_assessment": {
            "related_to_quartz_10nm_dynamic_sources": True,
            "absolute_reflectance_proof_found": bool(
                triage_candidate.get("absolute_reflectance_proof")
                or triage_candidate.get("can_prove_absolute_reflectance")
            ),
            "exact_source_identity_proven": False,
            "can_feed_serious_core": False,
        },
        "manual_review_questions": REVIEW_QUESTIONS,
        "required_evidence_to_pass": REQUIRED_PROOF_GATES,
        "failure_classification_if_unresolved": "related_but_not_source_identity",
    }


def build_phase3a11_packet(
    decision: dict[str, Any],
    triage: dict[str, Any],
) -> dict[str, Any]:
    if decision.get("phase_id") != "Phase 3A.10":
        raise ValueError("Phase 3A.11 requires Phase 3A.10 decision input")
    if triage.get("phase_id") != "Phase 3A.8":
        raise ValueError("Phase 3A.11 requires Phase 3A.8 triage input")

    selected_branch = decision.get("decision", {}).get("selected_branch")
    if selected_branch != "limited_manual_source_followup_first":
        raise ValueError(
            "Phase 3A.11 is only valid after limited_manual_source_followup_first"
        )

    targets = decision.get("manual_source_followup", {}).get("targets", [])
    by_sha = _triage_by_sha(triage)
    candidates = [
        _candidate_packet(target, by_sha.get(str(target.get("sha256", ""))), index)
        for index, target in enumerate(targets[:3], start=1)
    ]
    return {
        "phase_id": "Phase 3A.11",
        "title": "Bounded Manual Source Follow-Up Packet",
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "input_decision_ref": "docs/phase3a10_branch_decision.json",
        "input_triage_ref": "docs/phase3a8_source_candidate_triage.json",
        "decision": {
            "status": "manual_review_packet_ready",
            "selected_branch": selected_branch,
            "candidate_count": len(candidates),
            "stop_after_candidate_count": len(candidates),
            "can_feed_serious_core": False,
            "can_promote_calibrated_linear_evidence": False,
            "claim_status_ceiling_before_manual_proof": "weak_within_dataset_holdout",
            "requires_pro_checkpoint_before_thresholds_or_promotion": True,
        },
        "scope": {
            "search_mode": "no_new_broad_search",
            "allowed_work": [
                "open or inspect only the listed source candidates",
                "record exact source-backed evidence lines or external screenshots if needed",
                "classify each candidate against the proof gates",
            ],
            "forbidden_work": [
                "adding unregistered large binary source files to the repo",
                "assuming intensity is absolute reflectance without source proof",
                "tuning thresholds from run_f35a15cef565fb15",
                "promoting any existing run to calibrated_linear_evidence",
            ],
        },
        "proof_gates": REQUIRED_PROOF_GATES,
        "candidates": candidates,
        "outcome_rules": {
            "all_gates_pass": (
                "prepare a future Phase 3A.12 absolute-reflectance policy packet; "
                "do not retroactively promote existing inspected residuals"
            ),
            "any_gate_unresolved": (
                "keep Phase 3A relative-only and use Phase 3A.6 clean export/new "
                "measurement packet or return to Phase 3B evidence gathering"
            ),
            "all_candidates_unresolved": "mark manual source follow-up exhausted",
        },
        "recommended_manual_log_fields": [
            "reviewer",
            "review_date",
            "candidate_id",
            "tool_used",
            "evidence_location",
            "evidence_quote_or_note",
            "passed_gates",
            "failed_or_unresolved_gates",
            "decision",
        ],
    }


def build_phase3a11_packet_from_paths(
    decision_path: Path,
    triage_path: Path,
) -> dict[str, Any]:
    return build_phase3a11_packet(_load_json(decision_path), _load_json(triage_path))


def packet_markdown(packet: dict[str, Any]) -> str:
    decision = packet["decision"]
    lines = [
        "# Phase 3A.11 Bounded Manual Source Follow-Up Packet",
        "",
        "## Decision",
        "",
        f"- Status: `{decision['status']}`",
        f"- Selected branch: `{decision['selected_branch']}`",
        f"- Candidate count: `{decision['candidate_count']}`",
        f"- Stop after candidate count: `{decision['stop_after_candidate_count']}`",
        f"- Can feed serious core: `{decision['can_feed_serious_core']}`",
        (
            "- Can promote calibrated evidence: "
            f"`{decision['can_promote_calibrated_linear_evidence']}`"
        ),
        (
            "- Claim-status ceiling before manual proof: "
            f"`{decision['claim_status_ceiling_before_manual_proof']}`"
        ),
        "",
        "## Scope",
        "",
        f"- Search mode: `{packet['scope']['search_mode']}`",
        "",
        "Allowed work:",
    ]
    lines.extend(f"- {item}" for item in packet["scope"]["allowed_work"])
    lines.extend(["", "Forbidden work:"])
    lines.extend(f"- {item}" for item in packet["scope"]["forbidden_work"])
    lines.extend(["", "## Proof Gates", ""])
    lines.extend(f"- `{gate}`" for gate in packet["proof_gates"])
    lines.extend(["", "## Candidates", ""])
    for candidate in packet["candidates"]:
        lines.extend(
            [
                f"### {candidate['candidate_id']}",
                "",
                f"- Review status: `{candidate['review_status']}`",
                f"- SHA-256: `{candidate.get('sha256')}`",
                f"- Path: `{candidate.get('path')}`",
                f"- Inner iSE entries: {', '.join(candidate.get('inner_ise_entries') or ['none'])}",
                (
                    "- Current assessment: "
                    f"`absolute_reflectance_proof_found="
                    f"{candidate['current_assessment']['absolute_reflectance_proof_found']}`, "
                    f"`exact_source_identity_proven="
                    f"{candidate['current_assessment']['exact_source_identity_proven']}`"
                ),
                "",
                "Evidence snippets to inspect first:",
            ]
        )
        snippets = candidate.get("evidence_snippets", [])
        if snippets:
            lines.extend(f"- `{snippet}`" for snippet in snippets[:6])
        else:
            lines.append("- No snippets available in the triage artifact.")
        lines.extend(["", "Manual review questions:"])
        lines.extend(f"- {question}" for question in candidate["manual_review_questions"])
        lines.append("")
    lines.extend(
        [
            "## Outcome Rules",
            "",
            f"- All gates pass: {packet['outcome_rules']['all_gates_pass']}",
            f"- Any gate unresolved: {packet['outcome_rules']['any_gate_unresolved']}",
            f"- All candidates unresolved: {packet['outcome_rules']['all_candidates_unresolved']}",
            "",
            "Recommended manual log fields: "
            + ", ".join(f"`{field}`" for field in packet["recommended_manual_log_fields"])
            + ".",
            "",
        ]
    )
    return "\n".join(lines)


def write_phase3a11_packet(output_dir: Path, packet: dict[str, Any]) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase3a11_manual_source_followup_packet.json"
    md_path = output_dir / "phase3a11_manual_source_followup_packet.md"
    json_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(packet_markdown(packet), encoding="utf-8")
    return json_path, md_path
