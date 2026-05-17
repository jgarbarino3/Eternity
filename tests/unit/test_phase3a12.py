import json

from eternity.phase3a12 import (
    build_phase3a12_result,
    build_phase3a12_result_from_path,
    write_phase3a12_result,
)


def _review_input(all_gates_pass: bool = False) -> dict:
    gates = {
        "exact_3l2_quartz_identity": "passed" if all_gates_pass else "failed",
        "stack_30nm_tin_10nm_sio2_20nm_tin": "passed" if all_gates_pass else "failed",
        "s_polarized_or_te_reflectance_channel": "passed" if all_gates_pass else "unresolved",
        "sixty_degree_incidence": "passed",
        "absolute_reflectance_units_or_calibration_state": "passed"
        if all_gates_pass
        else "failed",
        "export_or_source_lineage_to_d10nm_text_trace": "passed" if all_gates_pass else "failed",
    }
    return {
        "phase_id": "Phase 3A.12",
        "source_packet": "docs/phase3a11_manual_source_followup_packet.json",
        "reviewed_candidates": [
            {
                "candidate_id": "phase3a11_candidate_1",
                "sha256": "abc",
                "path": "/tmp/candidate.SEsnap",
                "positive_evidence": ["FitLog line 216 records 60.0 degrees"],
                "negative_evidence": ["No FitLog hits for 3L2 or absolute reflectance."],
                "proof_gate_results": gates,
                "candidate_decision": "source_identity_proven"
                if all_gates_pass
                else "related_but_not_source_identity",
            }
        ],
    }


def test_phase3a12_exhausts_manual_followup_when_gates_fail() -> None:
    result = build_phase3a12_result(_review_input())

    assert result["decision"]["status"] == "manual_source_followup_exhausted"
    assert result["decision"]["source_proof_found"] is False
    assert result["decision"]["can_feed_serious_core"] is False
    assert result["decision"]["phase3a_manual_followup_continuation_recommended"] is False
    assert "absolute_reflectance_units_or_calibration_state" in (
        result["candidate_results"][0]["failed_or_unresolved_gates"]
    )


def test_phase3a12_detects_all_gates_passed_checkpoint_case() -> None:
    result = build_phase3a12_result(_review_input(all_gates_pass=True))

    assert result["decision"]["status"] == "source_proof_found_requires_xhigh_policy_checkpoint"
    assert result["decision"]["source_proof_found"] is True
    assert result["decision"]["can_promote_calibrated_linear_evidence"] is False


def test_phase3a12_writes_result_artifacts_from_path(tmp_path) -> None:
    review_path = tmp_path / "review.json"
    review_path.write_text(json.dumps(_review_input()), encoding="utf-8")

    result = build_phase3a12_result_from_path(review_path)
    json_path, md_path = write_phase3a12_result(tmp_path / "out", result)

    assert json.loads(json_path.read_text())["phase_id"] == "Phase 3A.12"
    assert "Manual Source Review Result" in md_path.read_text()
