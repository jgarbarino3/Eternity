from __future__ import annotations

from pathlib import Path

from eternity.research_memory.digest import write_digest
from eternity.research_memory.search import search_records
from eternity.research_memory.store import load_records


def test_example_records_validate() -> None:
    loaded = load_records(Path("research_memory/examples"))

    assert len(loaded) >= 3
    assert {item.record.record_type for item in loaded} >= {
        "method_transfer",
        "lab_failure_mode",
        "hypothesis",
    }


def test_search_orders_relevant_records_and_shows_evidence() -> None:
    loaded = load_records(Path("research_memory/examples"))

    results = search_records([item.record for item in loaded], "scalar GDD TiN FROG", limit=3)

    assert results
    assert results[0].record.record_type == "lab_failure_mode"
    assert results[0].record.evidence_state == "observed_lab"
    assert "scalar" in results[0].snippet.lower()


def test_digest_writes_conservative_markdown(tmp_path: Path) -> None:
    loaded = load_records(Path("research_memory/examples"))

    output_path = write_digest(
        [item.record for item in loaded],
        output_root=tmp_path,
        project_area="tin_frog",
    )

    digest = output_path.read_text()
    assert output_path.name == "digest.md"
    assert "Eternity Research Memory Digest" in digest
    assert "Weak claims / needs validation" in digest
    assert "not validated evidence" in digest
    assert "## Provenance" in digest
    assert "source_refs=" in digest
