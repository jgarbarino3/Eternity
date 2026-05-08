"""Typed V1 data contracts for lab-twin inputs and evidence gates."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class QuantityWithUncertainty(BaseModel):
    value: float
    unit: str
    uncertainty: float | None = Field(default=None, ge=0)

    model_config = ConfigDict(extra="forbid")


class AxisSpec(BaseModel):
    quantity: Literal["vacuum_wavelength", "photon_energy", "frequency"]
    unit: str
    values_column: str

    model_config = ConfigDict(extra="forbid")


class RawArtifactRecord(BaseModel):
    raw_artifact_id: str
    kind: Literal["csv", "hdf5", "json", "image_digitization", "vendor_export"]
    path: str
    sha256: str
    bytes: int = Field(gt=0)
    source_type: Literal["lab", "literature_table", "literature_digitized", "synthetic"]
    immutable: bool

    model_config = ConfigDict(extra="forbid")

    @field_validator("sha256")
    @classmethod
    def validate_sha256(cls, value: str) -> str:
        if len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
            raise ValueError("sha256 must be a lowercase 64-character hex digest")
        return value


class MeasurementRecord(BaseModel):
    measurement_id: str
    kind: Literal[
        "transmission_spectrum",
        "reflection_spectrum",
        "ellipsometry_psi_delta",
        "nk_table",
        "epsilon_table",
    ]
    raw_artifact_ref: str
    sample_ref: str
    stack_ref: str
    x_axis: AxisSpec
    y_quantity: str
    y_unit: str
    y_values_column: str
    uncertainty_type: Literal["per_point", "scalar", "unknown"]
    geometry_incidence_angle: QuantityWithUncertainty
    geometry_polarization: Literal["TE", "TM", "unpolarized", "mixed", "unknown"]
    preprocessing: list[str] = Field(default_factory=list)
    forbidden_for_fitting: bool

    model_config = ConfigDict(extra="forbid")


class DataSplitRecord(BaseModel):
    split_id: str
    raw_data_refs: list[str]
    created_before_fit: bool
    method: Literal["explicit_indices", "wavelength_blocks", "measurement_ids", "random_seeded"]
    calibration_measurement_refs: list[str]
    holdout_measurement_refs: list[str]
    fitting_may_access_holdout_y: bool
    ai_playground_may_access_holdout_y_before_fit: bool
    evidence_strength: Literal[
        "independent_measurement",
        "same_raw_spectrum_holdout",
        "literature_reproduction",
        "synthetic_fixture",
    ]

    model_config = ConfigDict(extra="forbid")
