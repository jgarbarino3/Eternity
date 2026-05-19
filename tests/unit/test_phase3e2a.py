from __future__ import annotations

from pathlib import Path

import pytest

from eternity.phase3e2a import build_phase3e2a_packet

RAW_DIR = Path("lab_data/raw/public_wang_wo3_fp_2020")
METADATA_PATH = RAW_DIR / "figshare_article_11154791.json"


@pytest.mark.skipif(
    not METADATA_PATH.exists(),
    reason="Wang W/WO3 Figshare metadata snapshot is absent",
)
def test_phase3e2a_records_non_enz_baseline_without_promotion() -> None:
    packet = build_phase3e2a_packet(METADATA_PATH, RAW_DIR)

    assert packet["decision"]["status"] == (
        "non_enz_baseline_source_data_snapshotted_semantics_partial"
    )
    assert packet["decision"]["download_integrity"] == "selected_downloaded_md5_match"
    assert packet["decision"]["non_enz_planar_tmm_baseline_intake_ready"] is True
    assert packet["decision"]["phase4_enz_ready"] is False
    assert packet["decision"]["can_promote_calibrated_linear_evidence"] is False
    assert packet["decision"]["claim_status_ceiling"] == "non_enz_planar_tmm_baseline_candidate"

    constants = packet["target_inspection"]["constants"]["sheets"]
    assert constants["WO3"]["present"] is True
    assert constants["WO3"]["columns"] == ["wavelength_nm", "n", "k"]
    assert constants["W"]["present"] is True
    assert constants["W"]["wavelength_monotonic_increasing"] is True

    fig2f = packet["target_inspection"]["fig2f_reflectance"]["inspection"]
    assert fig2f["expected_thicknesses_match"] is True
    assert fig2f["thicknesses_nm"] == [152, 163, 185, 200, 215, 233, 250]
    assert fig2f["semantics_status"] == "offset_plot_traces_not_plain_absolute_reflectance"
    assert fig2f["contains_nonphysical_plot_values"] is True
    assert fig2f["measured_vs_simulated_assignment"] == "unlabeled_in_workbook"

    ellipsometry = packet["target_inspection"]["ellipsometry_source_data"]
    assert ellipsometry["FigS1-W.xlsx"]["sheets"]["cos"]["angle_labels_deg"] == [55, 65, 75]
    assert ellipsometry["FigS1-WO3.xlsx"]["sheets"]["tan"]["angle_labels_deg"] == [
        55,
        65,
        75,
    ]
