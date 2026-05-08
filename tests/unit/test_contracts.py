import pytest
from pydantic import ValidationError

from eternity.contracts import (
    AxisSpec,
    DataSplitRecord,
    MeasurementRecord,
    QuantityWithUncertainty,
    RawArtifactRecord,
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
