"""Typed models for the Eternity research radar."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

THEMES: tuple[str, ...] = (
    "hypothesis_generation",
    "agent_memory",
    "context_engineering",
    "scientific_evals",
    "self_driving_labs",
    "bayesian_experiment_design",
    "photonic_agents",
    "ultrafast_ml",
    "frog_retrieval",
    "materials_agents",
    "claim_verification",
)


class RadarGrade(StrEnum):
    ACT_NOW = "A"
    ARCHITECTURE_IDEA = "B"
    RELEVANT_NOT_ACTIONABLE = "C"
    HYPE_OR_NOISE = "D"
    READ_LATER = "E"


class RadarSourceType(StrEnum):
    ARXIV_QUERY = "arxiv_query"
    ARXIV_CATEGORY = "arxiv_category"
    OPENREVIEW_SEARCH = "openreview_search"
    HUGGINGFACE_DAILY_PAPERS = "huggingface_daily_papers"
    RSS_FEED = "rss_feed"
    SEMANTIC_SCHOLAR_SEARCH = "semantic_scholar_search"
    GOOGLE_SCHOLAR_MANUAL = "google_scholar_manual"


class RadarCandidate(BaseModel):
    """One raw paper/source lead from a configured source."""

    source_id: str = Field(min_length=1)
    source_type: RadarSourceType
    title: str = Field(min_length=1)
    abstract: str = ""
    authors: list[str] = Field(default_factory=list)
    year: int | None = None
    published_at: str | None = None
    url: str | None = None
    canonical_url: str | None = None
    doi: str | None = None
    arxiv_id: str | None = None
    openreview_forum: str | None = None
    venue: str | None = None
    query: str | None = None
    tags: list[str] = Field(default_factory=list)
    project_areas: list[str] = Field(default_factory=list)
    raw_metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(extra="forbid", use_enum_values=True)


class RankedRadarCandidate(BaseModel):
    """A candidate after deterministic Eternity relevance scoring."""

    candidate: RadarCandidate
    grade: RadarGrade
    score: int
    themes: list[str]
    reasons: list[str]
    why_this_matters: str
    possible_experiment: str
    possible_code_module: str
    risk_or_limitation: str
    should_we_act_now: str
    strong_b: bool = False

    model_config = ConfigDict(extra="forbid", use_enum_values=True)


class RadarRunManifest(BaseModel):
    """Small manifest for a radar scan artifact."""

    schema_version: Literal["0.1"] = "0.1"
    run_id: str
    generated_at: datetime
    config_path: str
    dry_run: bool
    source_count: int
    raw_candidate_count: int
    deduped_candidate_count: int
    warnings: list[str]
    recurring_queries: list[str]
    arxiv_categories: list[str]
    themes: list[str]

    model_config = ConfigDict(extra="forbid")
