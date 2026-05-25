from __future__ import annotations

from pathlib import Path

import pytest

from eternity.phase3e5 import (
    DEFAULT_PHASE3E3B_GATE_PATH,
    build_phase3e5_packet,
    write_phase3e5_packet,
)


@pytest.mark.skipif(
    not DEFAULT_PHASE3E3B_GATE_PATH.exists(),
    reason="Phase 3E.3B Saha stack gate is absent",
)
def test_phase3e5_builds_non_promoting_sensitivity_fixture() -> None:
    packet, rows = build_phase3e5_packet(DEFAULT_PHASE3E3B_GATE_PATH)

    assert packet["decision"]["status"] == "phase3e5_saha_sensitivity_fixture_ready"
    assert packet["decision"]["calibrated_linear_evidence_allowed"] is False
    assert packet["decision"]["phase4_candidate"] is False
    assert packet["decision"]["validation_residual_modeling_performed"] is False
    assert packet["decision"]["diagnostic_comparisons_performed"] is True
    assert packet["assumption_space"]["variant_count"] == 12
    assert packet["spread_summary"]["rp"]["max_spread"] > 0
    assert packet["spread_summary"]["rs"]["max_spread"] > 0
    assert packet["remembered_next_work"]["phase_id"] == "Phase 3F"
    assert rows
    assert "measured_rp" in rows[0]


@pytest.mark.skipif(
    not DEFAULT_PHASE3E3B_GATE_PATH.exists(),
    reason="Phase 3E.3B Saha stack gate is absent",
)
def test_phase3e5_writes_report_and_curve_artifacts(tmp_path: Path) -> None:
    packet, rows = build_phase3e5_packet(DEFAULT_PHASE3E3B_GATE_PATH)
    json_path, md_path, csv_path = write_phase3e5_packet(tmp_path, packet, rows)

    assert json_path.exists()
    assert md_path.exists()
    assert csv_path.exists()
    assert "Saha No-Claim Stack-Assumption" in md_path.read_text(encoding="utf-8")
    assert "wavelength_nm" in csv_path.read_text(encoding="utf-8").splitlines()[0]
