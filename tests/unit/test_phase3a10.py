import json
from pathlib import Path

import yaml

from eternity.phase3a10 import (
    build_phase3a10_decision,
    build_phase3a10_decision_from_paths,
    write_phase3a10_decision,
)


def _triage(manual: bool = True) -> dict:
    return {
        "phase_id": "Phase 3A.8",
        "categories": {
            "manual_followup_priority": [
                {
                    "path": "/tmp/quartz 10nm pulsed.SEsnap",
                    "sha256": "abc",
                    "triage_priority_score": 86,
                    "score": 40,
                    "triage_rationale": "matches quartz plus 10 nm/dynamic-source clues",
                }
            ]
            if manual
            else []
        },
    }


def _diagnostic(shape_correlation: float = 0.986, trend_agreement: bool = True) -> dict:
    return {
        "phase_id": "Phase 3A.9",
        "decision": {"status": "relative_only_diagnostic_packet_ready"},
        "diagnostics": {
            "shape_correlation_minmax": shape_correlation,
            "trend_direction_agreement": trend_agreement,
        },
    }


def _registry(with_tion_rt: bool = False) -> dict:
    measurements = {
        "tion_48_0p8pa_epsilon_measurement": {
            "sample_ref": "tion_48_40nm_0p8pa",
            "kind": "epsilon_table",
            "y_quantity": "complex_dielectric_function",
        }
    }
    if with_tion_rt:
        measurements["tion_48_reflectance_measurement"] = {
            "sample_ref": "tion_48_40nm_0p8pa",
            "kind": "reflection_spectrum",
            "y_quantity": "reflectance",
        }
    return {
        "raw_artifacts": {
            "tion_48_0p8pa_epsilon": {},
            "tion_49_1p0pa_epsilon": {},
        },
        "measurements": measurements,
        "material_models": {
            "tion_48_0p8pa_epsilon_model": {},
            "tion_49_1p0pa_epsilon_model": {},
        },
    }


def test_phase3a10_selects_limited_manual_followup_for_strong_clue() -> None:
    packet = build_phase3a10_decision(_triage(), _diagnostic(), _registry())

    assert packet["decision"]["selected_branch"] == "limited_manual_source_followup_first"
    assert packet["decision"]["can_feed_serious_core"] is False
    assert packet["manual_source_followup"]["candidate_count"] == 1
    assert packet["phase3b_return"]["tion_status"]["phase3b_ready_for_calibrated_evidence"] is False


def test_phase3a10_returns_to_phase3b_if_tion_rt_exists_and_manual_clue_is_weak() -> None:
    packet = build_phase3a10_decision(
        _triage(),
        _diagnostic(shape_correlation=0.5, trend_agreement=False),
        _registry(with_tion_rt=True),
    )

    assert packet["decision"]["selected_branch"] == "return_to_phase3b_evidence_gathering"
    assert packet["phase3b_return"]["tion_status"]["raw_rt_measurements_registered"] == [
        "tion_48_reflectance_measurement"
    ]


def test_phase3a10_requests_clean_export_when_no_manual_or_tion_rt() -> None:
    packet = build_phase3a10_decision(_triage(manual=False), _diagnostic(), _registry())

    assert packet["decision"]["selected_branch"] == "request_clean_export_or_measurement"
    assert packet["manual_source_followup"]["status"] == "no_candidates"


def test_phase3a10_writes_decision_artifacts_from_paths(tmp_path: Path) -> None:
    triage_path = tmp_path / "triage.json"
    diagnostic_path = tmp_path / "diagnostic.json"
    registry_path = tmp_path / "registry.yaml"
    triage_path.write_text(json.dumps(_triage()), encoding="utf-8")
    diagnostic_path.write_text(json.dumps(_diagnostic()), encoding="utf-8")
    registry_path.write_text(yaml.safe_dump(_registry()), encoding="utf-8")

    packet = build_phase3a10_decision_from_paths(triage_path, diagnostic_path, registry_path)
    json_path, md_path = write_phase3a10_decision(tmp_path / "out", packet)

    assert json.loads(json_path.read_text())["phase_id"] == "Phase 3A.10"
    assert "Phase 3A.10 Branch Decision" in md_path.read_text()
