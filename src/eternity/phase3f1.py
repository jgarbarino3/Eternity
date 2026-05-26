"""Phase 3F.1 simple thin-film simulator-validation scout."""

from __future__ import annotations

import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

DEFAULT_REGISTRY_PATH = Path("docs/phase3f_simulator_validation_candidate_registry.yaml")

HardGateLabel = Literal[
    "simulator_validation_candidate",
    "simulator_validation_fallback",
    "promising_but_blocked",
    "constants_only_fixture",
    "measured_only_fixture",
    "software_or_simulation_fixture",
    "bulk_substrate_sanity_fixture",
    "weak_within_dataset_holdout",
    "literature_reproduction_fixture",
    "calibration_only_no_holdout",
    "blocked_source_data_lead",
    "rejected_request_only",
    "rejected_candidate",
]

HARD_GATE_FLAGS = {
    "public_access": "public data access without private credentials or author contact",
    "machine_readable_material_constants": "machine-readable n,k, epsilon, or model constants",
    "machine_readable_measured_holdout": (
        "machine-readable measured R/T or ellipsometry holdout"
    ),
    "geometry_specified": "source-backed wavelength axis, angle, polarization, and units",
    "stack_thickness_specified": "source-backed layer order and thicknesses",
    "substrate_backside_coherence_specified": (
        "source-backed substrate/backside/coherence treatment or irrelevant backside"
    ),
    "leakage_safe_no_fit_split": (
        "material model and measured holdout can be used without residual-driven tuning"
    ),
    "tmm_suitable": "measurement is a planar linear TMM target",
    "source_hash_ready": "source-page files can be hashed or provide checksums before intake",
}


class Phase3F1Evidence(BaseModel):
    public_access: bool
    machine_readable_material_constants: bool
    machine_readable_measured_holdout: bool
    geometry_specified: bool
    stack_thickness_specified: bool
    substrate_backside_coherence_specified: bool
    leakage_safe_no_fit_split: bool
    tmm_suitable: bool
    source_hash_ready: bool

    model_config = ConfigDict(extra="forbid")


class Phase3F1TieBreakers(BaseModel):
    stack_simplicity_rank: int = Field(ge=1, le=5)
    normal_incidence: bool
    open_format_priority: int = Field(ge=1, le=5)
    non_enz_or_non_claim_context: bool
    substrate_backside_clarity_rank: int = Field(ge=1, le=5)

    model_config = ConfigDict(extra="forbid")


class Phase3F1Candidate(BaseModel):
    candidate_id: str
    title: str
    material_family: str
    source_type: str
    source_refs: list[str] = Field(default_factory=list)
    source_urls: list[str] = Field(default_factory=list)
    exact_files_or_records: list[str] = Field(default_factory=list)
    scouting_notes: list[str] = Field(default_factory=list)
    evidence: Phase3F1Evidence
    tie_breakers: Phase3F1TieBreakers
    proposed_scout_label: HardGateLabel
    decision: str
    blockers: list[str] = Field(default_factory=list)
    exact_next_action: str | None = None

    model_config = ConfigDict(extra="forbid")

    @field_validator("candidate_id")
    @classmethod
    def validate_candidate_id(cls, value: str) -> str:
        if not value or any(char.isspace() for char in value):
            raise ValueError("candidate_id must be non-empty and contain no whitespace")
        return value


class Phase3F1Registry(BaseModel):
    phase_id: str
    report_title: str = "Simple Thin-Film Simulator-Validation Scout"
    registry_version: int
    updated_at: str
    search_scope: str
    candidate_limit: int = Field(ge=1, le=20)
    selected_next_phase: str = (
        "Phase 3F.2 - source-file intake for selected simple thin-film candidate"
    )
    blocked_next_phase: str = (
        "Phase 3F.1 - continue bounded scout with stricter simple-stack leads"
    )
    candidates: list[Phase3F1Candidate]

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def validate_registry(self) -> Phase3F1Registry:
        ids = [candidate.candidate_id for candidate in self.candidates]
        if len(ids) != len(set(ids)):
            raise ValueError("candidate_id values must be unique")
        if len(self.candidates) > self.candidate_limit:
            raise ValueError("candidate count exceeds candidate_limit")
        return self


def load_phase3f1_registry(path: Path) -> Phase3F1Registry:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return Phase3F1Registry.model_validate(payload)


def evaluate_phase3f1_candidate(candidate: Phase3F1Candidate) -> dict[str, Any]:
    flags = candidate.evidence.model_dump()
    missing_flags = [flag for flag in HARD_GATE_FLAGS if flags.get(flag) is not True]
    gate_blockers = [
        {"flag": flag, "criterion": HARD_GATE_FLAGS[flag]} for flag in missing_flags
    ]
    hard_gate_pass = not missing_flags
    return {
        "candidate_id": candidate.candidate_id,
        "title": candidate.title,
        "material_family": candidate.material_family,
        "source_type": candidate.source_type,
        "proposed_scout_label": candidate.proposed_scout_label,
        "computed_gate_label": (
            "simulator_validation_candidate"
            if hard_gate_pass
            else candidate.proposed_scout_label
        ),
        "hard_gate_pass": hard_gate_pass,
        "missing_required_flags": missing_flags,
        "gate_blockers": gate_blockers,
        "decision": candidate.decision,
        "blockers": candidate.blockers,
        "exact_next_action": candidate.exact_next_action,
        "tie_breakers": candidate.tie_breakers.model_dump(),
    }


def _selection_key(candidate: Phase3F1Candidate) -> tuple[int, int, int, int, int, str]:
    tie = candidate.tie_breakers
    return (
        tie.stack_simplicity_rank,
        0 if tie.normal_incidence else 1,
        tie.open_format_priority,
        0 if tie.non_enz_or_non_claim_context else 1,
        tie.substrate_backside_clarity_rank,
        candidate.candidate_id,
    )


def _select_candidate(
    registry: Phase3F1Registry,
    evaluations: list[dict[str, Any]],
) -> Phase3F1Candidate | None:
    passing_ids = {
        evaluation["candidate_id"] for evaluation in evaluations if evaluation["hard_gate_pass"]
    }
    passing = [
        candidate for candidate in registry.candidates if candidate.candidate_id in passing_ids
    ]
    if not passing:
        return None
    return sorted(passing, key=_selection_key)[0]


def build_phase3f1_packet(registry_path: Path = DEFAULT_REGISTRY_PATH) -> dict[str, Any]:
    registry = load_phase3f1_registry(registry_path)
    evaluations = [evaluate_phase3f1_candidate(candidate) for candidate in registry.candidates]
    selected = _select_candidate(registry, evaluations)
    label_counts = Counter(item["computed_gate_label"] for item in evaluations)
    blocker_counts = Counter(
        blocker["flag"] for item in evaluations for blocker in item["gate_blockers"]
    )
    selected_id = selected.candidate_id if selected else None
    return {
        "phase_id": registry.phase_id,
        "title": registry.report_title,
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "inputs": {"registry_path": str(registry_path)},
        "search_bounds": {
            "candidate_limit": registry.candidate_limit,
            "search_scope": registry.search_scope,
            "residual_modeling_allowed": False,
            "tmm_adapter_allowed": False,
        },
        "hard_gate_flags": HARD_GATE_FLAGS,
        "registry": {
            "phase_id": registry.phase_id,
            "registry_version": registry.registry_version,
            "updated_at": registry.updated_at,
            "candidate_count": len(registry.candidates),
        },
        "candidate_evaluations": evaluations,
        "summary": {
            "candidate_count": len(evaluations),
            "hard_gate_pass_count": sum(1 for item in evaluations if item["hard_gate_pass"]),
            "selected_next_candidate_id": selected_id,
            "claim_label_counts": dict(sorted(label_counts.items())),
            "blocker_counts": dict(sorted(blocker_counts.items())),
        },
        "decision": {
            "status": (
                "phase3f1_candidate_ready_for_intake_gate"
                if selected
                else "phase3f1_no_candidate_ready_keep_phase3f_open"
            ),
            "selected_next_candidate_id": selected_id,
            "phase3f2_intake_allowed": selected is not None,
            "residual_modeling_performed": False,
            "tmm_adapter_started": False,
            "phase4_candidate": False,
            "serious_core_allowed_now": False,
            "claim_standard_changed": False,
            "recommended_next_phase": (
                registry.selected_next_phase if selected else registry.blocked_next_phase
            ),
        },
        "stop_rule": {
            "residual_modeling_stop_active": True,
            "reason": (
                f"{registry.phase_id} is scouting/gating only; residuals require a "
                "later Phase 3F.2 source-file intake and frozen no-fit adapter."
            ),
        },
    }


def phase3f1_markdown(packet: dict[str, Any]) -> str:
    decision = packet["decision"]
    summary = packet["summary"]
    rows = [
        "| Candidate | Label | Gate Pass? | Main Missing Flags |",
        "| --- | --- | --- | --- |",
    ]
    for item in packet["candidate_evaluations"]:
        missing = ", ".join(item["missing_required_flags"][:4])
        if len(item["missing_required_flags"]) > 4:
            missing += ", ..."
        rows.append(
            "| "
            + item["candidate_id"]
            + " | `"
            + item["computed_gate_label"]
            + "` | "
            + ("yes" if item["hard_gate_pass"] else "no")
            + " | "
            + (missing or "none")
            + " |"
        )

    selected = decision["selected_next_candidate_id"] or "none"
    return "\n".join(
        [
            f"# {packet['phase_id']} - {packet['title']}",
            "",
            "## Decision",
            "",
            f"- Status: `{decision['status']}`",
            f"- Selected next candidate: `{selected}`",
            (
                "- Phase 3F.2 intake allowed: "
                f"`{str(decision['phase3f2_intake_allowed']).lower()}`"
            ),
            (
                "- Residual modeling performed: "
                f"`{str(decision['residual_modeling_performed']).lower()}`"
            ),
            f"- Phase 4 candidate: `{str(decision['phase4_candidate']).lower()}`",
            f"- Recommended next phase: `{decision['recommended_next_phase']}`",
            "",
            "This scout is contract-first and does not download source files, build a TMM",
            "adapter, choose model variants, or inspect residuals.",
            "",
            "## Search Summary",
            "",
            f"- Candidate count: `{summary['candidate_count']}`",
            f"- Hard-gate pass count: `{summary['hard_gate_pass_count']}`",
            f"- Candidate limit: `{packet['search_bounds']['candidate_limit']}`",
            "",
            "## Candidate Gate Table",
            "",
            *rows,
            "",
            "## Stop Rule",
            "",
            (
                "- Residual stop active: "
                f"`{str(packet['stop_rule']['residual_modeling_stop_active']).lower()}`"
            ),
            f"- Reason: {packet['stop_rule']['reason']}",
            "",
        ]
    )


def write_phase3f1_packet(
    output_dir: Path,
    packet: dict[str, Any],
    report_stem: str = "phase3f1_simulator_validation_scout",
) -> tuple[Path, Path]:
    if report_stem != Path(report_stem).name or not report_stem:
        raise ValueError("report_stem must be a non-empty filename stem")
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{report_stem}.json"
    md_path = output_dir / f"{report_stem}.md"
    json_path.write_text(json.dumps(packet, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(phase3f1_markdown(packet), encoding="utf-8")
    return json_path, md_path
