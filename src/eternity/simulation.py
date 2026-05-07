"""Linear transfer-matrix V0 simulation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from tmm import coh_tmm

from eternity.materials import drude_lorentz_ito, refractive_index_from_epsilon
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


def run_linear_tmm(spec: ExperimentSpec) -> SimulationResult:
    grid = spec.simulator.wavelength_range
    wavelengths_nm = np.linspace(grid.min, grid.max, grid.points)
    epsilon = drude_lorentz_ito(wavelengths_nm)
    n_film = refractive_index_from_epsilon(epsilon)
    thickness_nm = spec.sample.thickness.to("nm").magnitude
    incidence_angle_rad = spec.geometry.incidence_angle.to("rad").magnitude
    pol = "p" if spec.geometry.polarization == "TM" else "s"

    transmission = np.empty_like(wavelengths_nm, dtype=float)
    reflection = np.empty_like(wavelengths_nm, dtype=float)

    for index, wavelength_nm in enumerate(wavelengths_nm):
        result = coh_tmm(
            pol,
            [1.0, n_film[index], 1.45],
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
        "model_level": "linear_tmm_synthetic_v0",
    }

    warnings = [
        {
            "severity": "info",
            "source": "v0_simulation",
            "message": "Synthetic ITO parameters are used; no lab sample has been fitted.",
        },
        {
            "severity": "warning",
            "source": "v0_simulation",
            "message": "Linear transfer-matrix model only; no pump-induced ENZ dynamics.",
        },
    ]
    assumptions = [
        "The ITO film is perfectly flat and homogeneous.",
        "The substrate is modeled as lossless glass with n=1.45.",
        "The incident medium is modeled as air with n=1.0.",
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
