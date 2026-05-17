"""Phase 3A.7 CompleteEASE source recovery utilities."""

from __future__ import annotations

import json
import re
import zipfile
from dataclasses import dataclass
from datetime import UTC, datetime
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from typing import Any

from eternity.artifacts import sha256_file

DEFAULT_SOURCE_ROOT = Path("/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD")
DEFAULT_THESIS_PDF = Path(
    "/Users/joegarbarino/Desktop/Research Optics/Thesis/Checkpoints/"
    "Thesis Final Draft v13 May 17 committee.pdf"
)
DEFAULT_D10_INITIAL = Path(
    "/Users/joegarbarino/Desktop/Research Optics/Thesis/Data/d_10nm_initial.txt"
)
DEFAULT_D10_12V = Path("/Users/joegarbarino/Desktop/Research Optics/Thesis/Data/d_10nm_12V.txt")
DEFAULT_302010_PS_INTENSITY = Path(
    "/Users/joegarbarino/Desktop/Research Optics/Coding/txt/30_20_10 p_s intensity.txt"
)
DEFAULT_302010_REFLECTANCE = Path(
    "/Users/joegarbarino/Desktop/Research Optics/Coding/txt/30_20_10 reflectance.txt"
)

RECOVERY_EXTENSIONS = {".se", ".sesnap", ".ise"}
CONTAINER_EXTENSIONS = {".zip"}
MAX_TEXT_CHARS = 80_000
MAX_SNIPPETS_PER_FILE = 24
MAX_CANDIDATES = 30

KEYWORD_PATTERN = re.compile(
    r"3l2|30[_ -]?20[_ -]?10|30\s*nm|10\s*nm|20\s*nm|3\s*layer|"
    r"cap test|quartz|sio2|tin|60|s-?polar|te|reflect|intensity|"
    r"completeease|woollam|rc2|%r|absolute",
    re.IGNORECASE,
)
ASCII_STRING_PATTERN = re.compile(rb"[\x20-\x7e]{4,}")
ABSOLUTE_REFLECTANCE_PROOF_PATTERN = re.compile(
    r"(absolute|calibrated).{0,40}(reflectance|%r)|reflectance\s*\(%\s*r?\s*\)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class RecoveryInputs:
    source_root: Path = DEFAULT_SOURCE_ROOT
    thesis_pdf: Path = DEFAULT_THESIS_PDF
    d10_initial: Path = DEFAULT_D10_INITIAL
    d10_12v: Path = DEFAULT_D10_12V
    candidate_ps_intensity: Path = DEFAULT_302010_PS_INTENSITY
    candidate_reflectance: Path = DEFAULT_302010_REFLECTANCE


def _file_record(path: Path, *, role: str) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return {
        "role": role,
        "path": str(path),
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def _ascii_strings(payload: bytes) -> str:
    matches = ASCII_STRING_PATTERN.findall(payload)
    text = "\n".join(match.decode("utf-8", errors="replace") for match in matches)
    return text[:MAX_TEXT_CHARS]


def _snippets(text: str) -> list[str]:
    hits: list[str] = []
    for line in text.splitlines():
        clean = " ".join(line.strip().split())
        if clean and KEYWORD_PATTERN.search(clean):
            hits.append(clean[:220])
        if len(hits) >= MAX_SNIPPETS_PER_FILE:
            break
    return hits


def _score_text(path: Path, text: str) -> tuple[int, list[str]]:
    haystack = f"{path.name}\n{text}".lower()
    checks: list[tuple[str, int, tuple[str, ...]]] = [
        ("mentions_3l2", 24, ("3l2",)),
        ("mentions_30_20_10", 22, ("30_20_10", "30 20 10", "30-20-10")),
        ("mentions_quartz", 10, ("quartz",)),
        ("mentions_completeease", 10, ("completeease", "complete ease")),
        ("mentions_woollam_or_rc2", 8, ("woollam", "rc2")),
        ("mentions_reflectance", 8, ("reflectance", "reflective")),
        ("mentions_intensity", 8, ("intensity",)),
        ("mentions_s_polarized_or_te", 8, ("s-polar", "s polar", "te")),
        ("mentions_60_degree", 6, ("60 degree", "60-degree", "60 deg", "60°")),
        ("mentions_three_layer", 6, ("3 layer", "three-layer", "3-layer", "cap test")),
        ("mentions_tin", 4, ("tin",)),
        ("mentions_sio2", 4, ("sio2", "sio 2")),
        ("mentions_30nm", 4, ("30 nm", "30nm")),
        ("mentions_10nm_or_11nm", 4, ("10 nm", "10nm", "11 nm", "11nm")),
        ("mentions_20nm", 4, ("20 nm", "20nm")),
    ]
    reasons = []
    score = 0
    for label, points, terms in checks:
        if any(term in haystack for term in terms):
            reasons.append(label)
            score += points
    return score, reasons


def _has_absolute_reflectance_proof(text: str) -> bool:
    return ABSOLUTE_REFLECTANCE_PROOF_PATTERN.search(text) is not None


def _read_sesnap_bytes(payload: bytes) -> tuple[str, dict[str, Any]]:
    with zipfile.ZipFile(BytesIO(payload)) as archive:
        names = archive.namelist()
        text_parts: list[str] = []
        if "_FitLog" in names:
            text_parts.append(archive.read("_FitLog").decode("utf-8", errors="replace"))
        for name in names:
            if name.lower().endswith(".ise"):
                text_parts.append(_ascii_strings(archive.read(name)))
        return "\n".join(text_parts), {
            "archive_entries": [
                {"name": info.filename, "size_bytes": info.file_size}
                for info in archive.infolist()
            ],
            "has_fit_log": "_FitLog" in names,
            "inner_ise_entries": [name for name in names if name.lower().endswith(".ise")],
        }


def _candidate_from_payload(
    *,
    display_path: str,
    kind: str,
    payload: bytes,
    original_path: Path,
    container_path: str | None = None,
    member_path: str | None = None,
    zip_crc32: int | None = None,
    zip_mtime: tuple[int, int, int, int, int, int] | None = None,
) -> dict[str, Any]:
    archive_metadata: dict[str, Any] = {}
    if kind == "sesnap":
        try:
            text, archive_metadata = _read_sesnap_bytes(payload)
        except zipfile.BadZipFile:
            text = _ascii_strings(payload)
            archive_metadata = {"archive_error": "bad_zip_file"}
    else:
        text = _ascii_strings(payload)

    score, reasons = _score_text(Path(display_path), text)
    record: dict[str, Any] = {
        "path": display_path,
        "original_path": str(original_path),
        "kind": kind,
        "size_bytes": len(payload),
        "sha256": sha256(payload).hexdigest(),
        "score": score,
        "match_reasons": reasons,
        "absolute_reflectance_proof": _has_absolute_reflectance_proof(text),
        "evidence_snippets": _snippets(text),
    }
    if container_path is not None:
        record["container_path"] = container_path
    if member_path is not None:
        record["member_path"] = member_path
    if zip_crc32 is not None:
        record["zip_crc32"] = f"{zip_crc32:08x}"
    if zip_mtime is not None:
        record["zip_mtime"] = "-".join(
            [
                f"{zip_mtime[0]:04d}",
                f"{zip_mtime[1]:02d}",
                f"{zip_mtime[2]:02d}",
                f"{zip_mtime[3]:02d}:{zip_mtime[4]:02d}:{zip_mtime[5]:02d}",
            ]
        )
    if archive_metadata:
        record.update(archive_metadata)
    return record


def _candidate_record(path: Path) -> dict[str, Any]:
    return _candidate_from_payload(
        display_path=str(path),
        kind=path.suffix.lower().lstrip("."),
        payload=path.read_bytes(),
        original_path=path,
    )


def _container_candidate_records(path: Path) -> list[dict[str, Any]]:
    records = []
    try:
        with zipfile.ZipFile(path) as archive:
            for info in archive.infolist():
                suffix = Path(info.filename).suffix.lower()
                if suffix not in RECOVERY_EXTENSIONS:
                    continue
                payload = archive.read(info.filename)
                records.append(
                    _candidate_from_payload(
                        display_path=f"{path}::{info.filename}",
                        kind=suffix.lstrip("."),
                        payload=payload,
                        original_path=path,
                        container_path=str(path),
                        member_path=info.filename,
                        zip_crc32=info.CRC,
                        zip_mtime=info.date_time,
                    )
                )
    except zipfile.BadZipFile:
        return []
    return records


def scan_completeease_sources(source_root: Path) -> list[dict[str, Any]]:
    if not source_root.exists():
        raise FileNotFoundError(source_root)
    direct_paths = sorted(
        path
        for path in source_root.rglob("*")
        if path.is_file() and path.suffix.lower() in RECOVERY_EXTENSIONS
    )
    container_paths = sorted(
        path
        for path in source_root.rglob("*")
        if path.is_file() and path.suffix.lower() in CONTAINER_EXTENSIONS
    )
    candidates = [_candidate_record(path) for path in direct_paths]
    for path in container_paths:
        candidates.extend(_container_candidate_records(path))
    candidates.sort(key=lambda item: (-item["score"], item["path"]))
    return candidates


def build_phase3a7_recovery(inputs: RecoveryInputs) -> dict[str, Any]:
    supporting_files = [
        _file_record(inputs.thesis_pdf, role="thesis_final_pdf"),
        _file_record(inputs.d10_initial, role="d_10nm_initial_export"),
        _file_record(inputs.d10_12v, role="d_10nm_12v_export"),
        _file_record(inputs.candidate_ps_intensity, role="phase3a_30_20_10_p_s_intensity"),
        _file_record(inputs.candidate_reflectance, role="phase3a_30_20_10_reflectance"),
    ]
    all_candidates = scan_completeease_sources(inputs.source_root)
    top_candidates = all_candidates[:MAX_CANDIDATES]
    absolute_evidence = [
        candidate
        for candidate in top_candidates
        if candidate["absolute_reflectance_proof"]
    ]
    exact_identity_candidates = [
        candidate
        for candidate in top_candidates
        if "mentions_3l2" in candidate["match_reasons"]
        or "mentions_30_20_10" in candidate["match_reasons"]
    ]

    return {
        "phase_id": "Phase 3A.7",
        "title": "CompleteEASE Source Recovery + 3L2 Provenance Lock",
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "inputs": {
            "source_root": str(inputs.source_root),
            "candidate_limit": MAX_CANDIDATES,
            "scanned_source_file_count": len(all_candidates),
            "scanner_note": (
                "Includes direct .SE/.SEsnap/.iSE files and matching members "
                "inside .zip containers."
            ),
        },
        "thesis_backed_mapping": {
            "status": "stack_mapping_confirmed",
            "sample": "3L2/Quartz",
            "stack": "30 nm TiN / 10 nm SiO2 / 20 nm TiN on quartz",
            "measurement": "S-polarized RC2 in-situ reflectance/reflective intensity at 60 degrees",
            "figure": "Thesis Figure 4.1",
            "normalization_boundary": (
                "Thesis text supports reflective-intensity/reflectance provenance, "
                "but not absolute calibrated %R for the exported Intensity columns."
            ),
        },
        "supporting_files": supporting_files,
        "candidate_sources": top_candidates,
        "decision": {
            "source_recovery_status": "related_source_candidates_found"
            if top_candidates
            else "no_source_candidates_found",
            "exact_source_identity_status": "candidate_found_needs_manual_review"
            if exact_identity_candidates
            else "not_found",
            "stack_mapping": "stack_mapping_confirmed",
            "normalization_basis": "relative_intensity_only",
            "absolute_reflectance_status": "absolute_reflectance_evidence_found"
            if absolute_evidence
            else "absolute_reflectance_blocked",
            "can_promote_calibrated_linear_evidence": False,
            "can_feed_serious_core": False,
            "claim_status_ceiling": "weak_within_dataset_holdout",
            "blocked_gates": ["normalization_gate", "thresholds_predeclared"],
        },
        "notes": [
            (
                "Large CompleteEASE/Woollam binary sources are registered by path, "
                "size, hash, and readable metadata only."
            ),
            (
                "No binary .SE, .SEsnap, or .iSE file is copied into the repository "
                "by this recovery artifact."
            ),
            "Existing run_f35a15cef565fb15 remains historical and cannot be promoted.",
        ],
    }


def recovery_markdown(recovery: dict[str, Any]) -> str:
    mapping = recovery["thesis_backed_mapping"]
    decision = recovery["decision"]
    lines = [
        "# Phase 3A.7 CompleteEASE Source Recovery",
        "",
        "## Decision",
        "",
        f"- Source recovery status: `{decision['source_recovery_status']}`",
        f"- Exact source identity status: `{decision['exact_source_identity_status']}`",
        f"- Stack mapping: `{decision['stack_mapping']}`",
        f"- Normalization basis: `{decision['normalization_basis']}`",
        f"- Absolute reflectance status: `{decision['absolute_reflectance_status']}`",
        (
            "- Can promote calibrated evidence: "
            f"`{decision['can_promote_calibrated_linear_evidence']}`"
        ),
        f"- Claim-status ceiling: `{decision['claim_status_ceiling']}`",
        "",
        "## Thesis-Backed Mapping",
        "",
        f"- Sample: `{mapping['sample']}`",
        f"- Stack: {mapping['stack']}",
        f"- Measurement: {mapping['measurement']}",
        f"- Figure: {mapping['figure']}",
        f"- Boundary: {mapping['normalization_boundary']}",
        "",
        "## Supporting Files",
        "",
        "| Role | Path | SHA-256 |",
        "| --- | --- | --- |",
    ]
    for item in recovery["supporting_files"]:
        lines.append(f"| {item['role']} | `{item['path']}` | `{item['sha256']}` |")

    lines.extend(
        [
            "",
            "## Top CompleteEASE/Woollam Candidates",
            "",
            "| Score | Reasons | Path |",
            "| ---: | --- | --- |",
        ]
    )
    for candidate in recovery["candidate_sources"][:15]:
        reasons = ", ".join(candidate["match_reasons"]) or "none"
        lines.append(f"| {candidate['score']} | {reasons} | `{candidate['path']}` |")

    lines.extend(
        [
            "",
            "## Consequence",
            "",
            "Phase 3A.7 strengthens the `3L2/Quartz` stack and geometry provenance,",
            "and it finds related local source candidates. It does not find an exact",
            "`3L2`, `30_20_10`, or source-export identity record for the thesis",
            "`d_10nm` traces.",
            "",
            "It keeps absolute reflectance blocked. The exported `Intensity` columns",
            "may remain useful for relative diagnostics and figure provenance; they",
            "cannot feed `calibrated_linear_evidence` without source-backed",
            "absolute-normalization evidence and future predeclared thresholds.",
            "",
        ]
    )
    return "\n".join(lines)


def write_phase3a7_recovery(
    output_dir: Path,
    recovery: dict[str, Any],
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase3a7_completeease_source_recovery.json"
    md_path = output_dir / "phase3a7_completeease_source_recovery.md"
    json_path.write_text(
        json.dumps(recovery, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(recovery_markdown(recovery), encoding="utf-8")
    return json_path, md_path
