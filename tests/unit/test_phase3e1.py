from __future__ import annotations

from pathlib import Path

from eternity.phase3e1 import DatasetCandidate, build_phase3e1_scaffold, evaluate_candidate

REGISTRY_PATH = Path("docs/phase3e1_dataset_candidate_registry.yaml")


def test_phase3e1_registry_blocks_current_candidates_from_phase4() -> None:
    packet = build_phase3e1_scaffold(REGISTRY_PATH)

    assert packet["decision"]["status"] == "phase3e1_scaffold_ready_no_phase4_candidate"
    assert packet["decision"]["can_open_phase4_now"] is False
    assert packet["decision"]["can_feed_serious_core_now"] is False
    assert packet["decision"]["claim_standard_changed"] is False
    assert packet["decision"]["recommended_next_phase"] == (
        "Phase 3E.4 - renewed ENZ public-data search through stack-contract gate"
    )
    assert packet["summary"]["candidate_count"] >= 8
    assert packet["summary"]["phase4_candidate_count"] == 0
    assert packet["summary"]["phase4_candidate_ids"] == []

    by_id = {item["candidate_id"]: item for item in packet["candidate_evaluations"]}
    assert by_id["saha_tin_azo_2023"]["computed_gate_label"] == "weak_within_dataset_holdout"
    assert "machine_readable_numerical_data" not in by_id["saha_tin_azo_2023"][
        "missing_required_flags"
    ]
    assert "absolute_calibration_documented" in by_id["saha_tin_azo_2023"][
        "missing_required_flags"
    ]
    assert by_id["acs_intracavity_ito_2025"]["computed_gate_label"] == (
        "literature_reproduction_fixture"
    )
    assert "independent_measured_holdout" in by_id["acs_intracavity_ito_2025"][
        "missing_required_flags"
    ]


def test_phase3e1_gate_allows_only_full_public_holdout_candidate() -> None:
    candidate = DatasetCandidate.model_validate(
        {
            "candidate_id": "hypothetical_clean_candidate",
            "title": "Hypothetical clean public dataset",
            "material_family": "ITO",
            "source_type": "public_csv_repository",
            "source_refs": ["DOI 10.example/example"],
            "public_data_links": ["https://example.com/data.zip"],
            "exact_files": ["epsilon.csv", "absolute_reflectance.csv"],
            "evidence": {
                "data_are_public": True,
                "no_author_contact_required": True,
                "identified_sample_stack": True,
                "source_qualified_material_model": True,
                "independent_measured_holdout": True,
                "machine_readable_numerical_data": True,
                "absolute_calibration_documented": True,
                "geometry_specified": True,
                "calibration_holdout_split_predeclared": True,
                "holdout_not_known_used_for_fit": True,
                "tmm_appropriate": True,
                "no_existing_nonpromoting_validation": True,
            },
            "proposed_claim_label": "calibrated_linear_candidate",
            "decision": "ready_for_phase4_gate_review",
        }
    )

    evaluation = evaluate_candidate(candidate)

    assert evaluation["can_enter_phase4"] is True
    assert evaluation["computed_gate_label"] == "calibrated_linear_candidate"
    assert evaluation["missing_required_flags"] == []
    assert evaluation["serious_core_allowed_now"] is False
