"""Deterministic lexical search for research-memory records."""

from __future__ import annotations

import re
from dataclasses import dataclass

from eternity.research_memory.records import ResearchRecord

TOKEN_RE = re.compile(r"[a-z0-9]+")


@dataclass(frozen=True)
class SearchResult:
    record: ResearchRecord
    score: int
    snippet: str


def tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


def _count_matches(text: str, query_tokens: list[str]) -> int:
    tokens = tokenize(text)
    return sum(tokens.count(query_token) for query_token in query_tokens)


def _field_text(record: ResearchRecord, field: str) -> str:
    value = getattr(record, field)
    if isinstance(value, list):
        return " ".join(str(item) for item in value)
    return str(value)


def _record_text(record: ResearchRecord) -> str:
    payload = record.model_dump(mode="json", exclude_none=True)
    return " ".join(str(value) for value in payload.values())


def make_snippet(record: ResearchRecord, query_tokens: list[str], *, max_length: int = 150) -> str:
    """Return a short evidence-aware search snippet."""

    candidates = [record.summary, " ".join(record.claims), record.body, _record_text(record)]
    for candidate in candidates:
        lower = candidate.lower()
        if any(token in lower for token in query_tokens):
            snippet = " ".join(candidate.split())
            return snippet[:max_length]
    return " ".join(record.summary.split())[:max_length]


def score_record(record: ResearchRecord, query_tokens: list[str]) -> int:
    """Score a record with stable, explainable lexical weights."""

    return (
        _count_matches(record.title, query_tokens) * 6
        + _count_matches(record.summary, query_tokens) * 4
        + _count_matches(" ".join(record.tags), query_tokens) * 5
        + _count_matches(" ".join(record.claims), query_tokens) * 3
        + _count_matches(_field_text(record, "body"), query_tokens)
    )


def search_records(
    records: list[ResearchRecord],
    query: str,
    *,
    limit: int = 10,
) -> list[SearchResult]:
    """Return deterministic lexical search results."""

    query_tokens = tokenize(query)
    if not query_tokens:
        return []

    results = [
        SearchResult(record=record, score=score, snippet=make_snippet(record, query_tokens))
        for record in records
        if (score := score_record(record, query_tokens)) > 0
    ]
    return sorted(results, key=lambda result: (-result.score, result.record.record_id or ""))[
        :limit
    ]
