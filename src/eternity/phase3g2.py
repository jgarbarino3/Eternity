"""Phase 3G.2 assistant ergonomics and safe research-memory promotion."""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from eternity.phase3g1 import (
    DEFAULT_PHASE3F1F_DECISION_PATH,
    DEFAULT_QUEUE_PATH,
    HARD_GATE_FLAGS,
    build_phase3g1_packet,
)
from eternity.research_memory.records import validate_record_payload

DEFAULT_RECORD_DRAFT_DIR = Path("research_memory/examples/intake_queue")
DEFAULT_PHASE3G2_REPORT_STEM = "phase3g2_assistant_intake_ergonomics"
DEFAULT_PHASE3G2_STATUS_CARDS_STEM = "phase3g2_status_cards"
PHASE3G2_PHASE_ID = "Phase 3G.2"
QUEUE_WARNING = "queue_record_not_validation_evidence"
NO_RESIDUAL_WARNING = "no_measured_residual_modeling_from_queue_record"
TEMPLATE_LEAD_IDS = {"future_clean_teaching_stack_template"}


def _utc_now() -> str:
    return datetime.now(tz=UTC).isoformat()


def _slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_]+", "_", value).strip("_").lower()
    return slug or "unknown"


def _compact_missing_flags(evaluation: dict[str, Any], limit: int = 4) -> list[str]:
    flags = list(evaluation["missing_required_flags"])
    if len(flags) <= limit:
        return flags
    return [*flags[:limit], f"+{len(flags) - limit}_more"]


def _lead_card(evaluation: dict[str, Any]) -> dict[str, Any]:
    return {
        "card_type": "lead_status",
        "lead_id": evaluation["lead_id"],
        "title": evaluation["title"],
        "canonical_dataset_label": evaluation["canonical_dataset_label"],
        "computed_intake_label": evaluation["computed_intake_label"],
        "hard_gate_pass": evaluation["hard_gate_pass"],
        "phase3f2_intake_candidate": evaluation["phase3f2_intake_candidate"],
        "missing_count": len(evaluation["missing_required_flags"]),
        "top_missing_flags": _compact_missing_flags(evaluation),
        "memory_links": evaluation["known_failure_memory"],
        "next_action": evaluation["exact_next_action"] or "No next action recorded.",
        "claim_ceiling": (
            "candidate_ready_for_phase3f2_source_intake"
            if evaluation["hard_gate_pass"]
            else evaluation["canonical_dataset_label"]
        ),
    }


def phase3g2_status_cards(packet: dict[str, Any]) -> list[dict[str, Any]]:
    """Build compact assistant cards from a Phase 3G.1 intake packet."""

    source_summary = packet["phase3g1_packet"]["summary"]
    source_decision = packet["phase3g1_packet"]["decision"]
    global_card = {
        "card_type": "queue_status",
        "phase_id": PHASE3G2_PHASE_ID,
        "source_phase_id": packet["phase3g1_packet"]["phase_id"],
        "status": packet["decision"]["status"],
        "phase3f2_intake_allowed": source_decision["phase3f2_intake_allowed"],
        "residual_modeling_allowed_now": source_decision[
            "residual_modeling_allowed_now"
        ],
        "phase4_candidate_ready_now": source_decision["phase4_candidate_ready_now"],
        "lead_count": source_summary["lead_count"],
        "hard_gate_pass_count": source_summary["hard_gate_pass_count"],
        "selected_next_lead_id": source_decision["selected_next_lead_id"],
        "top_blockers": [
            {"flag": flag, "count": count, "criterion": HARD_GATE_FLAGS[flag]}
            for flag, count in sorted(
                source_summary["blocker_counts"].items(),
                key=lambda item: (-item[1], item[0]),
            )[:6]
        ],
        "next_phase": packet["decision"]["recommended_next_phase"],
        "warnings": [QUEUE_WARNING, NO_RESIDUAL_WARNING],
    }
    lead_cards = [
        _lead_card(evaluation)
        for evaluation in sorted(
            packet["phase3g1_packet"]["lead_evaluations"],
            key=lambda item: (
                item["priority_rank"],
                len(item["missing_required_flags"]),
                item["lead_id"],
            ),
        )
    ]
    return [global_card, *lead_cards]


def _source_refs_for_lead(evaluation: dict[str, Any]) -> list[dict[str, str]]:
    refs = [
        {
            "source_type": "local_note",
            "locator": "docs/phase3g_measured_data_intake_queue.yaml",
            "description": "Phase 3G.1 machine-readable measured-data intake queue.",
        },
        {
            "source_type": "local_note",
            "locator": "docs/phase3g_measured_data_intake_queue.md",
            "description": "Phase 3G.1 generated assistant brief for the intake queue.",
        },
    ]
    for ref in evaluation["source_refs"]:
        refs.append(
            {
                "source_type": "local_note",
                "locator": ref,
                "description": f"Queue-cited source reference for {evaluation['lead_id']}.",
            }
        )
    for url in evaluation["source_urls"]:
        refs.append(
            {
                "source_type": "other",
                "locator": url,
                "description": f"Queue-cited public URL for {evaluation['lead_id']}.",
            }
        )
    return refs


def _record_body(evaluation: dict[str, Any]) -> str:
    missing = ", ".join(evaluation["missing_required_flags"]) or "none"
    memories = "; ".join(evaluation["known_failure_memory"]) or "none"
    notes = "; ".join(evaluation["notes"]) or "none"
    files = "; ".join(evaluation["exact_files_or_records"]) or "none"
    return (
        f"Phase 3G.1 queue lead `{evaluation['lead_id']}` was classified as "
        f"`{evaluation['computed_intake_label']}` with canonical label "
        f"`{evaluation['canonical_dataset_label']}`. Hard-gate pass is "
        f"{str(evaluation['hard_gate_pass']).lower()}. Missing or risky gates: "
        f"{missing}. Exact files or records named by the queue: {files}. "
        f"Known failure memory: {memories}. Notes: {notes}. "
        f"Next action: {evaluation['exact_next_action'] or 'none recorded'}. "
        "This draft preserves intake memory only; it is not validation evidence."
    )


def source_record_draft_for_lead(
    evaluation: dict[str, Any],
    *,
    created_at: str = "2026-05-26T00:00:00Z",
) -> dict[str, Any]:
    """Create a review-gated research-memory source-record draft for one lead."""

    label = evaluation["canonical_dataset_label"]
    lead_tag = _slug(evaluation["lead_id"])
    missing = evaluation["missing_required_flags"]
    payload: dict[str, Any] = {
        "schema_version": "0.1",
        "record_type": "source",
        "title": f"Phase 3G.1 queue lead - {evaluation['title']}",
        "summary": (
            f"{evaluation['lead_id']} is queued as {label}; hard-gate pass is "
            f"{str(evaluation['hard_gate_pass']).lower()}."
        ),
        "body": _record_body(evaluation),
        "evidence_state": "literature_supported",
        "review_state": "needs_human_review",
        "source_refs": _source_refs_for_lead(evaluation),
        "created_at": created_at,
        "tags": ["phase3g", "intake_queue", label, lead_tag],
        "project_areas": ["calibrated_linear_evidence", "research_memory"],
        "related_record_ids": [],
        "claims": [
            (
                f"The Phase 3G.1 queue currently classifies {evaluation['lead_id']} "
                f"as {label}."
            )
        ],
        "limitations": [
            "Queue classification is not measured validation evidence.",
            "No residual modeling or Phase 4 claim promotion is implied.",
            (
                "Phase 3F.2 intake can open only after every hard gate is "
                "source-backed before fitting."
            ),
        ],
        "next_actions": [
            evaluation["exact_next_action"]
            or "Inspect source files and hard gates before any intake escalation."
        ],
        "warnings": [QUEUE_WARNING, NO_RESIDUAL_WARNING],
        "source_kind": "measured_data_intake_queue_lead",
        "canonical_id": f"phase3g1_queue_{lead_tag}",
        "license_notes": "Repo-local queue memory only; inspect upstream licenses before intake.",
        "trust_notes": (
            "Derived from the Phase 3G.1 queue and prior failure-memory records; "
            "requires human review before use as an active source record."
        ),
    }
    if missing:
        payload["limitations"].append(
            "Missing or risky hard gates: " + ", ".join(missing) + "."
        )
    validate_record_payload(payload)
    return payload


def build_phase3g2_packet(
    queue_path: Path = DEFAULT_QUEUE_PATH,
    phase3f1f_decision_path: Path = DEFAULT_PHASE3F1F_DECISION_PATH,
    *,
    include_templates: bool = False,
) -> dict[str, Any]:
    """Build the Phase 3G.2 assistant packet from the Phase 3G.1 queue."""

    phase3g1_packet = build_phase3g1_packet(queue_path, phase3f1f_decision_path)
    included_evaluations = [
        evaluation
        for evaluation in phase3g1_packet["lead_evaluations"]
        if include_templates or evaluation["lead_id"] not in TEMPLATE_LEAD_IDS
    ]
    record_drafts = [
        source_record_draft_for_lead(evaluation) for evaluation in included_evaluations
    ]
    packet: dict[str, Any] = {
        "phase_id": PHASE3G2_PHASE_ID,
        "title": "Assistant Intake Ergonomics And Research-Memory Record Promotion",
        "generated_at": _utc_now(),
        "inputs": {
            "queue_path": str(queue_path),
            "phase3f1f_decision_path": str(phase3f1f_decision_path),
            "include_templates": include_templates,
        },
        "phase3g1_packet": phase3g1_packet,
        "promotion_policy": {
            "record_drafts_are_validation_evidence": False,
            "default_review_state": "needs_human_review",
            "default_evidence_state": "literature_supported",
            "skipped_template_lead_ids": (
                [] if include_templates else sorted(TEMPLATE_LEAD_IDS)
            ),
            "warnings": [QUEUE_WARNING, NO_RESIDUAL_WARNING],
        },
        "record_drafts": record_drafts,
        "record_draft_manifest": [],
        "decision": {
            "status": "phase3g2_assistant_ergonomics_ready",
            "record_draft_count": len(record_drafts),
            "phase3f2_intake_allowed": phase3g1_packet["decision"][
                "phase3f2_intake_allowed"
            ],
            "residual_modeling_allowed_now": False,
            "phase4_candidate_ready_now": False,
            "claim_standard_changed": False,
            "recommended_next_phase": (
                "Phase 3G.3 - new-lead intake dry run and queue maintenance"
            ),
        },
    }
    packet["cards"] = phase3g2_status_cards(packet)
    return packet


def phase3g2_status_cards_markdown(packet: dict[str, Any]) -> str:
    """Render compact Markdown cards for assistant-facing status."""

    cards = packet["cards"]
    global_card = cards[0]
    lines = [
        "# Phase 3G.2 Status Cards",
        "",
        "## Queue",
        "",
        f"- Status: `{global_card['status']}`",
        (
            "- Phase 3F.2 intake allowed: "
            f"`{str(global_card['phase3f2_intake_allowed']).lower()}`"
        ),
        (
            "- Residual modeling allowed now: "
            f"`{str(global_card['residual_modeling_allowed_now']).lower()}`"
        ),
        (
            "- Hard-gate passes: "
            f"`{global_card['hard_gate_pass_count']}` / `{global_card['lead_count']}`"
        ),
        f"- Next phase: `{global_card['next_phase']}`",
        "",
        "## Lead Cards",
        "",
    ]
    for card in cards[1:]:
        missing = ", ".join(card["top_missing_flags"]) or "none"
        lines.extend(
            [
                f"### {card['lead_id']}",
                "",
                f"- Label: `{card['canonical_dataset_label']}`",
                f"- Gate pass: `{str(card['hard_gate_pass']).lower()}`",
                f"- Missing count: `{card['missing_count']}`",
                f"- Top missing flags: {missing}",
                f"- Claim ceiling: `{card['claim_ceiling']}`",
                f"- Next action: {card['next_action']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Warnings",
            "",
            f"- `{QUEUE_WARNING}`",
            f"- `{NO_RESIDUAL_WARNING}`",
            "",
        ]
    )
    return "\n".join(lines)


def phase3g2_assistant_brief_markdown(packet: dict[str, Any]) -> str:
    """Render the Phase 3G.2 assistant brief."""

    decision = packet["decision"]
    promotion = packet["promotion_policy"]
    lines = [
        f"# {packet['phase_id']} - {packet['title']}",
        "",
        "## Decision",
        "",
        f"- Status: `{decision['status']}`",
        f"- Record drafts: `{decision['record_draft_count']}`",
        (
            "- Phase 3F.2 intake allowed: "
            f"`{str(decision['phase3f2_intake_allowed']).lower()}`"
        ),
        (
            "- Residual modeling allowed now: "
            f"`{str(decision['residual_modeling_allowed_now']).lower()}`"
        ),
        (
            "- Phase 4 candidate ready now: "
            f"`{str(decision['phase4_candidate_ready_now']).lower()}`"
        ),
        f"- Recommended next phase: `{decision['recommended_next_phase']}`",
        "",
        "Phase 3G.2 makes the assistant intake queue easier to use. It writes",
        "compact status cards and review-gated research-memory draft records from",
        "the Phase 3G.1 queue. It does not change any hard gate, open Phase 3F.2,",
        "or authorize measured residual modeling.",
        "",
        "## Promotion Policy",
        "",
        (
            "- Record drafts are validation evidence: "
            f"`{str(promotion['record_drafts_are_validation_evidence']).lower()}`"
        ),
        f"- Default review state: `{promotion['default_review_state']}`",
        f"- Default evidence state: `{promotion['default_evidence_state']}`",
        "",
        "## Generated Draft Records",
        "",
    ]
    for draft in packet["record_drafts"]:
        lines.append(
            f"- `{draft['canonical_id']}`: {draft['summary']} "
            f"Warnings: {', '.join(draft['warnings'])}."
        )
    lines.extend(["", "## Status Cards", "", phase3g2_status_cards_markdown(packet)])
    return "\n".join(lines)


def write_phase3g2_record_drafts(
    output_dir: Path,
    packet: dict[str, Any],
) -> list[dict[str, str]]:
    """Write review-gated research-memory record drafts and return a manifest."""

    output_dir.mkdir(parents=True, exist_ok=True)
    manifest: list[dict[str, str]] = []
    for draft in packet["record_drafts"]:
        filename = f"{draft['canonical_id']}.yaml"
        path = output_dir / filename
        path.write_text(yaml.safe_dump(draft, sort_keys=False), encoding="utf-8")
        manifest.append(
            {
                "canonical_id": draft["canonical_id"],
                "path": str(path),
                "review_state": draft["review_state"],
                "evidence_state": draft["evidence_state"],
            }
        )
    packet["record_draft_manifest"] = manifest
    return manifest


def write_phase3g2_packet(
    output_dir: Path,
    packet: dict[str, Any],
    *,
    report_stem: str = DEFAULT_PHASE3G2_REPORT_STEM,
    status_cards_stem: str = DEFAULT_PHASE3G2_STATUS_CARDS_STEM,
) -> tuple[Path, Path, Path]:
    """Write Phase 3G.2 JSON, assistant brief, and status-card artifacts."""

    if report_stem != Path(report_stem).name or not report_stem:
        raise ValueError("report_stem must be a non-empty filename stem")
    if status_cards_stem != Path(status_cards_stem).name or not status_cards_stem:
        raise ValueError("status_cards_stem must be a non-empty filename stem")
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{report_stem}.json"
    md_path = output_dir / f"{report_stem}.md"
    cards_path = output_dir / f"{status_cards_stem}.md"
    json_path.write_text(json.dumps(packet, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(phase3g2_assistant_brief_markdown(packet), encoding="utf-8")
    cards_path.write_text(phase3g2_status_cards_markdown(packet), encoding="utf-8")
    return json_path, md_path, cards_path
