"""Load small tabulated optical and reflectance data artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass(frozen=True)
class EpsilonTable:
    wavelengths_nm: np.ndarray
    epsilon: np.ndarray


@dataclass(frozen=True)
class ReflectanceSpectrum:
    wavelengths_nm: np.ndarray
    intensity: np.ndarray


@dataclass(frozen=True)
class MultiChannelSpectrum:
    wavelengths_nm: np.ndarray
    channels: dict[str, np.ndarray]


@dataclass(frozen=True)
class EllipsometryPsiDelta:
    wavelengths_nm: np.ndarray
    psi: np.ndarray
    delta: np.ndarray


def _numeric_fields(line: str) -> list[float] | None:
    stripped = line.strip()
    if not stripped:
        return None
    if "\t" in stripped or " " in stripped:
        fields = stripped.replace(",", ".").split()
    else:
        fields = stripped.split(",")
    values: list[float] = []
    for field in fields:
        try:
            values.append(float(field))
        except ValueError:
            return None
    return values


def _validate_axis(wavelengths_nm: np.ndarray, path: Path) -> None:
    if wavelengths_nm.size < 2:
        raise ValueError(f"{path} must contain at least two numeric rows")
    if not np.all(np.isfinite(wavelengths_nm)):
        raise ValueError(f"{path} contains non-finite wavelength values")
    if np.any(np.diff(wavelengths_nm) <= 0):
        raise ValueError(f"{path} wavelength axis must be strictly increasing")


def load_epsilon_table(path: Path) -> EpsilonTable:
    """Load wavelength/e1/e2 text tables exported with dot or comma decimals."""

    rows: list[list[float]] = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        values = _numeric_fields(line)
        if values is not None and len(values) >= 3:
            rows.append(values[:3])

    table = np.asarray(rows, dtype=float)
    if table.ndim != 2 or table.shape[1] != 3:
        raise ValueError(f"{path} does not look like a wavelength/e1/e2 table")

    wavelengths_nm = table[:, 0]
    epsilon = table[:, 1] + 1j * table[:, 2]
    _validate_axis(wavelengths_nm, path)
    if not np.all(np.isfinite(epsilon.real)) or not np.all(np.isfinite(epsilon.imag)):
        raise ValueError(f"{path} contains non-finite epsilon values")
    return EpsilonTable(wavelengths_nm=wavelengths_nm, epsilon=epsilon)


def load_reflectance_spectrum(path: Path) -> ReflectanceSpectrum:
    """Load thesis wavelength/intensity reflectance spectra."""

    rows: list[list[float]] = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        values = _numeric_fields(line)
        if values is not None and len(values) >= 2:
            rows.append(values[:2])

    table = np.asarray(rows, dtype=float)
    if table.ndim != 2 or table.shape[1] != 2:
        raise ValueError(f"{path} does not look like a wavelength/intensity table")

    wavelengths_nm = table[:, 0]
    intensity = table[:, 1]
    _validate_axis(wavelengths_nm, path)
    if not np.all(np.isfinite(intensity)):
        raise ValueError(f"{path} contains non-finite intensity values")
    return ReflectanceSpectrum(wavelengths_nm=wavelengths_nm, intensity=intensity)


def load_multichannel_spectrum(
    path: Path,
    channel_names: list[str] | None = None,
) -> MultiChannelSpectrum:
    """Load wavelength plus one or more numeric optical channels."""

    rows: list[list[float]] = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        values = _numeric_fields(line)
        if values is not None and len(values) >= 2:
            rows.append(values)

    table = np.asarray(rows, dtype=float)
    if table.ndim != 2 or table.shape[1] < 2:
        raise ValueError(f"{path} does not look like a wavelength/channel table")

    wavelengths_nm = table[:, 0]
    _validate_axis(wavelengths_nm, path)
    channel_count = table.shape[1] - 1
    names = channel_names or [f"channel_{index + 1}" for index in range(channel_count)]
    if len(names) != channel_count:
        raise ValueError(
            f"{path} has {channel_count} numeric channels, but {len(names)} names were provided"
        )
    channels = {
        name: table[:, index + 1]
        for index, name in enumerate(names)
    }
    for name, values in channels.items():
        if not np.all(np.isfinite(values)):
            raise ValueError(f"{path} contains non-finite values for {name}")
    return MultiChannelSpectrum(wavelengths_nm=wavelengths_nm, channels=channels)


def load_ellipsometry_psi_delta(path: Path) -> EllipsometryPsiDelta:
    """Load wavelength/Psi/Delta ellipsometry exports."""

    table = load_multichannel_spectrum(path, ["psi", "delta"])
    return EllipsometryPsiDelta(
        wavelengths_nm=table.wavelengths_nm,
        psi=table.channels["psi"],
        delta=table.channels["delta"],
    )


def interpolate_epsilon(table: EpsilonTable, wavelengths_nm: np.ndarray) -> np.ndarray:
    requested = np.asarray(wavelengths_nm, dtype=float)
    lower = float(table.wavelengths_nm.min())
    upper = float(table.wavelengths_nm.max())
    if requested.min() < lower or requested.max() > upper:
        raise ValueError(
            "requested wavelength grid extends outside tabulated material range "
            f"{lower:.3f}-{upper:.3f} nm"
        )

    real = np.interp(requested, table.wavelengths_nm, table.epsilon.real)
    imag = np.interp(requested, table.wavelengths_nm, table.epsilon.imag)
    return real + 1j * imag
