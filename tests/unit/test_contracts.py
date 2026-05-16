import pytest
from pydantic import ValidationError

from eternity.contracts import (
    AxisSpec,
    DataSplitRecord,
    MaterialModelRecord,
    MeasurementRecord,
    QuantityWithUncertainty,
    RawArtifactRecord,
    SampleRecord,
)


def test_raw_artifact_record_requires_sha256_and_source_type() -> None:
    record = RawArtifactRecord(
        raw_artifact_id="synthetic_transmission_csv",
        kind="csv",
        path="lab_data/raw/synthetic_v0/transmission_fixture.csv",
        sha256="a" * 64,
        bytes=100,
        source_type="synthetic",
        immutable=True,
    )

    assert record.sha256 == "a" * 64
    assert record.source_type == "synthetic"


def test_raw_artifact_record_rejects_bad_sha256() -> None:
    with pytest.raises(ValidationError):
        RawArtifactRecord(
            raw_artifact_id="bad",
            kind="csv",
            path="bad.csv",
            sha256="not-a-hash",
            bytes=1,
            source_type="synthetic",
            immutable=True,
        )


def test_measurement_record_requires_geometry_and_uncertainty_label() -> None:
    record = MeasurementRecord(
        measurement_id="synthetic_t_001",
        kind="transmission_spectrum",
        raw_artifact_ref="synthetic_transmission_csv",
        sample_ref="synthetic_ito_001",
        stack_ref="synthetic_air_ito_glass",
        x_axis=AxisSpec(
            quantity="vacuum_wavelength",
            unit="nm",
            values_column="wavelength_nm",
        ),
        y_quantity="transmission",
        y_unit="fraction",
        y_values_column="transmission",
        uncertainty_type="scalar",
        geometry_incidence_angle=QuantityWithUncertainty(value=0, unit="deg"),
        geometry_polarization="TM",
        preprocessing=["synthetic fixture generated from V0 model"],
        forbidden_for_fitting=False,
    )

    assert record.geometry_polarization == "TM"
    assert record.uncertainty_type == "scalar"


def test_split_declares_evidence_strength_and_no_holdout_access() -> None:
    split = DataSplitRecord(
        split_id="synthetic_contract_split",
        raw_data_refs=["synthetic_transmission_csv"],
        created_before_fit=True,
        method="explicit_indices",
        calibration_measurement_refs=["synthetic_t_001"],
        holdout_measurement_refs=[],
        fitting_may_access_holdout_y=False,
        ai_playground_may_access_holdout_y_before_fit=False,
        evidence_strength="synthetic_fixture",
    )

    assert split.created_before_fit
    assert not split.fitting_may_access_holdout_y


def test_split_accepts_weak_within_dataset_holdout_label() -> None:
    split = DataSplitRecord(
        split_id="phase3a_candidate_split",
        raw_data_refs=["tin", "reflectance"],
        created_before_fit=True,
        method="measurement_ids",
        calibration_measurement_refs=["tin_epsilon"],
        holdout_measurement_refs=["d10_initial"],
        fitting_may_access_holdout_y=False,
        ai_playground_may_access_holdout_y_before_fit=False,
        evidence_strength="weak_within_dataset_holdout",
    )

    assert split.evidence_strength == "weak_within_dataset_holdout"


def test_material_model_record_declares_tabulated_epsilon_boundaries() -> None:
    sample = SampleRecord(
        sample_id="tion_48_40nm_0p8pa",
        material="TiON",
        source_type="lab",
        nominal_thickness=QuantityWithUncertainty(value=40, unit="nm"),
    )
    model = MaterialModelRecord(
        material_model_id="tion_48_0p8pa_epsilon_model",
        sample_ref=sample.sample_id,
        kind="tabulated_epsilon",
        source_type="lab",
        raw_artifact_ref="tion_48_0p8pa_epsilon",
        source_measurement_ref="tion_48_0p8pa_epsilon_measurement",
        equation_convention="epsilon = epsilon_real + i epsilon_imag",
        sign_convention="exp(-i omega t)",
        interpolation="linear",
        extrapolation="forbidden",
        enz_definition="Re(epsilon)=0 crossing",
        enz_wavelengths_nm=[497.271],
        wavelength_min_nm=433.428676,
        wavelength_max_nm=1707.810202,
        passivity_check="pass",
    )

    assert model.kind == "tabulated_epsilon"
    assert model.extrapolation == "forbidden"
