"""Promotion from radar leads into reviewable research-memory records."""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path

import yaml

from eternity.research_memory.ids import record_id_for_payload
from eternity.research_memory.radar.models import RankedRadarCandidate
from eternity.research_memory.store import load_records

GRADE_ORDER = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4}


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")[:80] or "paper"


def _payload_for_item(item: RankedRadarCandidate) -> dict:
    candidate = item.candidate
    now = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    source_type = (
        "preprint" if candidate.source_type in {"arxiv_query", "arxiv_category"} else "other"
    )
    source_locator = (
        candidate.url
        or candidate.canonical_url
        or candidate.arxiv_id
        or candidate.openreview_forum
        or candidate.title
    )
    return {
        "schema_version": "0.1",
        "record_type": "paper_card",
        "title": candidate.title,
        "summary": item.why_this_matters,
        "body": (
            "Promoted from the weekly research radar. "
            "This is a review queue item, not validated evidence."
        ),
        "evidence_state": "literature_supported",
        "review_state": "needs_human_review",
        "source_refs": [
            {
                "source_type": source_type,
                "locator": source_locator,
                "description": f"Research radar source `{candidate.source_id}`.",
                "retrieved_at": now,
            }
        ],
        "source_type": source_type,
        "created_at": now,
        "tags": sorted(set(candidate.tags + item.themes + ["radar"])),
        "project_areas": candidate.project_areas,
        "related_record_ids": [],
        "claims": [
            f"Radar grade {item.grade} with score {item.score}: {candidate.title}",
            item.why_this_matters,
        ],
        "limitations": [item.risk_or_limitation],
        "next_actions": [
            item.should_we_act_now,
            item.possible_experiment,
            item.possible_code_module,
        ],
        "warnings": [
            "radar_keyword_classification",
            "needs_human_review",
            "not_serious_core_evidence",
        ],
        "paper_title": candidate.title,
        "paper_authors": candidate.authors or ["Unknown"],
        "year": candidate.year,
        "doi": candidate.doi,
        "arxiv_id": candidate.arxiv_id,
        "paper_url": candidate.url or candidate.canonical_url,
        "main_claims": [item.why_this_matters],
        "methods": item.themes,
        "measurements": [],
        "suggested_simulation_tasks": [item.possible_experiment],
        "suggested_lab_tests": [],
        "suggested_codex_tasks": [item.possible_code_module],
        "caveats": [item.risk_or_limitation],
    }


def promote_radar_run(
    *,
    run_dir: Path,
    min_grade: str = "A",
    record_dir: Path = Path("data/research_memory/radar"),
) -> list[Path]:
    """Promote selected radar items into paper_card YAML files."""

    ranked_payload = json.loads((run_dir / "ranked.json").read_text())
    ranked = [RankedRadarCandidate.model_validate(item) for item in ranked_payload]
    selected = [
        item for item in ranked if GRADE_ORDER[item.grade] <= GRADE_ORDER[min_grade.upper()]
    ]
    record_dir.mkdir(parents=True, exist_ok=True)
    existing_ids = {
        loaded.record.record_id
        for loaded in load_records(record_dir)
    } if any(record_dir.glob("*.y*ml")) else set()

    written: list[Path] = []
    for item in selected:
        payload = _payload_for_item(item)
        record_id = record_id_for_payload(payload)
        if record_id in existing_ids:
            continue
        path = record_dir / f"{record_id}_{_slug(item.candidate.title)}.yaml"
        path.write_text(yaml.safe_dump(payload, sort_keys=False))
        written.append(path)
    return written
