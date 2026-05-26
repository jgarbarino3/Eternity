from __future__ import annotations

from pathlib import Path

import yaml

from eternity.phase3g1 import (
    DEFAULT_QUEUE_PATH,
    Phase3G1Lead,
    build_phase3g1_packet,
    evaluate_phase3g1_lead,
    write_phase3g1_packet,
)


def _lead(
    lead_id: str,
    *,
    intended_use: str = "simulator_validation",
    public: str = "pass",
    constants: str = "pass",
    holdout: str = "pass",
    backside: str = "pass",
    leakage: str = "pass",
    tmm: str = "pass",
    source_hash: str = "pass",
    priority: int = 1,
) -> dict:
    return {
        "lead_id": lead_id,
        "title": f"{lead_id} title",
        "material_family": "simple planar stack",
        "intended_use": intended_use,
        "source_type": "fixture",
        "source_refs": ["fixture"],
        "source_urls": ["https://example.test"],
        "exact_files_or_records": ["nk.csv", "rt.csv"],
        "evidence": {
            "public_access": public,
            "source_qualified_constants_or_model": constants,
            "independent_measured_holdout": holdout,
            "machine_readable_files": "pass",
            "geometry_backed": "pass",
            "stack_thickness_backed": "pass",
            "substrate_backside_coherence_clear": backside,
            "leakage_safe_no_fit_split": leakage,
            "planar_linear_tmm_suitable": tmm,
            "source_hash_ready": source_hash,
        },
        "priority_rank": priority,
        "known_failure_memory": [],
        "notes": [],
        "exact_next_action": "fixture next action",
    }


def _write_queue(path: Path, leads: list[dict]) -> None:
    path.write_text(
        yaml.safe_dump(
            {
                "phase_id": "Phase 3G.1",
                "queue_version": 1,
                "updated_at": "2026-05-26",
                "queue_scope": "fixture",
                "lead_limit": 50,
                "leads": leads,
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )


def test_phase3g1_default_queue_keeps_phase3f2_closed() -> None:
    packet = build_phase3g1_packet(DEFAULT_QUEUE_PATH)

    assert packet["decision"]["status"] == "phase3g1_intake_queue_ready_no_candidate"
    assert packet["decision"]["phase3f2_intake_allowed"] is False
    assert packet["decision"]["residual_modeling_allowed_now"] is False
    assert packet["decision"]["phase4_candidate_ready_now"] is False
    assert packet["summary"]["hard_gate_pass_count"] == 0
    assert packet["failure_memory"]["prior_measured_data_leads"] == 37


def test_phase3g1_selects_full_pass_candidate(tmp_path: Path) -> None:
    queue = tmp_path / "queue.yaml"
    _write_queue(
        queue,
        [
            _lead("full_but_lower_priority", priority=2),
            _lead("full_high_priority", priority=1),
            _lead("blocked_holdout", holdout="missing", priority=1),
        ],
    )

    packet = build_phase3g1_packet(queue)

    assert packet["decision"]["status"] == "phase3g1_candidate_ready_for_phase3f2_source_intake"
    assert packet["decision"]["selected_next_lead_id"] == "full_high_priority"
    assert packet["decision"]["phase3f2_intake_allowed"] is True
    assert packet["decision"]["residual_modeling_allowed_now"] is False
    assert packet["summary"]["hard_gate_pass_count"] == 2


def test_phase3g1_classifies_missing_holdout_as_constants_only() -> None:
    evaluation = evaluate_phase3g1_lead(
        Phase3G1Lead.model_validate(_lead("constants_only", holdout="missing"))
    )

    assert evaluation["computed_intake_label"] == "constants_only"
    assert evaluation["hard_gate_pass"] is False
    assert "independent_measured_holdout" in evaluation["missing_required_flags"]


def test_phase3g1_classifies_leakage_risk_as_weak_holdout() -> None:
    evaluation = evaluate_phase3g1_lead(
        Phase3G1Lead.model_validate(_lead("leakage_risk", leakage="risk"))
    )

    assert evaluation["computed_intake_label"] == "weak_within_dataset_holdout"
    assert evaluation["hard_gate_pass"] is False
    assert "leakage_safe_no_fit_split" in evaluation["missing_required_flags"]


def test_phase3g1_public_labels_cover_future_intake_classes() -> None:
    calibrated = evaluate_phase3g1_lead(
        Phase3G1Lead.model_validate(
            _lead("calibrated", intended_use="enz_calibrated")
        )
    )
    literature = evaluate_phase3g1_lead(
        Phase3G1Lead.model_validate(_lead("literature", tmm="not_applicable"))
    )
    rejected = evaluate_phase3g1_lead(
        Phase3G1Lead.model_validate(_lead("request_only", public="missing"))
    )

    assert calibrated["computed_intake_label"] == "calibrated_candidate_possible"
    assert calibrated["canonical_dataset_label"] == "calibrated_candidate_possible"
    assert literature["computed_intake_label"] == "literature_reproduction_fixture"
    assert literature["canonical_dataset_label"] == "literature_reproduction_fixture"
    assert rejected["computed_intake_label"] == "reject"
    assert rejected["canonical_dataset_label"] == "reject"


def test_phase3g1_writes_report_artifacts(tmp_path: Path) -> None:
    packet = build_phase3g1_packet(DEFAULT_QUEUE_PATH)
    json_path, md_path = write_phase3g1_packet(
        tmp_path,
        packet,
        report_stem="phase3g1_fixture",
    )

    assert json_path.name == "phase3g1_fixture.json"
    assert json_path.exists()
    assert md_path.name == "phase3g1_fixture.md"
    assert md_path.exists()
    assert "Measured-Data Intake Queue" in md_path.read_text(encoding="utf-8")
