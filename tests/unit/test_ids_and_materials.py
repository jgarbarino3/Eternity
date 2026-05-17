from pathlib import Path

import numpy as np

from eternity.ids import deterministic_hash, run_id_for_spec
from eternity.material_provider import epsilon_for_spec
from eternity.materials import drude_lorentz_ito
from eternity.runner import load_spec
from eternity.simulation import run_linear_tmm


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


def test_tabulated_material_provider_loads_registry_epsilon() -> None:
    spec = load_spec(Path("experiments/examples/linear_tion_48_tabulated.yaml"))

    response = epsilon_for_spec(spec, np.array([500.0, 600.0]))

    assert response.metadata["model_level"] == "linear_tmm_tabulated_epsilon_v1_grounding"
    assert np.iscomplexobj(response.epsilon)
    assert np.all(np.isfinite(response.epsilon.real))
    assert np.all(response.epsilon.imag > 0)


def test_phase3a_multilayer_tmm_outputs_finite_spectra() -> None:
    spec = load_spec(Path("experiments/examples/linear_tin_sio2_d10nm_validation_candidate.yaml"))

    result = run_linear_tmm(spec)

    assert result.metrics["model_level"] == "linear_tmm_registry_multilayer_validation_candidate"
    assert result.layer_names == ["TiN", "SiO2", "TiN"]
    assert np.all(np.isfinite(result.reflection))
    assert np.all(np.isfinite(result.transmission))
    assert np.allclose(result.transmission + result.reflection + result.absorption, 1.0)


def test_standrews_multilayer_tmm_outputs_finite_spectra() -> None:
    spec = load_spec(
        Path("experiments/examples/linear_standrews_tin_50nm_validation_candidate.yaml")
    )

    result = run_linear_tmm(spec)

    assert result.metrics["model_level"] == "linear_tmm_registry_multilayer_validation_candidate"
    assert result.layer_names == ["TiN"]
    assert np.all(np.isfinite(result.reflection))
    assert np.all(np.isfinite(result.transmission))
    assert np.allclose(result.transmission + result.reflection + result.absorption, 1.0)
