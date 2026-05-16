"""Registry loading for lab-twin contracts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field

from eternity.artifacts import sha256_file
from eternity.contracts import (
    DataSplitRecord,
    MaterialModelRecord,
    MeasurementRecord,
    RawArtifactRecord,
    SampleRecord,
    StackRecord,
)
from eternity.optical_data import (
    load_ellipsometry_psi_delta,
    load_epsilon_table,
    load_multichannel_spectrum,
    load_reflectance_spectrum,
)


class LabDataRegistry(BaseModel):
    schema_version: Literal["0.1"]
    raw_artifacts: dict[str, RawArtifactRecord] = Field(default_factory=dict)
    samples: dict[str, SampleRecord] = Field(default_factory=dict)
    stacks: dict[str, StackRecord] = Field(default_factory=dict)
    measurements: dict[str, MeasurementRecord] = Field(default_factory=dict)
    material_models: dict[str, MaterialModelRecord] = Field(default_factory=dict)
    splits: dict[str, DataSplitRecord] = Field(default_factory=dict)

    model_config = ConfigDict(extra="forbid")


def load_registry(path: Path = Path("lab_data/registry.yaml")) -> LabDataRegistry:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return LabDataRegistry.model_validate(payload)


@dataclass(frozen=True)
class RegistryIntegrityReport:
    issues: list[str]
    warnings: list[str]

    @property
    def ok(self) -> bool:
        return not self.issues


def artifact_path(record: RawArtifactRecord, registry_path: Path) -> Path:
    path = Path(record.path)
    if path.is_absolute():
        return path
    return registry_path.parent.parent / path if registry_path.parent.name == "lab_data" else path


def validate_registry_integrity(
    registry: LabDataRegistry,
    registry_path: Path = Path("lab_data/registry.yaml"),
) -> RegistryIntegrityReport:
    issues: list[str] = []
    warnings: list[str] = []

    for artifact_id, artifact in registry.raw_artifacts.items():
        resolved = artifact_path(artifact, registry_path)
        if not resolved.exists():
            issues.append(f"{artifact_id}: missing artifact path {artifact.path}")
            continue

        actual_bytes = resolved.stat().st_size
        if actual_bytes != artifact.bytes:
            issues.append(
                f"{artifact_id}: byte count mismatch "
                f"registry={artifact.bytes} actual={actual_bytes}"
            )

        actual_sha256 = sha256_file(resolved)
        if actual_sha256 != artifact.sha256:
            issues.append(
                f"{artifact_id}: sha256 mismatch registry={artifact.sha256} actual={actual_sha256}"
            )

    for measurement_id, measurement in registry.measurements.items():
        artifact = registry.raw_artifacts.get(measurement.raw_artifact_ref)
        if measurement.raw_artifact_ref not in registry.raw_artifacts:
            issues.append(
                f"{measurement_id}: raw_artifact_ref {measurement.raw_artifact_ref} not found"
            )
        elif artifact is not None:
            resolved = artifact_path(artifact, registry_path)
            try:
                if measurement.kind == "epsilon_table":
                    load_epsilon_table(resolved)
                elif measurement.kind == "ellipsometry_psi_delta":
                    load_ellipsometry_psi_delta(resolved)
                elif measurement.kind in {"reflection_spectrum", "transmission_spectrum"}:
                    if len(measurement.y_values_columns) > 1:
                        load_multichannel_spectrum(
                            resolved,
                            list(measurement.y_values_columns),
                        )
                    else:
                        load_reflectance_spectrum(resolved)
            except ValueError as error:
                issues.append(f"{measurement_id}: {error}")
        if measurement.sample_ref not in registry.samples and not measurement.sample_ref.startswith(
            "synthetic_"
        ):
            warnings.append(f"{measurement_id}: sample_ref {measurement.sample_ref} has no record")
        if measurement.stack_ref not in registry.stacks and not measurement.stack_ref.startswith(
            "synthetic_"
        ):
            warnings.append(f"{measurement_id}: stack_ref {measurement.stack_ref} has no record")

    for model_id, model in registry.material_models.items():
        if model.sample_ref not in registry.samples:
            issues.append(f"{model_id}: sample_ref {model.sample_ref} not found")
        if model.raw_artifact_ref and model.raw_artifact_ref not in registry.raw_artifacts:
            issues.append(f"{model_id}: raw_artifact_ref {model.raw_artifact_ref} not found")
        if (
            model.source_measurement_ref
            and model.source_measurement_ref not in registry.measurements
        ):
            issues.append(
                f"{model_id}: source_measurement_ref {model.source_measurement_ref} not found"
            )

    for split_id, split in registry.splits.items():
        for raw_ref in split.raw_data_refs:
            if raw_ref not in registry.raw_artifacts:
                issues.append(f"{split_id}: raw_data_ref {raw_ref} not found")
        for measurement_ref in split.calibration_measurement_refs + split.holdout_measurement_refs:
            if measurement_ref not in registry.measurements:
                issues.append(f"{split_id}: measurement_ref {measurement_ref} not found")
        if (
            split.evidence_strength == "calibration_only_no_holdout"
            and split.holdout_measurement_refs
        ):
            issues.append(f"{split_id}: calibration_only_no_holdout split declares holdouts")

    return RegistryIntegrityReport(issues=issues, warnings=warnings)
