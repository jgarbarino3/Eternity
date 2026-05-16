from pathlib import Path

from eternity.registry import load_registry, validate_registry_integrity


def test_registry_loads_contract_fixture() -> None:
    registry = load_registry(Path("lab_data/registry.yaml"))

    assert registry.raw_artifacts["synthetic_v0_transmission"].source_type == "synthetic"
    assert registry.raw_artifacts["tion_48_0p8pa_epsilon"].source_type == "lab"
    assert registry.material_models["tion_48_0p8pa_epsilon_model"].kind == "tabulated_epsilon"
    assert registry.material_models["sio2_sellmeier_epsilon_model"].kind == "tabulated_epsilon"
    assert registry.measurements["synthetic_v0_transmission_measurement"].kind == (
        "transmission_spectrum"
    )
    assert registry.measurements["phase3a_30_20_10_psi_delta_measurement"].kind == (
        "ellipsometry_psi_delta"
    )
    assert registry.splits["synthetic_v0_contract_split"].evidence_strength == "synthetic_fixture"
    assert registry.splits["tin_tion_optical_constants_no_holdout"].evidence_strength == (
        "calibration_only_no_holdout"
    )
    assert registry.splits["thesis_d_10nm_phase3a_validation_candidate"].evidence_strength == (
        "weak_within_dataset_holdout"
    )


def test_registry_integrity_checks_real_data_snapshots() -> None:
    registry_path = Path("lab_data/registry.yaml")
    registry = load_registry(registry_path)

    report = validate_registry_integrity(registry, registry_path)

    assert report.ok
    assert report.issues == []
