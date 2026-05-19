"""Phase 3D.1C Exeter/Bohn package-constant no-fit reconstruction."""

from __future__ import annotations

import cmath
import csv
import json
import math
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
import yaml

SPEED_OF_LIGHT = 299792458.0
EPS_INF = 3.42725287
WP0 = 2.8561e15
GAMMA0 = 2.2379e14
WP2 = -0.3 / 100
GAMMA2 = 0.0
ITO_THICKNESS_NM = 60.0
INCIDENT_INDEX_N = 1.43
ANGLE_OFFSET_DTH_DEG = 3.4
SECOND_INTERFACE_INDEX_OFFSET = -1j * 0.0001
PLOT_FREQUENCY_WINDOW_THZ = (210.0, 260.0)
PLOT_THETA_WINDOW_DEG = (42.5, 50.5)


def _parse_float(value: str) -> float:
    parsed = float(value)
    if not math.isfinite(parsed):
        raise ValueError(f"non-finite numeric value: {value}")
    return parsed


def _load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _load_static_r0(path: Path) -> list[dict[str, float]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError("static R0 table is empty")

    parsed = []
    for row in rows:
        parsed.append(
            {
                "wavelength_nm": _parse_float(row["wavelength_nm"]),
                "frequency_thz": _parse_float(row["frequency_thz"]),
                "theta_air_raw_deg": _parse_float(row["theta_air_raw_deg"]),
                "theta_prism_deg": _parse_float(row["theta_prism_deg"]),
                "observed_r0_reflectance_fraction": _parse_float(
                    row["r0_reflectance_fraction"]
                ),
                "power_norm_std": _parse_float(row["power_norm_std"]),
                "prepump_rows": _parse_float(row["prepump_rows"]),
                "delay_min_ps": _parse_float(row["delay_min_ps"]),
                "delay_max_ps": _parse_float(row["delay_max_ps"]),
            }
        )
    return parsed


def _epsilon_drude(frequency_hz: float) -> complex:
    angular_frequency = frequency_hz * 2 * math.pi
    plasma_frequency = WP0 * (1 + WP2 * 0.0)
    damping = GAMMA0 * (1 + GAMMA2 * 0.0)
    return EPS_INF - plasma_frequency**2 / (
        angular_frequency**2 + 1j * angular_frequency * damping
    )


def _r_p(n1: complex, n2: complex, theta_i: float) -> tuple[complex, complex]:
    theta_t = cmath.asin(n1 / n2 * cmath.sin(theta_i))
    reflection = (n2 * cmath.cos(theta_i) - n1 * cmath.cos(theta_t)) / (
        n2 * cmath.cos(theta_i) + n1 * cmath.cos(theta_t)
    )
    return theta_t, reflection


def _t_p(n1: complex, n2: complex, theta_i: float) -> tuple[complex, complex]:
    theta_t = cmath.asin(n1 / n2 * cmath.sin(theta_i))
    transmission = 2 * n1 * cmath.cos(theta_i) / (
        n2 * cmath.cos(theta_i) + n1 * cmath.cos(theta_t)
    )
    return theta_t, transmission


def _package_static_reflectance_p(theta_prism_deg: float, frequency_thz: float) -> float:
    n1 = complex(INCIDENT_INDEX_N)
    n2 = cmath.sqrt(_epsilon_drude(frequency_thz * 1e12))
    n3 = 1.0 + 0j
    theta = math.radians(theta_prism_deg)
    thickness_m = ITO_THICKNESS_NM * 1e-9

    theta2, r12 = _r_p(n1, n2, theta)
    theta3, r23 = _r_p(n2 + SECOND_INTERFACE_INDEX_OFFSET, n3, theta2)
    _, t12 = _t_p(n1, n2, theta)
    _, t23 = _t_p(n2 + SECOND_INTERFACE_INDEX_OFFSET, n3, theta2)

    k2 = n2 * 2 * math.pi * frequency_thz * 1e12 / SPEED_OF_LIGHT * cmath.cos(theta2)
    round_trip = cmath.exp(2j * k2 * thickness_m)
    amplitude_reflection = (r12 + r23 * round_trip) / (1 + r12 * r23 * round_trip)
    reflectance = abs(amplitude_reflection) ** 2

    amplitude_transmission = (
        t12
        * t23
        * cmath.exp(1j * k2 * thickness_m)
        / (1 + r12 * r23 * round_trip)
    )
    _transmittance = abs(amplitude_transmission**2) * (
        (n3 * cmath.cos(theta3)).real / (n1 * cmath.cos(theta)).real
    )
    return float(reflectance)


def _comparison_rows(static_r0_rows: list[dict[str, float]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in static_r0_rows:
        prediction = _package_static_reflectance_p(
            row["theta_prism_deg"],
            row["frequency_thz"],
        )
        observed = row["observed_r0_reflectance_fraction"]
        frequency_thz = row["frequency_thz"]
        theta_prism_deg = row["theta_prism_deg"]
        in_plotted_window = (
            PLOT_FREQUENCY_WINDOW_THZ[0] <= frequency_thz <= PLOT_FREQUENCY_WINDOW_THZ[1]
            and PLOT_THETA_WINDOW_DEG[0] <= theta_prism_deg <= PLOT_THETA_WINDOW_DEG[1]
        )
        rows.append(
            {
                **row,
                "package_static_prediction_fraction": prediction,
                "residual_prediction_minus_observed": prediction - observed,
                "absolute_residual": abs(prediction - observed),
                "in_figure2_plotted_window": in_plotted_window,
            }
        )
    return rows


def _minmax(values: np.ndarray) -> np.ndarray:
    low = float(np.min(values))
    high = float(np.max(values))
    if math.isclose(low, high):
        return np.zeros_like(values)
    return (values - low) / (high - low)


def _pearson(left: np.ndarray, right: np.ndarray) -> float | None:
    if left.size < 2 or left.size != right.size:
        return None
    left_centered = left - float(np.mean(left))
    right_centered = right - float(np.mean(right))
    denominator = float(np.linalg.norm(left_centered) * np.linalg.norm(right_centered))
    if math.isclose(denominator, 0.0):
        return None
    return float(np.dot(left_centered, right_centered) / denominator)


def _metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {"points": 0}
    observed = np.asarray([row["observed_r0_reflectance_fraction"] for row in rows])
    prediction = np.asarray([row["package_static_prediction_fraction"] for row in rows])
    residual = prediction - observed
    observed_span = float(np.max(observed) - np.min(observed))
    return {
        "points": len(rows),
        "wavelength_nm": [
            float(min(row["wavelength_nm"] for row in rows)),
            float(max(row["wavelength_nm"] for row in rows)),
        ],
        "frequency_thz": [
            float(min(row["frequency_thz"] for row in rows)),
            float(max(row["frequency_thz"] for row in rows)),
        ],
        "theta_prism_deg": [
            float(min(row["theta_prism_deg"] for row in rows)),
            float(max(row["theta_prism_deg"] for row in rows)),
        ],
        "observed_range": [float(np.min(observed)), float(np.max(observed))],
        "prediction_range": [float(np.min(prediction)), float(np.max(prediction))],
        "mean_absolute_error": float(np.mean(np.abs(residual))),
        "root_mean_square_error": float(np.sqrt(np.mean(residual**2))),
        "max_absolute_residual": float(np.max(np.abs(residual))),
        "bias_prediction_minus_observed": float(np.mean(residual)),
        "shape_correlation": _pearson(prediction, observed),
        "shape_correlation_minmax": _pearson(_minmax(prediction), _minmax(observed)),
        "normalized_rmse_over_observed_span": (
            float(np.sqrt(np.mean(residual**2)) / observed_span)
            if not math.isclose(observed_span, 0.0)
            else None
        ),
    }


def _validate_split_lock(split_lock: dict[str, Any]) -> None:
    if split_lock.get("phase_id") != "Phase 3D.1B":
        raise ValueError("Phase 3D.1C requires a Phase 3D.1B split lock")
    if split_lock.get("fitting_may_access_holdout_y") is not False:
        raise ValueError("Phase 3D.1C requires fitting_may_access_holdout_y=false")
    locked = split_lock.get("locked_nuisance_values", {})
    required = {
        "ito_thickness_nm": ITO_THICKNESS_NM,
        "incident_index_n": INCIDENT_INDEX_N,
        "angle_offset_dth_deg": ANGLE_OFFSET_DTH_DEG,
    }
    for name, expected in required.items():
        if not math.isclose(float(locked.get(name, float("nan"))), expected):
            raise ValueError(f"split lock {name} does not match package constant {expected}")


def build_phase3d1c_packet(static_r0_path: Path, split_lock_path: Path) -> dict[str, Any]:
    split_lock = _load_yaml(split_lock_path)
    _validate_split_lock(split_lock)
    table = _comparison_rows(_load_static_r0(static_r0_path))
    plotted_rows = [row for row in table if row["in_figure2_plotted_window"]]

    return {
        "phase_id": "Phase 3D.1C",
        "title": "Exeter/Bohn Package-Constant No-Fit Model Reconstruction",
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "inputs": {
            "static_r0_path": str(static_r0_path),
            "split_lock_path": str(split_lock_path),
        },
        "decision": {
            "status": "no_fit_reconstruction_completed_nonpromoting",
            "can_feed_serious_core": False,
            "can_promote_calibrated_linear_evidence": False,
            "phase4_ready": False,
            "claim_status_ceiling": "weak_within_dataset_holdout",
            "result_interpretation": (
                "The locked package model reconstructs the Figure 2 static pattern "
                "well in shape but not at calibrated-evidence authority. Numeric "
                "pass/fail thresholds were not predeclared before residual inspection, "
                "and the holdout is still within the source package's nonlinear "
                "experiment lane."
            ),
            "recommended_next_phase": "Phase 3D.2 - Saha TiN/AZO source-data intake",
        },
        "locked_package_constants": {
            "epsilon_model": "Drude constants from Figure2/JUPYTER_Figure2a,b,c.ipynb",
            "eps_inf": EPS_INF,
            "wp0_rad_s": WP0,
            "gamma0_rad_s": GAMMA0,
            "wp2_per_gw_cm2": WP2,
            "gamma2_per_gw_cm2": GAMMA2,
            "ito_thickness_nm": ITO_THICKNESS_NM,
            "incident_index_n": INCIDENT_INDEX_N,
            "angle_offset_dth_deg": ANGLE_OFFSET_DTH_DEG,
            "polarization": "p",
            "intensity_gw_cm2": 0.0,
            "second_interface_index_offset": str(SECOND_INTERFACE_INDEX_OFFSET),
        },
        "metrics": {
            "all_locked_points": _metrics(table),
            "figure2_plotted_window": _metrics(plotted_rows),
        },
        "window_definition": {
            "basis": "Figure 2 notebook contour axes",
            "frequency_thz": list(PLOT_FREQUENCY_WINDOW_THZ),
            "theta_prism_deg": list(PLOT_THETA_WINDOW_DEG),
        },
        "leakage_guard": {
            "holdout_y_used_for_fitting": False,
            "residuals_seen_before_numeric_thresholds": True,
            "promotion_for_this_run": "forbidden",
            "forbidden_after_residuals": split_lock["forbidden_after_residuals"],
        },
        "interpretation_boundary": (
            "This phase is a no-fit reconstruction diagnostic. It may preserve a "
            "weak-within-dataset holdout result, but it cannot become calibrated "
            "linear evidence without an independent promotion review that was not "
            "contaminated by these inspected residuals."
        ),
        "table": table,
    }


def comparison_table_csv(packet: dict[str, Any]) -> str:
    fieldnames = [
        "wavelength_nm",
        "frequency_thz",
        "theta_air_raw_deg",
        "theta_prism_deg",
        "observed_r0_reflectance_fraction",
        "package_static_prediction_fraction",
        "residual_prediction_minus_observed",
        "absolute_residual",
        "power_norm_std",
        "prepump_rows",
        "delay_min_ps",
        "delay_max_ps",
        "in_figure2_plotted_window",
    ]
    output = []
    output.append(",".join(fieldnames))
    for row in packet["table"]:
        output.append(
            ",".join(
                [
                    f"{row['wavelength_nm']:.12g}",
                    f"{row['frequency_thz']:.12g}",
                    f"{row['theta_air_raw_deg']:.12g}",
                    f"{row['theta_prism_deg']:.12g}",
                    f"{row['observed_r0_reflectance_fraction']:.12g}",
                    f"{row['package_static_prediction_fraction']:.12g}",
                    f"{row['residual_prediction_minus_observed']:.12g}",
                    f"{row['absolute_residual']:.12g}",
                    f"{row['power_norm_std']:.12g}",
                    f"{row['prepump_rows']:.12g}",
                    f"{row['delay_min_ps']:.12g}",
                    f"{row['delay_max_ps']:.12g}",
                    str(row["in_figure2_plotted_window"]).lower(),
                ]
            )
        )
    return "\n".join(output) + "\n"


def phase3d1c_markdown(packet: dict[str, Any]) -> str:
    decision = packet["decision"]
    all_metrics = packet["metrics"]["all_locked_points"]
    plot_metrics = packet["metrics"]["figure2_plotted_window"]
    return "\n".join(
        [
            "# Phase 3D.1C - Exeter/Bohn No-Fit Reconstruction",
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
            "## Figure 2 Plotted-Window Metrics",
            "",
            f"- Points: `{plot_metrics['points']}`",
            f"- RMSE: `{plot_metrics['root_mean_square_error']}`",
            f"- MAE: `{plot_metrics['mean_absolute_error']}`",
            f"- Max absolute residual: `{plot_metrics['max_absolute_residual']}`",
            f"- Bias prediction-observed: `{plot_metrics['bias_prediction_minus_observed']}`",
            f"- Shape correlation: `{plot_metrics['shape_correlation']}`",
            "",
            "## All Locked-Point Metrics",
            "",
            f"- Points: `{all_metrics['points']}`",
            f"- RMSE: `{all_metrics['root_mean_square_error']}`",
            f"- MAE: `{all_metrics['mean_absolute_error']}`",
            f"- Max absolute residual: `{all_metrics['max_absolute_residual']}`",
            f"- Bias prediction-observed: `{all_metrics['bias_prediction_minus_observed']}`",
            f"- Shape correlation: `{all_metrics['shape_correlation']}`",
            "",
            "## Boundary",
            "",
            packet["interpretation_boundary"],
            "",
        ]
    )


def write_phase3d1c_packet(output_dir: Path, packet: dict[str, Any]) -> tuple[Path, Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase3d1c_exeter_bohn_no_fit_reconstruction.json"
    md_path = output_dir / "phase3d1c_exeter_bohn_no_fit_reconstruction.md"
    csv_path = output_dir / "phase3d1c_exeter_bohn_no_fit_comparison.csv"
    json_packet = dict(packet)
    json_packet.pop("table", None)
    json_path.write_text(json.dumps(json_packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(phase3d1c_markdown(packet), encoding="utf-8")
    csv_path.write_text(comparison_table_csv(packet), encoding="utf-8")
    return json_path, md_path, csv_path
