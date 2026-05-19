"""Phase 3E.2A Wang W/WO3 non-ENZ baseline intake."""

from __future__ import annotations

import hashlib
import json
import math
import re
import zipfile
from collections.abc import Iterable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

XLSX_NS = {
    "x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "p": "http://schemas.openxmlformats.org/package/2006/relationships",
}

DEFAULT_RAW_DIR = Path("lab_data/raw/public_wang_wo3_fp_2020")
DEFAULT_METADATA_PATH = DEFAULT_RAW_DIR / "figshare_article_11154791.json"
TARGET_FILES = {
    "w_ellipsometry": "FigS1-W.xlsx",
    "wo3_ellipsometry": "FigS1-WO3.xlsx",
    "nk_constants": "FigS2-nk.xlsx",
    "fig2f_reflectance": "Fig2f-R.xlsx",
}
EXPECTED_FIG2F_THICKNESSES_NM = [152, 163, 185, 200, 215, 233, 250]

CellValue = str | float | int | bool | None


def _hashes(path: Path) -> dict[str, Any]:
    payload = path.read_bytes()
    return {
        "bytes": len(payload),
        "md5": hashlib.md5(payload).hexdigest(),
        "sha256": hashlib.sha256(payload).hexdigest(),
    }


def _column_name(cell_ref: str) -> str:
    return re.sub(r"\d+", "", cell_ref)


def _column_index(column_name: str) -> int:
    index = 0
    for char in column_name:
        index = index * 26 + ord(char.upper()) - 64
    return index


def _column_label(index: int) -> str:
    label = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        label = chr(65 + remainder) + label
    return label


def _as_float(value: CellValue) -> float | None:
    if isinstance(value, bool) or value is None:
        return None
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    return parsed if math.isfinite(parsed) else None


def _compact_value(value: CellValue) -> CellValue:
    parsed = _as_float(value)
    if parsed is None:
        return value
    if parsed.is_integer():
        return int(parsed)
    return round(parsed, 6)


def _compact_float(value: float) -> float | int:
    return int(value) if float(value).is_integer() else round(value, 6)


def _shared_strings(workbook_zip: zipfile.ZipFile) -> list[str]:
    try:
        payload = workbook_zip.read("xl/sharedStrings.xml")
    except KeyError:
        return []
    root = ElementTree.fromstring(payload)
    strings: list[str] = []
    for item in root.findall("x:si", XLSX_NS):
        parts = [text.text or "" for text in item.findall(".//x:t", XLSX_NS)]
        strings.append("".join(parts))
    return strings


def _workbook_sheet_paths(workbook_zip: zipfile.ZipFile) -> dict[str, str]:
    workbook = ElementTree.fromstring(workbook_zip.read("xl/workbook.xml"))
    relationships = ElementTree.fromstring(workbook_zip.read("xl/_rels/workbook.xml.rels"))
    relationship_targets = {
        item.attrib["Id"]: item.attrib["Target"]
        for item in relationships.findall("p:Relationship", XLSX_NS)
    }
    sheet_paths: dict[str, str] = {}
    for sheet in workbook.findall(".//x:sheet", XLSX_NS):
        relationship_id = sheet.attrib[
            "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
        ]
        target = relationship_targets[relationship_id]
        if not target.startswith("xl/"):
            target = f"xl/{target}"
        sheet_paths[sheet.attrib["name"]] = target
    return sheet_paths


def _cell_value(cell: ElementTree.Element, shared_strings: list[str]) -> CellValue:
    cell_type = cell.attrib.get("t")
    if cell_type == "inlineStr":
        return "".join(text.text or "" for text in cell.findall(".//x:t", XLSX_NS))
    value = cell.find("x:v", XLSX_NS)
    if value is None or value.text is None:
        return None
    if cell_type == "s":
        return shared_strings[int(value.text)]
    if cell_type == "b":
        return value.text == "1"
    parsed = _as_float(value.text)
    return parsed if parsed is not None else value.text


def _parse_xlsx(path: Path) -> dict[str, list[list[CellValue]]]:
    with zipfile.ZipFile(path) as workbook_zip:
        shared_strings = _shared_strings(workbook_zip)
        sheet_paths = _workbook_sheet_paths(workbook_zip)
        workbook: dict[str, list[list[CellValue]]] = {}
        for sheet_name, sheet_path in sheet_paths.items():
            root = ElementTree.fromstring(workbook_zip.read(sheet_path))
            rows_by_index: dict[int, dict[int, CellValue]] = {}
            max_row = 0
            max_column = 0
            for row in root.findall(".//x:row", XLSX_NS):
                row_index = int(row.attrib.get("r", len(rows_by_index) + 1))
                max_row = max(max_row, row_index)
                row_cells: dict[int, CellValue] = {}
                for cell in row.findall("x:c", XLSX_NS):
                    column_index = _column_index(_column_name(cell.attrib["r"]))
                    max_column = max(max_column, column_index)
                    row_cells[column_index] = _cell_value(cell, shared_strings)
                rows_by_index[row_index] = row_cells
            workbook[sheet_name] = [
                [
                    rows_by_index.get(row_index, {}).get(column_index)
                    for column_index in range(1, max_column + 1)
                ]
                for row_index in range(1, max_row + 1)
            ]
        return workbook


def _numeric_values(values: Iterable[CellValue]) -> list[float]:
    return [parsed for value in values if (parsed := _as_float(value)) is not None]


def _column_numeric_profiles(rows: list[list[CellValue]]) -> list[dict[str, Any]]:
    if not rows:
        return []
    max_columns = max((len(row) for row in rows), default=0)
    profiles = []
    for column_index in range(max_columns):
        values = [row[column_index] if column_index < len(row) else None for row in rows]
        numeric = _numeric_values(values)
        header_candidates = [
            _compact_value(row[column_index])
            for row in rows[:3]
            if column_index < len(row) and row[column_index] is not None
        ]
        profile: dict[str, Any] = {
            "column": _column_label(column_index + 1),
            "header_candidates": header_candidates,
            "numeric_count": len(numeric),
        }
        if numeric:
            profile.update(
                {
                    "min": _compact_float(min(numeric)),
                    "max": _compact_float(max(numeric)),
                    "negative_count": sum(1 for value in numeric if value < 0),
                    "above_100_count": sum(1 for value in numeric if value > 100),
                }
            )
        profiles.append(profile)
    return profiles


def _sheet_summary(rows: list[list[CellValue]]) -> dict[str, Any]:
    nonempty_rows = [row for row in rows if any(value is not None for value in row)]
    return {
        "row_count": len(rows),
        "nonempty_row_count": len(nonempty_rows),
        "column_count": max((len(row) for row in rows), default=0),
        "preview_rows": [
            [_compact_value(value) for value in row[:8]] for row in nonempty_rows[:5]
        ],
        "numeric_profiles": _column_numeric_profiles(rows),
    }


def _workbook_summary(path: Path) -> dict[str, Any]:
    workbook = _parse_xlsx(path)
    return {
        "filename": path.name,
        "local_path": str(path),
        "hashes": _hashes(path),
        "sheets": {
            sheet_name: _sheet_summary(rows) for sheet_name, rows in workbook.items()
        },
    }


def _extract_nk_sheet(rows: list[list[CellValue]]) -> dict[str, Any]:
    triples: list[tuple[float, float, float]] = []
    for row in rows:
        if len(row) < 3:
            continue
        wavelength = _as_float(row[0])
        n_value = _as_float(row[1])
        k_value = _as_float(row[2])
        if wavelength is None or n_value is None or k_value is None:
            continue
        triples.append((wavelength, n_value, k_value))
    if not triples:
        return {"present": False, "row_count": 0}
    wavelengths = [row[0] for row in triples]
    n_values = [row[1] for row in triples]
    k_values = [row[2] for row in triples]
    return {
        "present": True,
        "row_count": len(triples),
        "columns": ["wavelength_nm", "n", "k"],
        "wavelength_nm_range": [
            _compact_float(min(wavelengths)),
            _compact_float(max(wavelengths)),
        ],
        "n_range": [_compact_float(min(n_values)), _compact_float(max(n_values))],
        "k_range": [_compact_float(min(k_values)), _compact_float(max(k_values))],
        "wavelength_monotonic_increasing": all(
            current < following
            for current, following in zip(wavelengths, wavelengths[1:], strict=False)
        ),
        "first_row": [_compact_float(value) for value in triples[0]],
        "last_row": [_compact_float(value) for value in triples[-1]],
    }


def _constants_inspection(raw_dir: Path) -> dict[str, Any]:
    path = raw_dir / TARGET_FILES["nk_constants"]
    workbook = _parse_xlsx(path)
    sheets = {name: _extract_nk_sheet(rows) for name, rows in workbook.items()}
    return {
        "filename": path.name,
        "expected_sheets_present": all(sheet in sheets for sheet in ["W", "WO3"]),
        "sheet_count": len(sheets),
        "sheets": sheets,
        "interpretation": (
            "FigS2-nk.xlsx is the cleanest calibration-input source: it contains "
            "direct W and WO3 n,k tables on wavelength axes around the visible range."
        ),
    }


def _angle_labels(rows: list[list[CellValue]]) -> list[int]:
    labels: list[int] = []
    for row in rows[:3]:
        for value in row[1:]:
            parsed = _as_float(value)
            if parsed is not None and 0 < parsed < 90 and parsed.is_integer():
                labels.append(int(parsed))
    return sorted(set(labels))


def _ellipsometry_inspection(raw_dir: Path) -> dict[str, Any]:
    inspections: dict[str, Any] = {}
    for key in ["w_ellipsometry", "wo3_ellipsometry"]:
        path = raw_dir / TARGET_FILES[key]
        workbook = _parse_xlsx(path)
        sheet_info = {}
        for sheet_name, rows in workbook.items():
            sheet_info[sheet_name] = {
                "row_count": len(rows),
                "column_count": max((len(row) for row in rows), default=0),
                "angle_labels_deg": _angle_labels(rows),
                "value_columns_are_paired": max((len(row) for row in rows), default=0) == 7,
                "first_nonempty_rows": _sheet_summary(rows)["preview_rows"][:3],
            }
        inspections[path.name] = {
            "sheets": sheet_info,
            "interpretation": (
                "Workbook exposes cos/tan ellipsometry-like source-data sheets with "
                "paired columns for angle-labeled series. It source-qualifies the "
                "n,k table, but the angle labels should be reconciled before a formal "
                "modeling claim."
            ),
        }
    return inspections


def _find_thickness_row(rows: list[list[CellValue]]) -> int | None:
    best_index: int | None = None
    best_count = 0
    for index, row in enumerate(rows[:6]):
        count = 0
        for value in row[1:]:
            parsed = _as_float(value)
            if parsed is not None and 100 <= parsed <= 300 and parsed.is_integer():
                count += 1
        if count > best_count:
            best_count = count
            best_index = index
    return best_index if best_count else None


def _reflectance_pair_inspection(rows: list[list[CellValue]]) -> dict[str, Any]:
    thickness_row_index = _find_thickness_row(rows)
    if thickness_row_index is None:
        return {"present": False, "reason": "no thickness header row found"}

    thickness_row = rows[thickness_row_index]
    data_rows = rows[thickness_row_index + 1 :]
    wavelengths = [
        parsed
        for row in data_rows
        if row and (parsed := _as_float(row[0])) is not None
    ]
    pairs: list[dict[str, Any]] = []
    for column_index, value in enumerate(thickness_row[1:], start=2):
        thickness = _as_float(value)
        if thickness is None or not thickness.is_integer():
            continue
        second_column_index = column_index + 1
        first_values: list[float] = []
        second_values: list[float] = []
        for row in data_rows:
            if (
                len(row) >= column_index
                and (parsed := _as_float(row[column_index - 1])) is not None
            ):
                first_values.append(parsed)
            if len(row) >= second_column_index and (
                parsed := _as_float(row[second_column_index - 1])
            ) is not None:
                second_values.append(parsed)
        all_values = [*first_values, *second_values]
        pairs.append(
            {
                "thickness_nm": int(thickness),
                "columns": [
                    _column_label(column_index),
                    _column_label(second_column_index),
                ],
                "data_count_per_column": [len(first_values), len(second_values)],
                "value_range": (
                    [_compact_float(min(all_values)), _compact_float(max(all_values))]
                    if all_values
                    else []
                ),
                "negative_value_count": sum(1 for item in all_values if item < 0),
                "above_100_count": sum(1 for item in all_values if item > 100),
                "plain_absolute_reflectance_like": bool(all_values)
                and all(0 <= item <= 100 for item in all_values),
            }
        )
    all_pair_values = [
        value
        for pair in pairs
        for value in pair.get("value_range", [])
        if isinstance(value, int | float)
    ]
    return {
        "present": True,
        "sheet": "Sheet1",
        "thickness_header_row_1based": thickness_row_index + 1,
        "thicknesses_nm": [pair["thickness_nm"] for pair in pairs],
        "expected_thicknesses_match": [pair["thickness_nm"] for pair in pairs]
        == EXPECTED_FIG2F_THICKNESSES_NM,
        "wavelength_nm_range": (
            [_compact_float(min(wavelengths)), _compact_float(max(wavelengths))]
            if wavelengths
            else []
        ),
        "wavelength_monotonic_descending": all(
            current > following
            for current, following in zip(wavelengths, wavelengths[1:], strict=False)
        ),
        "pairs": pairs,
        "contains_nonphysical_plot_values": any(
            not pair["plain_absolute_reflectance_like"] for pair in pairs
        ),
        "global_value_range": (
            [_compact_float(min(all_pair_values)), _compact_float(max(all_pair_values))]
            if all_pair_values
            else []
        ),
        "measured_vs_simulated_assignment": "unlabeled_in_workbook",
        "semantics_status": "offset_plot_traces_not_plain_absolute_reflectance",
    }


def _reflectance_inspection(raw_dir: Path) -> dict[str, Any]:
    path = raw_dir / TARGET_FILES["fig2f_reflectance"]
    workbook = _parse_xlsx(path)
    rows = workbook.get("Sheet1", [])
    return {
        "filename": path.name,
        "inspection": _reflectance_pair_inspection(rows),
        "interpretation": (
            "Fig2f-R.xlsx is machine-readable but not immediately usable as an "
            "absolute reflectance holdout: the paired traces are unlabeled in the "
            "workbook and contain large negative offsets consistent with plotted "
            "stacked traces."
        ),
    }


def _figshare_file_summary(raw_dir: Path, item: dict[str, Any]) -> dict[str, Any]:
    path = raw_dir / item.get("name", "")
    summary = {
        "figshare_file_id": item.get("id"),
        "name": item.get("name"),
        "download_url": item.get("download_url"),
        "figshare_bytes": item.get("size"),
        "supplied_md5": item.get("supplied_md5"),
        "downloaded": path.exists(),
    }
    if path.exists():
        hashes = _hashes(path)
        summary.update({"local_path": str(path), **hashes})
        summary["md5_matches_figshare"] = hashes["md5"] == item.get("supplied_md5")
    return summary


def build_phase3e2a_packet(metadata_path: Path, raw_dir: Path) -> dict[str, Any]:
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    missing = [filename for filename in TARGET_FILES.values() if not (raw_dir / filename).exists()]
    if missing:
        raise FileNotFoundError(f"missing Wang W/WO3 source files: {', '.join(missing)}")

    file_summaries = [
        _figshare_file_summary(raw_dir, item)
        for item in metadata.get("files", [])
        if item.get("name") in TARGET_FILES.values()
    ]
    workbook_summaries = {
        filename: _workbook_summary(raw_dir / filename) for filename in TARGET_FILES.values()
    }
    downloaded_md5_match = all(
        bool(item.get("md5_matches_figshare")) for item in file_summaries
    )
    constants = _constants_inspection(raw_dir)
    reflectance = _reflectance_inspection(raw_dir)

    return {
        "phase_id": "Phase 3E.2A",
        "title": "Wang W/WO3 Non-ENZ Baseline Intake",
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "inputs": {"metadata_path": str(metadata_path), "raw_dir": str(raw_dir)},
        "source": {
            "title": metadata.get("title"),
            "doi": metadata.get("doi"),
            "figshare_url": metadata.get("figshare_url") or metadata.get("url_public_html"),
            "api_url": metadata.get("url_public_api") or metadata.get("url"),
            "license": metadata.get("license", {}),
            "status": metadata.get("status"),
            "is_public": metadata.get("is_public"),
            "published_date": metadata.get("published_date"),
            "file_count": len(metadata.get("files", [])),
            "browse_page_observation": (
                "Figshare page states characteristic-matrix modeling and reports "
                "UV-vis / angle-resolved reflection measurements over 350-850 nm."
            ),
        },
        "files": file_summaries,
        "workbooks": workbook_summaries,
        "target_inspection": {
            "constants": constants,
            "ellipsometry_source_data": _ellipsometry_inspection(raw_dir),
            "fig2f_reflectance": reflectance,
        },
        "decision": {
            "status": "non_enz_baseline_source_data_snapshotted_semantics_partial",
            "download_integrity": (
                "selected_downloaded_md5_match" if downloaded_md5_match else "md5_mismatch"
            ),
            "non_enz_planar_tmm_baseline_intake_ready": True,
            "phase4_enz_ready": False,
            "can_feed_serious_core": False,
            "can_promote_calibrated_linear_evidence": False,
            "claim_label": "candidate_non_enz_tmm_baseline_source_data_semantics_partial",
            "claim_status_ceiling": "non_enz_planar_tmm_baseline_candidate",
            "reason": (
                "The package has public source-data spreadsheets, direct W/WO3 n,k "
                "tables, and a W/WO3 thickness-series reflectance workbook. It is not "
                "ENZ evidence, and Fig. 2f reflectance semantics are not clean enough "
                "for a no-fit validation residual yet."
            ),
            "recommended_next_phase": (
                "Phase 3E.2B - Wang Fig. 2f semantics and no-fit baseline plan"
            ),
        },
        "blockers": [
            "W/WO3 Fabry-Perot is a non-ENZ planar TMM baseline, not ENZ calibrated evidence.",
            (
                "Fig2f-R.xlsx contains vertically offset/nonphysical plotted traces "
                "rather than plain 0-100 reflectance columns."
            ),
            "Fig2f-R.xlsx pairs are not labeled as measured versus simulated inside the workbook.",
            (
                "Absolute reflectance normalization and holdout-not-used-for-fit status "
                "are not proven by the selected spreadsheets alone."
            ),
            (
                "Ellipsometry source workbook angle labels should be reconciled with "
                "article/supplement method wording before formal modeling."
            ),
        ],
        "next_actions": [
            (
                "Inspect the article figure/caption and any supplementary text to recover "
                "the Fig. 2f vertical-offset convention."
            ),
            (
                "Identify which column in each Fig2f-R.xlsx pair is measured and which "
                "is simulated before computing residuals."
            ),
            (
                "If offsets and measured columns can be source-backed, build a no-fit "
                "TMM baseline using FigS2-nk.xlsx constants only."
            ),
            (
                "Keep Saha TiN/AZO as the ENZ backup; do not let Wang count as the "
                "first ENZ Phase 4 evidence."
            ),
        ],
    }


def phase3e2a_markdown(packet: dict[str, Any]) -> str:
    decision = packet["decision"]
    source = packet["source"]
    constants = packet["target_inspection"]["constants"]["sheets"]
    fig2f = packet["target_inspection"]["fig2f_reflectance"]["inspection"]
    rows = [
        "| File | Bytes | MD5 Match |",
        "| --- | ---: | --- |",
    ]
    for item in packet["files"]:
        rows.append(
            f"| `{item['name']}` | `{item.get('bytes', 'n/a')}` | "
            f"`{str(item.get('md5_matches_figshare')).lower()}` |"
        )

    constant_rows = [
        "| Sheet | Rows | Wavelength Range | n Range | k Range |",
        "| --- | ---: | --- | --- | --- |",
    ]
    for sheet_name in ["WO3", "W"]:
        item = constants.get(sheet_name, {})
        constant_rows.append(
            f"| `{sheet_name}` | `{item.get('row_count')}` | "
            f"`{item.get('wavelength_nm_range')}` | `{item.get('n_range')}` | "
            f"`{item.get('k_range')}` |"
        )

    return "\n".join(
        [
            "# Phase 3E.2A - Wang W/WO3 Non-ENZ Baseline Intake",
            "",
            "## Decision",
            "",
            f"- Status: `{decision['status']}`",
            f"- Claim label: `{decision['claim_label']}`",
            f"- Claim ceiling: `{decision['claim_status_ceiling']}`",
            (
                "- Non-ENZ baseline intake ready: "
                f"`{decision['non_enz_planar_tmm_baseline_intake_ready']}`"
            ),
            f"- Phase 4 ENZ ready: `{decision['phase4_enz_ready']}`",
            f"- Can feed serious core: `{decision['can_feed_serious_core']}`",
            (
                "- Can promote calibrated evidence: "
                f"`{decision['can_promote_calibrated_linear_evidence']}`"
            ),
            f"- Download integrity: `{decision['download_integrity']}`",
            f"- Recommended next phase: `{decision['recommended_next_phase']}`",
            "",
            decision["reason"],
            "",
            "## Source",
            "",
            f"- Title: `{source['title']}`",
            f"- DOI: `{source['doi']}`",
            f"- Figshare URL: `{source['figshare_url']}`",
            f"- Public: `{source['is_public']}`",
            f"- License: `{source['license'].get('name')}`",
            f"- File count in source package: `{source['file_count']}`",
            "",
            "## Selected Files",
            "",
            *rows,
            "",
            "## Constants",
            "",
            *constant_rows,
            "",
            "## Fig. 2f Reflectance Workbook",
            "",
            f"- Semantics status: `{fig2f.get('semantics_status')}`",
            f"- Thicknesses: `{fig2f.get('thicknesses_nm')}`",
            f"- Expected thicknesses match: `{fig2f.get('expected_thicknesses_match')}`",
            f"- Wavelength range: `{fig2f.get('wavelength_nm_range')}` nm",
            f"- Wavelength axis descending: `{fig2f.get('wavelength_monotonic_descending')}`",
            f"- Measured/simulated assignment: `{fig2f.get('measured_vs_simulated_assignment')}`",
            (
                "- Contains nonphysical plot values: "
                f"`{fig2f.get('contains_nonphysical_plot_values')}`"
            ),
            "",
            "## Blockers",
            "",
            *[f"- {item}" for item in packet["blockers"]],
            "",
            "## Next Actions",
            "",
            *[f"- {item}" for item in packet["next_actions"]],
            "",
        ]
    )


def write_phase3e2a_packet(output_dir: Path, packet: dict[str, Any]) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase3e2a_wang_wo3_baseline_intake.json"
    md_path = output_dir / "phase3e2a_wang_wo3_baseline_intake.md"
    json_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(phase3e2a_markdown(packet), encoding="utf-8")
    return json_path, md_path
