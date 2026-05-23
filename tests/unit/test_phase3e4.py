from __future__ import annotations

from pathlib import Path

from eternity.phase3e4 import build_phase3e4_packet, write_phase3e4_packet

REGISTRY_PATH = Path("docs/phase3e1_dataset_candidate_registry.yaml")


def test_phase3e4_search_snapshot_blocks_phase4_and_residuals() -> None:
    packet = build_phase3e4_packet(REGISTRY_PATH)

    assert packet["decision"]["status"] == "phase3e4_search_snapshot_no_phase4_candidate"
    assert packet["decision"]["can_open_phase4_now"] is False
    assert packet["decision"]["can_feed_serious_core_now"] is False
    assert packet["decision"]["residual_modeling_performed"] is False
    assert packet["decision"]["tmm_adapter_started"] is False
    assert packet["summary"]["phase4_candidate_count"] == 0
    assert packet["stop_rule"]["triggered"] is True


def test_phase3e4_records_intracavity_zenodo_correction_without_promotion() -> None:
    packet = build_phase3e4_packet(REGISTRY_PATH)
    by_id = {lead["lead_id"]: lead for lead in packet["inspected_leads"]}
    lead = by_id["acs_intracavity_ito_2025_zenodo_data"]

    assert lead["decision"] == "zenodo_matlab_package_found_not_phase4_ready"
    assert lead["gate"]["machine_readable_tables"] is True
    assert lead["gate"]["independent_measured_holdout"] is False
    assert lead["gate"]["leakage_boundary"] is False
    assert lead["claim_label"] == "literature_reproduction_fixture"


def test_phase3e4_writes_report_artifacts(tmp_path: Path) -> None:
    packet = build_phase3e4_packet(REGISTRY_PATH)
    json_path, md_path = write_phase3e4_packet(tmp_path, packet)

    assert json_path.exists()
    assert md_path.exists()
    assert "Renewed ENZ Public-Data Search" in md_path.read_text(encoding="utf-8")
