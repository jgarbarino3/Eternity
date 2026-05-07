"""Synthetic V0 optical material models."""

from __future__ import annotations

import numpy as np

SPEED_OF_LIGHT = 299_792_458.0


def drude_lorentz_ito(wavelengths_nm: np.ndarray) -> np.ndarray:
    """Return synthetic ITO epsilon for the V0 toy model.

    The parameters are deliberately synthetic. They are chosen to make a stable
    ENZ-like spectrum near the telecom band, not to represent a lab sample.
    """

    wavelengths_m = np.asarray(wavelengths_nm, dtype=float) * 1e-9
    omega = 2 * np.pi * SPEED_OF_LIGHT / wavelengths_m

    eps_inf = 3.8
    omega_p = 2.45e15
    gamma = 1.8e14
    drude = -(omega_p**2) / (omega**2 + 1j * gamma * omega)

    oscillator_strength = 0.18
    omega_0 = 3.3e15
    gamma_l = 4.8e14
    lorentz = oscillator_strength * omega_0**2 / (omega_0**2 - omega**2 - 1j * gamma_l * omega)

    return eps_inf + drude + lorentz


def refractive_index_from_epsilon(epsilon: np.ndarray) -> np.ndarray:
    return np.sqrt(epsilon.astype(complex))
