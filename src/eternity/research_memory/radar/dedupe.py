"""Deduplication helpers for radar candidates."""

from __future__ import annotations

import hashlib
import re
from urllib.parse import urlsplit, urlunsplit

from eternity.research_memory.radar.models import RadarCandidate


def normalize_title(title: str) -> str:
    """Return a stable normalized title for title-hash deduplication."""

    return " ".join(re.findall(r"[a-z0-9]+", title.lower()))


def normalize_url(url: str) -> str:
    """Normalize a paper URL enough for conservative deduplication."""

    parsed = urlsplit(url)
    path = parsed.path.rstrip("/") or parsed.path
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), path, "", ""))


def candidate_key(candidate: RadarCandidate) -> str:
    """Return the strongest stable dedupe key available for a candidate."""

    if candidate.doi:
        return f"doi:{candidate.doi.lower().strip()}"
    if candidate.arxiv_id:
        return f"arxiv:{candidate.arxiv_id.lower().strip()}"
    if candidate.openreview_forum:
        return f"openreview:{normalize_url(candidate.openreview_forum)}"
    if candidate.canonical_url or candidate.url:
        return f"url:{normalize_url(candidate.canonical_url or candidate.url or '')}"
    title_hash = hashlib.sha256(normalize_title(candidate.title).encode("utf-8")).hexdigest()
    return f"title:{title_hash[:16]}"


def _merge_candidate(existing: RadarCandidate, incoming: RadarCandidate) -> RadarCandidate:
    tags = sorted(set(existing.tags) | set(incoming.tags))
    project_areas = sorted(set(existing.project_areas) | set(incoming.project_areas))
    raw_metadata = dict(existing.raw_metadata)
    raw_metadata.setdefault("duplicate_sources", [])
    raw_metadata["duplicate_sources"].append(
        {
            "source_id": incoming.source_id,
            "source_type": incoming.source_type,
            "url": incoming.url,
        }
    )
    return existing.model_copy(
        update={"tags": tags, "project_areas": project_areas, "raw_metadata": raw_metadata}
    )


def dedupe_candidates(candidates: list[RadarCandidate]) -> list[RadarCandidate]:
    """Deduplicate candidates by DOI, arXiv ID, OpenReview forum, URL, then title."""

    by_key: dict[str, RadarCandidate] = {}
    for candidate in candidates:
        key = candidate_key(candidate)
        if key in by_key:
            by_key[key] = _merge_candidate(by_key[key], candidate)
        else:
            by_key[key] = candidate
    return list(by_key.values())
