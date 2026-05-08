"""Configuration loading for the weekly research radar."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator

from eternity.research_memory.radar.models import THEMES, RadarSourceType


class RadarCadence(BaseModel):
    frequency: Literal["weekly"] = "weekly"
    day_of_week: Literal["sunday"] = "sunday"
    timezone: str = "Europe/Rome"
    local_time: str = "09:00"

    model_config = ConfigDict(extra="forbid")


class RadarScoringConfig(BaseModel):
    grade_thresholds: dict[str, int] = Field(
        default_factory=lambda: {"A": 28, "B": 18, "C": 8}
    )
    strong_b_threshold: int = 22
    weights: dict[str, int] = Field(
        default_factory=lambda: {
            "exact_theme_phrase": 6,
            "theme_keyword": 3,
            "eternity_domain_keyword": 5,
            "implementation_keyword": 3,
            "experiment_keyword": 3,
            "source_quality": 2,
            "hype_penalty": -5,
        }
    )

    model_config = ConfigDict(extra="forbid")


class RadarSourceConfig(BaseModel):
    id: str = Field(min_length=1)
    type: RadarSourceType
    enabled: bool = False
    query: str | None = None
    categories: list[str] = Field(default_factory=list)
    feed_url: str | None = None
    manual_path: Path | None = None
    invitation: str | None = None
    max_results: int = Field(default=10, ge=1, le=100)
    tags: list[str] = Field(default_factory=list)
    project_areas: list[str] = Field(default_factory=list)
    source_notes: str = ""

    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    @model_validator(mode="after")
    def validate_source_shape(self) -> RadarSourceConfig:
        if self.type == RadarSourceType.GOOGLE_SCHOLAR_MANUAL and self.enabled:
            if self.manual_path is None:
                raise ValueError("google_scholar_manual requires manual_path when enabled")
            if str(self.manual_path).startswith(("http://", "https://", "http:/", "https:/")):
                raise ValueError("google_scholar_manual accepts local exported alert text only")
        if self.type == RadarSourceType.RSS_FEED and self.enabled and not self.feed_url:
            raise ValueError("rss_feed requires feed_url when enabled")
        if self.type in {
            RadarSourceType.ARXIV_QUERY,
            RadarSourceType.SEMANTIC_SCHOLAR_SEARCH,
        } and self.enabled and not self.query:
            raise ValueError(f"{self.type} requires query when enabled")
        return self


class RadarConfig(BaseModel):
    schema_version: Literal["0.1"] = "0.1"
    cadence: RadarCadence = Field(default_factory=RadarCadence)
    themes: list[str] = Field(default_factory=lambda: list(THEMES))
    recurring_queries: list[str] = Field(min_length=1)
    arxiv_categories: list[str] = Field(default_factory=list)
    scoring: RadarScoringConfig = Field(default_factory=RadarScoringConfig)
    sources: list[RadarSourceConfig] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def validate_themes(self) -> RadarConfig:
        unknown = sorted(set(self.themes) - set(THEMES))
        if unknown:
            raise ValueError(f"unknown radar themes: {', '.join(unknown)}")
        return self


def load_radar_config(path: Path) -> RadarConfig:
    """Load and validate a research-radar YAML config."""

    payload = yaml.safe_load(path.read_text())
    if not isinstance(payload, dict):
        raise ValueError(f"Research radar config must be a mapping: {path}")
    return RadarConfig.model_validate(payload)
