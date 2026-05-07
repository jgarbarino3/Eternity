import numpy as np

from eternity.ids import deterministic_hash, run_id_for_spec
from eternity.materials import drude_lorentz_ito


def test_hashing_and_run_id_are_deterministic() -> None:
    payload = {"b": [2, 1], "a": "same"}

    assert deterministic_hash(payload) == deterministic_hash(payload)
    assert run_id_for_spec(payload) == run_id_for_spec(payload)


def test_drude_material_has_finite_complex_epsilon() -> None:
    wavelengths_nm = np.linspace(1300, 1700, 21)

    epsilon = drude_lorentz_ito(wavelengths_nm)

    assert np.iscomplexobj(epsilon)
    assert np.all(np.isfinite(epsilon.real))
    assert np.all(np.isfinite(epsilon.imag))
