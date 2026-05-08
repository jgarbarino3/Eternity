"""Claim-status labels for Eternity run outputs."""

from __future__ import annotations

from enum import StrEnum


class ClaimStatus(StrEnum):
    SYNTHETIC_SOFTWARE_FIXTURE = "synthetic_software_fixture"
    LITERATURE_REPRODUCTION_FIXTURE = "literature_reproduction_fixture"
    CALIBRATION_ONLY_NO_HOLDOUT = "calibration_only_no_holdout"
    WEAK_WITHIN_DATASET_HOLDOUT = "weak_within_dataset_holdout"
    CALIBRATED_LINEAR_EVIDENCE = "calibrated_linear_evidence"
    FAILED_VALIDATION = "failed_validation"


def can_feed_serious_core(status: ClaimStatus) -> bool:
    return status is ClaimStatus.CALIBRATED_LINEAR_EVIDENCE
