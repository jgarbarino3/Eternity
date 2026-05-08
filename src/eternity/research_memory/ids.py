"""Deterministic identifiers for research-memory records."""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any

from pydantic import BaseModel

VOLATILE_ID_FIELDS = {"record_id", "created_at", "updated_at"}
UNORDERED_LIST_FIELDS = {"tags", "project_areas", "related_record_ids"}


def _canonical_json(payload: Any) -> str:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        default=str,
    )


def _normalize(value: Any, *, key: str | None = None) -> Any:
    if isinstance(value, BaseModel):
        value = value.model_dump(mode="json", exclude_none=True)
    if isinstance(value, dict):
        return {
            item_key: _normalize(item_value, key=item_key)
            for item_key, item_value in sorted(value.items())
            if item_key not in VOLATILE_ID_FIELDS and item_value is not None
        }
    if isinstance(value, list):
        normalized = [_normalize(item) for item in value]
        if key in UNORDERED_LIST_FIELDS:
            return sorted(normalized, key=_canonical_json)
        return normalized
    return value


def normalized_identity_payload(payload: Any) -> Any:
    """Return the deterministic identity payload for a record."""

    return _normalize(payload)


def content_hash_for_record(payload: Any) -> str:
    """Return the canonical SHA-256 content hash for a record."""

    return hashlib.sha256(
        _canonical_json(normalized_identity_payload(payload)).encode("utf-8")
    ).hexdigest()


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return slug or "record"


def record_id_for_payload(payload: Any) -> str:
    """Return a stable research-memory record id for a raw or typed record."""

    if isinstance(payload, BaseModel):
        data = payload.model_dump(mode="json", exclude_none=True)
    else:
        data = dict(payload)
    record_type = str(data.get("record_type", "record"))
    return f"rm_{_slug(record_type)}_{content_hash_for_record(data)[:12]}"
