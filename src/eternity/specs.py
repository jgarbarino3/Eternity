"""Pydantic schemas for V0 experiment specifications."""

from __future__ import annotations

from typing import Literal

from pint import UnitRegistry
from pydantic import BaseModel, ConfigDict, Field, field_validator

ureg = UnitRegistry()


class QuantitySpec(BaseModel):
    """A physical scalar quantity with an explicit unit."""

    value: float
    unit: str

    model_config = ConfigDict(extra="forbid")

    @field_validator("unit")
    @classmethod
    def validate_unit(cls, unit: str) -> str:
        ureg.Unit(unit)
        return unit

    def to(self, unit: str):
        return ureg.Quantity(self.value, self.unit).to(unit)


class RangeSpec(BaseModel):
    min: float
    max: float
    unit: str

    model_config = ConfigDict(extra="forbid")

    @field_validator("unit")
    @classmethod
    def validate_unit(cls, unit: str) -> str:
        ureg.Unit(unit)
        return unit


class WavelengthGridSpec(RangeSpec):
    points: int = Field(gt=1)


class MaterialModelSpec(BaseModel):
    type: str
    parameters_ref: str

    model_config = ConfigDict(extra="forbid")


class SampleSpec(BaseModel):
    sample_id: str
    material: str
    thickness: QuantitySpec
    material_model: MaterialModelSpec

    model_config = ConfigDict(extra="forbid")


class InputPulseSpec(BaseModel):
    kind: str
    center_wavelength: QuantitySpec
    bandwidth: QuantitySpec

    model_config = ConfigDict(extra="forbid")


class GeometrySpec(BaseModel):
    incidence_angle: QuantitySpec
    polarization: Literal["TE", "TM"]
    incident_medium: str
    substrate: str

    model_config = ConfigDict(extra="forbid")


class SimulatorSpec(BaseModel):
    name: Literal["linear_transfer_matrix"]
    version: str
    wavelength_range: WavelengthGridSpec

    model_config = ConfigDict(extra="forbid")


class ValidityEnvelopeSpec(BaseModel):
    wavelength: RangeSpec
    fluence: RangeSpec
    trusted_notes: list[str]
    untrusted_notes: list[str]

    model_config = ConfigDict(extra="forbid")


class ExperimentSpec(BaseModel):
    schema_version: Literal["0.1"]
    experiment_id: str
    question: str
    hypothesis: str
    sample: SampleSpec
    input_pulse: InputPulseSpec
    geometry: GeometrySpec
    simulator: SimulatorSpec
    observables: list[str]
    acceptance_tests: list[str]
    validity_envelope: ValidityEnvelopeSpec

    model_config = ConfigDict(extra="forbid")
