from pathlib import Path

import numpy as np

from eternity.optical_data import (
    interpolate_epsilon,
    load_ellipsometry_psi_delta,
    load_epsilon_table,
    load_multichannel_spectrum,
    load_reflectance_spectrum,
)


def test_load_epsilon_table_accepts_comma_decimal_tabs(tmp_path: Path) -> None:
    path = tmp_path / "epsilon.txt"
    path.write_text("wvl ( nm)\te1\te2\n433,5\t1,0\t2,5\n434,5\t0,5\t3,5\n")

    table = load_epsilon_table(path)

    assert np.allclose(table.wavelengths_nm, [433.5, 434.5])
    assert np.allclose(table.epsilon.real, [1.0, 0.5])
    assert np.allclose(table.epsilon.imag, [2.5, 3.5])


def test_interpolate_epsilon_inside_table(tmp_path: Path) -> None:
    path = tmp_path / "epsilon.txt"
    path.write_text("Wavelength (nm)\te1\te2\n500\t1\t2\n600\t3\t4\n")
    table = load_epsilon_table(path)

    values = interpolate_epsilon(table, np.array([550.0]))

    assert np.allclose(values.real, [2.0])
    assert np.allclose(values.imag, [3.0])


def test_load_reflectance_spectrum_accepts_thesis_export(tmp_path: Path) -> None:
    path = tmp_path / "reflectance.txt"
    path.write_text(
        "Spectroscopic Data at 3.081 min.\n"
        "Wavelength (nm)\tIntensity\n"
        "210\t0.3\n"
        "211\t0.4\n"
    )

    spectrum = load_reflectance_spectrum(path)

    assert np.allclose(spectrum.wavelengths_nm, [210, 211])
    assert np.allclose(spectrum.intensity, [0.3, 0.4])


def test_load_multichannel_spectrum_accepts_p_s_intensity_export(tmp_path: Path) -> None:
    path = tmp_path / "p_s.txt"
    path.write_text(
        "Spectroscopic Data at 13.069 min.\n"
        "Wavelength (nm)\tp-Intensity\ts-Intensity\n"
        "210\t0.08\t0.51\n"
        "211\t0.09\t0.52\n"
    )

    spectrum = load_multichannel_spectrum(path, ["p_intensity", "s_intensity"])

    assert np.allclose(spectrum.wavelengths_nm, [210, 211])
    assert np.allclose(spectrum.channels["p_intensity"], [0.08, 0.09])
    assert np.allclose(spectrum.channels["s_intensity"], [0.51, 0.52])


def test_load_ellipsometry_psi_delta_accepts_export(tmp_path: Path) -> None:
    path = tmp_path / "psi_delta.txt"
    path.write_text(
        "Spectroscopic Data at 13.069 min.\n"
        "Wavelength (nm)\tPsi\tDelta\n"
        "210\t22.0\t130.0\n"
        "211\t21.9\t130.4\n"
    )

    spectrum = load_ellipsometry_psi_delta(path)

    assert np.allclose(spectrum.wavelengths_nm, [210, 211])
    assert np.allclose(spectrum.psi, [22.0, 21.9])
    assert np.allclose(spectrum.delta, [130.0, 130.4])
