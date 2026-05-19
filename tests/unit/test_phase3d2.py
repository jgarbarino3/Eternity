from __future__ import annotations

from pathlib import Path

import pytest

from eternity.phase3d2 import build_phase3d2_packet

RAW_DIR = Path("lab_data/raw/public_saha_tin_azo_2023")
METADATA_PATH = RAW_DIR / "figshare_article_23734116.json"


@pytest.mark.skipif(
    not METADATA_PATH.exists(),
    reason="Saha TiN/AZO Figshare metadata snapshot is absent",
)
def test_phase3d2_records_origin_export_blocker_without_promotion() -> None:
    packet = build_phase3d2_packet(METADATA_PATH, RAW_DIR)

    assert packet["decision"]["status"] == "source_package_snapshotted_origin_export_blocked"
    assert packet["decision"]["can_promote_calibrated_linear_evidence"] is False
    assert packet["decision"]["phase4_ready"] is False
    assert packet["decision"]["download_integrity"] == "all_downloaded_md5_match"
    assert packet["source"]["file_count"] == 12

    fig2b = packet["target_inspection"]["fig2b_reflectance"]
    assert fig2b["downloaded"] is True
    assert "Measured Rp" in fig2b["labels_found"]
    assert "Measured Rs" in fig2b["labels_found"]
    assert "Simulated Rp" in fig2b["labels_found"]
    assert fig2b["embedded_preview_png"]["present"] is True
    assert fig2b["table_extraction_status"] == "blocked_by_origin_binary_container"

    fig2cd = packet["target_inspection"]["fig2cd_permittivity"]
    assert fig2cd["downloaded"] is True
    assert "Film thickness 130 nm" in fig2cd["labels_found"]
    assert "Film thickness 250 nm" in fig2cd["labels_found"]
    assert "TiN real part of permittivity" in fig2cd["labels_found"]
    assert "AZO real part of permittivity" in fig2cd["labels_found"]
    assert fig2cd["embedded_preview_png"]["present"] is True
