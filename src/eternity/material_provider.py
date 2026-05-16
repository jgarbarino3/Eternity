"""Material-response resolution for synthetic and registry-backed runs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from eternity.materials import drude_lorentz_ito
from eternity.optical_data import interpolate_epsilon, load_epsilon_table
from eternity.registry import LabDataRegistry, artifact_path, load_registry
from eternity.specs import ExperimentSpec


@dataclass(frozen=True)
class MaterialResponse:
    epsilon: np.ndarray
    assumptions: list[str]
    warnings: list[dict[str, str]]
    metadata: dict[str, object]


def epsilon_for_material_model_ref(
    registry: LabDataRegistry,
    registry_path: Path,
    material_model_ref: str,
    wavelengths_nm: np.ndarray,
) -> MaterialResponse:
    material_record = registry.material_models[material_model_ref]
    if material_record.raw_artifact_ref is None:
        raise ValueError(f"{material_model_ref} has no raw_artifact_ref")
    artifact = registry.raw_artifacts[material_record.raw_artifact_ref]
    table = load_epsilon_table(artifact_path(artifact, registry_path))

    return MaterialResponse(
        epsilon=interpolate_epsilon(table, wavelengths_nm),
        assumptions=[
            f"{material_model_ref} is treated as a frozen linear material response.",
            "Interpolation is linear inside the measured wavelength range.",
        ],
        warnings=[
            {
                "severity": "warning",
                "source": "material_provider",
                "message": (
                    f"{material_model_ref} is a registry-backed optical-constant input; "
                    "claim status depends on separate validation gates."
                ),
            }
        ],
        metadata={
            "model_level": "linear_tmm_tabulated_epsilon_v1_grounding",
            "source_type": material_record.source_type,
            "material_model_ref": material_record.material_model_id,
            "raw_artifact_ref": material_record.raw_artifact_ref,
            "source_measurement_ref": material_record.source_measurement_ref,
        },
    )


def epsilon_for_spec(spec: ExperimentSpec, wavelengths_nm: np.ndarray) -> MaterialResponse:
    model = spec.sample.material_model
    if model.type == "drude_lorentz_synthetic":
        return MaterialResponse(
            epsilon=drude_lorentz_ito(wavelengths_nm),
            assumptions=["Synthetic Drude-Lorentz ITO parameters are used."],
            warnings=[
                {
                    "severity": "info",
                    "source": "material_provider",
                    "message": "Synthetic ITO parameters are used; no lab sample has been fitted.",
                }
            ],
            metadata={
                "model_level": "linear_tmm_synthetic_v0",
                "source_type": "synthetic",
                "material_model_ref": model.parameters_ref,
            },
        )

    if model.type != "tabulated_epsilon":
        raise ValueError(f"unsupported material model type: {model.type}")

    registry_path = Path(model.registry_path or "lab_data/registry.yaml")
    registry = load_registry(registry_path)
    if model.material_model_ref is None:
        raise ValueError("tabulated_epsilon material model requires material_model_ref")
    response = epsilon_for_material_model_ref(
        registry,
        registry_path,
        model.material_model_ref,
        wavelengths_nm,
    )
    return MaterialResponse(
        epsilon=response.epsilon,
        assumptions=[
            "Tabulated epsilon is treated as a frozen linear material response.",
            "Interpolation is linear inside the measured wavelength range.",
        ],
        warnings=[
            {
                "severity": "warning",
                "source": "material_provider",
                "message": (
                    "Registry-backed optical constants are real data inputs, but this run has "
                    "no independent R/T holdout by itself."
                ),
            }
        ],
        metadata=response.metadata,
    )
