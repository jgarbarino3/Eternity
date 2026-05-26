from __future__ import annotations

import json
from pathlib import Path

from eternity.phase3g1 import DEFAULT_QUEUE_PATH, build_phase3g1_packet
from eternity.phase3g2 import (
    NO_RESIDUAL_WARNING,
    QUEUE_WARNING,
    build_phase3g2_packet,
    phase3g2_status_cards_markdown,
    write_phase3g2_packet,
    write_phase3g2_record_drafts,
)
from eternity.research_memory.store import load_records


def test_phase3g2_builds_status_cards_without_opening_gate() -> None:
    packet = build_phase3g2_packet(DEFAULT_QUEUE_PATH)

    assert packet["decision"]["status"] == "phase3g2_assistant_ergonomics_ready"
    assert packet["decision"]["record_draft_count"] == 4
    assert packet["decision"]["phase3f2_intake_allowed"] is False
    assert packet["decision"]["residual_modeling_allowed_now"] is False
    assert packet["decision"]["phase4_candidate_ready_now"] is False
    assert packet["cards"][0]["card_type"] == "queue_status"
    assert packet["cards"][0]["hard_gate_pass_count"] == 0
    assert QUEUE_WARNING in packet["cards"][0]["warnings"]
    assert NO_RESIDUAL_WARNING in packet["cards"][0]["warnings"]


def test_phase3g2_skips_placeholder_template_by_default() -> None:
    packet = build_phase3g2_packet(DEFAULT_QUEUE_PATH)
    draft_ids = {draft["canonical_id"] for draft in packet["record_drafts"]}

    assert "phase3g1_queue_future_clean_teaching_stack_template" not in draft_ids
    assert "phase3g1_queue_saha_tin_azo_2023_exported_tables" in draft_ids

    with_templates = build_phase3g2_packet(DEFAULT_QUEUE_PATH, include_templates=True)
    assert with_templates["decision"]["record_draft_count"] == 5


def test_phase3g2_record_drafts_validate_as_research_memory(tmp_path: Path) -> None:
    packet = build_phase3g2_packet(DEFAULT_QUEUE_PATH)
    manifest = write_phase3g2_record_drafts(tmp_path, packet)

    assert len(manifest) == 4
    loaded = load_records(tmp_path)
    assert len(loaded) == 4
    for item in loaded:
        assert item.record.review_state == "needs_human_review"
        assert item.record.evidence_state == "literature_supported"
        assert QUEUE_WARNING in item.record.warnings
        assert item.record.validation_artifact_ref is None


def test_phase3g2_writes_assistant_artifacts(tmp_path: Path) -> None:
    packet = build_phase3g2_packet(DEFAULT_QUEUE_PATH)
    json_path, md_path, cards_path = write_phase3g2_packet(
        tmp_path,
        packet,
        report_stem="phase3g2_fixture",
        status_cards_stem="phase3g2_cards_fixture",
    )

    assert json_path.name == "phase3g2_fixture.json"
    assert md_path.name == "phase3g2_fixture.md"
    assert cards_path.name == "phase3g2_cards_fixture.md"

    saved = json.loads(json_path.read_text(encoding="utf-8"))
    assert saved["decision"]["record_draft_count"] == 4
    assert "Assistant Intake Ergonomics" in md_path.read_text(encoding="utf-8")
    assert "Status Cards" in cards_path.read_text(encoding="utf-8")


def test_phase3g2_status_cards_follow_phase3g1_decision() -> None:
    source_packet = build_phase3g1_packet(DEFAULT_QUEUE_PATH)
    packet = build_phase3g2_packet(DEFAULT_QUEUE_PATH)
    markdown = phase3g2_status_cards_markdown(packet)

    assert packet["phase3g1_packet"]["decision"] == source_packet["decision"]
    assert "saha_tin_azo_2023_exported_tables" in markdown
    assert "queue_record_not_validation_evidence" in markdown
