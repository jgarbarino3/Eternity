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
    kind: Literal["csv", "txt", "hdf5", "json", "image_digitization", "vendor_export"]
    path: str
    sha256: str
    bytes: int = Field(gt=0)
    source_type: Literal["lab", "literature_table", "literature_digitized", "synthetic"]
    immutable: bool
    original_filename: str | None = None
    original_path: str | None = None
    acquired_at: str | None = None
    source_notes: str | None = None
    access_notes: str | None = None
    provenance_refs: list[str] = Field(default_factory=list)

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
    y_values_columns: dict[str, str] = Field(default_factory=dict)
    uncertainty_type: Literal["per_point", "scalar", "unknown"]
    geometry_incidence_angle: QuantityWithUncertainty
    geometry_polarization: Literal["TE", "TM", "unpolarized", "mixed", "unknown"]
    instrument_or_source_notes: str | None = None
    preprocessing: list[str] = Field(default_factory=list)
    forbidden_for_fitting: bool

    model_config = ConfigDict(extra="forbid")


class SampleRecord(BaseModel):
    sample_id: str
    material: str
    source_type: Literal["lab", "literature", "synthetic"]
    nominal_thickness: QuantityWithUncertainty | None = None
    composition: str | None = None
    process_notes: list[str] = Field(default_factory=list)
    provenance_refs: list[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")


class StackLayerRecord(BaseModel):
    role: Literal["incident_medium", "film", "substrate", "oxide", "metal", "other"]
    material: str
    thickness: QuantityWithUncertainty | None = None
    notes: str | None = None

    model_config = ConfigDict(extra="forbid")


class StackRecord(BaseModel):
    stack_id: str
    sample_ref: str
    layers: list[StackLayerRecord]
    notes: str | None = None

    model_config = ConfigDict(extra="forbid")


class MaterialModelRecord(BaseModel):
    material_model_id: str
    sample_ref: str
    kind: Literal[
        "synthetic_drude_lorentz",
        "tabulated_epsilon",
        "tabulated_nk",
        "drude_lorentz_fit",
    ]
    source_type: Literal["lab", "literature_table", "literature_digitized", "synthetic"]
    raw_artifact_ref: str | None = None
    source_measurement_ref: str | None = None
    equation_convention: str
    sign_convention: str
    interpolation: Literal["linear", "nearest", "none"]
    extrapolation: Literal["forbidden", "clamped", "allowed_with_warning"]
    enz_definition: str | None = None
    enz_wavelengths_nm: list[float] = Field(default_factory=list)
    wavelength_min_nm: float | None = None
    wavelength_max_nm: float | None = None
    passivity_check: Literal["pass", "fail", "not_checked", "not_applicable"]
    fit_provenance: str | None = None
    validity_notes: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)

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
        "weak_within_dataset_holdout",
        "calibration_only_no_holdout",
        "literature_reproduction",
        "synthetic_fixture",
    ]

    model_config = ConfigDict(extra="forbid")
