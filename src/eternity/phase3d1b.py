"""Phase 3D.1B Exeter/Bohn ITO no-fit extraction utilities."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import zipfile
from collections import defaultdict
from datetime import UTC, datetime
from io import StringIO
from pathlib import Path
from typing import Any

import numpy as np
import yaml

FIG1_EPSILON_MEMBER = "Figure1/DATA_ellipsometer_fit.txt"
FIG2_TIR_MEMBER = "Figure2/DATA/DATA_Figure2a,b,c_calibration_probe_TIR.csv"
FIG2_EXPERIMENT_MEMBER = "Figure2/DATA/DATA_Figure2a,b,c_experiment.csv"


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _artifact_metadata(path: Path, source_member: str, role: str) -> dict[str, Any]:
    return {
        "path": str(path),
        "role": role,
        "bytes": path.stat().st_size,
        "sha256": _sha256_file(path),
        "source_member": source_member,
    }


def _parse_float(value: str) -> float:
    parsed = float(value)
    if not math.isfinite(parsed):
        raise ValueError(f"non-finite numeric value: {value}")
    return parsed


def _read_csv_member(archive: zipfile.ZipFile, member: str) -> list[dict[str, str]]:
    text = archive.read(member).decode("utf-8-sig").replace("\r\n", "\n")
    return list(csv.DictReader(StringIO(text)))


def _parse_fig1_epsilon(archive: zipfile.ZipFile) -> list[dict[str, float]]:
    text = archive.read(FIG1_EPSILON_MEMBER).decode("utf-8-sig").replace("\r\n", "\n")
    rows: list[dict[str, float]] = []
    for line in text.splitlines()[2:]:
        fields = line.split()
        if len(fields) < 5:
            continue
        rows.append(
            {
                "wavelength_nm": _parse_float(fields[0]),
                "epsilon_real": _parse_float(fields[1]),
                "epsilon_imag": _parse_float(fields[2]),
                "epsilon_real_ref": _parse_float(fields[3]),
                "epsilon_imag_ref": _parse_float(fields[4]),
            }
        )
    _validate_increasing([row["wavelength_nm"] for row in rows], FIG1_EPSILON_MEMBER)
    return rows


def _validate_increasing(values: list[float], label: str) -> None:
    if len(values) < 2:
        raise ValueError(f"{label} must contain at least two rows")
    if any(right <= left for left, right in zip(values, values[1:], strict=False)):
        raise ValueError(f"{label} axis must be strictly increasing")


def _enz_crossings(rows: list[dict[str, float]]) -> list[float]:
    crossings: list[float] = []
    for left, right in zip(rows, rows[1:], strict=False):
        e_left = left["epsilon_real"]
        e_right = right["epsilon_real"]
        if e_left == 0:
            crossings.append(round(left["wavelength_nm"], 6))
        elif e_left * e_right < 0:
            fraction = -e_left / (e_right - e_left)
            wavelength = left["wavelength_nm"] + fraction * (
                right["wavelength_nm"] - left["wavelength_nm"]
            )
            crossings.append(round(wavelength, 6))
    return crossings


def _write_epsilon_csv(path: Path, rows: list[dict[str, float]]) -> None:
    output = StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "wavelength_nm",
            "epsilon_real",
            "epsilon_imag",
            "epsilon_real_ref",
            "epsilon_imag_ref",
        ],
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(rows)
    _write_text(path, output.getvalue())


def _tir_reference_rows(raw_rows: list[dict[str, str]]) -> list[dict[str, float]]:
    grouped: dict[tuple[float, float], list[float]] = defaultdict(list)
    for row in raw_rows:
        theta = _parse_float(row["theta"])
        if theta < 45:
            continue
        wavelength = _parse_float(row["wavelength_2"])
        power_s = _parse_float(row["power_s"])
        power_r_probe = _parse_float(row["power_r_probe"])
        grouped[(wavelength, theta)].append(power_s / power_r_probe)

    by_wavelength: dict[float, list[float]] = defaultdict(list)
    theta_values_by_wavelength: dict[float, set[float]] = defaultdict(set)
    for (wavelength, theta), ratios in grouped.items():
        by_wavelength[wavelength].append(float(np.mean(ratios)))
        theta_values_by_wavelength[wavelength].add(theta)

    rows: list[dict[str, float]] = []
    for wavelength in sorted(by_wavelength):
        theta_values = sorted(theta_values_by_wavelength[wavelength])
        rows.append(
            {
                "wavelength_nm": wavelength,
                "tir_reference_mean": float(np.mean(by_wavelength[wavelength])),
                "tir_reference_theta_count": float(len(theta_values)),
                "theta_min_raw_deg": theta_values[0],
                "theta_max_raw_deg": theta_values[-1],
            }
        )
    _validate_increasing([row["wavelength_nm"] for row in rows], FIG2_TIR_MEMBER)
    return rows


def _write_tir_reference_csv(path: Path, rows: list[dict[str, float]]) -> None:
    output = StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "wavelength_nm",
            "tir_reference_mean",
            "tir_reference_theta_count",
            "theta_min_raw_deg",
            "theta_max_raw_deg",
        ],
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(rows)
    _write_text(path, output.getvalue())


def _not_a_knot_cubic_interpolator(x: np.ndarray, y: np.ndarray):
    """Return a SciPy interp1d(kind='cubic')-equivalent not-a-knot spline for 1D data."""

    if x.ndim != 1 or y.ndim != 1 or x.size != y.size:
        raise ValueError("cubic interpolation requires same-length 1D arrays")
    if x.size < 4:
        raise ValueError("cubic interpolation requires at least four points")
    if np.any(np.diff(x) <= 0):
        raise ValueError("cubic interpolation x-axis must be strictly increasing")

    count = x.size
    h = np.diff(x)
    matrix = np.zeros((count, count), dtype=float)
    rhs = np.zeros(count, dtype=float)

    matrix[0, 0] = -h[1]
    matrix[0, 1] = h[0] + h[1]
    matrix[0, 2] = -h[0]
    for index in range(1, count - 1):
        matrix[index, index - 1] = h[index - 1]
        matrix[index, index] = 2 * (h[index - 1] + h[index])
        matrix[index, index + 1] = h[index]
        rhs[index] = 6 * (
            (y[index + 1] - y[index]) / h[index]
            - (y[index] - y[index - 1]) / h[index - 1]
        )
    matrix[-1, -3] = -h[-1]
    matrix[-1, -2] = h[-2] + h[-1]
    matrix[-1, -1] = -h[-2]
    second_derivatives = np.linalg.solve(matrix, rhs)

    def evaluate(query: float) -> float:
        if query < x[0] or query > x[-1]:
            raise ValueError("cubic interpolation query outside reference range")
        interval = int(np.searchsorted(x, query) - 1)
        interval = max(0, min(interval, count - 2))
        left = x[interval]
        right = x[interval + 1]
        width = right - left
        left_weight = (right - query) / width
        right_weight = (query - left) / width
        value = (
            second_derivatives[interval] * (right - query) ** 3 / (6 * width)
            + second_derivatives[interval + 1] * (query - left) ** 3 / (6 * width)
            + (y[interval] - second_derivatives[interval] * width**2 / 6) * left_weight
            + (y[interval + 1] - second_derivatives[interval + 1] * width**2 / 6)
            * right_weight
        )
        return float(value)

    return evaluate


def _prism_angle_deg(theta_air_deg: float, prism_angle_deg: float = 45.0) -> float:
    return prism_angle_deg + math.degrees(
        math.asin(math.sin(math.radians(theta_air_deg - prism_angle_deg)) / 1.5)
    )


def _static_r0_rows(
    raw_rows: list[dict[str, str]],
    tir_rows: list[dict[str, float]],
) -> list[dict[str, float]]:
    x = np.asarray([row["wavelength_nm"] for row in tir_rows], dtype=float)
    y = np.asarray([row["tir_reference_mean"] for row in tir_rows], dtype=float)
    tir_reference = _not_a_knot_cubic_interpolator(x, y)

    grouped: dict[tuple[float, float, float], list[dict[str, float]]] = defaultdict(list)
    for row in raw_rows:
        wavelength_1 = _parse_float(row["wavelength_1"])
        wavelength_2 = _parse_float(row["wavelength_2"])
        if wavelength_1 != wavelength_2:
            continue
        delay = _parse_float(row["delay"])
        if delay > -0.4:
            continue
        theta_raw = _parse_float(row["theta"])
        theta_prism = _prism_angle_deg(theta_raw)
        power_norm = (
            _parse_float(row["power_s"])
            / _parse_float(row["power_r_probe"])
            / tir_reference(wavelength_2)
        )
        grouped[(wavelength_2, theta_raw, theta_prism)].append(
            {
                "power_norm": power_norm,
                "delay": delay,
            }
        )

    rows: list[dict[str, float]] = []
    speed_of_light = 299792458.0
    for wavelength, theta_raw, theta_prism in sorted(grouped):
        values = grouped[(wavelength, theta_raw, theta_prism)]
        power_norm_values = np.asarray([value["power_norm"] for value in values], dtype=float)
        delays = [value["delay"] for value in values]
        rows.append(
            {
                "wavelength_nm": wavelength,
                "frequency_thz": speed_of_light / (wavelength * 1e-9) / 1e12,
                "theta_air_raw_deg": theta_raw,
                "theta_prism_deg": theta_prism,
                "r0_reflectance_fraction": float(np.mean(power_norm_values)),
                "power_norm_std": float(np.std(power_norm_values, ddof=0)),
                "prepump_rows": float(len(values)),
                "delay_min_ps": min(delays),
                "delay_max_ps": max(delays),
            }
        )
    if not rows:
        raise ValueError("Figure 2 experiment produced no static pre-pump R0 rows")
    return rows


def _write_static_r0_csv(path: Path, rows: list[dict[str, float]]) -> None:
    output = StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "wavelength_nm",
            "frequency_thz",
            "theta_air_raw_deg",
            "theta_prism_deg",
            "r0_reflectance_fraction",
            "power_norm_std",
            "prepump_rows",
            "delay_min_ps",
            "delay_max_ps",
        ],
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(rows)
    _write_text(path, output.getvalue())


def _range(values: list[float]) -> list[float]:
    return [min(values), max(values)]


def _split_lock(artifacts: dict[str, dict[str, Any]]) -> dict[str, Any]:
    return {
        "phase_id": "Phase 3D.1B",
        "split_id": "public_exeter_bohn_ito_2021_fig1_fig2_no_fit_static_r0",
        "created_at": "2026-05-19",
        "claim_status_ceiling": "weak_within_dataset_holdout",
        "calibration": {
            "material_input": artifacts["fig1_epsilon"]["path"],
            "source_member": FIG1_EPSILON_MEMBER,
            "allowed_inputs": [
                "tabulated Figure 1 epsilon columns",
                "package Drude constants only if explicitly selected before residuals",
            ],
        },
        "holdout": {
            "static_r0_surface": artifacts["fig2_static_r0"]["path"],
            "tir_reference": artifacts["fig2_tir_reference"]["path"],
            "source_members": [FIG2_TIR_MEMBER, FIG2_EXPERIMENT_MEMBER],
            "selection": "Figure 2 rows with wavelength_1 == wavelength_2 and delay <= -0.4 ps",
        },
        "locked_nuisance_values": {
            "ito_thickness_nm": 60.0,
            "incident_index_n": 1.43,
            "angle_offset_dth_deg": 3.4,
            "tir_reference_interpolation": (
                "not_a_knot_cubic_spline_matching_scipy_interp1d_kind_cubic"
            ),
        },
        "forbidden_after_residuals": [
            "material parameter refit",
            "thickness tuning",
            "incident-index tuning",
            "angle-offset tuning",
            "vertical scaling",
            "wavelength shifting",
            "threshold loosening",
            "using Figure 3/4 to rescue Figure 2",
        ],
        "fitting_may_access_holdout_y": False,
        "ai_playground_may_access_holdout_y_before_fit": False,
    }


def build_phase3d1b_packet_from_paths(zip_path: Path, raw_output_dir: Path) -> dict[str, Any]:
    if not zip_path.exists():
        raise FileNotFoundError(zip_path)

    raw_output_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as archive:
        epsilon_rows = _parse_fig1_epsilon(archive)
        tir_rows = _tir_reference_rows(_read_csv_member(archive, FIG2_TIR_MEMBER))
        static_r0_rows = _static_r0_rows(
            _read_csv_member(archive, FIG2_EXPERIMENT_MEMBER),
            tir_rows,
        )

    epsilon_path = raw_output_dir / "exeter_bohn_ito_fig1_epsilon.csv"
    tir_reference_path = raw_output_dir / "exeter_bohn_fig2_tir_reference.csv"
    static_r0_path = raw_output_dir / "exeter_bohn_fig2_static_r0.csv"
    _write_epsilon_csv(epsilon_path, epsilon_rows)
    _write_tir_reference_csv(tir_reference_path, tir_rows)
    _write_static_r0_csv(static_r0_path, static_r0_rows)

    artifacts = {
        "fig1_epsilon": _artifact_metadata(
            epsilon_path,
            FIG1_EPSILON_MEMBER,
            "calibration_material_input",
        ),
        "fig2_tir_reference": _artifact_metadata(
            tir_reference_path,
            FIG2_TIR_MEMBER,
            "holdout_normalization_reference",
        ),
        "fig2_static_r0": _artifact_metadata(
            static_r0_path,
            FIG2_EXPERIMENT_MEMBER,
            "holdout_static_prepump_reflection_surface",
        ),
    }
    r0_values = [row["r0_reflectance_fraction"] for row in static_r0_rows]
    wavelengths = [row["wavelength_nm"] for row in static_r0_rows]
    theta_prism_values = [row["theta_prism_deg"] for row in static_r0_rows]
    epsilon_real = [row["epsilon_real"] for row in epsilon_rows]
    epsilon_imag = [row["epsilon_imag"] for row in epsilon_rows]
    split_lock = _split_lock(artifacts)

    return {
        "phase_id": "Phase 3D.1B",
        "title": "Exeter/Bohn No-Fit Static R0 Extraction and Split Lock",
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "inputs": {
            "zip_path": str(zip_path),
            "raw_output_dir": str(raw_output_dir),
        },
        "decision": {
            "status": "static_r0_extracted_split_locked_no_residuals",
            "can_feed_serious_core": False,
            "can_promote_calibrated_linear_evidence": False,
            "phase4_ready": False,
            "claim_status_ceiling": "weak_within_dataset_holdout",
            "recommended_next_phase": (
                "Phase 3D.1C - Exeter/Bohn package-constant no-fit model reconstruction"
            ),
        },
        "artifacts": artifacts,
        "calibration_summary": {
            "rows": len(epsilon_rows),
            "wavelength_nm": _range([row["wavelength_nm"] for row in epsilon_rows]),
            "epsilon_real": _range(epsilon_real),
            "epsilon_imag": _range(epsilon_imag),
            "enz_wavelengths_nm": _enz_crossings(epsilon_rows),
            "passivity_check": "pass" if min(epsilon_imag) > 0 else "fail",
        },
        "holdout_summary": {
            "tir_reference_rows": len(tir_rows),
            "static_r0_rows": len(static_r0_rows),
            "wavelength_nm": _range(wavelengths),
            "theta_prism_deg": _range(theta_prism_values),
            "r0_reflectance_fraction": _range(r0_values),
            "prepump_rows_per_point": sorted(
                {int(row["prepump_rows"]) for row in static_r0_rows}
            ),
            "r0_grid": {
                "wavelength_count": len({row["wavelength_nm"] for row in static_r0_rows}),
                "theta_count": len({row["theta_prism_deg"] for row in static_r0_rows}),
            },
        },
        "split_lock": split_lock,
        "allowed_next": [
            (
                "Use the locked Figure 1/Figure 2 artifacts for a package-constant "
                "no-fit reconstruction."
            ),
            (
                "Compare against Figure 2 static R0 only after model constants and "
                "thresholds are fixed."
            ),
            "Keep Figure 3/4 auxiliary unless Figure 2 is explicitly parked.",
        ],
        "forbidden_next": split_lock["forbidden_after_residuals"],
    }


def phase3d1b_markdown(packet: dict[str, Any]) -> str:
    decision = packet["decision"]
    calibration = packet["calibration_summary"]
    holdout = packet["holdout_summary"]
    lines = [
        "# Phase 3D.1B - Exeter/Bohn No-Fit Static R0 Extraction",
        "",
        "## Decision",
        "",
        f"- Status: `{decision['status']}`",
        f"- Can feed serious core: `{decision['can_feed_serious_core']}`",
        (
            "- Can promote calibrated evidence: "
            f"`{decision['can_promote_calibrated_linear_evidence']}`"
        ),
        f"- Phase 4 ready: `{decision['phase4_ready']}`",
        f"- Claim-status ceiling: `{decision['claim_status_ceiling']}`",
        f"- Recommended next phase: `{decision['recommended_next_phase']}`",
        "",
        "## Canonical Artifacts",
        "",
    ]
    for artifact_id, artifact in packet["artifacts"].items():
        lines.extend(
            [
                f"- `{artifact_id}`: `{artifact['path']}`",
                f"  - SHA-256: `{artifact['sha256']}`",
                f"  - Source member: `{artifact['source_member']}`",
            ]
        )
    lines.extend(
        [
            "",
            "## Calibration Summary",
            "",
            f"- Rows: `{calibration['rows']}`",
            (
                f"- Wavelength range: `{calibration['wavelength_nm'][0]}`-"
                f"`{calibration['wavelength_nm'][1]}` nm"
            ),
            (
                f"- Re(epsilon) range: `{calibration['epsilon_real'][0]}`-"
                f"`{calibration['epsilon_real'][1]}`"
            ),
            (
                f"- Im(epsilon) range: `{calibration['epsilon_imag'][0]}`-"
                f"`{calibration['epsilon_imag'][1]}`"
            ),
            f"- ENZ crossings: `{calibration['enz_wavelengths_nm']}` nm",
            f"- Passivity check: `{calibration['passivity_check']}`",
            "",
            "## Holdout Summary",
            "",
            f"- TIR reference rows: `{holdout['tir_reference_rows']}`",
            f"- Static R0 rows: `{holdout['static_r0_rows']}`",
            (
                f"- Wavelength range: `{holdout['wavelength_nm'][0]}`-"
                f"`{holdout['wavelength_nm'][1]}` nm"
            ),
            (
                f"- Prism-angle range: `{holdout['theta_prism_deg'][0]}`-"
                f"`{holdout['theta_prism_deg'][1]}` deg"
            ),
            (
                "- R0 reflectance fraction range: "
                f"`{holdout['r0_reflectance_fraction'][0]}`-`{holdout['r0_reflectance_fraction'][1]}`"
            ),
            f"- Prepump rows per point: `{holdout['prepump_rows_per_point']}`",
            "",
            "## Split Lock",
            "",
            "- Calibration is Figure 1 epsilon.",
            "- Holdout is Figure 2 TIR-normalized static pre-pump `R0`.",
            "- Figure 2 reflection rows are forbidden for fitting.",
            "- No residuals were run in this phase.",
            "",
            "## Forbidden After Residuals",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in packet["forbidden_next"])
    lines.append("")
    return "\n".join(lines)


def write_phase3d1b_packet(output_dir: Path, packet: dict[str, Any]) -> tuple[Path, Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase3d1b_exeter_bohn_static_r0_extraction.json"
    md_path = output_dir / "phase3d1b_exeter_bohn_static_r0_extraction.md"
    split_path = output_dir / "phase3d1b_exeter_bohn_split_lock.yaml"
    json_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(phase3d1b_markdown(packet), encoding="utf-8")
    split_path.write_text(
        yaml.safe_dump(packet["split_lock"], sort_keys=False),
        encoding="utf-8",
    )
    return json_path, md_path, split_path
