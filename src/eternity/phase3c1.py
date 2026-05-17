"""Phase 3C.1 St Andrews TiN public-dataset pairing utilities."""

from __future__ import annotations

import hashlib
import json
import math
import re
import zipfile
from io import BytesIO
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

NS = {"x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

RT_MEMBER = "TiN-data_Pure/RT.xlsx"
SELECTED_EPSILON_MEMBER = "TiN-data_Pure/Ellipsometry/50nm-MTiN-50c.txt"
CANDIDATE_EPSILON_MEMBERS = [
    "TiN-data_Pure/Ellipsometry/50nm-MTiN-40c.txt",
    SELECTED_EPSILON_MEMBER,
    "TiN-data_Pure/Ellipsometry/50nm-MTiN-60c.txt",
    "TiN-data_Pure/Ellipsometry/50 nm-MTiN-Anntemp-50C.txt",
    "TiN-data_Pure/Ellipsometry/50nm TiN-RoomTemp.txt",
]


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _write_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def _canonical_text_payload(payload: bytes) -> bytes:
    text = payload.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    return ("\n".join(lines) + "\n").encode("utf-8")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _artifact_metadata(path: Path, source_member: str) -> dict[str, Any]:
    return {
        "path": str(path),
        "bytes": path.stat().st_size,
        "sha256": _sha256_file(path),
        "source_member": source_member,
    }


def _shared_strings(workbook_zip: zipfile.ZipFile) -> list[str]:
    try:
        payload = workbook_zip.read("xl/sharedStrings.xml")
    except KeyError:
        return []
    root = ElementTree.fromstring(payload)
    strings: list[str] = []
    for item in root.findall("x:si", NS):
        parts = [text.text or "" for text in item.findall(".//x:t", NS)]
        strings.append("".join(parts))
    return strings


def _column_name(cell_ref: str) -> str:
    return re.sub(r"\d+", "", cell_ref)


def _cell_value(cell: ElementTree.Element, shared_strings: list[str]) -> str | None:
    value = cell.find("x:v", NS)
    if value is None or value.text is None:
        return None
    if cell.attrib.get("t") == "s":
        return shared_strings[int(value.text)]
    return value.text


def _parse_float(value: str | None) -> float | None:
    if value is None:
        return None
    try:
        parsed = float(value)
    except ValueError:
        return None
    return parsed if math.isfinite(parsed) else None


def _parse_rt_xlsx(payload: bytes) -> dict[str, list[tuple[float, float]]]:
    with zipfile.ZipFile(BytesIO(payload)) as workbook_zip:
        shared_strings = _shared_strings(workbook_zip)
        sheet = ElementTree.fromstring(workbook_zip.read("xl/worksheets/sheet1.xml"))

    rows: dict[str, list[tuple[float, float]]] = {
        "transmittance": [],
        "reflectance": [],
    }
    for row in sheet.findall(".//x:row", NS):
        cells: dict[str, str | None] = {}
        for cell in row.findall("x:c", NS):
            cells[_column_name(cell.attrib["r"])] = _cell_value(cell, shared_strings)
        t_wavelength = _parse_float(cells.get("A"))
        transmittance = _parse_float(cells.get("B"))
        r_wavelength = _parse_float(cells.get("D"))
        reflectance = _parse_float(cells.get("E"))
        if t_wavelength is not None and transmittance is not None:
            rows["transmittance"].append((t_wavelength, transmittance))
        if r_wavelength is not None and reflectance is not None:
            rows["reflectance"].append((r_wavelength, reflectance))

    for name, values in rows.items():
        _validate_spectrum_rows(values, name)
    return rows


def _validate_spectrum_rows(rows: list[tuple[float, float]], name: str) -> None:
    if len(rows) < 2:
        raise ValueError(f"{name} must contain at least two rows")
    wavelengths = [row[0] for row in rows]
    values = [row[1] for row in rows]
    if any(not math.isfinite(value) for value in [*wavelengths, *values]):
        raise ValueError(f"{name} contains non-finite values")
    if any(
        next_value <= value
        for value, next_value in zip(wavelengths, wavelengths[1:], strict=False)
    ):
        raise ValueError(f"{name} wavelength axis must be strictly increasing")


def _write_spectrum_csv(path: Path, channel: str, rows: list[tuple[float, float]]) -> None:
    lines = [f"wavelength_nm,{channel}"]
    lines.extend(f"{wavelength:.8g},{value:.8g}" for wavelength, value in rows)
    _write_text(path, "\n".join(lines) + "\n")


def _numeric_rows_from_epsilon_text(text: str) -> list[tuple[float, float, float]]:
    rows: list[tuple[float, float, float]] = []
    for line in text.splitlines():
        fields = line.replace(",", ".").split()
        if len(fields) < 3:
            continue
        try:
            rows.append((float(fields[0]), float(fields[1]), float(fields[2])))
        except ValueError:
            continue
    if len(rows) < 2:
        raise ValueError("epsilon table must contain at least two rows")
    wavelengths = [row[0] for row in rows]
    if any(
        next_value <= value
        for value, next_value in zip(wavelengths, wavelengths[1:], strict=False)
    ):
        raise ValueError("epsilon wavelength axis must be strictly increasing")
    return rows


def _enz_crossings(rows: list[tuple[float, float, float]]) -> list[float]:
    crossings: list[float] = []
    for left, right in zip(rows, rows[1:], strict=False):
        wl_left, e1_left, _ = left
        wl_right, e1_right, _ = right
        if e1_left == 0:
            crossings.append(round(wl_left, 3))
        elif e1_left * e1_right < 0:
            fraction = -e1_left / (e1_right - e1_left)
            crossings.append(round(wl_left + fraction * (wl_right - wl_left), 3))
    return crossings


def _epsilon_summary(member: str, payload: bytes) -> dict[str, Any]:
    text = payload.decode("utf-8-sig")
    rows = _numeric_rows_from_epsilon_text(text)
    wavelengths = [row[0] for row in rows]
    e1 = [row[1] for row in rows]
    e2 = [row[2] for row in rows]
    return {
        "member": member,
        "rows": len(rows),
        "wavelength_min_nm": min(wavelengths),
        "wavelength_max_nm": max(wavelengths),
        "epsilon_real_min": min(e1),
        "epsilon_real_max": max(e1),
        "epsilon_imag_min": min(e2),
        "epsilon_imag_max": max(e2),
        "enz_wavelengths_nm": _enz_crossings(rows),
        "passivity_check": "pass" if min(e2) > 0 else "fail",
        "sha256": _sha256_bytes(payload),
        "bytes": len(payload),
    }


def _spectrum_summary(
    rows: list[tuple[float, float]],
    window: tuple[float, float],
) -> dict[str, Any]:
    lower, upper = window
    window_rows = [row for row in rows if lower <= row[0] <= upper]
    if not window_rows:
        raise ValueError("spectrum has no rows in requested paper window")
    min_row = min(window_rows, key=lambda row: row[1])
    max_row = max(window_rows, key=lambda row: row[1])
    return {
        "rows_total": len(rows),
        "wavelength_nm_total_min": min(row[0] for row in rows),
        "wavelength_nm_total_max": max(row[0] for row in rows),
        "paper_window_nm": [lower, upper],
        "rows_in_paper_window": len(window_rows),
        "min_in_paper_window": {"wavelength_nm": min_row[0], "value": min_row[1]},
        "max_in_paper_window": {"wavelength_nm": max_row[0], "value": max_row[1]},
    }


def build_phase3c1_packet(zip_path: Path, raw_output_dir: Path) -> dict[str, Any]:
    """Extract deterministic Phase 3C.1 raw-member snapshots and report pairing status."""

    archive_sha256 = _sha256_file(zip_path)
    with zipfile.ZipFile(zip_path) as archive:
        rt_payload = archive.read(RT_MEMBER)
        epsilon_payload = archive.read(SELECTED_EPSILON_MEMBER)
        candidates = {
            member: _epsilon_summary(member, archive.read(member))
            for member in CANDIDATE_EPSILON_MEMBERS
        }
    selected_epsilon_payload = _canonical_text_payload(epsilon_payload)

    rt_rows = _parse_rt_xlsx(rt_payload)
    reflectance_csv = raw_output_dir / "standrews_tin_50nm_reflectance.csv"
    transmittance_csv = raw_output_dir / "standrews_tin_50nm_transmittance.csv"
    selected_epsilon = raw_output_dir / "standrews_tin_50nm_50c_epsilon.txt"
    _write_spectrum_csv(reflectance_csv, "reflectance", rt_rows["reflectance"])
    _write_spectrum_csv(transmittance_csv, "transmittance", rt_rows["transmittance"])
    _write_bytes(selected_epsilon, selected_epsilon_payload)

    reflectance_summary = _spectrum_summary(rt_rows["reflectance"], (400.0, 1000.0))
    transmittance_summary = _spectrum_summary(rt_rows["transmittance"], (400.0, 1000.0))
    reflectance_min = reflectance_summary["min_in_paper_window"]
    figure4_match = (
        abs(reflectance_min["wavelength_nm"] - 540.0) <= 5.0
        and 0.18 <= reflectance_min["value"] <= 0.23
    )
    pairing_status = (
        "candidate_supported_reflectance_only" if figure4_match else "blocked_ambiguous"
    )

    return {
        "phase_id": "Phase 3C.1",
        "title": "St Andrews TiN pairing and fail-closed validation candidate",
        "date": "2026-05-17",
        "source_archive": {
            "path": str(zip_path),
            "sha256": archive_sha256,
            "rt_member": RT_MEMBER,
            "selected_epsilon_member": SELECTED_EPSILON_MEMBER,
        },
        "generated_artifacts": {
            "reflectance_csv": _artifact_metadata(reflectance_csv, RT_MEMBER),
            "transmittance_csv": _artifact_metadata(transmittance_csv, RT_MEMBER),
            "selected_epsilon": _artifact_metadata(selected_epsilon, SELECTED_EPSILON_MEMBER),
        },
        "rt_summary": {
            "reflectance": reflectance_summary,
            "transmittance": transmittance_summary,
        },
        "candidate_epsilon_tables": list(candidates.values()),
        "selected_pairing": {
            "sample_id": "public_standrews_tin_50nm_50c",
            "pairing_status": pairing_status,
            "selected_material_member": SELECTED_EPSILON_MEMBER,
            "holdout_member": RT_MEMBER,
            "evidence": [
                "The linked paper identifies Figure 4 as 50 nm TiN on glass at normal incidence.",
                "The linked paper says reflectance reaches about 20% near 540 nm.",
                (
                    "RT.xlsx reflectance minimum in 400-1000 nm is "
                    f"{reflectance_min['value']:.5g} at {reflectance_min['wavelength_nm']:.2f} nm."
                ),
                (
                    "The 50nm-MTiN-50c epsilon table is the best default material input "
                    "because the paper identifies the 50 C film as the optimized 50 nm TiN sample."
                ),
            ],
            "caveats": [
                "RT.xlsx itself does not name the annealing condition.",
                (
                    "Transmittance scaling/noise does not yet cleanly match the paper text, "
                    "so transmittance stays auxiliary."
                ),
                "No residual thresholds are approved before this first validation-candidate run.",
            ],
        },
        "decision": {
            "status": pairing_status,
            "can_feed_serious_core": False,
            "can_promote_calibrated_linear_evidence": False,
        },
        "policy": {
            "can_feed_serious_core": False,
            "claim_status_ceiling": "weak_within_dataset_holdout",
            "normalization_status": "reflectance_fraction_paper_consistent_not_promotion_approved",
            "threshold_status": "blocked_not_predeclared",
            "no_fit_leakage_status": "prepared_for_runner_gate",
            "calibrated_linear_evidence_allowed": False,
        },
        "next_phase": "Phase 3C.2 threshold/pro-checkpoint only if residual policy is requested",
    }


def build_phase3c1_packet_from_paths(zip_path: Path, raw_output_dir: Path) -> dict[str, Any]:
    if not zip_path.exists():
        raise FileNotFoundError(zip_path)
    return build_phase3c1_packet(zip_path, raw_output_dir)


def _render_markdown(packet: dict[str, Any]) -> str:
    pairing = packet["selected_pairing"]
    reflectance = packet["rt_summary"]["reflectance"]["min_in_paper_window"]
    transmittance = packet["rt_summary"]["transmittance"]
    transmittance_min = transmittance["min_in_paper_window"]["value"]
    transmittance_max = transmittance["max_in_paper_window"]["value"]
    selected = next(
        table
        for table in packet["candidate_epsilon_tables"]
        if table["member"] == packet["source_archive"]["selected_epsilon_member"]
    )
    reflectance_line = (
        "The extracted `RT.xlsx` reflectance minimum in 400-1000 nm is "
        f"`{reflectance['value']:.5g}` at `{reflectance['wavelength_nm']:.2f} nm`."
    )
    selected_line = (
        "The selected 50 C epsilon table has ENZ crossings "
        f"`{selected['enz_wavelengths_nm']}` and passivity "
        f"`{selected['passivity_check']}`."
    )
    transmittance_line = (
        "`RT.xlsx` does not independently label the annealing condition. "
        "Transmittance remains auxiliary: its 400-1000 nm range is "
        f"`{transmittance_min:.5g}` to `{transmittance_max:.5g}` and requires "
        "scaling/noise review before it becomes a clean absolute channel."
    )
    return f"""# Phase 3C.1 - St Andrews TiN Pairing

Date: {packet["date"]}

## Decision

- Pairing status: `{pairing["pairing_status"]}`
- Selected sample: `{pairing["sample_id"]}`
- Selected epsilon member: `{pairing["selected_material_member"]}`
- Holdout member: `{pairing["holdout_member"]}`
- Claim ceiling: `{packet["policy"]["claim_status_ceiling"]}`
- Can feed serious core: `{str(packet["policy"]["can_feed_serious_core"]).lower()}`

## Evidence

- The paper identifies Figure 4 as 50 nm TiN on glass at normal incidence.
- The paper describes a reflectance minimum of about 20% near 540 nm.
- {reflectance_line}
- {selected_line}

## Caveats

- {transmittance_line}
- Thresholds are not predeclared, so calibrated promotion is blocked.

## Generated Raw-Member Snapshots

- `{packet["generated_artifacts"]["reflectance_csv"]["path"]}`
- `{packet["generated_artifacts"]["transmittance_csv"]["path"]}`
- `{packet["generated_artifacts"]["selected_epsilon"]["path"]}`
"""


def write_phase3c1_packet(output_dir: Path, packet: dict[str, Any]) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase3c1_standrews_tin_pairing.json"
    md_path = output_dir / "phase3c1_standrews_tin_pairing.md"
    _write_text(json_path, json.dumps(packet, indent=2, sort_keys=True) + "\n")
    _write_text(md_path, _render_markdown(packet))
    return json_path, md_path
