from __future__ import annotations

from pathlib import Path

import yaml

from eternity.phase3f1 import (
    DEFAULT_REGISTRY_PATH,
    Phase3F1Candidate,
    build_phase3f1_packet,
    evaluate_phase3f1_candidate,
    write_phase3f1_packet,
)


def _candidate(
    candidate_id: str,
    *,
    material: bool = True,
    holdout: bool = True,
    backside: bool = True,
    leakage: bool = True,
    simplicity: int = 1,
) -> dict:
    return {
        "candidate_id": candidate_id,
        "title": f"{candidate_id} title",
        "material_family": "simple oxide",
        "source_type": "fixture",
        "source_refs": ["fixture"],
        "source_urls": ["https://example.com"],
        "exact_files_or_records": ["nk.csv", "rt.csv"],
        "scouting_notes": ["fixture candidate"],
        "evidence": {
            "public_access": True,
            "machine_readable_material_constants": material,
            "machine_readable_measured_holdout": holdout,
            "geometry_specified": True,
            "stack_thickness_specified": True,
            "substrate_backside_coherence_specified": backside,
            "leakage_safe_no_fit_split": leakage,
            "tmm_suitable": True,
            "source_hash_ready": True,
        },
        "tie_breakers": {
            "stack_simplicity_rank": simplicity,
            "normal_incidence": True,
            "open_format_priority": 1,
            "non_enz_or_non_claim_context": True,
            "substrate_backside_clarity_rank": 1,
        },
        "proposed_scout_label": "promising_but_blocked",
        "decision": "fixture_decision",
        "blockers": [],
        "exact_next_action": "fixture_next",
    }


def _write_registry(path: Path, candidates: list[dict]) -> None:
    path.write_text(
        yaml.safe_dump(
            {
                "phase_id": "Phase 3F.1",
                "registry_version": 1,
                "updated_at": "2026-05-25",
                "search_scope": "fixture",
                "candidate_limit": 10,
                "candidates": candidates,
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )


def test_phase3f1_default_registry_keeps_phase_open_without_residuals() -> None:
    packet = build_phase3f1_packet(DEFAULT_REGISTRY_PATH)

    assert packet["decision"]["status"] == "phase3f1_no_candidate_ready_keep_phase3f_open"
    assert packet["decision"]["phase3f2_intake_allowed"] is False
    assert packet["decision"]["residual_modeling_performed"] is False
    assert packet["decision"]["tmm_adapter_started"] is False
    assert packet["summary"]["candidate_count"] == 10
    assert packet["summary"]["hard_gate_pass_count"] == 0


def test_phase3f1_gate_allows_full_candidate_and_selects_simplest(tmp_path: Path) -> None:
    registry = tmp_path / "registry.yaml"
    _write_registry(
        registry,
        [
            _candidate("full_but_less_simple", simplicity=2),
            _candidate("full_simpler", simplicity=1),
            _candidate("missing_holdout", holdout=False),
            _candidate("missing_backside", backside=False),
            _candidate("leakage_risk", leakage=False),
        ],
    )

    packet = build_phase3f1_packet(registry)

    assert packet["decision"]["status"] == "phase3f1_candidate_ready_for_intake_gate"
    assert packet["decision"]["selected_next_candidate_id"] == "full_simpler"
    assert packet["decision"]["phase3f2_intake_allowed"] is True
    assert packet["summary"]["hard_gate_pass_count"] == 2


def test_phase3f1_evaluation_reports_specific_missing_flags() -> None:
    evaluation = evaluate_phase3f1_candidate(
        Phase3F1Candidate.model_validate(
            _candidate("blocked", holdout=False, backside=False, leakage=False)
        )
    )

    assert evaluation["hard_gate_pass"] is False
    assert "machine_readable_measured_holdout" in evaluation["missing_required_flags"]
    assert "substrate_backside_coherence_specified" in evaluation["missing_required_flags"]
    assert "leakage_safe_no_fit_split" in evaluation["missing_required_flags"]


def test_phase3f1_writes_report_artifacts(tmp_path: Path) -> None:
    packet = build_phase3f1_packet(DEFAULT_REGISTRY_PATH)
    json_path, md_path = write_phase3f1_packet(tmp_path, packet)

    assert json_path.exists()
    assert md_path.exists()
    assert "Simple Thin-Film Simulator-Validation Scout" in md_path.read_text(
        encoding="utf-8"
    )
