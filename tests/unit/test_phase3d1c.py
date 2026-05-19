from __future__ import annotations

from pathlib import Path

import pytest

from eternity.phase3d1c import build_phase3d1c_packet

STATIC_R0_PATH = Path(
    "lab_data/raw/public_exeter_bohn_ito_2021/exeter_bohn_fig2_static_r0.csv"
)
SPLIT_LOCK_PATH = Path("docs/phase3d1b_exeter_bohn_split_lock.yaml")


@pytest.mark.skipif(
    not STATIC_R0_PATH.exists() or not SPLIT_LOCK_PATH.exists(),
    reason="Phase 3D.1B Exeter/Bohn artifacts are absent",
)
def test_phase3d1c_reconstructs_no_fit_package_model_without_promotion() -> None:
    packet = build_phase3d1c_packet(STATIC_R0_PATH, SPLIT_LOCK_PATH)

    assert packet["decision"]["status"] == "no_fit_reconstruction_completed_nonpromoting"
    assert packet["decision"]["can_promote_calibrated_linear_evidence"] is False
    assert packet["decision"]["phase4_ready"] is False
    assert packet["locked_package_constants"]["eps_inf"] == 3.42725287
    assert packet["locked_package_constants"]["ito_thickness_nm"] == 60.0

    all_metrics = packet["metrics"]["all_locked_points"]
    assert all_metrics["points"] == 806
    assert all_metrics["shape_correlation"] == pytest.approx(0.9405464512393112)
    assert all_metrics["root_mean_square_error"] == pytest.approx(0.0427242277728512)

    plot_metrics = packet["metrics"]["figure2_plotted_window"]
    assert plot_metrics["points"] == 324
    assert plot_metrics["wavelength_nm"] == [1160.0, 1420.0]
    assert plot_metrics["shape_correlation"] == pytest.approx(0.9808096173689083)
    assert plot_metrics["root_mean_square_error"] == pytest.approx(0.03417097064799868)

    assert packet["leakage_guard"]["holdout_y_used_for_fitting"] is False
    assert packet["leakage_guard"]["promotion_for_this_run"] == "forbidden"
    assert len(packet["table"]) == 806
