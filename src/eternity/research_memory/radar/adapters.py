"""Conservative source adapters for the research radar."""

from __future__ import annotations

import json
import os
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from eternity.research_memory.radar.config import RadarConfig, RadarSourceConfig
from eternity.research_memory.radar.models import RadarCandidate, RadarSourceType

USER_AGENT = "EternityResearchRadar/0.1 (metadata-only; no PDF mirroring)"
ARXIV_API_URL = "https://export.arxiv.org/api/query"
OPENREVIEW_API2_NOTES_URL = "https://api2.openreview.net/notes"
HF_DAILY_PAPERS_URL = "https://huggingface.co/api/daily_papers"
SEMANTIC_SCHOLAR_SEARCH_URL = "https://api.semanticscholar.org/graph/v1/paper/search"


class Clock(Protocol):
    def now(self) -> float: ...

    def sleep(self, seconds: float) -> None: ...


class RealClock:
    def now(self) -> float:
        return time.monotonic()

    def sleep(self, seconds: float) -> None:
        time.sleep(seconds)


@dataclass
class ArxivRateLimiter:
    """Global arXiv legacy-API rate limiter."""

    clock: Clock
    min_interval_seconds: float = 3.0
    last_request_at: float | None = None

    def wait(self) -> None:
        now = self.clock.now()
        if self.last_request_at is not None:
            elapsed = now - self.last_request_at
            remaining = self.min_interval_seconds - elapsed
            if remaining > 0:
                self.clock.sleep(remaining)
                now = self.clock.now()
        self.last_request_at = now


def fetch_text(url: str, *, headers: dict[str, str] | None = None, timeout: int = 20) -> str:
    """Fetch text with a radar-specific user agent."""

    request_headers = {"User-Agent": USER_AGENT}
    if headers:
        request_headers.update(headers)
    request = urllib.request.Request(url, headers=request_headers)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8")


def fetch_json(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    timeout: int = 20,
) -> dict[str, Any] | list[Any]:
    """Fetch JSON with a radar-specific user agent."""

    return json.loads(fetch_text(url, headers=headers, timeout=timeout))


def _author_names_from_arxiv(entry: ET.Element, ns: dict[str, str]) -> list[str]:
    return [
        (author.findtext("atom:name", default="", namespaces=ns) or "").strip()
        for author in entry.findall("atom:author", ns)
        if (author.findtext("atom:name", default="", namespaces=ns) or "").strip()
    ]


def _arxiv_id_from_url(url: str | None) -> str | None:
    if not url:
        return None
    return url.rstrip("/").rsplit("/", maxsplit=1)[-1]


def _parse_arxiv_feed(xml_text: str, source: RadarSourceConfig) -> list[RadarCandidate]:
    ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    root = ET.fromstring(xml_text)
    candidates: list[RadarCandidate] = []
    for entry in root.findall("atom:entry", ns):
        url = (entry.findtext("atom:id", default="", namespaces=ns) or "").strip() or None
        title = " ".join((entry.findtext("atom:title", default="", namespaces=ns) or "").split())
        abstract = " ".join(
            (entry.findtext("atom:summary", default="", namespaces=ns) or "").split()
        )
        if not title:
            continue
        published_at = entry.findtext("atom:published", default=None, namespaces=ns)
        year = int(published_at[:4]) if published_at and published_at[:4].isdigit() else None
        doi = entry.findtext("arxiv:doi", default=None, namespaces=ns)
        primary_category = entry.find("arxiv:primary_category", ns)
        category_tag = primary_category.attrib.get("term") if primary_category is not None else None
        tags = source.tags + ([category_tag] if category_tag else [])
        candidates.append(
            RadarCandidate(
                source_id=source.id,
                source_type=source.type,
                title=title,
                abstract=abstract,
                authors=_author_names_from_arxiv(entry, ns),
                year=year,
                published_at=published_at,
                url=url,
                canonical_url=url,
                doi=doi,
                arxiv_id=_arxiv_id_from_url(url),
                query=source.query,
                tags=tags,
                project_areas=source.project_areas,
                raw_metadata={"source": "arxiv_atom"},
            )
        )
    return candidates


def _arxiv_search_query(source: RadarSourceConfig) -> str:
    category_query = " OR ".join(f"cat:{category}" for category in source.categories)
    if source.query and category_query:
        return f"({category_query}) AND ({source.query})"
    return source.query or category_query


def scan_arxiv(
    source: RadarSourceConfig,
    *,
    text_fetcher: Callable[..., str] = fetch_text,
    rate_limiter: ArxivRateLimiter,
) -> list[RadarCandidate]:
    """Scan arXiv metadata only through the official API endpoint."""

    query = _arxiv_search_query(source)
    params = {
        "search_query": query,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "max_results": str(source.max_results),
    }
    url = f"{ARXIV_API_URL}?{urllib.parse.urlencode(params)}"
    rate_limiter.wait()
    return _parse_arxiv_feed(text_fetcher(url), source)


def _parse_openreview_payload(
    payload: dict[str, Any], source: RadarSourceConfig
) -> list[RadarCandidate]:
    notes = payload.get("notes", [])
    candidates: list[RadarCandidate] = []
    for note in notes[: source.max_results]:
        content = note.get("content", {})
        title_value = content.get("title", {})
        abstract_value = content.get("abstract", {})
        title = title_value.get("value") if isinstance(title_value, dict) else title_value
        abstract = (
            abstract_value.get("value") if isinstance(abstract_value, dict) else abstract_value
        )
        if not title:
            continue
        forum = note.get("forum") or note.get("id")
        url = f"https://openreview.net/forum?id={forum}" if forum else None
        candidates.append(
            RadarCandidate(
                source_id=source.id,
                source_type=source.type,
                title=str(title),
                abstract=str(abstract or ""),
                url=url,
                canonical_url=url,
                openreview_forum=url,
                venue=source.query,
                query=source.query,
                tags=source.tags,
                project_areas=source.project_areas,
                raw_metadata={"source": "openreview_api2", "id": note.get("id")},
            )
        )
    return candidates


def scan_openreview(
    source: RadarSourceConfig,
    *,
    json_fetcher: Callable[..., dict[str, Any] | list[Any]] = fetch_json,
) -> list[RadarCandidate]:
    """Scan OpenReview API 2 metadata when a source is explicitly enabled."""

    params: dict[str, str] = {"limit": str(source.max_results)}
    if source.invitation:
        params["invitation"] = source.invitation
    if source.query:
        params["search"] = source.query
    url = f"{OPENREVIEW_API2_NOTES_URL}?{urllib.parse.urlencode(params)}"
    payload = json_fetcher(url)
    if not isinstance(payload, dict):
        return []
    return _parse_openreview_payload(payload, source)


def _paper_url_from_hf(paper: dict[str, Any]) -> str | None:
    paper_id = paper.get("id") or paper.get("arxivId")
    if paper.get("url"):
        return str(paper["url"])
    if paper_id:
        return f"https://huggingface.co/papers/{paper_id}"
    return None


def scan_huggingface_daily_papers(
    source: RadarSourceConfig,
    *,
    json_fetcher: Callable[..., dict[str, Any] | list[Any]] = fetch_json,
) -> list[RadarCandidate]:
    """Scan Hugging Face Daily Papers metadata."""

    payload = json_fetcher(HF_DAILY_PAPERS_URL)
    items = payload if isinstance(payload, list) else payload.get("dailyPapers", [])
    candidates: list[RadarCandidate] = []
    for item in items[: source.max_results]:
        paper = item.get("paper", item) if isinstance(item, dict) else {}
        if not isinstance(paper, dict):
            continue
        title = paper.get("title")
        if not title:
            continue
        authors = paper.get("authors") or []
        author_names = [
            author.get("name", "") if isinstance(author, dict) else str(author)
            for author in authors
        ]
        url = _paper_url_from_hf(paper)
        candidates.append(
            RadarCandidate(
                source_id=source.id,
                source_type=source.type,
                title=str(title),
                abstract=str(paper.get("summary") or paper.get("abstract") or ""),
                authors=[name for name in author_names if name],
                url=url,
                canonical_url=url,
                arxiv_id=paper.get("arxivId"),
                query=source.query,
                tags=source.tags,
                project_areas=source.project_areas,
                raw_metadata={"source": "huggingface_daily_papers"},
            )
        )
    return candidates


def scan_semantic_scholar(
    source: RadarSourceConfig,
    *,
    json_fetcher: Callable[..., dict[str, Any] | list[Any]] = fetch_json,
) -> list[RadarCandidate]:
    """Scan Semantic Scholar metadata at low volume."""

    fields = "title,abstract,authors,year,url,externalIds,venue,publicationDate"
    params = {"query": source.query or "", "limit": str(source.max_results), "fields": fields}
    url = f"{SEMANTIC_SCHOLAR_SEARCH_URL}?{urllib.parse.urlencode(params)}"
    headers: dict[str, str] = {}
    if api_key := os.environ.get("SEMANTIC_SCHOLAR_API_KEY"):
        headers["x-api-key"] = api_key
    payload = json_fetcher(url, headers=headers)
    if not isinstance(payload, dict):
        return []
    candidates: list[RadarCandidate] = []
    for paper in payload.get("data", [])[: source.max_results]:
        title = paper.get("title")
        if not title:
            continue
        external_ids = paper.get("externalIds") or {}
        authors = paper.get("authors") or []
        candidates.append(
            RadarCandidate(
                source_id=source.id,
                source_type=source.type,
                title=str(title),
                abstract=str(paper.get("abstract") or ""),
                authors=[author.get("name", "") for author in authors if isinstance(author, dict)],
                year=paper.get("year"),
                published_at=paper.get("publicationDate"),
                url=paper.get("url"),
                canonical_url=paper.get("url"),
                doi=external_ids.get("DOI"),
                arxiv_id=external_ids.get("ArXiv"),
                venue=paper.get("venue"),
                query=source.query,
                tags=source.tags,
                project_areas=source.project_areas,
                raw_metadata={"source": "semantic_scholar"},
            )
        )
    return candidates


def scan_rss_feed(
    source: RadarSourceConfig,
    *,
    text_fetcher: Callable[..., str] = fetch_text,
) -> list[RadarCandidate]:
    """Scan a simple RSS/Atom feed as metadata-only leads."""

    if not source.feed_url:
        return []
    root = ET.fromstring(text_fetcher(source.feed_url))
    candidates: list[RadarCandidate] = []
    for item in root.findall(".//item")[: source.max_results]:
        title = " ".join((item.findtext("title") or "").split())
        if not title:
            continue
        url = item.findtext("link")
        candidates.append(
            RadarCandidate(
                source_id=source.id,
                source_type=source.type,
                title=title,
                abstract=" ".join((item.findtext("description") or "").split()),
                published_at=item.findtext("pubDate"),
                url=url,
                canonical_url=url,
                query=source.query,
                tags=source.tags,
                project_areas=source.project_areas,
                raw_metadata={"source": "rss"},
            )
        )
    if candidates:
        return candidates
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    for entry in root.findall(".//atom:entry", ns)[: source.max_results]:
        title = " ".join((entry.findtext("atom:title", default="", namespaces=ns) or "").split())
        if not title:
            continue
        link = entry.find("atom:link", ns)
        url = link.attrib.get("href") if link is not None else None
        candidates.append(
            RadarCandidate(
                source_id=source.id,
                source_type=source.type,
                title=title,
                abstract=" ".join(
                    (entry.findtext("atom:summary", default="", namespaces=ns) or "").split()
                ),
                published_at=entry.findtext("atom:published", default=None, namespaces=ns),
                url=url,
                canonical_url=url,
                query=source.query,
                tags=source.tags,
                project_areas=source.project_areas,
                raw_metadata={"source": "atom"},
            )
        )
    return candidates


def scan_google_scholar_manual(source: RadarSourceConfig) -> list[RadarCandidate]:
    """Parse a local text export of Google Scholar alerts; never scrape Scholar."""

    if source.manual_path is None:
        return []
    if str(source.manual_path).startswith(("http://", "https://", "http:/", "https:/")):
        raise ValueError("Google Scholar radar source accepts local alert exports only")
    path = Path(source.manual_path)
    if not path.exists():
        return []
    chunks = [chunk.strip() for chunk in path.read_text().split("\n\n") if chunk.strip()]
    candidates: list[RadarCandidate] = []
    for chunk in chunks[: source.max_results]:
        lines = [line.strip() for line in chunk.splitlines() if line.strip()]
        if not lines:
            continue
        url = next((line for line in lines if line.startswith(("http://", "https://"))), None)
        candidates.append(
            RadarCandidate(
                source_id=source.id,
                source_type=source.type,
                title=lines[0],
                abstract=" ".join(lines[1:4]),
                url=url,
                canonical_url=url,
                query=source.query,
                tags=source.tags,
                project_areas=source.project_areas,
                raw_metadata={"source": "google_scholar_manual_export"},
            )
        )
    return candidates


def scan_source(
    source: RadarSourceConfig,
    *,
    text_fetcher: Callable[..., str] = fetch_text,
    json_fetcher: Callable[..., dict[str, Any] | list[Any]] = fetch_json,
    arxiv_rate_limiter: ArxivRateLimiter | None = None,
) -> list[RadarCandidate]:
    """Scan one enabled source."""

    if not source.enabled:
        return []
    if source.type in {RadarSourceType.ARXIV_QUERY, RadarSourceType.ARXIV_CATEGORY}:
        if arxiv_rate_limiter is None:
            arxiv_rate_limiter = ArxivRateLimiter(clock=RealClock())
        return scan_arxiv(source, text_fetcher=text_fetcher, rate_limiter=arxiv_rate_limiter)
    if source.type == RadarSourceType.OPENREVIEW_SEARCH:
        return scan_openreview(source, json_fetcher=json_fetcher)
    if source.type == RadarSourceType.HUGGINGFACE_DAILY_PAPERS:
        return scan_huggingface_daily_papers(source, json_fetcher=json_fetcher)
    if source.type == RadarSourceType.RSS_FEED:
        return scan_rss_feed(source, text_fetcher=text_fetcher)
    if source.type == RadarSourceType.SEMANTIC_SCHOLAR_SEARCH:
        return scan_semantic_scholar(source, json_fetcher=json_fetcher)
    if source.type == RadarSourceType.GOOGLE_SCHOLAR_MANUAL:
        return scan_google_scholar_manual(source)
    return []


def scan_enabled_sources(
    config: RadarConfig,
    *,
    text_fetcher: Callable[..., str] = fetch_text,
    json_fetcher: Callable[..., dict[str, Any] | list[Any]] = fetch_json,
    clock: Clock | None = None,
) -> tuple[list[RadarCandidate], list[str]]:
    """Scan all enabled sources and return candidates plus recoverable warnings."""

    warnings: list[str] = []
    candidates: list[RadarCandidate] = []
    rate_limiter = ArxivRateLimiter(clock=clock or RealClock())
    for source in config.sources:
        try:
            candidates.extend(
                scan_source(
                    source,
                    text_fetcher=text_fetcher,
                    json_fetcher=json_fetcher,
                    arxiv_rate_limiter=rate_limiter,
                )
            )
        except Exception as error:  # pragma: no cover - exercised through CLI behavior
            warnings.append(f"{source.id}: {error}")
    return candidates, warnings
