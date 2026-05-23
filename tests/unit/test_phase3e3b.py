from __future__ import annotations

from pathlib import Path

import pytest

from eternity.phase3e3b import build_phase3e3b_packet, write_phase3e3b_packet

PHASE3E3A_AUDIT = Path("docs/phase3e3a_saha_exported_table_audit.json")


@pytest.mark.skipif(not PHASE3E3A_AUDIT.exists(), reason="Phase 3E.3A audit is absent")
def test_phase3e3b_blocks_saha_tmm_without_source_backed_stack_contract() -> None:
    packet = build_phase3e3b_packet(PHASE3E3A_AUDIT)

    assert packet["decision"]["status"] == "frozen_stack_contract_not_source_backed_tmm_blocked"
    assert packet["decision"]["claim_status_ceiling"] == "weak_within_dataset_holdout"
    assert packet["decision"]["adapter_contract_frozen"] is False
    assert packet["decision"]["full_no_fit_tmm_validation_allowed"] is False
    assert packet["decision"]["residual_modeling_performed"] is False
    assert packet["decision"]["stop_rule_triggered"] is True

    assert packet["contract_items"]["stack_order_and_thickness"]["status"] == (
        "pass_for_source_semantics"
    )
    assert packet["contract_items"]["incidence_and_polarization"]["status"] == "pass"
    assert packet["contract_items"]["silicon_optical_constants"]["status"] == "blocked"
    assert packet["contract_items"]["substrate_backside_and_coherence"]["status"] == (
        "blocked"
    )
    assert "silicon_optical_constants" in packet["blocked_items"]
    assert "substrate_backside_and_coherence" in packet["blocked_items"]


@pytest.mark.skipif(not PHASE3E3A_AUDIT.exists(), reason="Phase 3E.3A audit is absent")
def test_phase3e3b_writes_report_artifacts(tmp_path: Path) -> None:
    packet = build_phase3e3b_packet(PHASE3E3A_AUDIT)
    json_path, md_path = write_phase3e3b_packet(tmp_path, packet)

    assert json_path.exists()
    assert md_path.exists()
    assert "Saha Frozen-Stack Model Provenance" in md_path.read_text(encoding="utf-8")
