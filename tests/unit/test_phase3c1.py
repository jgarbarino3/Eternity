from pathlib import Path

import pytest

from eternity.optical_data import load_epsilon_table, load_reflectance_spectrum
from eternity.phase3c1 import build_phase3c1_packet_from_paths


def test_phase3c1_extracts_member_snapshots_and_pairing_packet(tmp_path: Path) -> None:
    packet = build_phase3c1_packet_from_paths(
        Path("lab_data/raw/public_st_andrews_tin_2025/TiN-data_Pure.zip"),
        tmp_path,
    )

    assert packet["selected_pairing"]["pairing_status"] == "candidate_supported_reflectance_only"
    assert packet["policy"]["can_feed_serious_core"] is False
    assert packet["policy"]["threshold_status"] == "blocked_not_predeclared"

    reflectance = tmp_path / "standrews_tin_50nm_reflectance.csv"
    transmittance = tmp_path / "standrews_tin_50nm_transmittance.csv"
    epsilon = tmp_path / "standrews_tin_50nm_50c_epsilon.txt"
    assert reflectance.exists()
    assert transmittance.exists()
    assert epsilon.exists()

    reflectance_spectrum = load_reflectance_spectrum(reflectance)
    epsilon_table = load_epsilon_table(epsilon)
    assert reflectance_spectrum.wavelengths_nm[0] == pytest.approx(340.02)
    assert reflectance_spectrum.wavelengths_nm[-1] == pytest.approx(1029.8)
    assert epsilon_table.wavelengths_nm[0] == pytest.approx(245.874191)
    assert epsilon_table.wavelengths_nm[-1] == pytest.approx(1689.241577)


def test_phase3c1_rejects_missing_zip(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        build_phase3c1_packet_from_paths(tmp_path / "missing.zip", tmp_path)
