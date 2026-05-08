"""Registry loading for lab-twin contracts."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field

from eternity.contracts import DataSplitRecord, MeasurementRecord, RawArtifactRecord


class LabDataRegistry(BaseModel):
    schema_version: Literal["0.1"]
    raw_artifacts: dict[str, RawArtifactRecord] = Field(default_factory=dict)
    measurements: dict[str, MeasurementRecord] = Field(default_factory=dict)
    splits: dict[str, DataSplitRecord] = Field(default_factory=dict)

    model_config = ConfigDict(extra="forbid")


def load_registry(path: Path = Path("lab_data/registry.yaml")) -> LabDataRegistry:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return LabDataRegistry.model_validate(payload)
