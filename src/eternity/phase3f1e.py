"""Phase 3F.1E non-promoting TMM code-regression fixture."""

from __future__ import annotations

import importlib.util
import json
import sys
import types
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
from tmm import coh_tmm

DEFAULT_SOURCE_ROOT = Path(
    "lab_data/raw/phase3f1c_structural_color_froc_2023/"
    "structural_color_FROCs_7c0998d/"
    "structural_color_FROCs-7c0998d720c387f1efbffe6d1417593ba2f845b1"
)
DEFAULT_ARCHIVE_PATH = Path(
    "lab_data/raw/phase3f1c_structural_color_froc_2023/"
    "structural_color_FROCs_7c0998d.zip"
)
PINNED_GITHUB_REVISION = "7c0998d720c387f1efbffe6d1417593ba2f845b1"
PINNED_ARCHIVE_SHA256 = (
    "9d595ac110fc203b500780c97393a070c876fc81c5b75e7c20f0e1abf7949d92"
)
PARITY_TOLERANCE_ABS = 1e-12


@dataclass(frozen=True)
class Phase3F1ECase:
    case_id: str
    description: str
    rho: int
    polarization: str
    angle_deg: float
    wavelength_m: float
    n_layers: np.ndarray
    thicknesses_m: np.ndarray
    n_cover: complex
    n_substrate: complex
    source_inputs: dict[str, Any]


def _sha256(path: Path) -> str:
    import hashlib

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_source_tmm_module(source_root: Path):
    tmm_path = source_root / "TMM_numba.py"
    if not tmm_path.exists():
        raise FileNotFoundError(f"missing structural_color_FROCs TMM helper: {tmm_path}")

    previous_numba = sys.modules.get("numba")
    fake_numba = types.ModuleType("numba")

    def identity_jit(*args, **kwargs):  # noqa: ANN001, ANN202
        if args and callable(args[0]) and len(args) == 1 and not kwargs:
            return args[0]
        return lambda function: function

    fake_numba.jit = identity_jit
    sys.modules["numba"] = fake_numba
    try:
        spec = importlib.util.spec_from_file_location("phase3f1e_source_tmm", tmm_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"could not import source TMM helper from {tmm_path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        if previous_numba is None:
            sys.modules.pop("numba", None)
        else:
            sys.modules["numba"] = previous_numba


def _interp_source_materials(source_root: Path, wavelength_m: float) -> dict[str, complex]:
    n_ge = np.loadtxt(source_root / "nGe.txt")
    k_ge = np.loadtxt(source_root / "kGe.txt")
    ge = np.interp(wavelength_m, np.arange(300, 1001) * 1e-9, n_ge - 1j * k_ge)

    constants = np.loadtxt(source_root / "constants.csv", delimiter=",", skiprows=1)
    sio2 = np.interp(
        wavelength_m,
        constants[:, 0] * 1e-9,
        constants[:, 1] + 1j * constants[:, 2],
    )
    tio2 = np.interp(
        wavelength_m,
        constants[:, 6] * 1e-9,
        constants[:, 7] + 1j * constants[:, 8],
    )
    return {"Ge": complex(ge), "SiO2": complex(sio2), "TiO2": complex(tio2)}


def _build_cases(source_root: Path) -> list[Phase3F1ECase]:
    source_wavelength_m = 550e-9
    source_materials = _interp_source_materials(source_root, source_wavelength_m)
    return [
        Phase3F1ECase(
            case_id="lossless_te_single_layer",
            description="One lossless film at normal incidence; checks TE layer-matrix convention.",
            rho=0,
            polarization="s",
            angle_deg=0.0,
            wavelength_m=550e-9,
            n_layers=np.array([1.5 + 0j], dtype=np.complex128),
            thicknesses_m=np.array([100e-9], dtype=float),
            n_cover=1.0 + 0j,
            n_substrate=1.45 + 0j,
            source_inputs={"origin": "synthetic closed-form sanity case"},
        ),
        Phase3F1ECase(
            case_id="lossy_tm_double_layer_angle",
            description=(
                "Two-layer lossy/transparent stack at oblique incidence; "
                "checks TM convention."
            ),
            rho=1,
            polarization="p",
            angle_deg=35.0,
            wavelength_m=650e-9,
            n_layers=np.array([2.0 + 0.15j, 1.7 + 0j], dtype=np.complex128),
            thicknesses_m=np.array([20e-9, 80e-9], dtype=float),
            n_cover=1.0 + 0j,
            n_substrate=1.52 + 0j,
            source_inputs={"origin": "synthetic lossy oblique-incidence sanity case"},
        ),
        Phase3F1ECase(
            case_id="source_table_ge_sio2_tio2_tm",
            description=(
                "Three-layer TM stack using structural_color_FROCs Ge, SiO2, "
                "and TiO2 source material tables at 550 nm."
            ),
            rho=1,
            polarization="p",
            angle_deg=25.0,
            wavelength_m=source_wavelength_m,
            n_layers=np.array(
                [
                    source_materials["Ge"],
                    source_materials["SiO2"],
                    source_materials["TiO2"],
                ],
                dtype=np.complex128,
            ),
            thicknesses_m=np.array([15e-9, 50e-9, 75e-9], dtype=float),
            n_cover=1.0 + 0j,
            n_substrate=1.0 + 0j,
            source_inputs={
                "origin": "structural_color_FROCs material tables",
                "material_files": ["nGe.txt", "kGe.txt", "constants.csv"],
                "materials_top_to_bottom": ["Ge", "SiO2", "TiO2"],
            },
        ),
    ]


def _evaluate_case(source_tmm: Any, case: Phase3F1ECase) -> dict[str, Any]:
    source_reflection = float(
        source_tmm.reflect_amp(
            case.rho,
            case.angle_deg,
            case.wavelength_m,
            case.n_layers,
            case.thicknesses_m,
            case.n_cover,
            case.n_substrate,
        )
    )
    source_transmission = float(
        source_tmm.trans_amp(
            case.rho,
            case.angle_deg,
            case.wavelength_m,
            case.n_layers,
            case.thicknesses_m,
            case.n_cover,
            case.n_substrate,
        )
    )
    backend = coh_tmm(
        case.polarization,
        [case.n_cover, *list(case.n_layers), case.n_substrate],
        [np.inf, *list(case.thicknesses_m * 1e9), np.inf],
        np.deg2rad(case.angle_deg),
        case.wavelength_m * 1e9,
    )
    backend_reflection = float(backend["R"])
    backend_transmission = float(backend["T"])
    reflection_abs_delta = abs(source_reflection - backend_reflection)
    transmission_abs_delta = abs(source_transmission - backend_transmission)
    return {
        "case_id": case.case_id,
        "description": case.description,
        "polarization": case.polarization,
        "rho": case.rho,
        "angle_deg": case.angle_deg,
        "wavelength_nm": case.wavelength_m * 1e9,
        "layer_thicknesses_nm": [float(value) for value in case.thicknesses_m * 1e9],
        "n_cover": _complex_record(case.n_cover),
        "n_substrate": _complex_record(case.n_substrate),
        "n_layers": [_complex_record(value) for value in case.n_layers],
        "source_inputs": case.source_inputs,
        "source_reflection": source_reflection,
        "backend_reflection": backend_reflection,
        "reflection_abs_delta": reflection_abs_delta,
        "source_transmission": source_transmission,
        "backend_transmission": backend_transmission,
        "transmission_abs_delta": transmission_abs_delta,
        "pass": (
            reflection_abs_delta <= PARITY_TOLERANCE_ABS
            and transmission_abs_delta <= PARITY_TOLERANCE_ABS
        ),
    }


def _complex_record(value: complex) -> dict[str, float]:
    return {"real": float(np.real(value)), "imag": float(np.imag(value))}


def build_phase3f1e_packet(
    source_root: Path = DEFAULT_SOURCE_ROOT,
    archive_path: Path = DEFAULT_ARCHIVE_PATH,
) -> dict[str, Any]:
    source_tmm = _load_source_tmm_module(source_root)
    cases = [_evaluate_case(source_tmm, case) for case in _build_cases(source_root)]
    max_reflection_delta = max(case["reflection_abs_delta"] for case in cases)
    max_transmission_delta = max(case["transmission_abs_delta"] for case in cases)
    archive_sha256 = _sha256(archive_path) if archive_path.exists() else None
    tmm_helper_sha256 = _sha256(source_root / "TMM_numba.py")
    pass_count = sum(1 for case in cases if case["pass"])
    all_passed = pass_count == len(cases)
    archive_hash_matches = archive_sha256 == PINNED_ARCHIVE_SHA256

    return {
        "phase_id": "Phase 3F.1E",
        "title": "Non-Promoting TMM Code-Regression Fixture Contract",
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "inputs": {
            "source_root": str(source_root),
            "archive_path": str(archive_path),
            "pinned_github_revision": PINNED_GITHUB_REVISION,
            "expected_archive_sha256": PINNED_ARCHIVE_SHA256,
            "observed_archive_sha256": archive_sha256,
            "archive_hash_matches": archive_hash_matches,
            "tmm_helper_sha256": tmm_helper_sha256,
        },
        "claim_boundary": {
            "label": "non_promoting_code_regression_fixture",
            "phase3f2_intake_allowed": False,
            "measured_residual_modeling_performed": False,
            "experimental_validation": False,
            "phase4_candidate": False,
            "claim_status_changed": False,
        },
        "method": {
            "source_oracle": "structural_color_FROCs TMM_numba.py reflect_amp/trans_amp",
            "backend_under_test": "sbyrnes321/tmm coh_tmm through Eternity's current dependency",
            "numba_handling": (
                "TMM_numba.py is loaded with numba.jit stubbed as an identity "
                "decorator so the public source formula runs without local "
                "NumPy/Numba binary compatibility requirements."
            ),
            "tolerance_abs": PARITY_TOLERANCE_ABS,
        },
        "case_results": cases,
        "summary": {
            "case_count": len(cases),
            "pass_count": pass_count,
            "all_cases_passed": all_passed,
            "max_reflection_abs_delta": max_reflection_delta,
            "max_transmission_abs_delta": max_transmission_delta,
        },
        "decision": {
            "status": (
                "phase3f1e_code_regression_fixture_ready"
                if all_passed and archive_hash_matches
                else "phase3f1e_code_regression_fixture_needs_attention"
            ),
            "recommended_next_phase": (
                "Phase 3F.1F - decide whether code-regression coverage is enough "
                "for now or continue public measured-data scouting"
            ),
            "phase3f2_intake_allowed": False,
            "residual_modeling_allowed": False,
        },
    }


def phase3f1e_markdown(packet: dict[str, Any]) -> str:
    rows = [
        "| Case | Polarization | Wavelength (nm) | R Delta | T Delta | Pass? |",
        "| --- | --- | ---: | ---: | ---: | --- |",
    ]
    for case in packet["case_results"]:
        rows.append(
            "| "
            f"`{case['case_id']}` | `{case['polarization']}` | "
            f"{case['wavelength_nm']:.3f} | "
            f"{case['reflection_abs_delta']:.3e} | "
            f"{case['transmission_abs_delta']:.3e} | "
            f"{'yes' if case['pass'] else 'no'} |"
        )

    summary = packet["summary"]
    decision = packet["decision"]
    claim = packet["claim_boundary"]
    inputs = packet["inputs"]
    return "\n".join(
        [
            f"# {packet['phase_id']} - {packet['title']}",
            "",
            "Date: 2026-05-26",
            "",
            "## Decision",
            "",
            f"- Status: `{decision['status']}`",
            f"- Case count: `{summary['case_count']}`",
            f"- Pass count: `{summary['pass_count']}`",
            f"- All cases passed: `{str(summary['all_cases_passed']).lower()}`",
            (
                "- Max reflection absolute delta: "
                f"`{summary['max_reflection_abs_delta']:.17g}`"
            ),
            (
                "- Max transmission absolute delta: "
                f"`{summary['max_transmission_abs_delta']:.17g}`"
            ),
            f"- Phase 3F.2 intake allowed: `{str(decision['phase3f2_intake_allowed']).lower()}`",
            f"- Residual modeling allowed: `{str(decision['residual_modeling_allowed']).lower()}`",
            f"- Recommended next phase: `{decision['recommended_next_phase']}`",
            "",
            "This is a non-promoting code-regression fixture. It compares deterministic",
            "transfer-matrix convention outputs only. It does not compare to measured",
            "spectra, fit parameters, validate a public dataset, or change any claim",
            "label.",
            "",
            "## Pinned Source",
            "",
            f"- Source root: `{inputs['source_root']}`",
            f"- GitHub revision: `{inputs['pinned_github_revision']}`",
            f"- Archive SHA-256: `{inputs['observed_archive_sha256']}`",
            f"- Archive hash matches expected: `{str(inputs['archive_hash_matches']).lower()}`",
            f"- `TMM_numba.py` SHA-256: `{inputs['tmm_helper_sha256']}`",
            "",
            "## Claim Boundary",
            "",
            f"- Label: `{claim['label']}`",
            f"- Experimental validation: `{str(claim['experimental_validation']).lower()}`",
            (
                "- Measured residual modeling performed: "
                f"`{str(claim['measured_residual_modeling_performed']).lower()}`"
            ),
            f"- Phase 4 candidate: `{str(claim['phase4_candidate']).lower()}`",
            "",
            "## Parity Table",
            "",
            *rows,
            "",
            "## Method Note",
            "",
            packet["method"]["numba_handling"],
            "",
        ]
    )


def write_phase3f1e_packet(
    output_dir: Path,
    packet: dict[str, Any],
    report_stem: str = "phase3f1e_code_regression_fixture",
) -> tuple[Path, Path]:
    if report_stem != Path(report_stem).name or not report_stem:
        raise ValueError("report_stem must be a non-empty filename stem")
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{report_stem}.json"
    md_path = output_dir / f"{report_stem}.md"
    json_path.write_text(json.dumps(packet, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(phase3f1e_markdown(packet), encoding="utf-8")
    return json_path, md_path
