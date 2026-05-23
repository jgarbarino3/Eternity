from __future__ import annotations

from pathlib import Path

import pytest

from eternity.phase3e3a import build_phase3e3a_packet, write_phase3e3a_packet

RAW_DIR = Path("lab_data/raw/public_saha_tin_azo_2023")
METADATA_PATH = RAW_DIR / "figshare_article_23734116.json"
FIG2B_EXPORT = RAW_DIR / "origin_viewer_exports/saha_fig2b_origin_viewer_export.csv"
FIG2CD_EXPORT = RAW_DIR / "origin_viewer_exports/saha_fig2cd_origin_viewer_export.csv"


@pytest.mark.skipif(
    not (METADATA_PATH.exists() and FIG2B_EXPORT.exists() and FIG2CD_EXPORT.exists()),
    reason="Saha Origin Viewer exports are absent",
)
def test_phase3e3a_canonicalizes_saha_exports_and_blocks_tmm(tmp_path: Path) -> None:
    canonical_dir = tmp_path / "canonical"
    packet = build_phase3e3a_packet(METADATA_PATH, RAW_DIR, canonical_dir)

    assert packet["decision"]["status"] == "canonical_tables_ready_tmm_adapter_blocked"
    assert packet["decision"]["claim_status_ceiling"] == "weak_within_dataset_holdout"
    assert packet["decision"]["full_no_fit_tmm_validation_allowed"] is False
    assert packet["decision"]["stop_rule_triggered"] is True

    reflectance = packet["table_audit"]["fig2b_reflectance"]
    assert reflectance["numeric_rows"] == 175
    assert reflectance["wavelength_nm"] == [260.0, 2000.0]
    assert reflectance["wavelength_step_nm"] == 10.0
    assert reflectance["unit_interval_check"] == "pass"
    assert reflectance["measured_and_source_simulated_split"] == "explicit_source_labels"

    epsilon = packet["table_audit"]["fig2cd_permittivity"]
    assert epsilon["tin"]["numeric_rows"] == 181
    assert epsilon["tin"]["wavelength_nm"] == [300.0, 2100.0]
    assert epsilon["tin"]["enz_wavelengths_nm"] == [484.054679]
    assert epsilon["azo"]["numeric_rows"] == 171
    assert epsilon["azo"]["wavelength_nm"] == [300.0, 2000.0]
    assert epsilon["azo"]["enz_wavelengths_nm"] == [1364.223257]

    assert packet["gate_review"]["split_gate"]["status"] == "pass"
    assert packet["gate_review"]["stack_model_gate"]["status"] == "blocked"

    for artifact in packet["artifacts"].values():
        path = Path(artifact["path"])
        assert path.exists()
        assert path.parent == canonical_dir
        assert len(artifact["sha256"]) == 64


@pytest.mark.skipif(
    not (METADATA_PATH.exists() and FIG2B_EXPORT.exists() and FIG2CD_EXPORT.exists()),
    reason="Saha Origin Viewer exports are absent",
)
def test_phase3e3a_writes_report_artifacts(tmp_path: Path) -> None:
    packet = build_phase3e3a_packet(METADATA_PATH, RAW_DIR, tmp_path / "canonical")
    json_path, md_path = write_phase3e3a_packet(tmp_path / "docs", packet)

    assert json_path.exists()
    assert md_path.exists()
    assert "Saha Exported-Table Audit" in md_path.read_text(encoding="utf-8")
