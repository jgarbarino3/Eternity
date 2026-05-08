"""File-backed research-memory loading and validation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from eternity.research_memory.ids import record_id_for_payload
from eternity.research_memory.records import ResearchRecord, validate_record_payload

DEFAULT_RECORD_DIR = Path("research_memory/examples")
RECORD_SUFFIXES = {".json", ".yaml", ".yml"}


@dataclass(frozen=True)
class LoadedRecord:
    path: Path
    record: ResearchRecord


def record_files(path: Path) -> list[Path]:
    """Return candidate record files for a path or directory."""

    if path.is_file():
        if path.suffix.lower() not in RECORD_SUFFIXES:
            raise ValueError(f"Unsupported research-memory file type: {path}")
        return [path]
    if path.is_dir():
        return sorted(
            candidate
            for candidate in path.rglob("*")
            if candidate.is_file() and candidate.suffix.lower() in RECORD_SUFFIXES
        )
    raise FileNotFoundError(f"Research-memory path not found: {path}")


def read_record_payload(path: Path) -> dict[str, Any]:
    """Read a JSON/YAML record payload."""

    if path.suffix.lower() == ".json":
        payload = json.loads(path.read_text())
    else:
        payload = yaml.safe_load(path.read_text())
    if not isinstance(payload, dict):
        raise ValueError(f"Research-memory record must be a mapping: {path}")
    return payload


def load_record_file(path: Path) -> LoadedRecord:
    """Load and validate one record file, assigning its deterministic id when omitted."""

    payload = read_record_payload(path)
    record = validate_record_payload(payload)
    expected_id = record_id_for_payload(record)
    if record.record_id is not None and record.record_id != expected_id:
        raise ValueError(
            f"{path} has record_id {record.record_id}, expected deterministic id {expected_id}"
        )
    return LoadedRecord(path=path, record=record.model_copy(update={"record_id": expected_id}))


def load_records(path: Path) -> list[LoadedRecord]:
    """Load and validate all records under a path."""

    return [load_record_file(record_path) for record_path in record_files(path)]


def resolve_record(record_id_or_path: str, *, directory: Path = DEFAULT_RECORD_DIR) -> LoadedRecord:
    """Resolve a record by explicit file path or deterministic record id."""

    candidate = Path(record_id_or_path)
    if candidate.exists():
        return load_record_file(candidate)

    for loaded in load_records(directory):
        if loaded.record.record_id == record_id_or_path:
            return loaded
    raise FileNotFoundError(f"Research-memory record not found: {record_id_or_path}")
