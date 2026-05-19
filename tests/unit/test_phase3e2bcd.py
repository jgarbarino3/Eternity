from __future__ import annotations

from pathlib import Path

import pytest

from eternity.phase3e2b import build_phase3e2b_packet
from eternity.phase3e2c import build_phase3e2c_fixture_rows, build_phase3e2c_packet
from eternity.phase3e2d import build_phase3e2d_packet

RAW_DIR = Path("lab_data/raw/public_wang_wo3_fp_2020")
FIG2F_PATH = RAW_DIR / "Fig2f-R.xlsx"


@pytest.mark.skipif(not FIG2F_PATH.exists(), reason="Wang Fig. 2f source data absent")
def test_phase3e2b_blocks_full_validation_but_allows_fixture() -> None:
    packet = build_phase3e2b_packet(RAW_DIR)

    assert packet["decision"]["status"] == (
        "source_backed_offsets_inferred_columns_not_source_labeled"
    )
    assert packet["decision"]["full_no_fit_tmm_validation_allowed"] is False
    assert packet["decision"]["bounded_deoffset_reproduction_fixture_allowed"] is True
    assert packet["workbook_archive_features"]["has_chart_xml"] is False
    assert packet["workbook_archive_features"]["has_drawing_xml"] is False

    layout = packet["fig2f_layout"]
    assert layout["expected_thicknesses_match"] is True
    assert layout["offset_rule"]["all_deoffseted_ranges_are_reflectance_like_percent"] is True
    assert layout["measured_simulated_assignment"]["workbook_has_explicit_labels"] is False
    assert layout["pairs"][0]["offset_added_percent"] == 420
    assert layout["pairs"][-1]["offset_added_percent"] == 0


@pytest.mark.skipif(not FIG2F_PATH.exists(), reason="Wang Fig. 2f source data absent")
def test_phase3e2c_writes_non_promoting_deoffset_fixture_rows() -> None:
    packet = build_phase3e2c_packet(RAW_DIR)
    rows = build_phase3e2c_fixture_rows(RAW_DIR)

    assert packet["decision"]["status"] == "bounded_deoffset_reproduction_fixture_ready"
    assert packet["decision"]["claim_status_ceiling"] == "literature_reproduction_fixture"
    assert packet["decision"]["full_no_fit_tmm_validation_allowed"] is False
    assert packet["row_count"] == len(rows)
    assert len(rows) == 3017
    assert rows[0]["thickness_nm"] == 152
    assert rows[0]["wavelength_nm"] == 780
    assert rows[0]["offset_added_percent"] == 420
    assert 0 <= rows[0]["inferred_measured_percent"] <= 70
    assert 0 <= rows[0]["inferred_simulated_percent"] <= 70
    assert packet["metrics"]["global"]["point_count"] == len(rows)


@pytest.mark.skipif(not FIG2F_PATH.exists(), reason="Wang Fig. 2f source data absent")
def test_phase3e2d_handoff_keeps_wang_below_phase4() -> None:
    packet = build_phase3e2d_packet(RAW_DIR)

    assert packet["decision"]["status"] == "phase3e2b_through_3e2d_complete"
    assert packet["lane_decision"]["candidate_label"] == "literature_reproduction_fixture"
    assert packet["lane_decision"]["phase4_candidate"] is False
    assert packet["lane_decision"]["serious_core_allowed"] is False
