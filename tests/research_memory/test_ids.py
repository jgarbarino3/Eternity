from __future__ import annotations

from eternity.research_memory.ids import content_hash_for_record, record_id_for_payload

PAYLOAD = {
    "schema_version": "0.1",
    "record_type": "hypothesis",
    "title": "H-014 TiN ENZ reflection phase may suppress satellites",
    "summary": "A possible wavelength-dependent reflection phase effect needs validation.",
    "evidence_state": "speculative",
    "source_refs": [
        {
            "source_type": "lab_note",
            "locator": "notebook:H-014",
            "description": "Curated hypothesis note.",
        }
    ],
    "created_at": "2026-05-08T12:00:00Z",
    "tags": ["frog", "tin", "enz"],
    "related_record_ids": [],
    "claims": ["TiN ENZ reflection may reshape broadband few-cycle pulses."],
    "limitations": ["No matched neutral-mirror control in this record."],
    "next_actions": ["Run synthetic thin-film phase comparison before stronger claims."],
    "hypothesis_id": "H-014",
    "hypothesis_statement": (
        "TiN ENZ reflection imposes a wavelength-dependent phase response that can reshape "
        "temporal satellites."
    ),
    "why_plausible": ["ENZ reflection phase can vary rapidly near resonance."],
    "what_would_support_it": ["Agreement with calibrated thin-film phase model."],
    "what_would_weaken_it": ["Neutral mirror produces the same reshaping."],
    "next_simulation": "Synthetic thin-film phase test.",
    "next_lab_test": "Matched no-sample/TiN/neutral-mirror FROG at multiple energies.",
    "current_confidence": "low",
    "validation_status": "untested",
}


def test_record_id_is_stable_for_same_normalized_payload() -> None:
    first = record_id_for_payload(PAYLOAD)
    reordered = PAYLOAD | {"tags": ["enz", "frog", "tin"], "created_at": "2026-05-09T12:00:00Z"}

    assert first == record_id_for_payload(reordered)
    assert first.startswith("rm_hypothesis_")


def test_record_id_changes_when_scientific_content_changes() -> None:
    changed = PAYLOAD | {"title": "Different hypothesis"}

    assert record_id_for_payload(PAYLOAD) != record_id_for_payload(changed)


def test_content_hash_is_stable_and_uses_record_content() -> None:
    digest = content_hash_for_record(PAYLOAD)

    assert len(digest) == 64
    assert digest == content_hash_for_record(PAYLOAD)
