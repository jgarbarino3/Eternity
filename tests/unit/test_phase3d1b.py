from __future__ import annotations

from pathlib import Path

import pytest

from eternity.phase3d1b import build_phase3d1b_packet_from_paths

ZIP_PATH = Path("lab_data/raw/public_exeter_bohn_ito_2021/OpenData.zip")


@pytest.mark.skipif(not ZIP_PATH.exists(), reason="Exeter/Bohn package snapshot is absent")
def test_phase3d1b_extracts_static_r0_without_promotion(tmp_path: Path) -> None:
    packet = build_phase3d1b_packet_from_paths(ZIP_PATH, tmp_path)

    assert packet["decision"]["status"] == "static_r0_extracted_split_locked_no_residuals"
    assert packet["decision"]["can_promote_calibrated_linear_evidence"] is False
    assert packet["calibration_summary"]["rows"] == 187
    assert packet["calibration_summary"]["passivity_check"] == "pass"
    assert packet["calibration_summary"]["enz_wavelengths_nm"] == [1233.996861]
    assert packet["holdout_summary"]["tir_reference_rows"] == 31
    assert packet["holdout_summary"]["static_r0_rows"] == 806
    assert packet["holdout_summary"]["r0_grid"] == {
        "theta_count": 26,
        "wavelength_count": 31,
    }
    assert packet["holdout_summary"]["prepump_rows_per_point"] == [11]
    assert packet["split_lock"]["fitting_may_access_holdout_y"] is False

    for artifact in packet["artifacts"].values():
        assert Path(artifact["path"]).exists()
        assert len(artifact["sha256"]) == 64
