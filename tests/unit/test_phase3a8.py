import json
from pathlib import Path

from eternity.phase3a8 import (
    build_phase3a8_triage,
    load_phase3a7_recovery,
    write_phase3a8_triage,
)


def _candidate(
    *,
    path: str,
    sha256: str,
    score: int,
    reasons: list[str],
    snippets: list[str],
    absolute_reflectance_proof: bool = False,
) -> dict:
    return {
        "path": path,
        "kind": "sesnap",
        "sha256": sha256,
        "score": score,
        "match_reasons": reasons,
        "absolute_reflectance_proof": absolute_reflectance_proof,
        "evidence_snippets": snippets,
    }


def _recovery(candidates: list[dict]) -> dict:
    return {
        "phase_id": "Phase 3A.7",
        "title": "CompleteEASE Source Recovery + 3L2 Provenance Lock",
        "decision": {
            "exact_source_identity_status": "not_found",
            "absolute_reflectance_status": "absolute_reflectance_blocked",
            "can_feed_serious_core": False,
            "can_promote_calibrated_linear_evidence": False,
        },
        "candidate_sources": candidates,
    }


def test_phase3a8_deduplicates_candidates_by_sha256() -> None:
    duplicate_a = _candidate(
        path="/tmp/archive.zip::quartz 10nm pulsed.SEsnap",
        sha256="abc",
        score=40,
        reasons=["mentions_quartz", "mentions_10nm_or_11nm"],
        snippets=["quartz 10nm SiO2 cap pulsed 0-12Vdc"],
    )
    duplicate_b = _candidate(
        path="/tmp/extracted/quartz 10nm pulsed.SEsnap",
        sha256="abc",
        score=42,
        reasons=["mentions_completeease"],
        snippets=["CompleteEASE quartz dynamic"],
    )

    triage = build_phase3a8_triage(_recovery([duplicate_a, duplicate_b]))

    assert triage["inputs"]["input_candidate_count"] == 2
    assert triage["inputs"]["deduped_candidate_count"] == 1
    candidate = triage["categories"]["manual_followup_priority"][0]
    assert candidate["duplicate_paths"] == [duplicate_a["path"], duplicate_b["path"]]
    assert candidate["score"] == 42
    assert "mentions_completeease" in candidate["match_reasons"]


def test_phase3a8_ranks_quartz_dynamic_candidate_above_si_control() -> None:
    si_control = _candidate(
        path="/tmp/Puck 1 Si 100 10nm intensity.SEsnap",
        sha256="si",
        score=46,
        reasons=["mentions_three_layer", "mentions_10nm_or_11nm"],
        snippets=["Si 100 N type 2 in-reflection intensity"],
    )
    quartz_dynamic = _candidate(
        path="/tmp/quartz 10nm SiO2 cap pulsed 0-12Vdc.SEsnap",
        sha256="quartz",
        score=40,
        reasons=["mentions_quartz", "mentions_10nm_or_11nm"],
        snippets=["CompleteEASE quartz 10nm SiO2 cap pulsed 0-12Vdc"],
    )

    triage = build_phase3a8_triage(_recovery([si_control, quartz_dynamic]))

    assert triage["categories"]["manual_followup_priority"][0]["sha256"] == "quartz"
    assert triage["categories"]["wrong_substrate_or_control"][0]["sha256"] == "si"


def test_phase3a8_keeps_absolute_reflectance_blocked_and_pivots_by_default() -> None:
    triage = build_phase3a8_triage(
        _recovery(
            [
                _candidate(
                    path="/tmp/quartz 10nm SiO2 cap pulsed.SEsnap",
                    sha256="quartz",
                    score=40,
                    reasons=["mentions_quartz", "mentions_10nm_or_11nm"],
                    snippets=["CompleteEASE quartz 10nm SiO2 cap pulsed"],
                )
            ]
        )
    )

    assert triage["decision"]["final_decision"] == "pivot_to_relative_only_diagnostic"
    assert triage["decision"]["absolute_reflectance_status"] == "absolute_reflectance_blocked"
    assert triage["decision"]["can_feed_serious_core"] is False
    assert triage["decision"]["can_promote_calibrated_linear_evidence"] is False


def test_phase3a8_writes_triage_and_policy_artifacts(tmp_path: Path) -> None:
    recovery_path = tmp_path / "phase3a7.json"
    recovery_path.write_text(
        json.dumps(
            _recovery(
                [
                    _candidate(
                        path="/tmp/quartz 10nm SiO2 cap pulsed.SEsnap",
                        sha256="quartz",
                        score=40,
                        reasons=["mentions_quartz", "mentions_10nm_or_11nm"],
                        snippets=["CompleteEASE quartz 10nm SiO2 cap pulsed"],
                    )
                ]
            )
        ),
        encoding="utf-8",
    )

    triage = build_phase3a8_triage(load_phase3a7_recovery(recovery_path))
    json_path, md_path, policy_path = write_phase3a8_triage(tmp_path / "out", triage)

    assert json.loads(json_path.read_text())["phase_id"] == "Phase 3A.8"
    assert "Source Candidate Triage" in md_path.read_text()
    policy = policy_path.read_text()
    assert "can_feed_serious_core: false" in policy
    assert "relative_only_diagnostic" in policy
