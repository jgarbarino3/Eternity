import json
import zipfile
from pathlib import Path

from eternity.phase3a7 import (
    RecoveryInputs,
    build_phase3a7_recovery,
    write_phase3a7_recovery,
)


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_phase3a7_recovery_ranks_sesnap_candidates_and_stays_blocked(tmp_path: Path) -> None:
    source_root = tmp_path / "sources"
    source_root.mkdir()
    sesnap = source_root / "20230519 - Puck 4 quartz 3 layer cap test.SEsnap"
    with zipfile.ZipFile(sesnap, "w") as archive:
        archive.writestr(
            "_FitLog",
            "\n".join(
                [
                    "C:\\CompleteEASE\\StateFileOpen\\example.iSE",
                    (
                        "20230518 - Puck 4 complete - 20 nm SiO2 - 53nm TiN "
                        "on quartz for 3 layer cap test"
                    ),
                    "Standard Ellipsometric",
                    "start_Simulation",
                    "45.0 75.0",
                ]
            ),
        )
        archive.writestr("example.iSE", b"reflective intensity and RC2 metadata")
    _write(source_root / "unrelated.SE", "nothing useful")

    recovery = build_phase3a7_recovery(
        RecoveryInputs(
            source_root=source_root,
            thesis_pdf=_write(tmp_path / "thesis.pdf", "3L2 Figure 4.1"),
            d10_initial=_write(
                tmp_path / "d_10nm_initial.txt",
                "Wavelength\tIntensity\n500\t0.1\n",
            ),
            d10_12v=_write(tmp_path / "d_10nm_12V.txt", "Wavelength\tIntensity\n500\t0.2\n"),
            candidate_ps_intensity=_write(
                tmp_path / "30_20_10 p_s intensity.txt",
                "Wavelength\tp-Intensity\ts-Intensity\n500\t0.1\t0.2\n",
            ),
            candidate_reflectance=_write(
                tmp_path / "30_20_10 reflectance.txt",
                "Wavelength\tIntensity\n500\t0.3\n",
            ),
        )
    )

    assert recovery["phase_id"] == "Phase 3A.7"
    assert recovery["decision"]["stack_mapping"] == "stack_mapping_confirmed"
    assert recovery["decision"]["absolute_reflectance_status"] == "absolute_reflectance_blocked"
    assert recovery["decision"]["can_promote_calibrated_linear_evidence"] is False
    assert recovery["candidate_sources"][0]["path"].endswith(".SEsnap")
    assert "has_fit_log" in recovery["candidate_sources"][0]


def test_phase3a7_recovery_writes_json_and_markdown(tmp_path: Path) -> None:
    source_root = tmp_path / "sources"
    source_root.mkdir()
    _write(source_root / "candidate.SE", "CompleteEASE reflectance intensity quartz")
    recovery = build_phase3a7_recovery(
        RecoveryInputs(
            source_root=source_root,
            thesis_pdf=_write(tmp_path / "thesis.pdf", "3L2 Figure 4.1"),
            d10_initial=_write(tmp_path / "d_10nm_initial.txt", "Wavelength\tIntensity\n"),
            d10_12v=_write(tmp_path / "d_10nm_12V.txt", "Wavelength\tIntensity\n"),
            candidate_ps_intensity=_write(
                tmp_path / "30_20_10 p_s intensity.txt",
                "Wavelength\tp-Intensity\ts-Intensity\n",
            ),
            candidate_reflectance=_write(
                tmp_path / "30_20_10 reflectance.txt",
                "Wavelength\tIntensity\n",
            ),
        )
    )

    json_path, md_path = write_phase3a7_recovery(tmp_path / "out", recovery)

    assert json.loads(json_path.read_text())["phase_id"] == "Phase 3A.7"
    assert "CompleteEASE Source Recovery" in md_path.read_text()


def test_phase3a7_recovery_reads_sesnap_members_inside_zip(tmp_path: Path) -> None:
    source_root = tmp_path / "sources"
    source_root.mkdir()
    sesnap_payload = tmp_path / "inner.SEsnap"
    with zipfile.ZipFile(sesnap_payload, "w") as archive:
        archive.writestr("_FitLog", "CompleteEASE quartz 10nm SiO2 cap pulsed 0-12Vdc")
    outer_zip = source_root / "DoD SAFE.zip"
    with zipfile.ZipFile(outer_zip, "w") as archive:
        archive.write(sesnap_payload, "DoD SAFE/20230524 - quartz - 10nm SiO2 - cap.SEsnap")

    recovery = build_phase3a7_recovery(
        RecoveryInputs(
            source_root=source_root,
            thesis_pdf=_write(tmp_path / "thesis.pdf", "3L2 Figure 4.1"),
            d10_initial=_write(tmp_path / "d_10nm_initial.txt", "Wavelength\tIntensity\n"),
            d10_12v=_write(tmp_path / "d_10nm_12V.txt", "Wavelength\tIntensity\n"),
            candidate_ps_intensity=_write(
                tmp_path / "30_20_10 p_s intensity.txt",
                "Wavelength\tp-Intensity\ts-Intensity\n",
            ),
            candidate_reflectance=_write(
                tmp_path / "30_20_10 reflectance.txt",
                "Wavelength\tIntensity\n",
            ),
        )
    )

    top = recovery["candidate_sources"][0]
    assert top["container_path"].endswith("DoD SAFE.zip")
    assert top["member_path"].endswith(".SEsnap")
    assert top["has_fit_log"] is True
