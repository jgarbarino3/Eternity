"""Phase 3D.2 Saha TiN/AZO Figshare source-data intake."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import shutil
import struct
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
PNG_END = b"IEND\xaeB`\x82"
TARGET_FILES = {
    "fig2b_reflectance": "Source data for Fig 2b.opju",
    "fig2cd_permittivity": "Source data for Fig 2cd.opju",
}
RELEVANT_LABEL_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        "wavelength",
        "measured",
        "simulated",
        "permittivity",
        "film thickness",
        "TiN",
        "AZO",
        "50 deg",
    ]
]


def _hashes(path: Path) -> dict[str, Any]:
    payload = path.read_bytes()
    return {
        "bytes": len(payload),
        "md5": hashlib.md5(payload).hexdigest(),
        "sha256": hashlib.sha256(payload).hexdigest(),
    }


def _ascii_strings(payload: bytes, min_length: int = 4) -> list[str]:
    strings: list[str] = []
    current = bytearray()
    for byte in payload:
        if 32 <= byte <= 126:
            current.append(byte)
        else:
            if len(current) >= min_length:
                strings.append(current.decode("ascii", errors="replace"))
            current = bytearray()
    if len(current) >= min_length:
        strings.append(current.decode("ascii", errors="replace"))
    return strings


def _matching_labels(path: Path) -> list[str]:
    labels: list[str] = []
    for value in _ascii_strings(path.read_bytes()):
        if any(pattern.search(value) for pattern in RELEVANT_LABEL_PATTERNS):
            labels.append(value)
    return labels


def _embedded_png(path: Path) -> dict[str, Any]:
    payload = path.read_bytes()
    start = payload.find(PNG_SIGNATURE)
    if start < 0:
        return {"present": False}
    end = payload.find(PNG_END, start)
    if end < 0:
        return {"present": False, "start_byte": start, "complete": False}
    png = payload[start : end + len(PNG_END)]
    width = None
    height = None
    if len(png) >= 24:
        width, height = struct.unpack(">II", png[16:24])
    return {
        "present": True,
        "complete": True,
        "start_byte": start,
        "bytes": len(png),
        "sha256": hashlib.sha256(png).hexdigest(),
        "width_px": width,
        "height_px": height,
    }


def _write_embedded_png(source_path: Path, output_path: Path) -> dict[str, Any]:
    payload = source_path.read_bytes()
    start = payload.find(PNG_SIGNATURE)
    end = payload.find(PNG_END, start)
    if start < 0 or end < 0:
        return {"written": False}
    png = payload[start : end + len(PNG_END)]
    output_path.write_bytes(png)
    return {"written": True, "path": str(output_path), **_hashes(output_path)}


def _file_summary(raw_dir: Path, item: dict[str, Any]) -> dict[str, Any]:
    path = raw_dir / item["name"]
    summary = {
        "figshare_file_id": item.get("id"),
        "name": item.get("name"),
        "download_url": item.get("download_url"),
        "mimetype": item.get("mimetype"),
        "figshare_bytes": item.get("size"),
        "supplied_md5": item.get("supplied_md5"),
        "local_path": str(path),
        "downloaded": path.exists(),
    }
    if path.exists():
        hashes = _hashes(path)
        summary.update(hashes)
        summary["md5_matches_figshare"] = hashes["md5"] == item.get("supplied_md5")
    return summary


def _local_tool_status() -> dict[str, Any]:
    return {
        "labplot_on_path": shutil.which("labplot") is not None,
        "scidavis_on_path": shutil.which("scidavis") is not None,
        "python_originpro_importable": importlib.util.find_spec("originpro") is not None,
        "python_pyorigin_importable": importlib.util.find_spec("PyOrigin") is not None,
        "python_liborigin_importable": importlib.util.find_spec("liborigin") is not None,
        "python_opj2dat_importable": importlib.util.find_spec("opj2dat") is not None,
    }


def build_phase3d2_packet(metadata_path: Path, raw_dir: Path) -> dict[str, Any]:
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    files = [_file_summary(raw_dir, item) for item in metadata.get("files", [])]

    target_inspection = {}
    for target_id, filename in TARGET_FILES.items():
        path = raw_dir / filename
        if not path.exists():
            target_inspection[target_id] = {
                "filename": filename,
                "downloaded": False,
            }
            continue
        target_inspection[target_id] = {
            "filename": filename,
            "downloaded": True,
            "local_path": str(path),
            "hashes": _hashes(path),
            "labels_found": _matching_labels(path),
            "embedded_preview_png": _embedded_png(path),
            "table_extraction_status": "blocked_by_origin_binary_container",
        }

    md5_all_match = all(
        bool(item.get("md5_matches_figshare")) for item in files if item.get("downloaded")
    )
    fig2b_labels = target_inspection.get("fig2b_reflectance", {}).get("labels_found", [])
    fig2cd_labels = target_inspection.get("fig2cd_permittivity", {}).get("labels_found", [])
    evidence_present = all(
        target_inspection.get(target_id, {}).get("downloaded") for target_id in TARGET_FILES
    )
    label_evidence_present = (
        any("Measured Rp" in label for label in fig2b_labels)
        and any("Measured Rs" in label for label in fig2b_labels)
        and any("TiN real part of permittivity" in label for label in fig2cd_labels)
        and any("AZO real part of permittivity" in label for label in fig2cd_labels)
    )

    return {
        "phase_id": "Phase 3D.2",
        "title": "Saha TiN/AZO Source-Data Intake",
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "inputs": {
            "metadata_path": str(metadata_path),
            "raw_dir": str(raw_dir),
        },
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
        },
        "files": files,
        "target_inspection": target_inspection,
        "local_tool_status": _local_tool_status(),
        "decision": {
            "status": "source_package_snapshotted_origin_export_blocked",
            "can_feed_serious_core": False,
            "can_promote_calibrated_linear_evidence": False,
            "phase4_ready": False,
            "claim_status_ceiling": "candidate_unclassified_until_table_export",
            "download_integrity": "all_downloaded_md5_match" if md5_all_match else "md5_mismatch",
            "fig2_evidence_present": evidence_present,
            "fig2_label_evidence_present": label_evidence_present,
            "result_interpretation": (
                "The public Figshare package contains the expected Fig. 2b reflectance "
                "and Fig. 2c/d permittivity Origin files, and their embedded labels "
                "match the intended calibration/holdout lanes. The current local "
                "environment cannot export the proprietary OPJU worksheet tables to "
                "CSV, so no residual run or promotion decision is allowed yet."
            ),
            "recommended_next_phase": (
                "Phase 3D.2A - Saha OPJU worksheet export or open-format alternate"
            ),
        },
        "extraction_options": [
            "Export the two OPJU worksheets to CSV with Origin or free Origin Viewer on Windows.",
            "Try LabPlot GUI import/export if installed on a compatible macOS system.",
            "Find a publisher-provided open-format mirror for Fig. 2b and Fig. 2c/d.",
            (
                "If only plot/image digitization is possible, downgrade to "
                "literature_reproduction_fixture."
            ),
        ],
        "external_tool_notes": (
            "OriginLab documents worksheet data access in the free Origin Viewer, but "
            "CSV export is a Windows Viewer feature. LabPlot documents Origin project "
            "import and spreadsheet export, but that path is GUI-mediated here."
        ),
    }


def write_phase3d2_packet(output_dir: Path, packet: dict[str, Any]) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase3d2_saha_tin_azo_source_intake.json"
    md_path = output_dir / "phase3d2_saha_tin_azo_source_intake.md"
    raw_dir = Path(packet["inputs"]["raw_dir"])

    for target_id, filename in TARGET_FILES.items():
        source_path = raw_dir / filename
        if source_path.exists():
            preview_name = f"{Path(filename).stem.replace(' ', '_')}_embedded_preview.png"
            preview_path = raw_dir / preview_name
            packet["target_inspection"][target_id]["written_preview_png"] = (
                _write_embedded_png(source_path, preview_path)
            )

    json_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(phase3d2_markdown(packet), encoding="utf-8")
    return json_path, md_path


def phase3d2_markdown(packet: dict[str, Any]) -> str:
    decision = packet["decision"]
    source = packet["source"]
    fig2b = packet["target_inspection"].get("fig2b_reflectance", {})
    fig2cd = packet["target_inspection"].get("fig2cd_permittivity", {})
    return "\n".join(
        [
            "# Phase 3D.2 - Saha TiN/AZO Source-Data Intake",
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
            f"- Download integrity: `{decision['download_integrity']}`",
            f"- Recommended next phase: `{decision['recommended_next_phase']}`",
            "",
            "## Source",
            "",
            f"- Title: `{source['title']}`",
            f"- DOI: `{source['doi']}`",
            f"- Figshare URL: `{source['figshare_url']}`",
            f"- Public: `{source['is_public']}`",
            f"- License: `{source['license'].get('name')}`",
            f"- File count: `{source['file_count']}`",
            "",
            "## Target Files",
            "",
            f"- Fig. 2b file: `{fig2b.get('filename')}`",
            f"- Fig. 2b labels: `{fig2b.get('labels_found')}`",
            f"- Fig. 2c/d file: `{fig2cd.get('filename')}`",
            f"- Fig. 2c/d labels: `{fig2cd.get('labels_found')}`",
            "",
            "## Interpretation",
            "",
            decision["result_interpretation"],
            "",
            "## Extraction Options",
            "",
            *[f"- {item}" for item in packet["extraction_options"]],
            "",
        ]
    )
