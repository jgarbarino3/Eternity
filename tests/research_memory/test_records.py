from __future__ import annotations

import pytest
from pydantic import ValidationError

from eternity.research_memory.records import LabFailureModeRecord, validate_record_payload

BASE_FAILURE_MODE = {
    "schema_version": "0.1",
    "record_type": "lab_failure_mode",
    "title": "TiN/FROG scalar GDD insufficiency",
    "summary": "A scalar GDD-only model does not explain all observed temporal reshaping.",
    "evidence_state": "observed_lab",
    "source_refs": [
        {
            "source_type": "lab_note",
            "locator": "research_memory/examples/tin_frog_failure_mode.yaml",
            "description": "Curated example derived from roadmap failure-mode notes.",
        }
    ],
    "created_at": "2026-05-08T12:00:00Z",
    "tags": ["tin", "frog", "gdd"],
    "related_record_ids": [],
    "claims": [
        "TiN/FROG observations are not universally reproduced by scalar GDD-only replacement."
    ],
    "limitations": ["Example record; not validated against lab holdout data."],
    "next_actions": ["Compare against matched no-sample and neutral-mirror controls."],
    "symptom": "FROG retrieval after TiN reflection shows changed temporal structure.",
    "known_observations": ["Scalar GDD-only replacement is insufficient in at least one run."],
    "likely_causes": ["higher-order spectral phase", "retrieval artifact"],
    "ruled_out_or_weakened": ["scalar GDD-only as a universal explanation"],
    "diagnostic_tests": ["matched no-sample/TiN/neutral-mirror FROG"],
    "related_runs_or_samples": ["B7 Run1"],
    "advisor_safe_summary": (
        "TiN modifies retrieved temporal structure; scalar GDD alone is insufficient in "
        "some cases."
    ),
}


def test_lab_failure_mode_rejects_extra_fields() -> None:
    payload = BASE_FAILURE_MODE | {"unexpected": "not allowed"}

    with pytest.raises(ValidationError):
        LabFailureModeRecord.model_validate(payload)


def test_invalid_evidence_state_fails() -> None:
    payload = BASE_FAILURE_MODE | {"evidence_state": "proven_new_physics"}

    with pytest.raises(ValidationError):
        LabFailureModeRecord.model_validate(payload)


def test_required_provenance_fields_fail_when_missing() -> None:
    payload = dict(BASE_FAILURE_MODE)
    payload.pop("source_refs")

    with pytest.raises(ValidationError):
        LabFailureModeRecord.model_validate(payload)


def test_validated_evidence_requires_validation_artifact_ref() -> None:
    payload = BASE_FAILURE_MODE | {"evidence_state": "validated"}

    with pytest.raises(ValidationError, match="validation_artifact_ref"):
        LabFailureModeRecord.model_validate(payload)


def test_record_dispatch_validates_by_record_type() -> None:
    record = validate_record_payload(BASE_FAILURE_MODE)

    assert isinstance(record, LabFailureModeRecord)
    assert record.record_type == "lab_failure_mode"
    assert record.evidence_state == "observed_lab"
