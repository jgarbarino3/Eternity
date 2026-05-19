"""Phase 3E.2B Wang Fig. 2f semantics audit."""

from __future__ import annotations

import json
import zipfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from eternity.phase3e2a import (
    DEFAULT_RAW_DIR,
    EXPECTED_FIG2F_THICKNESSES_NM,
    TARGET_FILES,
    _as_float,
    _column_label,
    _parse_xlsx,
)

ARTICLE_URL = "https://www.nature.com/articles/s41467-019-14194-y"
ARTICLE_PDF_URL = "https://www.nature.com/articles/s41467-019-14194-y.pdf"
SI_PDF_URL = (
    "https://static-content.springer.com/esm/"
    "art%3A10.1038%2Fs41467-019-14194-y/"
    "MediaObjects/41467_2019_14194_MOESM1_ESM.pdf"
)
FIGSHARE_URL = (
    "https://figshare.com/articles/dataset/"
    "Towards_Full-colour_Tunability_of_Inorganic_Electrochromic_Devices_Using_"
    "Ultracompact_Fabry-Perot_Nanocavities/11154791"
)


def _archive_features(path: Path) -> dict[str, Any]:
    with zipfile.ZipFile(path) as workbook_zip:
        names = workbook_zip.namelist()
        shared_strings = ""
        try:
            shared_strings = workbook_zip.read("xl/sharedStrings.xml").decode("utf-8")
        except KeyError:
            shared_strings = ""
    return {
        "has_chart_xml": any(name.startswith("xl/charts/") for name in names),
        "has_drawing_xml": any(name.startswith("xl/drawings/") for name in names),
        "has_comment_xml": any("comments" in name for name in names),
        "has_table_xml": any(name.startswith("xl/tables/") for name in names),
        "has_media": any(name.startswith("xl/media/") for name in names),
        "shared_strings_preview": shared_strings[:240],
        "member_count": len(names),
        "members": names,
    }


def _numeric_pair_values(
    rows: list[list[Any]], first_column_index: int, second_column_index: int
) -> list[tuple[float, float, float]]:
    values: list[tuple[float, float, float]] = []
    for row in rows[3:]:
        if len(row) <= max(first_column_index, second_column_index):
            continue
        wavelength = _as_float(row[0])
        first_value = _as_float(row[first_column_index])
        second_value = _as_float(row[second_column_index])
        if wavelength is None or first_value is None or second_value is None:
            continue
        values.append((wavelength, first_value, second_value))
    return values


def _mean_abs_first_difference(values: list[float]) -> float | None:
    if len(values) < 2:
        return None
    return sum(
        abs(current - following)
        for current, following in zip(values, values[1:], strict=False)
    ) / (len(values) - 1)


def _round_float(value: float | None, digits: int = 6) -> float | None:
    if value is None:
        return None
    return round(value, digits)


def _fig2f_layout(raw_dir: Path) -> dict[str, Any]:
    path = raw_dir / TARGET_FILES["fig2f_reflectance"]
    workbook = _parse_xlsx(path)
    rows = workbook["Sheet1"]
    thicknesses = [
        int(value)
        for index in range(1, 15, 2)
        if (value := _as_float(rows[1][index])) is not None
    ]
    pairs: list[dict[str, Any]] = []
    for pair_index, thickness_nm in enumerate(thicknesses):
        first_column_index = 1 + 2 * pair_index
        second_column_index = 2 + 2 * pair_index
        offset_added_percent = 70 * (len(thicknesses) - 1 - pair_index)
        values = _numeric_pair_values(rows, first_column_index, second_column_index)
        first_raw = [item[1] for item in values]
        second_raw = [item[2] for item in values]
        first_deoffseted = [value + offset_added_percent for value in first_raw]
        second_deoffseted = [value + offset_added_percent for value in second_raw]
        all_deoffseted = first_deoffseted + second_deoffseted
        pairs.append(
            {
                "thickness_nm": thickness_nm,
                "source_columns": {
                    "wavelength": "A",
                    "first_y": _column_label(first_column_index + 1),
                    "second_y": _column_label(second_column_index + 1),
                },
                "offset_added_percent": offset_added_percent,
                "point_count": len(values),
                "wavelength_nm_range": [
                    min(item[0] for item in values),
                    max(item[0] for item in values),
                ],
                "raw_y_range": [min(first_raw + second_raw), max(first_raw + second_raw)],
                "deoffseted_y_range_percent": [
                    min(all_deoffseted),
                    max(all_deoffseted),
                ],
                "first_y_mean_abs_step": _round_float(
                    _mean_abs_first_difference(first_raw)
                ),
                "second_y_mean_abs_step": _round_float(
                    _mean_abs_first_difference(second_raw)
                ),
                "inferred_first_y_is_measured": True,
                "inferred_second_y_is_simulated": True,
            }
        )
    return {
        "sheet_name": "Sheet1",
        "row_count": len(rows),
        "column_count": max((len(row) for row in rows), default=0),
        "thicknesses_nm": thicknesses,
        "expected_thicknesses_match": thicknesses == EXPECTED_FIG2F_THICKNESSES_NM,
        "wavelength_axis": {
            "column": "A",
            "direction": "descending",
            "range_nm": [
                min(
                    value
                    for row in rows
                    if (value := _as_float(row[0] if row else None)) is not None
                ),
                max(
                    value
                    for row in rows
                    if (value := _as_float(row[0] if row else None)) is not None
                ),
            ],
        },
        "pairs": pairs,
        "offset_rule": {
            "status": "source_figure_encoded_not_workbook_labeled",
            "added_offsets_percent_by_thickness": {
                str(pair["thickness_nm"]): pair["offset_added_percent"] for pair in pairs
            },
            "rule": (
                "add 70 percent reflectance steps from 420 to 0 across the seven "
                "stacked thickness groups"
            ),
            "all_deoffseted_ranges_are_reflectance_like_percent": all(
                pair["deoffseted_y_range_percent"][0] >= 0
                and pair["deoffseted_y_range_percent"][1] <= 70
                for pair in pairs
            ),
        },
        "measured_simulated_assignment": {
            "workbook_has_explicit_labels": False,
            "inferred_measured_column": "first_y_column_of_each_thickness_pair",
            "inferred_simulated_column": "second_y_column_of_each_thickness_pair",
            "basis": [
                "article caption separates simulated dashed and measured solid traces",
                "paired columns are not labeled in the workbook",
                (
                    "first y columns have visibly noisier point-to-point structure "
                    "than second y columns"
                ),
            ],
        },
    }


def build_phase3e2b_packet(raw_dir: Path = DEFAULT_RAW_DIR) -> dict[str, Any]:
    fig2f_path = raw_dir / TARGET_FILES["fig2f_reflectance"]
    if not fig2f_path.exists():
        raise FileNotFoundError(fig2f_path)
    archive_features = _archive_features(fig2f_path)
    layout = _fig2f_layout(raw_dir)
    return {
        "phase_id": "Phase 3E.2B",
        "title": "Wang Fig. 2f Semantics And No-Fit Baseline Plan",
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "inputs": {
            "raw_dir": str(raw_dir),
            "fig2f_workbook": str(fig2f_path),
            "article_url": ARTICLE_URL,
            "article_pdf_url": ARTICLE_PDF_URL,
            "supplementary_pdf_url": SI_PDF_URL,
            "figshare_url": FIGSHARE_URL,
        },
        "source_evidence": {
            "article": [
                "Figure 2f is described as simulated dashed lines and measured solid lines.",
                "The thickness series is 152, 163, 185, 200, 215, 233, and 250 nm WO3.",
                (
                    "The paper text says the underlying metallic W layer is fixed at "
                    "100 nm for the calculated thickness sweep."
                ),
            ],
            "supplementary_information": [
                (
                    "W and WO3 optical constants are derived from spectroscopic "
                    "ellipsometry on single-layer films."
                ),
                (
                    "The supplementary methods describe characteristic-matrix "
                    "reflectance/transmittance calculations."
                ),
                "The supplementary methods state normal incidence is used for the study.",
                (
                    "FDTD simulations use the W and WO3 optical constants shown in "
                    "Supplementary Figure 2."
                ),
            ],
            "figshare": [
                "The public source-data package contains Fig2f-R.xlsx and FigS2-nk.xlsx.",
            ],
        },
        "workbook_archive_features": archive_features,
        "fig2f_layout": layout,
        "decision": {
            "status": "source_backed_offsets_inferred_columns_not_source_labeled",
            "full_no_fit_tmm_validation_allowed": False,
            "bounded_deoffset_reproduction_fixture_allowed": True,
            "claim_status_ceiling": "literature_reproduction_fixture",
            "phase4_candidate": False,
            "phase4_enz_ready": False,
            "reason": (
                "The source paper backs the measured/simulated figure semantics and the "
                "SI backs the model inputs, but Fig2f-R.xlsx has no chart XML, no series "
                "labels, and no workbook-level measured/simulated headers. A de-offseted "
                "reproduction fixture is honest; a clean no-fit validation residual is not."
            ),
            "recommended_next_phase": (
                "Phase 3E.2C - Wang bounded de-offseted reproduction fixture"
            ),
        },
        "guardrails": [
            "Do not use Wang as ENZ evidence.",
            "Do not count de-offseting as experimental calibration.",
            "Do not promote inferred measured/simulated columns to source-labeled holdout columns.",
            "Use residuals only as source-data reproduction diagnostics.",
        ],
    }


def phase3e2b_markdown(packet: dict[str, Any]) -> str:
    decision = packet["decision"]
    layout = packet["fig2f_layout"]
    rows = [
        (
            "| Thickness nm | Columns | Offset added percent | De-offseted range "
            "percent | Assignment |"
        ),
        "| --- | --- | ---: | --- | --- |",
    ]
    for pair in layout["pairs"]:
        columns = pair["source_columns"]
        value_range = pair["deoffseted_y_range_percent"]
        rows.append(
            "| "
            + str(pair["thickness_nm"])
            + " | "
            + columns["first_y"]
            + "/"
            + columns["second_y"]
            + " | "
            + str(pair["offset_added_percent"])
            + " | "
            + f"{value_range[0]:.3f} to {value_range[1]:.3f}"
            + " | first=inferred measured, second=inferred simulated |"
        )
    return "\n".join(
        [
            "# Phase 3E.2B - Wang Fig. 2f Semantics Audit",
            "",
            "## Decision",
            "",
            f"- Status: `{decision['status']}`",
            (
                "- Full no-fit TMM validation allowed: "
                f"`{decision['full_no_fit_tmm_validation_allowed']}`"
            ),
            (
                "- Bounded de-offset reproduction fixture allowed: "
                f"`{decision['bounded_deoffset_reproduction_fixture_allowed']}`"
            ),
            f"- Claim-status ceiling: `{decision['claim_status_ceiling']}`",
            f"- Recommended next phase: `{decision['recommended_next_phase']}`",
            "",
            decision["reason"],
            "",
            "## Source Evidence",
            "",
            "- Article URL: "
            + packet["inputs"]["article_url"],
            "- Supplementary PDF URL: "
            + packet["inputs"]["supplementary_pdf_url"],
            "- Figshare URL: "
            + packet["inputs"]["figshare_url"],
            "",
            "The article backs Fig. 2f as measured solid traces and simulated dashed traces. "
            "The supplementary information backs ellipsometry-derived W/WO3 constants, "
            "normal-incidence characteristic-matrix calculations, and FDTD simulation inputs.",
            "",
            "## Workbook Findings",
            "",
            f"- Chart XML present: `{packet['workbook_archive_features']['has_chart_xml']}`",
            f"- Drawing XML present: `{packet['workbook_archive_features']['has_drawing_xml']}`",
            f"- Comments present: `{packet['workbook_archive_features']['has_comment_xml']}`",
            f"- Thicknesses: `{layout['thicknesses_nm']}`",
            f"- Expected thicknesses match: `{layout['expected_thicknesses_match']}`",
            f"- Offset rule status: `{layout['offset_rule']['status']}`",
            "",
            *rows,
            "",
            "## Guardrails",
            "",
            *["- " + item for item in packet["guardrails"]],
            "",
        ]
    )


def write_phase3e2b_packet(output_dir: Path, packet: dict[str, Any]) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase3e2b_wang_fig2f_semantics_audit.json"
    md_path = output_dir / "phase3e2b_wang_fig2f_semantics_audit.md"
    json_path.write_text(json.dumps(packet, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(phase3e2b_markdown(packet), encoding="utf-8")
    return json_path, md_path
