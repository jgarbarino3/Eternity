from __future__ import annotations

from pathlib import Path

from eternity.phase3f1e import build_phase3f1e_packet, write_phase3f1e_packet


def _write_fixture_source(root: Path) -> None:
    root.mkdir(parents=True)
    (root / "TMM_numba.py").write_text(
        """
from numba import jit
import numpy as np
from tmm import coh_tmm


@jit(nopython=True)
def reflect_amp(rho, ang_of_inc, wavelength, n, l, n_cover, n_subst):
    pol = "p" if rho == 1 else "s"
    result = coh_tmm(
        pol,
        [n_cover, *list(n), n_subst],
        [np.inf, *list(l * 1e9), np.inf],
        ang_of_inc * np.pi / 180,
        wavelength * 1e9,
    )
    return result["R"]


@jit(nopython=True)
def trans_amp(rho, ang_of_inc, wavelength, n, l, n_cover, n_subst):
    pol = "p" if rho == 1 else "s"
    result = coh_tmm(
        pol,
        [n_cover, *list(n), n_subst],
        [np.inf, *list(l * 1e9), np.inf],
        ang_of_inc * np.pi / 180,
        wavelength * 1e9,
    )
    return result["T"]
""".lstrip(),
        encoding="utf-8",
    )
    (root / "nGe.txt").write_text("\n".join(["3.2"] * 701) + "\n", encoding="utf-8")
    (root / "kGe.txt").write_text("\n".join(["-1.0"] * 701) + "\n", encoding="utf-8")
    rows = ["nm,n,k,nm,n,k,nm,n,k"]
    for wavelength_nm in range(500, 801):
        rows.append(
            f"{wavelength_nm},1.46,0,{wavelength_nm},1,0,{wavelength_nm},2.2,0"
        )
    (root / "constants.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")


def test_phase3f1e_packet_runs_with_stubbed_numba(tmp_path: Path) -> None:
    source_root = tmp_path / "source"
    _write_fixture_source(source_root)
    archive_path = tmp_path / "source.zip"
    archive_path.write_bytes(b"not the pinned archive")

    packet = build_phase3f1e_packet(source_root, archive_path)

    assert packet["phase_id"] == "Phase 3F.1E"
    assert packet["summary"]["case_count"] == 3
    assert packet["summary"]["all_cases_passed"] is True
    assert packet["claim_boundary"]["experimental_validation"] is False
    assert packet["decision"]["phase3f2_intake_allowed"] is False
    assert packet["decision"]["residual_modeling_allowed"] is False
    assert packet["inputs"]["archive_hash_matches"] is False
    assert (
        packet["decision"]["status"]
        == "phase3f1e_code_regression_fixture_needs_attention"
    )


def test_write_phase3f1e_packet_writes_json_and_markdown(tmp_path: Path) -> None:
    source_root = tmp_path / "source"
    _write_fixture_source(source_root)
    packet = build_phase3f1e_packet(source_root, tmp_path / "missing.zip")

    json_path, md_path = write_phase3f1e_packet(
        tmp_path / "out",
        packet,
        report_stem="phase3f1e_test",
    )

    assert json_path.exists()
    assert md_path.exists()
    assert "non-promoting code-regression fixture" in md_path.read_text(
        encoding="utf-8"
    )
