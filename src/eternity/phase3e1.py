"""Phase 3E.1 public-dataset gate and assistant scaffold."""

from __future__ import annotations

import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

GateLabel = Literal[
    "calibrated_linear_candidate",
    "weak_within_dataset_holdout",
    "calibration_only_no_holdout",
    "literature_reproduction_fixture",
    "failed_validation",
    "blocked_source_data_lead",
    "rejected_candidate",
]

REQUIRED_PHASE4_FLAGS = {
    "data_are_public": "public data access without private credentials",
    "no_author_contact_required": "no author contact or request-only dependency",
    "identified_sample_stack": "identified sample, stack, substrate, and thickness context",
    "source_qualified_material_model": "source-qualified optical constants or fitted model",
    "independent_measured_holdout": "independent measured optical holdout",
    "machine_readable_numerical_data": "machine-readable numerical calibration and holdout data",
    "absolute_calibration_documented": "documented absolute R/T/A or ellipsometry scale",
    "geometry_specified": "angle, polarization, side, and unit context specified",
    "calibration_holdout_split_predeclared": "calibration/holdout split can be predeclared",
    "holdout_not_known_used_for_fit": "holdout is not known to have fit/tuned the model",
    "tmm_appropriate": "planar linear TMM is physically appropriate",
    "no_existing_nonpromoting_validation": "candidate has not already failed or downgraded here",
}


class EvidenceFlags(BaseModel):
    data_are_public: bool
    no_author_contact_required: bool
    identified_sample_stack: bool
    source_qualified_material_model: bool
    independent_measured_holdout: bool
    machine_readable_numerical_data: bool
    absolute_calibration_documented: bool
    geometry_specified: bool
    calibration_holdout_split_predeclared: bool
    holdout_not_known_used_for_fit: bool
    tmm_appropriate: bool
    no_existing_nonpromoting_validation: bool

    model_config = ConfigDict(extra="forbid")


class DatasetCandidate(BaseModel):
    candidate_id: str
    title: str
    material_family: str
    source_type: str
    source_refs: list[str] = Field(default_factory=list)
    public_data_links: list[str] = Field(default_factory=list)
    exact_files: list[str] = Field(default_factory=list)
    evidence: EvidenceFlags
    proposed_claim_label: GateLabel
    decision: str
    blockers: list[str] = Field(default_factory=list)
    exact_next_file: str | None = None
    notes: list[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")

    @field_validator("candidate_id")
    @classmethod
    def validate_candidate_id(cls, value: str) -> str:
        if not value or any(char.isspace() for char in value):
            raise ValueError("candidate_id must be non-empty and contain no whitespace")
        return value


class PublicDatasetRegistry(BaseModel):
    phase_id: str
    registry_version: int
    updated_at: str
    acceptance_scope: str
    candidates: list[DatasetCandidate]

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def validate_unique_candidates(self) -> PublicDatasetRegistry:
        ids = [candidate.candidate_id for candidate in self.candidates]
        if len(ids) != len(set(ids)):
            raise ValueError("candidate_id values must be unique")
        return self


def load_public_dataset_registry(path: Path) -> PublicDatasetRegistry:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return PublicDatasetRegistry.model_validate(payload)


def evaluate_candidate(candidate: DatasetCandidate) -> dict[str, Any]:
    flag_values = candidate.evidence.model_dump()
    missing_flags = [
        flag for flag in REQUIRED_PHASE4_FLAGS if flag_values.get(flag) is not True
    ]
    gate_blockers = [
        {"flag": flag, "criterion": REQUIRED_PHASE4_FLAGS[flag]} for flag in missing_flags
    ]
    can_enter_phase4 = not gate_blockers
    computed_label: GateLabel = (
        "calibrated_linear_candidate"
        if can_enter_phase4
        else candidate.proposed_claim_label
    )
    return {
        "candidate_id": candidate.candidate_id,
        "title": candidate.title,
        "material_family": candidate.material_family,
        "proposed_claim_label": candidate.proposed_claim_label,
        "computed_gate_label": computed_label,
        "can_enter_phase4": can_enter_phase4,
        "serious_core_allowed_now": False,
        "missing_required_flags": missing_flags,
        "gate_blockers": gate_blockers,
        "decision": candidate.decision,
        "blockers": candidate.blockers,
        "exact_next_file": candidate.exact_next_file,
    }


def build_phase3e1_scaffold(registry_path: Path) -> dict[str, Any]:
    registry = load_public_dataset_registry(registry_path)
    evaluations = [evaluate_candidate(candidate) for candidate in registry.candidates]
    label_counts = Counter(item["computed_gate_label"] for item in evaluations)
    blocker_counts = Counter(
        blocker["flag"] for item in evaluations for blocker in item["gate_blockers"]
    )
    phase4_candidates = [
        item["candidate_id"] for item in evaluations if item["can_enter_phase4"]
    ]
    return {
        "phase_id": "Phase 3E.1",
        "title": "Public Dataset Gate And Executive Research Assistant Scaffold",
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "inputs": {"registry_path": str(registry_path)},
        "registry": {
            "phase_id": registry.phase_id,
            "registry_version": registry.registry_version,
            "updated_at": registry.updated_at,
            "acceptance_scope": registry.acceptance_scope,
            "candidate_count": len(registry.candidates),
        },
        "required_phase4_flags": REQUIRED_PHASE4_FLAGS,
        "candidate_evaluations": evaluations,
        "summary": {
            "candidate_count": len(evaluations),
            "phase4_candidate_count": len(phase4_candidates),
            "phase4_candidate_ids": phase4_candidates,
            "claim_label_counts": dict(sorted(label_counts.items())),
            "blocker_counts": dict(sorted(blocker_counts.items())),
        },
        "decision": {
            "status": (
                "phase4_candidate_available"
                if phase4_candidates
                else "phase3e1_scaffold_ready_no_phase4_candidate"
            ),
            "can_open_phase4_now": bool(phase4_candidates),
            "can_feed_serious_core_now": False,
            "claim_standard_changed": False,
            "recommended_next_phase": (
                "Phase 4 - calibrated-linear attempt for gated candidate"
                if phase4_candidates
                else "Phase 3E.2 - Browse/Plasmate-assisted literature sweep through gate"
            ),
        },
        "executive_assistant_contract": {
            "allowed_outputs": [
                "candidate cards and rejection cards",
                "dataset-gate reports and claim-label summaries",
                "phase-state briefs and next-action recommendations",
                "literature-search prompts and Browse/Plasmate scouting plans",
                "failed-validation memory summaries",
            ],
            "forbidden_outputs": [
                "promoting a candidate without all gate flags passing",
                "treating Browse/Plasmate text extraction as validation evidence",
                "lowering calibrated_linear_evidence standards to proceed",
                "recommending unavailable CompleteEASE, TiON raw R/T, or author-contact paths",
                "opening Phase 4 from plot-only, PDF-only, constants-only, or request-only data",
            ],
        },
    }


def phase3e1_markdown(packet: dict[str, Any]) -> str:
    summary = packet["summary"]
    decision = packet["decision"]
    rows = [
        "| Candidate | Label | Phase 4? | Main Blockers |",
        "| --- | --- | --- | --- |",
    ]
    for item in packet["candidate_evaluations"]:
        blockers = ", ".join(item["missing_required_flags"][:4])
        if len(item["missing_required_flags"]) > 4:
            blockers += ", ..."
        rows.append(
            "| "
            + item["candidate_id"]
            + " | `"
            + item["computed_gate_label"]
            + "` | "
            + ("yes" if item["can_enter_phase4"] else "no")
            + " | "
            + (blockers or "none")
            + " |"
        )

    return "\n".join(
        [
            "# Phase 3E.1 - Public Dataset Gate And Executive Research Assistant Scaffold",
            "",
            "## Decision",
            "",
            f"- Status: `{decision['status']}`",
            f"- Can open Phase 4 now: `{str(decision['can_open_phase4_now']).lower()}`",
            f"- Can feed Serious Core now: `{str(decision['can_feed_serious_core_now']).lower()}`",
            f"- Claim standard changed: `{str(decision['claim_standard_changed']).lower()}`",
            f"- Recommended next phase: `{decision['recommended_next_phase']}`",
            "",
            "## Candidate Gate Summary",
            "",
            f"- Candidates evaluated: `{summary['candidate_count']}`",
            f"- Phase 4 candidates: `{summary['phase4_candidate_count']}`",
            "",
            *rows,
            "",
            "## Assistant Contract",
            "",
            "Allowed outputs:",
            "",
            *[
                f"- {item}"
                for item in packet["executive_assistant_contract"]["allowed_outputs"]
            ],
            "",
            "Forbidden outputs:",
            "",
            *[
                f"- {item}"
                for item in packet["executive_assistant_contract"]["forbidden_outputs"]
            ],
            "",
            "## Interpretation",
            "",
            "Phase 3E.1 turns the blocked Phase 3D public-data search into durable "
            "machinery. The assistant may now organize candidates and search results "
            "aggressively, but the gate still refuses Phase 4 unless every required "
            "public-data flag passes.",
            "",
        ]
    )


def write_phase3e1_scaffold(output_dir: Path, packet: dict[str, Any]) -> tuple[Path, Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase3e1_public_dataset_gate_assistant_scaffold.json"
    md_path = output_dir / "phase3e1_public_dataset_gate_assistant_scaffold.md"
    summary_path = output_dir / "phase3e1_claim_status_summary.json"
    summary = {
        "phase_id": packet["phase_id"],
        "generated_at": packet["generated_at"],
        "can_open_phase4_now": packet["decision"]["can_open_phase4_now"],
        "can_feed_serious_core_now": packet["decision"]["can_feed_serious_core_now"],
        "claim_label_counts": packet["summary"]["claim_label_counts"],
        "phase4_candidate_ids": packet["summary"]["phase4_candidate_ids"],
        "recommended_next_phase": packet["decision"]["recommended_next_phase"],
    }
    json_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(phase3e1_markdown(packet), encoding="utf-8")
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return json_path, md_path, summary_path
