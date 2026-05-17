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
    assert (
        registry.measurements["phase3a_30_20_10_reflectance_measurement"].sample_ref
        == "phase3a_30_20_10_candidate"
    )
    assert (
        registry.measurements["thesis_reflectance_d_10nm_initial_measurement"].stack_ref
        == "thesis_d_10nm_thesis_reflectance_stack"
    )
    assert registry.splits["synthetic_v0_contract_split"].evidence_strength == "synthetic_fixture"
    assert registry.splits["tin_tion_optical_constants_no_holdout"].evidence_strength == (
        "calibration_only_no_holdout"
    )
    assert registry.splits["thesis_d_10nm_phase3a_validation_candidate"].evidence_strength == (
        "weak_within_dataset_holdout"
    )
    assert registry.raw_artifacts["public_standrews_tin_50nm_reflectance"].source_type == (
        "literature_table"
    )
    assert registry.material_models["public_standrews_tin_50nm_50c_epsilon_model"].kind == (
        "tabulated_epsilon"
    )
    split = registry.splits["public_standrews_tin_50nm_50c_validation_candidate"]
    assert split.evidence_strength == "weak_within_dataset_holdout"


def test_registry_integrity_checks_real_data_snapshots() -> None:
    registry_path = Path("lab_data/registry.yaml")
    registry = load_registry(registry_path)

    report = validate_registry_integrity(registry, registry_path)

    assert report.ok
    assert report.issues == []
