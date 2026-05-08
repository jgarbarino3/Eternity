from eternity.claim_status import ClaimStatus, can_feed_serious_core


def test_only_calibrated_linear_evidence_feeds_serious_core() -> None:
    assert can_feed_serious_core(ClaimStatus.CALIBRATED_LINEAR_EVIDENCE)
    assert not can_feed_serious_core(ClaimStatus.SYNTHETIC_SOFTWARE_FIXTURE)
    assert not can_feed_serious_core(ClaimStatus.LITERATURE_REPRODUCTION_FIXTURE)
    assert not can_feed_serious_core(ClaimStatus.CALIBRATION_ONLY_NO_HOLDOUT)
    assert not can_feed_serious_core(ClaimStatus.WEAK_WITHIN_DATASET_HOLDOUT)
    assert not can_feed_serious_core(ClaimStatus.FAILED_VALIDATION)
