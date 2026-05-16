"""Linear transfer-matrix V0 simulation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from tmm import coh_tmm

from eternity.material_provider import epsilon_for_material_model_ref, epsilon_for_spec
from eternity.materials import refractive_index_from_epsilon
from eternity.registry import load_registry
from eternity.specs import ExperimentSpec


@dataclass(frozen=True)
class SimulationResult:
    wavelengths_nm: np.ndarray
    epsilon: np.ndarray
    refractive_index: np.ndarray
    transmission: np.ndarray
    reflection: np.ndarray
    absorption: np.ndarray
    metrics: dict[str, float | str]
    warnings: list[dict[str, str]]
    assumptions: list[str]
    validity_notes: dict[str, list[str]]
    layer_names: list[str]
    layer_thicknesses_nm: list[float]


def _medium_index(name: str) -> complex:
    media = {
        "air": 1.0,
        "glass": 1.45,
        "quartz": 1.45,
        "fused_silica": 1.45,
        "silica": 1.45,
    }
    normalized = name.strip().lower().replace(" ", "_")
    if normalized not in media:
        raise ValueError(f"unsupported medium for linear TMM: {name}")
    return complex(media[normalized])


def _run_registry_multilayer_tmm(spec: ExperimentSpec) -> SimulationResult:
    grid = spec.simulator.wavelength_range
    wavelengths_nm = np.linspace(grid.min, grid.max, grid.points)
    registry_path = Path(spec.sample.material_model.registry_path or "lab_data/registry.yaml")
    registry = load_registry(registry_path)

    layer_epsilons: list[np.ndarray] = []
    layer_indices: list[np.ndarray] = []
    layer_names: list[str] = []
    layer_thicknesses_nm: list[float] = []
    assumptions: list[str] = [
        "Registry-backed multilayer stack is treated as frozen before comparison.",
        "No material parameters are fitted to the thesis reflectance spectra.",
    ]
    warnings: list[dict[str, str]] = [
        {
            "severity": "warning",
            "source": "phase3a_simulation",
            "message": (
                "Phase 3A is a validation candidate. Claim status is capped until "
                "normalization and predeclared residual gates are approved."
            ),
        }
    ]

    for layer in spec.sample.layers:
        response = epsilon_for_material_model_ref(
            registry,
            registry_path,
            layer.material_model_ref,
            wavelengths_nm,
        )
        layer_epsilons.append(response.epsilon)
        layer_indices.append(refractive_index_from_epsilon(response.epsilon))
        layer_names.append(layer.material)
        layer_thicknesses_nm.append(float(layer.thickness.to("nm").magnitude))
        assumptions.extend(response.assumptions)
        warnings.extend(response.warnings)

    incident_n = _medium_index(spec.geometry.incident_medium)
    substrate_n = _medium_index(spec.geometry.substrate)
    incidence_angle_rad = spec.geometry.incidence_angle.to("rad").magnitude
    pol = "p" if spec.geometry.polarization == "TM" else "s"

    transmission = np.empty_like(wavelengths_nm, dtype=float)
    reflection = np.empty_like(wavelengths_nm, dtype=float)

    for index, wavelength_nm in enumerate(wavelengths_nm):
        n_list = [incident_n, *(layer_index[index] for layer_index in layer_indices), substrate_n]
        result = coh_tmm(
            pol,
            n_list,
            [np.inf, *layer_thicknesses_nm, np.inf],
            incidence_angle_rad,
            wavelength_nm,
        )
        transmission[index] = float(result["T"])
        reflection[index] = float(result["R"])

    absorption = 1.0 - transmission - reflection
    energy_error = np.abs(transmission + reflection + absorption - 1.0)
    representative_epsilon = layer_epsilons[0]
    representative_index = layer_indices[0]

    metrics: dict[str, float | str] = {
        "min_wavelength_nm": float(wavelengths_nm.min()),
        "max_wavelength_nm": float(wavelengths_nm.max()),
        "points": float(wavelengths_nm.size),
        "mean_transmission": float(np.mean(transmission)),
        "mean_reflection": float(np.mean(reflection)),
        "mean_absorption": float(np.mean(absorption)),
        "max_energy_error": float(np.max(energy_error)),
        "model_level": "linear_tmm_registry_multilayer_phase3a_validation_candidate",
        "layer_count": float(len(layer_names)),
    }

    warnings.append(
        {
            "severity": "warning",
            "source": "v0_simulation",
            "message": "Linear transfer-matrix model only; no pump-induced ENZ dynamics.",
        }
    )
    assumptions.extend(
        [
            (
                f"The substrate `{spec.geometry.substrate}` is modeled "
                f"as lossless n={substrate_n.real:g}."
            ),
            (
                f"The incident medium `{spec.geometry.incident_medium}` is modeled "
                f"as n={incident_n.real:g}."
            ),
            "No roughness, detector response, pump-probe overlap, or noise is modeled.",
        ]
    )

    return SimulationResult(
        wavelengths_nm=wavelengths_nm,
        epsilon=representative_epsilon,
        refractive_index=representative_index,
        transmission=transmission,
        reflection=reflection,
        absorption=absorption,
        metrics=metrics,
        warnings=warnings,
        assumptions=assumptions,
        validity_notes={
            "trusted": spec.validity_envelope.trusted_notes,
            "untrusted": spec.validity_envelope.untrusted_notes,
        },
        layer_names=layer_names,
        layer_thicknesses_nm=layer_thicknesses_nm,
    )


def run_linear_tmm(spec: ExperimentSpec) -> SimulationResult:
    if spec.sample.layers:
        return _run_registry_multilayer_tmm(spec)

    grid = spec.simulator.wavelength_range
    wavelengths_nm = np.linspace(grid.min, grid.max, grid.points)
    material_response = epsilon_for_spec(spec, wavelengths_nm)
    epsilon = material_response.epsilon
    n_film = refractive_index_from_epsilon(epsilon)
    incident_n = _medium_index(spec.geometry.incident_medium)
    substrate_n = _medium_index(spec.geometry.substrate)
    thickness_nm = spec.sample.thickness.to("nm").magnitude
    incidence_angle_rad = spec.geometry.incidence_angle.to("rad").magnitude
    pol = "p" if spec.geometry.polarization == "TM" else "s"

    transmission = np.empty_like(wavelengths_nm, dtype=float)
    reflection = np.empty_like(wavelengths_nm, dtype=float)

    for index, wavelength_nm in enumerate(wavelengths_nm):
        result = coh_tmm(
            pol,
            [incident_n, n_film[index], substrate_n],
            [np.inf, thickness_nm, np.inf],
            incidence_angle_rad,
            wavelength_nm,
        )
        transmission[index] = float(result["T"])
        reflection[index] = float(result["R"])

    absorption = 1.0 - transmission - reflection
    energy_error = np.abs(transmission + reflection + absorption - 1.0)

    metrics: dict[str, float | str] = {
        "min_wavelength_nm": float(wavelengths_nm.min()),
        "max_wavelength_nm": float(wavelengths_nm.max()),
        "points": float(wavelengths_nm.size),
        "mean_transmission": float(np.mean(transmission)),
        "mean_reflection": float(np.mean(reflection)),
        "mean_absorption": float(np.mean(absorption)),
        "max_energy_error": float(np.max(energy_error)),
        "model_level": str(material_response.metadata["model_level"]),
    }

    warnings = [
        *material_response.warnings,
        {
            "severity": "warning",
            "source": "v0_simulation",
            "message": "Linear transfer-matrix model only; no pump-induced ENZ dynamics.",
        },
    ]
    assumptions = [
        *material_response.assumptions,
        f"The {spec.sample.material} film is modeled as perfectly flat and homogeneous.",
        f"The substrate `{spec.geometry.substrate}` is modeled as lossless n={substrate_n.real:g}.",
        (
            f"The incident medium `{spec.geometry.incident_medium}` is modeled "
            f"as n={incident_n.real:g}."
        ),
        "No roughness, detector response, pump-probe overlap, or noise is modeled.",
    ]

    return SimulationResult(
        wavelengths_nm=wavelengths_nm,
        epsilon=epsilon,
        refractive_index=n_film,
        transmission=transmission,
        reflection=reflection,
        absorption=absorption,
        metrics=metrics,
        warnings=warnings,
        assumptions=assumptions,
        validity_notes={
            "trusted": spec.validity_envelope.trusted_notes,
            "untrusted": spec.validity_envelope.untrusted_notes,
        },
        layer_names=[spec.sample.material],
        layer_thicknesses_nm=[float(thickness_nm)],
    )


def write_tables(result: SimulationResult, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    table_path = output_dir / "spectrum.csv"
    rows = np.column_stack(
        [
            result.wavelengths_nm,
            result.epsilon.real,
            result.epsilon.imag,
            result.refractive_index.real,
            result.refractive_index.imag,
            result.transmission,
            result.reflection,
            result.absorption,
        ]
    )
    header = "wavelength_nm,epsilon_real,epsilon_imag,n,k,transmission,reflection,absorption"
    np.savetxt(table_path, rows, delimiter=",", header=header, comments="")
    return table_path
