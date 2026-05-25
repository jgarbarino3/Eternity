"""Phase 3E.5 Saha no-claim stack-assumption sensitivity fixture."""

from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
from tmm import coh_tmm

from eternity.materials import refractive_index_from_epsilon
from eternity.optical_data import interpolate_epsilon, load_epsilon_table

DEFAULT_RAW_DIR = Path("lab_data/raw/public_saha_tin_azo_2023")
DEFAULT_PHASE3E3B_GATE_PATH = Path("docs/phase3e3b_saha_stack_model_gate.json")
MEASURED_PATH = DEFAULT_RAW_DIR / "saha_fig2b_measured_reflectance_canonical.csv"
SOURCE_SIMULATED_PATH = DEFAULT_RAW_DIR / "saha_fig2b_source_simulated_reflectance_canonical.csv"
TIN_EPSILON_PATH = DEFAULT_RAW_DIR / "saha_fig2cd_tin_epsilon_canonical.csv"
AZO_EPSILON_PATH = DEFAULT_RAW_DIR / "saha_fig2cd_azo_epsilon_canonical.csv"

AZO_THICKNESS_NM = 250.0
TIN_THICKNESS_NM = 130.0
INCIDENCE_ANGLE_DEG = 50.0


@dataclass(frozen=True)
class VariantSpec:
    variant_id: str
    substrate_model: str
    interface_model: str
    backside_model: str


def _read_channels(path: Path) -> dict[str, np.ndarray]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"{path} is empty")
    columns = rows[0].keys()
    parsed: dict[str, np.ndarray] = {}
    for column in columns:
        parsed[column] = np.asarray([float(row[column]) for row in rows], dtype=float)
    return parsed


def _require_same_axis(*axes: np.ndarray) -> None:
    reference = axes[0]
    for axis in axes[1:]:
        if axis.shape != reference.shape or not np.allclose(axis, reference):
            raise ValueError("Saha canonical artifacts do not share the expected wavelength axis")


def _pearson_minmax(left_values: np.ndarray, right_values: np.ndarray) -> float | None:
    def norm(values: np.ndarray) -> np.ndarray:
        low = float(np.min(values))
        high = float(np.max(values))
        if math.isclose(low, high):
            return np.zeros_like(values)
        return (values - low) / (high - low)

    left = norm(left_values)
    right = norm(right_values)
    left_centered = left - float(np.mean(left))
    right_centered = right - float(np.mean(right))
    denominator = float(np.linalg.norm(left_centered) * np.linalg.norm(right_centered))
    if math.isclose(denominator, 0.0):
        return None
    return float(np.dot(left_centered, right_centered) / denominator)


def _comparison_metrics(
    wavelengths_nm: np.ndarray,
    prediction: np.ndarray,
    target: np.ndarray,
) -> dict[str, Any]:
    residual = prediction - target
    max_index = int(np.argmax(np.abs(residual)))
    return {
        "points": int(wavelengths_nm.size),
        "wavelength_window_nm": [float(wavelengths_nm.min()), float(wavelengths_nm.max())],
        "mean_absolute_error": float(np.mean(np.abs(residual))),
        "root_mean_square_error": float(np.sqrt(np.mean(residual**2))),
        "max_absolute_residual": float(np.max(np.abs(residual))),
        "max_absolute_residual_wavelength_nm": float(wavelengths_nm[max_index]),
        "shape_correlation_minmax": _pearson_minmax(prediction, target),
        "prediction_range": [float(np.min(prediction)), float(np.max(prediction))],
        "target_range": [float(np.min(target)), float(np.max(target))],
    }


def _substrate_index(model: str, wavelengths_nm: np.ndarray) -> np.ndarray:
    if model == "si_lossless_fixed_n3p5":
        return np.full(wavelengths_nm.shape, 3.5 + 0j, dtype=complex)
    if model == "si_weak_absorbing_fixed_n3p7_k0p02":
        return np.full(wavelengths_nm.shape, 3.7 + 0.02j, dtype=complex)
    if model == "si_synthetic_blue_absorbing_dispersion":
        axis = np.asarray([300.0, 400.0, 500.0, 700.0, 1000.0, 2000.0])
        n_values = np.asarray([5.6, 5.35, 4.25, 3.75, 3.55, 3.45])
        k_values = np.asarray([2.4, 0.42, 0.08, 0.02, 0.0, 0.0])
        return np.interp(wavelengths_nm, axis, n_values) + 1j * np.interp(
            wavelengths_nm, axis, k_values
        )
    raise ValueError(f"unknown substrate model: {model}")


def _simulate_front_stack(
    wavelengths_nm: np.ndarray,
    azo_epsilon: np.ndarray,
    tin_epsilon: np.ndarray,
    substrate_index: np.ndarray,
    *,
    polarization: str,
    interface_model: str,
) -> tuple[np.ndarray, np.ndarray]:
    azo_index = refractive_index_from_epsilon(azo_epsilon)
    tin_index = refractive_index_from_epsilon(tin_epsilon)
    theta_rad = math.radians(INCIDENCE_ANGLE_DEG)
    reflection = np.empty_like(wavelengths_nm, dtype=float)
    transmission = np.empty_like(wavelengths_nm, dtype=float)
    include_sio2 = interface_model == "sio2_2nm_between_tin_and_si"
    if interface_model not in {"none", "sio2_2nm_between_tin_and_si"}:
        raise ValueError(f"unknown interface model: {interface_model}")

    for index, wavelength_nm in enumerate(wavelengths_nm):
        n_list = [1.0 + 0j, azo_index[index], tin_index[index]]
        d_list = [np.inf, AZO_THICKNESS_NM, TIN_THICKNESS_NM]
        if include_sio2:
            n_list.append(1.46 + 0j)
            d_list.append(2.0)
        n_list.append(substrate_index[index])
        d_list.append(np.inf)
        result = coh_tmm(polarization, n_list, d_list, theta_rad, float(wavelength_nm))
        reflection[index] = float(result["R"])
        transmission[index] = float(result["T"])
    return reflection, transmission


def _apply_backside_upper_bound(
    front_reflection: np.ndarray,
    front_transmission: np.ndarray,
    substrate_index: np.ndarray,
) -> np.ndarray:
    # This deliberately ignores substrate bulk absorption and uses a normal-incidence
    # substrate-air backside reflection. It is an upper-bound diagnostic, not a model claim.
    backside_reflection = np.abs((substrate_index - 1.0) / (substrate_index + 1.0)) ** 2
    denominator = 1.0 - front_reflection * backside_reflection
    return front_reflection + (front_transmission**2 * backside_reflection / denominator)


def _variant_specs() -> list[VariantSpec]:
    substrate_models = [
        "si_lossless_fixed_n3p5",
        "si_weak_absorbing_fixed_n3p7_k0p02",
        "si_synthetic_blue_absorbing_dispersion",
    ]
    interface_models = ["none", "sio2_2nm_between_tin_and_si"]
    backside_models = ["semi_infinite_substrate", "incoherent_air_backside_upper_bound"]
    variants = []
    for substrate_model in substrate_models:
        for interface_model in interface_models:
            for backside_model in backside_models:
                variants.append(
                    VariantSpec(
                        variant_id="__".join(
                            [substrate_model, interface_model, backside_model]
                        ),
                        substrate_model=substrate_model,
                        interface_model=interface_model,
                        backside_model=backside_model,
                    )
                )
    return variants


def _spread_summary(
    wavelengths_nm: np.ndarray,
    predictions: dict[str, np.ndarray],
) -> dict[str, Any]:
    matrix = np.vstack(list(predictions.values()))
    spread = np.max(matrix, axis=0) - np.min(matrix, axis=0)
    max_index = int(np.argmax(spread))
    return {
        "variant_count": int(matrix.shape[0]),
        "mean_spread": float(np.mean(spread)),
        "median_spread": float(np.median(spread)),
        "max_spread": float(spread[max_index]),
        "max_spread_wavelength_nm": float(wavelengths_nm[max_index]),
        "min_prediction": float(np.min(matrix)),
        "max_prediction": float(np.max(matrix)),
    }


def _load_inputs() -> dict[str, Any]:
    measured = _read_channels(MEASURED_PATH)
    source = _read_channels(SOURCE_SIMULATED_PATH)
    tin = load_epsilon_table(TIN_EPSILON_PATH)
    azo = load_epsilon_table(AZO_EPSILON_PATH)
    _require_same_axis(measured["wavelength_nm"], source["wavelength_nm"])
    wavelengths = measured["wavelength_nm"]
    lower = max(
        float(wavelengths.min()),
        float(tin.wavelengths_nm.min()),
        float(azo.wavelengths_nm.min()),
    )
    upper = min(
        float(wavelengths.max()),
        float(tin.wavelengths_nm.max()),
        float(azo.wavelengths_nm.max()),
    )
    mask = (wavelengths >= lower) & (wavelengths <= upper)
    wavelengths = wavelengths[mask]
    return {
        "wavelengths_nm": wavelengths,
        "measured_rp": measured["measured_rp_reflectance_fraction"][mask],
        "measured_rs": measured["measured_rs_reflectance_fraction"][mask],
        "source_simulated_rp": source["simulated_rp_reflectance_fraction"][mask],
        "source_simulated_rs": source["simulated_rs_reflectance_fraction"][mask],
        "tin_epsilon": interpolate_epsilon(tin, wavelengths),
        "azo_epsilon": interpolate_epsilon(azo, wavelengths),
    }


def build_phase3e5_packet(
    phase3e3b_gate_path: Path = DEFAULT_PHASE3E3B_GATE_PATH,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if not phase3e3b_gate_path.exists():
        raise FileNotFoundError(phase3e3b_gate_path)
    phase3e3b = json.loads(phase3e3b_gate_path.read_text(encoding="utf-8"))
    if phase3e3b["decision"]["status"] != "frozen_stack_contract_not_source_backed_tmm_blocked":
        raise ValueError("Phase 3E.5 requires the completed Phase 3E.3B Saha stack gate")

    inputs = _load_inputs()
    wavelengths_nm = inputs["wavelengths_nm"]
    predictions_by_pol: dict[str, dict[str, np.ndarray]] = {"rp": {}, "rs": {}}
    variant_records = []
    curve_rows: list[dict[str, Any]] = [
        {
            "wavelength_nm": float(wavelength_nm),
            "measured_rp": float(inputs["measured_rp"][index]),
            "measured_rs": float(inputs["measured_rs"][index]),
            "source_simulated_rp": float(inputs["source_simulated_rp"][index]),
            "source_simulated_rs": float(inputs["source_simulated_rs"][index]),
        }
        for index, wavelength_nm in enumerate(wavelengths_nm)
    ]

    for spec in _variant_specs():
        substrate_index = _substrate_index(spec.substrate_model, wavelengths_nm)
        pol_records: dict[str, Any] = {}
        for pol_key, tmm_pol in {"rp": "p", "rs": "s"}.items():
            front_reflection, front_transmission = _simulate_front_stack(
                wavelengths_nm,
                inputs["azo_epsilon"],
                inputs["tin_epsilon"],
                substrate_index,
                polarization=tmm_pol,
                interface_model=spec.interface_model,
            )
            if spec.backside_model == "semi_infinite_substrate":
                prediction = front_reflection
            elif spec.backside_model == "incoherent_air_backside_upper_bound":
                prediction = _apply_backside_upper_bound(
                    front_reflection,
                    front_transmission,
                    substrate_index,
                )
            else:
                raise ValueError(f"unknown backside model: {spec.backside_model}")

            predictions_by_pol[pol_key][spec.variant_id] = prediction
            for index, value in enumerate(prediction):
                curve_rows[index][f"{spec.variant_id}_{pol_key}"] = float(value)
            pol_records[pol_key] = {
                "vs_measured": _comparison_metrics(
                    wavelengths_nm,
                    prediction,
                    inputs[f"measured_{pol_key}"],
                ),
                "vs_source_simulated": _comparison_metrics(
                    wavelengths_nm,
                    prediction,
                    inputs[f"source_simulated_{pol_key}"],
                ),
            }
        variant_records.append(
            {
                "variant_id": spec.variant_id,
                "substrate_model": spec.substrate_model,
                "interface_model": spec.interface_model,
                "backside_model": spec.backside_model,
                "polarization_metrics": pol_records,
            }
        )

    spread_summary = {
        pol: _spread_summary(wavelengths_nm, predictions)
        for pol, predictions in predictions_by_pol.items()
    }
    reference_comparisons = {
        "rp": _comparison_metrics(
            wavelengths_nm,
            inputs["source_simulated_rp"],
            inputs["measured_rp"],
        ),
        "rs": _comparison_metrics(
            wavelengths_nm,
            inputs["source_simulated_rs"],
            inputs["measured_rs"],
        ),
    }
    rmse_values = [
        record["polarization_metrics"][pol]["vs_measured"]["root_mean_square_error"]
        for record in variant_records
        for pol in ("rp", "rs")
    ]

    packet = {
        "phase_id": "Phase 3E.5",
        "title": "Saha No-Claim Stack-Assumption Sensitivity Fixture",
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "inputs": {
            "phase3e3b_gate_path": str(phase3e3b_gate_path),
            "measured_reflectance": str(MEASURED_PATH),
            "source_simulated_reflectance": str(SOURCE_SIMULATED_PATH),
            "tin_epsilon": str(TIN_EPSILON_PATH),
            "azo_epsilon": str(AZO_EPSILON_PATH),
            "wavelength_window_nm": [float(wavelengths_nm.min()), float(wavelengths_nm.max())],
            "points": int(wavelengths_nm.size),
            "stack": "air / 250 nm AZO / 130 nm TiN / assumed silicon substrate",
            "incidence_angle_deg": INCIDENCE_ANGLE_DEG,
        },
        "assumption_space": {
            "substrate_models": [
                "si_lossless_fixed_n3p5",
                "si_weak_absorbing_fixed_n3p7_k0p02",
                "si_synthetic_blue_absorbing_dispersion",
            ],
            "interface_models": ["none", "sio2_2nm_between_tin_and_si"],
            "backside_models": [
                "semi_infinite_substrate",
                "incoherent_air_backside_upper_bound",
            ],
            "variant_count": len(variant_records),
        },
        "spread_summary": spread_summary,
        "reference_comparisons": reference_comparisons,
        "variant_records": variant_records,
        "decision": {
            "status": "phase3e5_saha_sensitivity_fixture_ready",
            "claim_label": "non_promoting_sensitivity_fixture",
            "claim_status_ceiling": "literature_reproduction_fixture",
            "calibrated_linear_evidence_allowed": False,
            "phase4_candidate": False,
            "serious_core_allowed": False,
            "validation_residual_modeling_performed": False,
            "diagnostic_comparisons_performed": True,
            "tmm_adapter_frozen": False,
            "claim_standard_changed": False,
            "rmse_vs_measured_range_across_all_diagnostics": [
                float(min(rmse_values)),
                float(max(rmse_values)),
            ],
            "recommended_next_phase": (
                "Phase 3F - simulator-validation fallback on simpler public thin-film data"
            ),
        },
        "warnings": [
            (
                "Every silicon/backside/interface variant is an external sensitivity "
                "assumption, not a recovered Saha author model."
            ),
            (
                "The source-simulated Fig. 2b curves are not an independent holdout; "
                "comparisons to them are author-curve context only."
            ),
            (
                "The incoherent backside variant is an upper-bound diagnostic that "
                "ignores substrate bulk absorption and must not be treated as a "
                "measurement model."
            ),
            "Do not promote Saha or tune variants from these diagnostic metrics.",
        ],
        "remembered_next_work": {
            "phase_id": "Phase 3F",
            "title": "Simulator-Validation Fallback On Simpler Public Thin-Film Data",
            "reason": (
                "Public ENZ packages are proving useful as fixtures but unlikely to "
                "supply a fully frozen calibrated-linear validation contract."
            ),
            "acceptance_target": (
                "Find a boring public planar thin-film dataset with machine-readable "
                "n/k or epsilon, measured R/T or ellipsometry, geometry, stack, and "
                "substrate details sufficient to validate the TMM machinery without "
                "making an ENZ evidence claim."
            ),
        },
    }
    return packet, curve_rows


def phase3e5_markdown(packet: dict[str, Any]) -> str:
    decision = packet["decision"]
    rows = [
        "| Polarization | Mean Spread | Median Spread | Max Spread | Max-Spread Wavelength |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for pol, summary in packet["spread_summary"].items():
        rows.append(
            "| "
            + pol
            + f" | {summary['mean_spread']:.6g}"
            + f" | {summary['median_spread']:.6g}"
            + f" | {summary['max_spread']:.6g}"
            + f" | {summary['max_spread_wavelength_nm']:.3f} |"
        )

    best_rows = [
        "| Variant | Pol | RMSE vs Measured | RMSE vs Source-Simulated |",
        "| --- | --- | ---: | ---: |",
    ]
    sortable = []
    for record in packet["variant_records"]:
        for pol in ("rp", "rs"):
            metrics = record["polarization_metrics"][pol]
            sortable.append(
                (
                    metrics["vs_measured"]["root_mean_square_error"],
                    record["variant_id"],
                    pol,
                    metrics["vs_source_simulated"]["root_mean_square_error"],
                )
            )
    for rmse, variant_id, pol, source_rmse in sorted(sortable)[:6]:
        best_rows.append(f"| `{variant_id}` | `{pol}` | {rmse:.6g} | {source_rmse:.6g} |")

    return "\n".join(
        [
            "# Phase 3E.5 - Saha No-Claim Stack-Assumption Sensitivity Fixture",
            "",
            "## Decision",
            "",
            f"- Status: `{decision['status']}`",
            f"- Claim label: `{decision['claim_label']}`",
            f"- Claim-status ceiling: `{decision['claim_status_ceiling']}`",
            (
                "- Calibrated linear evidence allowed: "
                f"`{str(decision['calibrated_linear_evidence_allowed']).lower()}`"
            ),
            f"- Phase 4 candidate: `{str(decision['phase4_candidate']).lower()}`",
            (
                "- Validation residual modeling performed: "
                f"`{str(decision['validation_residual_modeling_performed']).lower()}`"
            ),
            (
                "- Diagnostic comparisons performed: "
                f"`{str(decision['diagnostic_comparisons_performed']).lower()}`"
            ),
            f"- Recommended next phase: `{decision['recommended_next_phase']}`",
            "",
            "This fixture asks how much the Saha Fig. 2b predicted reflectance moves under",
            "explicitly non-source-backed silicon, interface, and backside assumptions.",
            "It is not validation and it does not select a correct variant.",
            "",
            "## Assumption Space",
            "",
            f"- Variants: `{packet['assumption_space']['variant_count']}`",
            f"- Stack: `{packet['inputs']['stack']}`",
            f"- Wavelength window: `{packet['inputs']['wavelength_window_nm']}` nm",
            f"- Points: `{packet['inputs']['points']}`",
            "",
            "## Variant Spread",
            "",
            *rows,
            "",
            "## Source-Simulated Versus Measured Context",
            "",
            (
                "- `rp` source-simulated RMSE versus measured: "
                f"`{packet['reference_comparisons']['rp']['root_mean_square_error']:.6g}`"
            ),
            (
                "- `rs` source-simulated RMSE versus measured: "
                f"`{packet['reference_comparisons']['rs']['root_mean_square_error']:.6g}`"
            ),
            "",
            "These source-simulated curves are author-curve context, not an independent holdout.",
            "",
            "## Lowest Diagnostic RMSE Rows",
            "",
            *best_rows,
            "",
            "These rows are descriptive only. A lower diagnostic RMSE is not a validation pass.",
            "",
            "## Warnings",
            "",
            *[f"- {warning}" for warning in packet["warnings"]],
            "",
            "## Remembered Next Work",
            "",
            f"- Phase: `{packet['remembered_next_work']['phase_id']}`",
            f"- Title: {packet['remembered_next_work']['title']}",
            f"- Reason: {packet['remembered_next_work']['reason']}",
            f"- Acceptance target: {packet['remembered_next_work']['acceptance_target']}",
            "",
        ]
    )


def write_phase3e5_packet(
    output_dir: Path,
    packet: dict[str, Any],
    curve_rows: list[dict[str, Any]],
) -> tuple[Path, Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase3e5_saha_sensitivity_fixture.json"
    md_path = output_dir / "phase3e5_saha_sensitivity_fixture.md"
    csv_path = output_dir / "phase3e5_saha_sensitivity_curves.csv"
    json_path.write_text(json.dumps(packet, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(phase3e5_markdown(packet), encoding="utf-8")
    if not curve_rows:
        raise ValueError("curve rows are empty")
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(curve_rows[0].keys()))
        writer.writeheader()
        writer.writerows(curve_rows)
    return json_path, md_path, csv_path
