"""Deterministic identifiers for specs and runs."""

from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)


def deterministic_hash(payload: Any) -> str:
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def run_id_for_spec(payload: Any) -> str:
    return f"run_{deterministic_hash(payload)[:16]}"
