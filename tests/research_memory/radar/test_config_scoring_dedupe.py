from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from eternity.research_memory.radar.config import RadarSourceConfig, load_radar_config
from eternity.research_memory.radar.dedupe import dedupe_candidates
from eternity.research_memory.radar.models import RadarCandidate
from eternity.research_memory.radar.scoring import grade_candidate


def test_example_config_loads_with_weekly_sunday_defaults() -> None:
    config = load_radar_config(Path("config/research_radar.example.yaml"))

    assert config.cadence.day_of_week == "sunday"
    assert config.cadence.timezone == "Europe/Rome"
    assert "frog_retrieval" in config.themes
    assert any(source.type == "google_scholar_manual" for source in config.sources)


def test_google_scholar_source_refuses_remote_scraping_path() -> None:
    payload = {
        "id": "bad_scholar",
        "type": "google_scholar_manual",
        "enabled": True,
        "manual_path": "https://scholar.google.com/scholar?q=enz",
    }

    with pytest.raises(ValidationError, match="local exported alert text"):
        RadarSourceConfig.model_validate(payload)


def test_grading_assigns_act_now_for_enz_frog_retrieval_lead() -> None:
    candidate = RadarCandidate(
        source_id="fixture",
        source_type="arxiv_query",
        title="Deep learning FROG retrieval for ultrafast spectroscopy of ENZ thin films",
        abstract=(
            "We present a benchmark dataset and retrieval algorithm for frequency-resolved "
            "optical gating, pump-probe spectroscopy, and epsilon near zero materials."
        ),
        tags=["frog", "ultrafast", "enz"],
    )

    ranked = grade_candidate(candidate)

    assert ranked.grade == "A"
    assert "frog_retrieval" in ranked.themes
    assert "ultrafast_ml" in ranked.themes
    assert "Potential future module" in ranked.possible_code_module


def test_grading_assigns_noise_for_hype_without_actionable_signal() -> None:
    candidate = RadarCandidate(
        source_id="fixture",
        source_type="rss_feed",
        title="Fully autonomous scientist promises AGI scientist breakthrough without validation",
    )

    ranked = grade_candidate(candidate)

    assert ranked.grade == "D"
    assert "hype warning" in "; ".join(ranked.reasons)


def test_dedupe_prefers_doi_arxiv_url_then_title_hash() -> None:
    duplicate_a = RadarCandidate(
        source_id="a",
        source_type="arxiv_query",
        title="Shared paper",
        doi="10.123/example",
        tags=["a"],
    )
    duplicate_b = RadarCandidate(
        source_id="b",
        source_type="semantic_scholar_search",
        title="Shared paper variant",
        doi="10.123/example",
        tags=["b"],
    )
    title_duplicate_a = RadarCandidate(
        source_id="c",
        source_type="rss_feed",
        title="Knowledge graph LLM scientific idea generation",
    )
    title_duplicate_b = RadarCandidate(
        source_id="d",
        source_type="rss_feed",
        title="Knowledge Graph: LLM scientific idea generation!",
    )

    deduped = dedupe_candidates(
        [duplicate_a, duplicate_b, title_duplicate_a, title_duplicate_b]
    )

    assert len(deduped) == 2
    assert sorted(deduped[0].tags) == ["a", "b"]
