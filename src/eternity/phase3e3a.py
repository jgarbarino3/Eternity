"""Phase 3E.3A Saha exported-table audit and candidate gate."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from datetime import UTC, datetime
from io import StringIO
from pathlib import Path
from typing import Any

DEFAULT_RAW_DIR = Path("lab_data/raw/public_saha_tin_azo_2023")
DEFAULT_METADATA_PATH = DEFAULT_RAW_DIR / "figshare_article_23734116.json"
FIG2B_EXPORT = DEFAULT_RAW_DIR / "origin_viewer_exports/saha_fig2b_origin_viewer_export.csv"
FIG2CD_EXPORT = DEFAULT_RAW_DIR / "origin_viewer_exports/saha_fig2cd_origin_viewer_export.csv"

EXPECTED_EXPORT_SHA256 = {
    "fig2b": "b8134a6ff368a2c8707453ca80dae862b27608bffbb1b9ad4bdb163a8cf2d0b2",
    "fig2cd": "436a6db455883ae66cc6f3880e563c0287c6f04842eb231150567737cc1caaa8",
}

ARTICLE_URL = "https://www.nature.com/articles/s41467-023-41377-5"
SUPPLEMENTARY_PDF_URL = (
    "https://static-content.springer.com/esm/"
    "art%3A10.1038%2Fs41467-023-41377-5/"
    "MediaObjects/41467_2023_41377_MOESM1_ESM.pdf"
)
FIGSHARE_API_URL = "https://api.figshare.com/v2/articles/23734116"


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _read_csv_rows(path: Path) -> list[list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.reader(handle))


def _parse_float(value: str, label: str) -> float:
    try:
        parsed = float(value)
    except ValueError as error:
        raise ValueError(f"{label} is not numeric: {value!r}") from error
    if not math.isfinite(parsed):
        raise ValueError(f"{label} is non-finite: {value!r}")
    return parsed


def _numeric_pair(
    rows: list[list[str]], wavelength_column: int, value_column: int, label: str
) -> list[tuple[float, float]]:
    values: list[tuple[float, float]] = []
    for row_index, row in enumerate(rows[3:], start=4):
        if len(row) <= max(wavelength_column, value_column):
            continue
        wavelength = row[wavelength_column].strip()
        value = row[value_column].strip()
        if not wavelength and not value:
            continue
        if not wavelength or not value:
            continue
        values.append(
            (
                _parse_float(wavelength, f"{label} wavelength row {row_index}"),
                _parse_float(value, f"{label} value row {row_index}"),
            )
        )
    if not values:
        raise ValueError(f"{label} has no numeric rows")
    return values


def _validate_increasing_axis(values: list[float], label: str) -> None:
    if len(values) < 2:
        raise ValueError(f"{label} must contain at least two points")
    if any(right <= left for left, right in zip(values, values[1:], strict=False)):
        raise ValueError(f"{label} wavelength axis must be strictly increasing")


def _validate_same_axis(
    reference: list[tuple[float, float]],
    other: list[tuple[float, float]],
    label: str,
) -> None:
    if len(reference) != len(other):
        raise ValueError(f"{label} row count {len(other)} does not match {len(reference)}")
    reference_axis = [item[0] for item in reference]
    other_axis = [item[0] for item in other]
    if other_axis != reference_axis:
        raise ValueError(f"{label} wavelength axis does not match the reference axis")


def _range(values: list[float]) -> list[float]:
    return [min(values), max(values)]


def _round_float(value: float, digits: int = 6) -> float:
    return round(value, digits)


def _axis_step(values: list[float]) -> float | None:
    if len(values) < 2:
        return None
    steps = {round(right - left, 9) for left, right in zip(values, values[1:], strict=False)}
    if len(steps) != 1:
        return None
    return steps.pop()


def _enz_crossings(rows: list[dict[str, float]]) -> list[float]:
    crossings: list[float] = []
    for left, right in zip(rows, rows[1:], strict=False):
        left_real = left["epsilon_real"]
        right_real = right["epsilon_real"]
        if left_real == 0:
            crossings.append(_round_float(left["wavelength_nm"]))
        elif left_real * right_real < 0:
            fraction = -left_real / (right_real - left_real)
            wavelength = left["wavelength_nm"] + fraction * (
                right["wavelength_nm"] - left["wavelength_nm"]
            )
            crossings.append(_round_float(wavelength))
    return crossings


def _reflectance_rows(fig2b_rows: list[list[str]]) -> dict[str, Any]:
    simulated_rp = _numeric_pair(fig2b_rows, 0, 1, "simulated Rp")
    measured_rp = _numeric_pair(fig2b_rows, 2, 3, "measured Rp")
    measured_rs = _numeric_pair(fig2b_rows, 4, 5, "measured Rs")
    simulated_rs = _numeric_pair(fig2b_rows, 6, 7, "simulated Rs")
    for label, values in {
        "measured Rp": measured_rp,
        "measured Rs": measured_rs,
        "simulated Rs": simulated_rs,
    }.items():
        _validate_same_axis(simulated_rp, values, label)
    wavelengths = [item[0] for item in simulated_rp]
    _validate_increasing_axis(wavelengths, "Fig. 2b")

    measured = [
        {
            "wavelength_nm": wavelength,
            "measured_rp_reflectance_fraction": rp,
            "measured_rs_reflectance_fraction": rs,
        }
        for (wavelength, rp), (_, rs) in zip(measured_rp, measured_rs, strict=True)
    ]
    source_simulated = [
        {
            "wavelength_nm": wavelength,
            "simulated_rp_reflectance_fraction": rp,
            "simulated_rs_reflectance_fraction": rs,
        }
        for (wavelength, rp), (_, rs) in zip(simulated_rp, simulated_rs, strict=True)
    ]
    all_values = [
        value
        for row in measured + source_simulated
        for key, value in row.items()
        if key != "wavelength_nm"
    ]
    if min(all_values) < 0 or max(all_values) > 1:
        raise ValueError("Fig. 2b reflectance values are not bounded in [0, 1]")

    return {
        "measured": measured,
        "source_simulated": source_simulated,
        "summary": {
            "source_rows_total": len(fig2b_rows),
            "numeric_rows": len(measured),
            "wavelength_nm": _range(wavelengths),
            "wavelength_step_nm": _axis_step(wavelengths),
            "columns": {
                "simulated_rp": {"source_columns": ["A", "B"], "comment": fig2b_rows[2][1]},
                "measured_rp": {"source_columns": ["C", "D"], "comment": fig2b_rows[2][3]},
                "measured_rs": {"source_columns": ["E", "F"], "comment": fig2b_rows[2][5]},
                "simulated_rs": {"source_columns": ["G", "H"], "comment": fig2b_rows[2][7]},
            },
            "measured_rp_reflectance_fraction": _range(
                [row["measured_rp_reflectance_fraction"] for row in measured]
            ),
            "measured_rs_reflectance_fraction": _range(
                [row["measured_rs_reflectance_fraction"] for row in measured]
            ),
            "simulated_rp_reflectance_fraction": _range(
                [row["simulated_rp_reflectance_fraction"] for row in source_simulated]
            ),
            "simulated_rs_reflectance_fraction": _range(
                [row["simulated_rs_reflectance_fraction"] for row in source_simulated]
            ),
            "unit_interval_check": "pass",
            "measured_and_source_simulated_split": "explicit_source_labels",
        },
    }


def _epsilon_rows(fig2cd_rows: list[list[str]]) -> dict[str, Any]:
    tin_real = _numeric_pair(fig2cd_rows, 0, 1, "TiN epsilon real")
    azo_real = _numeric_pair(fig2cd_rows, 2, 3, "AZO epsilon real")
    tin_imag = _numeric_pair(fig2cd_rows, 4, 5, "TiN epsilon imag")
    azo_imag = _numeric_pair(fig2cd_rows, 6, 7, "AZO epsilon imag")
    _validate_same_axis(tin_real, tin_imag, "TiN epsilon imaginary")
    _validate_same_axis(azo_real, azo_imag, "AZO epsilon imaginary")

    tin = [
        {"wavelength_nm": wavelength, "epsilon_real": real, "epsilon_imag": imag}
        for (wavelength, real), (_, imag) in zip(tin_real, tin_imag, strict=True)
    ]
    azo = [
        {"wavelength_nm": wavelength, "epsilon_real": real, "epsilon_imag": imag}
        for (wavelength, real), (_, imag) in zip(azo_real, azo_imag, strict=True)
    ]
    _validate_increasing_axis([row["wavelength_nm"] for row in tin], "TiN epsilon")
    _validate_increasing_axis([row["wavelength_nm"] for row in azo], "AZO epsilon")
    if min(row["epsilon_imag"] for row in tin + azo) <= 0:
        raise ValueError("Fig. 2c/d epsilon imaginary values are not strictly positive")

    return {
        "tin": tin,
        "azo": azo,
        "summary": {
            "source_rows_total": len(fig2cd_rows),
            "tin": {
                "numeric_rows": len(tin),
                "wavelength_nm": _range([row["wavelength_nm"] for row in tin]),
                "wavelength_step_nm": _axis_step([row["wavelength_nm"] for row in tin]),
                "epsilon_real": _range([row["epsilon_real"] for row in tin]),
                "epsilon_imag": _range([row["epsilon_imag"] for row in tin]),
                "enz_wavelengths_nm": _enz_crossings(tin),
                "passivity_check": "pass",
                "source_comment": fig2cd_rows[2][0],
            },
            "azo": {
                "numeric_rows": len(azo),
                "wavelength_nm": _range([row["wavelength_nm"] for row in azo]),
                "wavelength_step_nm": _axis_step([row["wavelength_nm"] for row in azo]),
                "epsilon_real": _range([row["epsilon_real"] for row in azo]),
                "epsilon_imag": _range([row["epsilon_imag"] for row in azo]),
                "enz_wavelengths_nm": _enz_crossings(azo),
                "passivity_check": "pass",
                "source_comment": fig2cd_rows[2][2],
            },
        },
    }


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    _write_text(path, output.getvalue())


def _artifact_metadata(path: Path, role: str, source_path: Path) -> dict[str, Any]:
    return {
        "path": str(path),
        "role": role,
        "bytes": path.stat().st_size,
        "sha256": _sha256_file(path),
        "source_export": str(source_path),
    }


def _load_metadata(metadata_path: Path) -> dict[str, Any]:
    return json.loads(metadata_path.read_text(encoding="utf-8"))


def _figshare_file_summary(metadata: dict[str, Any]) -> dict[str, Any]:
    files = {
        file_info["name"]: {
            "size": file_info["size"],
            "supplied_md5": file_info["supplied_md5"],
            "download_url": file_info["download_url"],
        }
        for file_info in metadata["files"]
    }
    return {
        "title": metadata["title"],
        "doi": metadata["doi"],
        "version": metadata["version"],
        "modified_date": metadata["modified_date"],
        "license": metadata["license"]["name"],
        "fig2b_file": files["Source data for Fig 2b.opju"],
        "fig2cd_file": files["Source data for Fig 2cd.opju"],
        "description_evidence": {
            "fig2b": (
                "Figshare description identifies Fig. 2b as simulated Rp/Rs and "
                "experimentally measured reflectance versus wavelength."
            ),
            "fig2cd": (
                "Figshare description identifies Fig. 2c/d as wavelength and "
                "permittivity tables for TiN and AZO, with thicknesses in comments."
            ),
        },
    }


def _source_evidence() -> dict[str, Any]:
    return {
        "article_url": ARTICLE_URL,
        "supplementary_pdf_url": SUPPLEMENTARY_PDF_URL,
        "figshare_api_url": FIGSHARE_API_URL,
        "article": [
            (
                "The paper describes a 130 nm TiN layer on silicon with a 250 nm "
                "AZO layer deposited on top."
            ),
            (
                "The paper describes 50 degree reflectance measurements and Fig. 2b "
                "as s- and p-polarized reflectance spectra."
            ),
            (
                "The paper says spectroscopic ellipsometry followed by Drude-Lorentz "
                "fitting gives the TiN and AZO permittivity curves."
            ),
            (
                "The author-contribution section says TMM calculations were performed, "
                "but the Fig. 2 source tables do not publish a complete TMM settings file."
            ),
        ],
        "supplementary_information": [
            (
                "Supplementary Section S3 says TiN films were measured by VASE at "
                "50 and 70 degrees and modeled with a Drude-Lorentz form."
            ),
            (
                "Supplementary growth notes say AZO was grown on TiN layers on silicon; "
                "the source table comments carry the 130 nm TiN and 250 nm AZO values."
            ),
        ],
    }


def build_phase3e3a_packet(
    metadata_path: Path = DEFAULT_METADATA_PATH,
    raw_dir: Path = DEFAULT_RAW_DIR,
    canonical_output_dir: Path | None = None,
) -> dict[str, Any]:
    fig2b_path = raw_dir / "origin_viewer_exports/saha_fig2b_origin_viewer_export.csv"
    fig2cd_path = raw_dir / "origin_viewer_exports/saha_fig2cd_origin_viewer_export.csv"
    if not metadata_path.exists():
        raise FileNotFoundError(metadata_path)
    if not fig2b_path.exists():
        raise FileNotFoundError(fig2b_path)
    if not fig2cd_path.exists():
        raise FileNotFoundError(fig2cd_path)

    fig2b_sha = _sha256_file(fig2b_path)
    fig2cd_sha = _sha256_file(fig2cd_path)
    if fig2b_sha != EXPECTED_EXPORT_SHA256["fig2b"]:
        raise ValueError(f"Fig. 2b export SHA-256 mismatch: {fig2b_sha}")
    if fig2cd_sha != EXPECTED_EXPORT_SHA256["fig2cd"]:
        raise ValueError(f"Fig. 2c/d export SHA-256 mismatch: {fig2cd_sha}")

    metadata = _load_metadata(metadata_path)
    reflectance = _reflectance_rows(_read_csv_rows(fig2b_path))
    epsilon = _epsilon_rows(_read_csv_rows(fig2cd_path))

    canonical_dir = canonical_output_dir or raw_dir
    measured_path = canonical_dir / "saha_fig2b_measured_reflectance_canonical.csv"
    source_simulated_path = (
        canonical_dir / "saha_fig2b_source_simulated_reflectance_canonical.csv"
    )
    tin_epsilon_path = canonical_dir / "saha_fig2cd_tin_epsilon_canonical.csv"
    azo_epsilon_path = canonical_dir / "saha_fig2cd_azo_epsilon_canonical.csv"

    _write_csv(measured_path, reflectance["measured"])
    _write_csv(source_simulated_path, reflectance["source_simulated"])
    _write_csv(tin_epsilon_path, epsilon["tin"])
    _write_csv(azo_epsilon_path, epsilon["azo"])

    artifacts = {
        "fig2b_measured_reflectance": _artifact_metadata(
            measured_path,
            "holdout_candidate_measured_reflectance_source_labeled",
            fig2b_path,
        ),
        "fig2b_source_simulated_reflectance": _artifact_metadata(
            source_simulated_path,
            "source_simulated_reference_for_audit_not_holdout",
            fig2b_path,
        ),
        "fig2cd_tin_epsilon": _artifact_metadata(
            tin_epsilon_path,
            "calibration_material_input_candidate_tin",
            fig2cd_path,
        ),
        "fig2cd_azo_epsilon": _artifact_metadata(
            azo_epsilon_path,
            "calibration_material_input_candidate_azo",
            fig2cd_path,
        ),
    }

    return {
        "phase_id": "Phase 3E.3A",
        "title": "Saha Exported-Table Audit And Candidate Gate",
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "inputs": {
            "metadata_path": str(metadata_path),
            "raw_dir": str(raw_dir),
            "fig2b_origin_viewer_export": str(fig2b_path),
            "fig2cd_origin_viewer_export": str(fig2cd_path),
            "fig2b_sha256": fig2b_sha,
            "fig2cd_sha256": fig2cd_sha,
            "canonical_output_dir": str(canonical_dir),
        },
        "figshare": _figshare_file_summary(metadata),
        "source_evidence": _source_evidence(),
        "table_audit": {
            "fig2b_reflectance": reflectance["summary"],
            "fig2cd_permittivity": epsilon["summary"],
        },
        "artifacts": artifacts,
        "gate_review": {
            "split_gate": {
                "status": "pass",
                "basis": (
                    "Origin Viewer export preserves explicit measured Rp/Rs and "
                    "source-simulated Rp/Rs labels. Canonical artifacts keep those "
                    "families in separate CSV files."
                ),
            },
            "geometry_gate": {
                "status": "pass_for_source_semantics",
                "basis": (
                    "Source comments and paper text agree on 50 degree s/p reflectance "
                    "from the air/AZO/TiN/silicon stack."
                ),
            },
            "normalization_gate": {
                "status": "conditional_pass_for_weak_holdout_only",
                "basis": (
                    "Figshare and paper call Fig. 2b reflectance, not normalized "
                    "modulation; all measured values are unit-interval fractions. "
                    "The source does not provide a separate instrument calibration "
                    "record, so this is not calibrated-linear evidence."
                ),
            },
            "leakage_gate": {
                "status": "partial_not_promotion_clean",
                "basis": (
                    "The source backs VASE/Drude-Lorentz material fitting, and no "
                    "source text found here says Fig. 2b measured reflectance was used "
                    "to fit the Fig. 2c/d epsilon tables. However, the same article "
                    "contains the source simulated Fig. 2b curves, TMM calculations, "
                    "and device design, so independence is only weak-within-dataset."
                ),
            },
            "stack_model_gate": {
                "status": "blocked",
                "basis": (
                    "A reproducible no-fit TMM adapter still needs a frozen silicon "
                    "substrate optical-constant source and substrate/backside handling. "
                    "Those are not specified by the exported Fig. 2 source tables."
                ),
            },
        },
        "decision": {
            "status": "canonical_tables_ready_tmm_adapter_blocked",
            "claim_status_ceiling": "weak_within_dataset_holdout",
            "current_claim_label": "source_tables_audited_not_tmm_ready",
            "canonical_tables_ready": True,
            "full_no_fit_tmm_validation_allowed": False,
            "phase4_candidate": False,
            "phase4_enz_ready": False,
            "serious_core_allowed": False,
            "stop_rule_triggered": True,
            "stop_rule_reason": (
                "Stop before TMM residual modeling because substrate optical constants, "
                "substrate/backside treatment, and full source-model leakage boundaries "
                "are not frozen by the source tables."
            ),
            "recommended_next_phase": (
                "Phase 3E.3B - Saha frozen-stack model provenance and no-fit adapter gate"
            ),
        },
        "forbidden_next": [
            "Do not use source-simulated Fig. 2b curves as a holdout measurement.",
            (
                "Do not tune TiN/AZO epsilon, thickness, roughness, substrate constants, "
                "scale, or offsets to Fig. 2b residuals."
            ),
            (
                "Do not run or report a TMM residual until a frozen substrate/backside "
                "model contract is recorded."
            ),
            (
                "Do not promote Saha beyond weak-within-dataset holdout without a future "
                "predeclared residual and uncertainty policy."
            ),
        ],
    }


def phase3e3a_markdown(packet: dict[str, Any]) -> str:
    decision = packet["decision"]
    reflectance = packet["table_audit"]["fig2b_reflectance"]
    epsilon = packet["table_audit"]["fig2cd_permittivity"]
    gate_review = packet["gate_review"]
    lines = [
        "# Phase 3E.3A - Saha Exported-Table Audit And Candidate Gate",
        "",
        "## Decision",
        "",
        f"- Status: `{decision['status']}`",
        f"- Claim-status ceiling: `{decision['claim_status_ceiling']}`",
        f"- Current claim label: `{decision['current_claim_label']}`",
        f"- Canonical tables ready: `{str(decision['canonical_tables_ready']).lower()}`",
        (
            "- Full no-fit TMM validation allowed: "
            f"`{str(decision['full_no_fit_tmm_validation_allowed']).lower()}`"
        ),
        f"- Stop rule triggered: `{str(decision['stop_rule_triggered']).lower()}`",
        f"- Recommended next phase: `{decision['recommended_next_phase']}`",
        "",
        decision["stop_rule_reason"],
        "",
        "## Canonical Artifacts",
        "",
    ]
    for artifact_id, artifact in packet["artifacts"].items():
        lines.extend(
            [
                f"- `{artifact_id}`: `{artifact['path']}`",
                f"  - Role: `{artifact['role']}`",
                f"  - SHA-256: `{artifact['sha256']}`",
            ]
        )
    lines.extend(
        [
            "",
            "## Fig. 2b Reflectance Audit",
            "",
            f"- Numeric rows: `{reflectance['numeric_rows']}`",
            (
                f"- Wavelength range: `{reflectance['wavelength_nm'][0]}`-"
                f"`{reflectance['wavelength_nm'][1]}` nm"
            ),
            f"- Wavelength step: `{reflectance['wavelength_step_nm']}` nm",
            (
                "- Measured Rp fraction range: "
                f"`{reflectance['measured_rp_reflectance_fraction'][0]}`-"
                f"`{reflectance['measured_rp_reflectance_fraction'][1]}`"
            ),
            (
                "- Measured Rs fraction range: "
                f"`{reflectance['measured_rs_reflectance_fraction'][0]}`-"
                f"`{reflectance['measured_rs_reflectance_fraction'][1]}`"
            ),
            f"- Unit-interval check: `{reflectance['unit_interval_check']}`",
            (
                "- Measured/source-simulated split: "
                f"`{reflectance['measured_and_source_simulated_split']}`"
            ),
            "",
            "## Fig. 2c/d Permittivity Audit",
            "",
            f"- TiN numeric rows: `{epsilon['tin']['numeric_rows']}`",
            (
                f"- TiN wavelength range: `{epsilon['tin']['wavelength_nm'][0]}`-"
                f"`{epsilon['tin']['wavelength_nm'][1]}` nm"
            ),
            f"- TiN ENZ crossings: `{epsilon['tin']['enz_wavelengths_nm']}` nm",
            f"- AZO numeric rows: `{epsilon['azo']['numeric_rows']}`",
            (
                f"- AZO wavelength range: `{epsilon['azo']['wavelength_nm'][0]}`-"
                f"`{epsilon['azo']['wavelength_nm'][1]}` nm"
            ),
            f"- AZO ENZ crossings: `{epsilon['azo']['enz_wavelengths_nm']}` nm",
            "",
            "## Gates",
            "",
        ]
    )
    for gate_id, gate in gate_review.items():
        lines.extend(
            [
                f"- `{gate_id}`: `{gate['status']}`",
                f"  - {gate['basis']}",
            ]
        )
    lines.extend(
        [
            "",
            "## Source Evidence",
            "",
            f"- Article: {packet['source_evidence']['article_url']}",
            f"- Supplementary information: {packet['source_evidence']['supplementary_pdf_url']}",
            f"- Figshare API: {packet['source_evidence']['figshare_api_url']}",
            (
                "- Figshare metadata: Fig. 2b has simulated and experimentally measured "
                "reflectance tables; Fig. 2c/d has TiN/AZO permittivity tables with "
                "thickness comments."
            ),
            "",
            "## Forbidden Next",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in packet["forbidden_next"])
    lines.append("")
    return "\n".join(lines)


def write_phase3e3a_packet(output_dir: Path, packet: dict[str, Any]) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase3e3a_saha_exported_table_audit.json"
    md_path = output_dir / "phase3e3a_saha_exported_table_audit.md"
    json_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(phase3e3a_markdown(packet), encoding="utf-8")
    return json_path, md_path
