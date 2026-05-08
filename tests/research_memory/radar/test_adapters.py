from __future__ import annotations

from pathlib import Path

import pytest

from eternity.research_memory.radar.adapters import (
    ArxivRateLimiter,
    scan_arxiv,
    scan_google_scholar_manual,
    scan_huggingface_daily_papers,
    scan_openreview,
)
from eternity.research_memory.radar.config import RadarSourceConfig


class FakeClock:
    def __init__(self) -> None:
        self.value = 10.0
        self.sleeps: list[float] = []

    def now(self) -> float:
        return self.value

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.value += seconds


ARXIV_XML = """\
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
  <entry>
    <id>http://arxiv.org/abs/2601.12345v1</id>
    <updated>2026-01-02T00:00:00Z</updated>
    <published>2026-01-01T00:00:00Z</published>
    <title>FROG retrieval for ultrafast ENZ pulses</title>
    <summary>Deep learning benchmark for frequency-resolved optical gating.</summary>
    <author><name>A. Researcher</name></author>
    <arxiv:primary_category term="physics.optics" />
  </entry>
</feed>
"""


def test_arxiv_adapter_parses_metadata_and_enforces_rate_limit() -> None:
    source = RadarSourceConfig.model_validate(
        {
            "id": "arxiv_fixture",
            "type": "arxiv_query",
            "enabled": True,
            "query": 'all:"FROG retrieval"',
            "max_results": 1,
        }
    )
    clock = FakeClock()
    limiter = ArxivRateLimiter(clock=clock)
    calls: list[str] = []

    def fetcher(url: str) -> str:
        calls.append(url)
        return ARXIV_XML

    first = scan_arxiv(source, text_fetcher=fetcher, rate_limiter=limiter)
    second = scan_arxiv(source, text_fetcher=fetcher, rate_limiter=limiter)

    assert len(first) == 1
    assert first[0].arxiv_id == "2601.12345v1"
    assert first[0].tags == ["physics.optics"]
    assert len(second) == 1
    assert clock.sleeps == [pytest.approx(3.0)]
    assert "max_results=1" in calls[0]


def test_openreview_adapter_parses_api2_payload() -> None:
    source = RadarSourceConfig.model_validate(
        {
            "id": "openreview_fixture",
            "type": "openreview_search",
            "enabled": True,
            "query": "AI scientist",
        }
    )

    def fetcher(url: str):
        assert "api2.openreview.net" in url
        return {
            "notes": [
                {
                    "id": "note1",
                    "forum": "forum1",
                    "content": {
                        "title": {"value": "AI Scientist failure modes"},
                        "abstract": {"value": "Experiment verification benchmark."},
                    },
                }
            ]
        }

    candidates = scan_openreview(source, json_fetcher=fetcher)

    assert candidates[0].title == "AI Scientist failure modes"
    assert candidates[0].openreview_forum == "https://openreview.net/forum?id=forum1"


def test_huggingface_daily_papers_adapter_parses_metadata() -> None:
    source = RadarSourceConfig.model_validate(
        {"id": "hf_fixture", "type": "huggingface_daily_papers", "enabled": True}
    )

    def fetcher(url: str):
        assert "huggingface.co/api/daily_papers" in url
        return [
            {
                "paper": {
                    "id": "2601.10000",
                    "title": "Scientific claim verification benchmark",
                    "summary": "A benchmark for LLM evidence verification.",
                    "authors": [{"name": "A. Author"}],
                    "arxivId": "2601.10000",
                }
            }
        ]

    candidates = scan_huggingface_daily_papers(source, json_fetcher=fetcher)

    assert candidates[0].url == "https://huggingface.co/papers/2601.10000"
    assert candidates[0].authors == ["A. Author"]


def test_google_scholar_adapter_uses_local_export_only(tmp_path: Path) -> None:
    alert_path = tmp_path / "scholar.txt"
    alert_path.write_text(
        "Knowledge graph LLM scientific idea generation\n"
        "https://example.test/paper\n"
        "A short alert snippet.\n"
    )
    source = RadarSourceConfig.model_validate(
        {
            "id": "scholar_manual",
            "type": "google_scholar_manual",
            "enabled": True,
            "manual_path": str(alert_path),
        }
    )

    candidates = scan_google_scholar_manual(source)

    assert len(candidates) == 1
    assert candidates[0].title == "Knowledge graph LLM scientific idea generation"
    assert candidates[0].url == "https://example.test/paper"


def test_google_scholar_adapter_rejects_url_path() -> None:
    source = RadarSourceConfig.model_construct(
        id="scholar_manual",
        type="google_scholar_manual",
        enabled=True,
        manual_path="https://scholar.google.com",
        max_results=10,
        tags=[],
        project_areas=[],
    )

    with pytest.raises(ValueError, match="local alert exports"):
        scan_google_scholar_manual(source)
