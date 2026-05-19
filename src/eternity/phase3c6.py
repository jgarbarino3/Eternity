"""Phase 3C.6A bounded St Andrews source-model parity diagnostics."""

from __future__ import annotations

import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
from tmm import coh_tmm, inc_tmm

from eternity.materials import refractive_index_from_epsilon
from eternity.optical_data import EpsilonTable, interpolate_epsilon
from eternity.phase3c4 import _comparison_metrics, _parse_epsilon_text, _threshold_status

ROUGHNESS_VOID_FRACTION = 0.5
ANGSTROM_TO_NM = 0.1
BACKSIDE_GLASS_THICKNESS_PLACEHOLDER_NM = 1_000_000.0


def _load_json(path: Path | str) -> dict[str, Any]:
    path = Path(path)
    return json.loads(path.read_text(encoding="utf-8"))


def _load_comparison(path: Path) -> tuple[np.ndarray, np.ndarray]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError("comparison table is empty")
    wavelengths_nm = np.asarray([float(row["wavelength_nm"]) for row in rows], dtype=float)
    measurement = np.asarray(
        [float(row.get("measurement", row.get("holdout", "nan"))) for row in rows],
        dtype=float,
    )
    if not np.all(np.isfinite(measurement)):
        raise ValueError("comparison table must include finite measurement or holdout values")
    return wavelengths_nm, measurement


def _cauchy_index(wavelengths_nm: np.ndarray, source_model: dict[str, Any]) -> np.ndarray:
    substrate = source_model["substrate_model"]
    wavelength_um = wavelengths_nm / 1000.0
    cauchy_a = float(substrate["cauchy_A"])
    cauchy_b = float(substrate["cauchy_B"])
    cauchy_c = float(substrate["cauchy_C"])
    return cauchy_a + cauchy_b / wavelength_um**2 + cauchy_c / wavelength_um**4


def _bruggeman_50_50(epsilon_a: np.ndarray, epsilon_b: np.ndarray) -> np.ndarray:
    """Return the symmetric Bruggeman EMA root nearest the volume average."""

    effective: list[complex] = []
    for left, right in zip(epsilon_a, epsilon_b, strict=True):
        roots = np.roots([4.0, -(left + right), -2.0 * left * right])
        target = (left + right) / 2.0
        effective.append(complex(min(roots, key=lambda root: abs(root - target))))
    return np.asarray(effective, dtype=complex)


def _load_selected_epsilon(
    pairing: dict[str, Any],
    wavelengths_nm: np.ndarray,
) -> np.ndarray:
    import zipfile

    zip_path = Path(pairing["source_archive"]["path"])
    selected_member = pairing["selected_pairing"]["selected_material_member"]
    with zipfile.ZipFile(zip_path) as archive:
        text = archive.read(selected_member).decode("utf-8-sig")
    table_wavelengths, table_epsilon = _parse_epsilon_text(text)
    return interpolate_epsilon(
        EpsilonTable(wavelengths_nm=table_wavelengths, epsilon=table_epsilon),
        wavelengths_nm,
    )


def _coherent_reflection(
    wavelengths_nm: np.ndarray,
    film_index: np.ndarray,
    *,
    film_thickness_nm: float,
    substrate_index: np.ndarray | float,
    roughness_index: np.ndarray | None = None,
    roughness_thickness_nm: float | None = None,
) -> np.ndarray:
    reflection = np.empty_like(wavelengths_nm, dtype=float)
    for index, wavelength_nm in enumerate(wavelengths_nm):
        substrate = (
            complex(substrate_index[index])
            if isinstance(substrate_index, np.ndarray)
            else complex(substrate_index)
        )
        if roughness_index is None:
            n_list = [1.0 + 0j, film_index[index], substrate]
            d_list = [np.inf, film_thickness_nm, np.inf]
        else:
            if roughness_thickness_nm is None:
                raise ValueError("roughness_thickness_nm is required with roughness_index")
            n_list = [1.0 + 0j, roughness_index[index], film_index[index], substrate]
            d_list = [np.inf, roughness_thickness_nm, film_thickness_nm, np.inf]
        result = coh_tmm("s", n_list, d_list, 0.0, float(wavelength_nm))
        reflection[index] = float(result["R"])
    return reflection


def _incoherent_backside_reflection(
    wavelengths_nm: np.ndarray,
    film_index: np.ndarray,
    *,
    film_thickness_nm: float,
    substrate_index: np.ndarray,
    roughness_index: np.ndarray | None = None,
    roughness_thickness_nm: float | None = None,
) -> np.ndarray:
    """Approximate a glass-air backside with an incoherent substrate layer.

    The Woollam source records back-reflection settings, but the public packet
    does not expose substrate thickness or the exact CompleteEASE acquisition
    reduction. This diagnostic therefore uses a lossless thick-glass
    incoherent layer as a bounded estimate, not an exact source reproduction.
    """

    reflection = np.empty_like(wavelengths_nm, dtype=float)
    for index, wavelength_nm in enumerate(wavelengths_nm):
        substrate = complex(substrate_index[index])
        if roughness_index is None:
            n_list = [1.0 + 0j, film_index[index], substrate, 1.0 + 0j]
            d_list = [
                np.inf,
                film_thickness_nm,
                BACKSIDE_GLASS_THICKNESS_PLACEHOLDER_NM,
                np.inf,
            ]
            c_list = ["i", "c", "i", "i"]
        else:
            if roughness_thickness_nm is None:
                raise ValueError("roughness_thickness_nm is required with roughness_index")
            n_list = [
                1.0 + 0j,
                roughness_index[index],
                film_index[index],
                substrate,
                1.0 + 0j,
            ]
            d_list = [
                np.inf,
                roughness_thickness_nm,
                film_thickness_nm,
                BACKSIDE_GLASS_THICKNESS_PLACEHOLDER_NM,
                np.inf,
            ]
            c_list = ["i", "c", "c", "i", "i"]
        result = inc_tmm("s", n_list, d_list, c_list, 0.0, float(wavelength_nm))
        reflection[index] = float(result["R"])
    return reflection


def _variant_record(
    *,
    name: str,
    description: str,
    prediction: np.ndarray,
    wavelengths_nm: np.ndarray,
    measurement: np.ndarray,
    threshold_metrics: list[dict[str, Any]],
    assumptions: list[str],
    limitations: list[str],
) -> dict[str, Any]:
    metrics = _comparison_metrics(wavelengths_nm, prediction, measurement)
    return {
        "name": name,
        "description": description,
        "assumptions": assumptions,
        "limitations": limitations,
        "metrics": metrics,
        "threshold_status": _threshold_status(metrics, threshold_metrics),
    }


def _source_length_inference(source_model: dict[str, Any]) -> dict[str, Any]:
    film_raw = source_model.get("film_thickness_raw")
    roughness_raw = source_model.get("roughness_raw")
    film_nm = float(film_raw) * ANGSTROM_TO_NM if film_raw is not None else None
    roughness_nm = (
        float(roughness_raw) * ANGSTROM_TO_NM if roughness_raw is not None else None
    )
    return {
        "basis": "completeease_length_values_interpreted_as_angstrom_for_bounded_test",
        "confidence": "plausible_not_independently_verified",
        "film_thickness_raw": film_raw,
        "film_thickness_nm": film_nm,
        "roughness_raw": roughness_raw,
        "roughness_thickness_nm": roughness_nm,
        "reason": (
            "The raw fit limits around the thickness parameter are 200-1500, "
            "which is plausible as Angstrom for a nominal 50 nm film. This is "
            "sufficient for a bounded parity test, not exact source-model proof."
        ),
    }


def build_phase3c6_packet(
    parity_json: Path,
    pairing_json: Path,
    run_dir: Path,
) -> dict[str, Any]:
    parity = _load_json(parity_json)
    pairing = _load_json(pairing_json)
    wavelengths_nm, measurement = _load_comparison(run_dir / "comparison_table.csv")
    threshold_metrics = parity["clean_run_model"].get("threshold_metrics")
    if threshold_metrics is None:
        triage = _load_json(parity["inputs"]["triage_json"])
        threshold_metrics = triage["current_run"]["threshold_evaluation"]["metrics"]

    source_model = parity["source_model"]
    length_inference = _source_length_inference(source_model)
    if length_inference["film_thickness_nm"] is None:
        raise ValueError("source film thickness is missing")

    epsilon = _load_selected_epsilon(pairing, wavelengths_nm)
    film_index = refractive_index_from_epsilon(epsilon)
    substrate_index = _cauchy_index(wavelengths_nm, source_model)
    roughness_index = None
    if length_inference["roughness_thickness_nm"] is not None:
        roughness_epsilon = _bruggeman_50_50(np.ones_like(epsilon), epsilon)
        roughness_index = refractive_index_from_epsilon(roughness_epsilon)

    film_source_nm = float(length_inference["film_thickness_nm"])
    roughness_nm = length_inference["roughness_thickness_nm"]
    variants = [
        _variant_record(
            name="clean_baseline_resimulated",
            description="Resimulated clean-run stack: 50 nm TiN on fixed n=1.45 glass.",
            prediction=_coherent_reflection(
                wavelengths_nm,
                film_index,
                film_thickness_nm=50.0,
                substrate_index=1.45,
            ),
            wavelengths_nm=wavelengths_nm,
            measurement=measurement,
            threshold_metrics=threshold_metrics,
            assumptions=["Fixed n=1.45 glass and nominal 50 nm compact TiN film."],
            limitations=["No source-model parity changes included."],
        ),
        _variant_record(
            name="source_cauchy_glass_nominal_thickness",
            description="Only the source Float Glass Cauchy substrate is enabled.",
            prediction=_coherent_reflection(
                wavelengths_nm,
                film_index,
                film_thickness_nm=50.0,
                substrate_index=substrate_index,
            ),
            wavelengths_nm=wavelengths_nm,
            measurement=measurement,
            threshold_metrics=threshold_metrics,
            assumptions=[
                "Cauchy substrate uses n(lambda_um)=A+B/lambda_um^2+C/lambda_um^4.",
                "The TiN layer remains the nominal 50 nm clean-run layer.",
            ],
            limitations=["Does not include roughness or back-reflection settings."],
        ),
        _variant_record(
            name="source_cauchy_glass_source_thickness",
            description="Source Cauchy substrate plus inferred compact TiN thickness.",
            prediction=_coherent_reflection(
                wavelengths_nm,
                film_index,
                film_thickness_nm=film_source_nm,
                substrate_index=substrate_index,
            ),
            wavelengths_nm=wavelengths_nm,
            measurement=measurement,
            threshold_metrics=threshold_metrics,
            assumptions=[
                f"Raw source thickness is interpreted as {film_source_nm:.6g} nm.",
                "No roughness or back-reflection estimate is included.",
            ],
            limitations=[
                "CompleteEASE internal length units are inferred, not independently decoded."
            ],
        ),
    ]

    if roughness_index is not None and roughness_nm is not None:
        variants.append(
            _variant_record(
                name="source_cauchy_thickness_roughness_ema",
                description=(
                    "Source Cauchy substrate, inferred compact TiN thickness, "
                    "and 50/50 air-TiN Bruggeman roughness layer."
                ),
                prediction=_coherent_reflection(
                    wavelengths_nm,
                    film_index,
                    film_thickness_nm=film_source_nm,
                    substrate_index=substrate_index,
                    roughness_index=roughness_index,
                    roughness_thickness_nm=float(roughness_nm),
                ),
                wavelengths_nm=wavelengths_nm,
                measurement=measurement,
                threshold_metrics=threshold_metrics,
                assumptions=[
                    f"Raw roughness is interpreted as {roughness_nm:.6g} nm.",
                    "Roughness is approximated as 50 percent void / 50 percent TiN EMA.",
                ],
                limitations=[
                    "The source file exposes roughness metadata but not a full public "
                    "EMA recipe, so this remains approximate."
                ],
            )
        )
        variants.append(
            _variant_record(
                name="source_cauchy_thickness_roughness_backside_estimate",
                description=(
                    "Roughness variant plus an incoherent glass-air backside estimate."
                ),
                prediction=_incoherent_backside_reflection(
                    wavelengths_nm,
                    film_index,
                    film_thickness_nm=film_source_nm,
                    substrate_index=substrate_index,
                    roughness_index=roughness_index,
                    roughness_thickness_nm=float(roughness_nm),
                ),
                wavelengths_nm=wavelengths_nm,
                measurement=measurement,
                threshold_metrics=threshold_metrics,
                assumptions=[
                    "Back-reflection estimate uses a thick lossless incoherent glass layer.",
                    "The source `% 1st Reflection` value is treated as 100 percent enabled.",
                ],
                limitations=[
                    "The public source does not expose exact substrate thickness or the "
                    "CompleteEASE acquisition reduction; this is not exact parity."
                ],
            )
        )

    passing = [
        variant["name"]
        for variant in variants
        if variant["threshold_status"]["status"] == "pass"
    ]
    best = min(
        variants,
        key=lambda variant: variant["metrics"]["root_mean_square_error"],
    )
    roughness_resolved = False
    back_reflection_resolved = False
    can_continue_to_phase4 = bool(passing) and roughness_resolved and back_reflection_resolved
    status = (
        "parity_variants_passed_ready_for_phase4_review"
        if can_continue_to_phase4
        else "parity_variants_failed_roughness_back_reflection_underdetermined"
    )
    return {
        "phase_id": "Phase 3C.6A",
        "title": "Bounded St Andrews Source-Model Parity Implementation",
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "inputs": {
            "parity_json": str(parity_json),
            "pairing_json": str(pairing_json),
            "run_dir": str(run_dir),
            "comparison_table": str(run_dir / "comparison_table.csv"),
        },
        "decision": {
            "status": status,
            "can_feed_serious_core": can_continue_to_phase4,
            "can_promote_calibrated_linear_evidence": can_continue_to_phase4,
            "phase4_ready": can_continue_to_phase4,
            "continue_to_phase4": can_continue_to_phase4,
            "stop_reason": (
                "Bounded source-derived variants still fail the locked thresholds, "
                "and roughness/back-reflection parity remains approximate rather than exact."
            ),
            "next_phase": "Phase 3B.1 or Phase 3C.6B only with new source-model evidence",
        },
        "source_model": source_model,
        "length_inference": length_inference,
        "implemented_parity": {
            "cauchy_substrate": "implemented_for_bounded_test",
            "source_thickness": "implemented_with_angstrom_inference",
            "roughness": "approximate_50_50_bruggeman_ema",
            "back_reflection": "approximate_incoherent_backside_estimate",
        },
        "resolved_status": {
            "cauchy_substrate": True,
            "source_thickness": True,
            "roughness": roughness_resolved,
            "back_reflection": back_reflection_resolved,
        },
        "threshold_summary": {
            "passing_variants": passing,
            "best_rmse_variant": best["name"],
            "best_rmse": best["metrics"]["root_mean_square_error"],
            "all_variants_failed": not passing,
        },
        "variants": variants,
        "interpretation_boundary": (
            "Phase 3C.6A implements bounded source-derived parity diagnostics. "
            "It does not fit to RT.xlsx, change thresholds, select a replacement "
            "material model for promotion, feed the serious core, or make the "
            "St Andrews lane Phase 4-ready."
        ),
    }


def _format_metric(value: Any) -> str:
    if value is None:
        return "none"
    return f"{float(value):.6g}"


def _metric_summary(metrics: dict[str, Any]) -> str:
    return (
        f"MAE `{_format_metric(metrics['mean_absolute_error'])}`, "
        f"RMSE `{_format_metric(metrics['root_mean_square_error'])}`, "
        f"max residual `{_format_metric(metrics['max_absolute_residual'])}`, "
        f"dip offset `{_format_metric(metrics['dip_wavelength_offset_nm'])}` nm, "
        f"shape corr `{_format_metric(metrics['shape_correlation_minmax'])}`"
    )


def phase3c6_markdown(packet: dict[str, Any]) -> str:
    decision = packet["decision"]
    length = packet["length_inference"]
    lines = [
        "# Phase 3C.6A - Bounded St Andrews Source-Model Parity Implementation",
        "",
        "## Decision",
        "",
        f"- Status: `{decision['status']}`",
        f"- Can feed serious core: `{decision['can_feed_serious_core']}`",
        "- Can promote calibrated evidence: "
        f"`{decision['can_promote_calibrated_linear_evidence']}`",
        f"- Phase 4 ready: `{decision['phase4_ready']}`",
        f"- Continue to Phase 4: `{decision['continue_to_phase4']}`",
        f"- Stop reason: {decision['stop_reason']}",
        f"- Next phase: `{decision['next_phase']}`",
        "",
        "## Source Length Inference",
        "",
        f"- Basis: `{length['basis']}`",
        f"- Confidence: `{length['confidence']}`",
        f"- Film thickness used: `{length['film_thickness_nm']}` nm",
        f"- Roughness thickness used: `{length['roughness_thickness_nm']}` nm",
        f"- Reason: {length['reason']}",
        "",
        "## Implemented Parity Pieces",
        "",
    ]
    lines.extend(
        f"- `{name}`: `{status}`"
        for name, status in packet["implemented_parity"].items()
    )
    lines.extend(
        [
            "",
            "## Resolution Status",
            "",
        ]
    )
    lines.extend(
        f"- `{name}`: `{status}`"
        for name, status in packet["resolved_status"].items()
    )
    lines.extend(
        [
            "",
            "## Variant Results",
            "",
            "| Variant | Metrics | Threshold status |",
            "| --- | --- | --- |",
        ]
    )
    for variant in packet["variants"]:
        lines.append(
            f"| `{variant['name']}` | {_metric_summary(variant['metrics'])} | "
            f"`{variant['threshold_status']['status']}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            packet["interpretation_boundary"],
            "",
        ]
    )
    return "\n".join(lines)


def phase3c6_csv(packet: dict[str, Any]) -> str:
    rows = [
        "variant,rmse,mae,max_absolute_residual,dip_offset_nm,"
        "shape_correlation_minmax,threshold_status,failed_metrics"
    ]
    for variant in packet["variants"]:
        metrics = variant["metrics"]
        rows.append(
            ",".join(
                [
                    variant["name"],
                    _format_metric(metrics["root_mean_square_error"]),
                    _format_metric(metrics["mean_absolute_error"]),
                    _format_metric(metrics["max_absolute_residual"]),
                    _format_metric(metrics["dip_wavelength_offset_nm"]),
                    _format_metric(metrics["shape_correlation_minmax"]),
                    variant["threshold_status"]["status"],
                    "|".join(variant["threshold_status"]["failed_metrics"]),
                ]
            )
        )
    return "\n".join(rows) + "\n"


def write_phase3c6_packet(output_dir: Path, packet: dict[str, Any]) -> tuple[Path, Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase3c6_source_model_parity_decision.json"
    md_path = output_dir / "phase3c6_source_model_parity_decision.md"
    csv_path = output_dir / "phase3c6_parity_variants.csv"
    json_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(phase3c6_markdown(packet), encoding="utf-8")
    csv_path.write_text(phase3c6_csv(packet), encoding="utf-8")
    return json_path, md_path, csv_path
