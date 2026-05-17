import json

import pytest

from eternity.phase3a11 import (
    build_phase3a11_packet,
    build_phase3a11_packet_from_paths,
    write_phase3a11_packet,
)


def _decision(branch: str = "limited_manual_source_followup_first") -> dict:
    return {
        "phase_id": "Phase 3A.10",
        "decision": {"selected_branch": branch},
        "manual_source_followup": {
            "targets": [
                {
                    "path": "/tmp/quartz 10nm pulsed.SEsnap",
                    "sha256": "abc",
                    "priority": 86,
                    "score": 40,
                    "rationale": "matches quartz dynamic",
                }
            ]
        },
    }


def _triage() -> dict:
    return {
        "phase_id": "Phase 3A.8",
        "categories": {
            "manual_followup_priority": [
                {
                    "path": "/tmp/quartz 10nm pulsed.SEsnap",
                    "sha256": "abc",
                    "triage_priority_score": 86,
                    "score": 40,
                    "triage_rationale": "matches quartz dynamic",
                    "member_path": "archive/candidate.SEsnap",
                    "container_path": "/tmp/source.zip",
                    "inner_ise_entries": ["candidate.iSE"],
                    "archive_entries": [{"name": "_FitLog", "size_bytes": 123}],
                    "match_reasons": ["mentions_quartz", "mentions_10nm_or_11nm"],
                    "evidence_snippets": [
                        "60.0 0.0 F -5.0 5.0 F '60.0deg'",
                        "'Absolute MSE'",
                    ],
                    "absolute_reflectance_proof": False,
                    "can_prove_absolute_reflectance": False,
                }
            ]
        },
    }


def test_phase3a11_builds_bounded_manual_packet() -> None:
    packet = build_phase3a11_packet(_decision(), _triage())

    assert packet["phase_id"] == "Phase 3A.11"
    assert packet["decision"]["status"] == "manual_review_packet_ready"
    assert packet["decision"]["candidate_count"] == 1
    assert packet["decision"]["can_feed_serious_core"] is False
    assert packet["scope"]["search_mode"] == "no_new_broad_search"
    assert packet["candidates"][0]["inner_ise_entries"] == ["candidate.iSE"]
    assessment = packet["candidates"][0]["current_assessment"]
    assert assessment["absolute_reflectance_proof_found"] is False
    assert "absolute_reflectance_units_or_calibration_state" in packet["proof_gates"]


def test_phase3a11_rejects_non_manual_branch() -> None:
    with pytest.raises(ValueError, match="limited_manual_source_followup_first"):
        build_phase3a11_packet(_decision(branch="return_to_phase3b_evidence_gathering"), _triage())


def test_phase3a11_writes_artifacts_from_paths(tmp_path) -> None:
    decision_path = tmp_path / "decision.json"
    triage_path = tmp_path / "triage.json"
    decision_path.write_text(json.dumps(_decision()), encoding="utf-8")
    triage_path.write_text(json.dumps(_triage()), encoding="utf-8")

    packet = build_phase3a11_packet_from_paths(decision_path, triage_path)
    json_path, md_path = write_phase3a11_packet(tmp_path / "out", packet)

    assert json.loads(json_path.read_text())["phase_id"] == "Phase 3A.11"
    assert "Phase 3A.11 Bounded Manual Source Follow-Up Packet" in md_path.read_text()
