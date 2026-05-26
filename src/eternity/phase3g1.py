"""Phase 3G.1 measured-data intake queue for assistant-facing triage."""

from __future__ import annotations

import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

DEFAULT_QUEUE_PATH = Path("docs/phase3g_measured_data_intake_queue.yaml")
DEFAULT_PHASE3F1F_DECISION_PATH = Path(
    "docs/phase3f1f_measured_data_scouting_decision.json"
)

GateState = Literal["pass", "missing", "unknown", "risk", "not_applicable"]
IntendedUse = Literal[
    "enz_calibrated",
    "simulator_validation",
    "literature_reproduction",
    "code_regression",
    "parser_fixture",
    "unknown",
]
IntakeLabel = Literal[
    "calibrated_candidate_possible",
    "simulator_validation_candidate",
    "weak_within_dataset_holdout",
    "literature_reproduction_fixture",
    "constants_only",
    "measured_only",
    "software_or_code_regression_fixture",
    "parser_fixture",
    "source_file_audit_needed",
    "blocked_source_data_lead",
    "reject",
]
CanonicalDatasetLabel = Literal[
    "calibrated_candidate_possible",
    "simulator_validation_candidate",
    "weak_within_dataset_holdout",
    "literature_reproduction_fixture",
    "constants_only",
    "reject",
]

HARD_GATE_FLAGS = {
    "public_access": "public data access without private credentials or author contact",
    "source_qualified_constants_or_model": "source-qualified n,k, epsilon, or model constants",
    "independent_measured_holdout": "independent measured R/T, A, or ellipsometry holdout",
    "machine_readable_files": "machine-readable files for constants and measured data",
    "geometry_backed": "source-backed wavelength axis, angle, polarization, side, and units",
    "stack_thickness_backed": "source-backed stack order, material identity, and thicknesses",
    "substrate_backside_coherence_clear": (
        "source-backed substrate/backside/coherence treatment or irrelevant backside"
    ),
    "leakage_safe_no_fit_split": (
        "material model and measured holdout can be separated without residual-driven tuning"
    ),
    "planar_linear_tmm_suitable": "measurement is appropriate for planar linear TMM",
    "source_hash_ready": "source files can be hashed or have checksums before intake",
}

BLOCKING_STATES = {"missing", "unknown", "risk", "not_applicable"}

SEARCHABLE_FAILURE_RECORDS = [
    "research_memory/examples/failure_memory/phase3f_public_measured_data_scouts.yaml",
    "research_memory/examples/failure_memory/saha_stack_contract_block.yaml",
    "research_memory/examples/failure_memory/st_andrews_tin_fail_closed.yaml",
    "research_memory/examples/failure_memory/wang_wo3_reproduction_fixture.yaml",
    "research_memory/examples/failure_memory/tion_local_data_exhausted.yaml",
]


class Phase3G1Evidence(BaseModel):
    public_access: GateState
    source_qualified_constants_or_model: GateState
    independent_measured_holdout: GateState
    machine_readable_files: GateState
    geometry_backed: GateState
    stack_thickness_backed: GateState
    substrate_backside_coherence_clear: GateState
    leakage_safe_no_fit_split: GateState
    planar_linear_tmm_suitable: GateState
    source_hash_ready: GateState

    model_config = ConfigDict(extra="forbid")


class Phase3G1Lead(BaseModel):
    lead_id: str
    title: str
    material_family: str
    intended_use: IntendedUse
    source_type: str
    source_refs: list[str] = Field(default_factory=list)
    source_urls: list[str] = Field(default_factory=list)
    exact_files_or_records: list[str] = Field(default_factory=list)
    evidence: Phase3G1Evidence
    priority_rank: int = Field(default=3, ge=1, le=5)
    known_failure_memory: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    exact_next_action: str | None = None

    model_config = ConfigDict(extra="forbid")

    @field_validator("lead_id")
    @classmethod
    def validate_lead_id(cls, value: str) -> str:
        if not value or any(char.isspace() for char in value):
            raise ValueError("lead_id must be non-empty and contain no whitespace")
        return value


class Phase3G1Queue(BaseModel):
    phase_id: str = "Phase 3G.1"
    report_title: str = "Measured-Data Intake Queue And Assistant Brief"
    queue_version: int = Field(ge=1)
    updated_at: str
    queue_scope: str
    candidates_note: str | None = None
    lead_limit: int = Field(default=50, ge=1, le=100)
    leads: list[Phase3G1Lead]

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def validate_queue(self) -> Phase3G1Queue:
        ids = [lead.lead_id for lead in self.leads]
        if len(ids) != len(set(ids)):
            raise ValueError("lead_id values must be unique")
        if len(self.leads) > self.lead_limit:
            raise ValueError("lead count exceeds lead_limit")
        return self


def load_phase3g1_queue(path: Path) -> Phase3G1Queue:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return Phase3G1Queue.model_validate(payload)


def load_phase3g1_lead(path: Path) -> Phase3G1Lead:
    if path.suffix.lower() == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
    else:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return Phase3G1Lead.model_validate(payload)


def _gate_states(evidence: Phase3G1Evidence) -> dict[str, GateState]:
    return evidence.model_dump()


def _missing_required_flags(evidence: Phase3G1Evidence) -> list[str]:
    states = _gate_states(evidence)
    return [flag for flag in HARD_GATE_FLAGS if states[flag] in BLOCKING_STATES]


def _gate_blockers(evidence: Phase3G1Evidence) -> list[dict[str, str]]:
    states = _gate_states(evidence)
    return [
        {
            "flag": flag,
            "state": states[flag],
            "criterion": HARD_GATE_FLAGS[flag],
        }
        for flag in HARD_GATE_FLAGS
        if states[flag] in BLOCKING_STATES
    ]


def _classify_lead(lead: Phase3G1Lead, missing_flags: list[str]) -> IntakeLabel:
    states = _gate_states(lead.evidence)
    if states["public_access"] in {"missing", "risk", "not_applicable"}:
        return "reject"
    if not missing_flags:
        if lead.intended_use == "enz_calibrated":
            return "calibrated_candidate_possible"
        return "simulator_validation_candidate"
    if lead.intended_use == "code_regression":
        return "software_or_code_regression_fixture"
    if lead.intended_use == "parser_fixture":
        return "parser_fixture"
    if states["planar_linear_tmm_suitable"] in {"missing", "risk", "not_applicable"}:
        return "literature_reproduction_fixture"
    if (
        states["independent_measured_holdout"] != "pass"
        and states["source_qualified_constants_or_model"] == "pass"
    ):
        return "constants_only"
    if (
        states["source_qualified_constants_or_model"] != "pass"
        and states["independent_measured_holdout"] == "pass"
    ):
        return "measured_only"
    if states["leakage_safe_no_fit_split"] != "pass" and (
        states["independent_measured_holdout"] == "pass"
    ):
        return "weak_within_dataset_holdout"
    if states["source_hash_ready"] != "pass" and states["machine_readable_files"] == "pass":
        return "source_file_audit_needed"
    return "blocked_source_data_lead"


def _canonical_dataset_label(label: IntakeLabel) -> CanonicalDatasetLabel:
    if label in {
        "calibrated_candidate_possible",
        "simulator_validation_candidate",
        "weak_within_dataset_holdout",
        "literature_reproduction_fixture",
        "constants_only",
    }:
        return label
    return "reject"


def evaluate_phase3g1_lead(lead: Phase3G1Lead) -> dict[str, Any]:
    missing_flags = _missing_required_flags(lead.evidence)
    hard_gate_pass = not missing_flags
    label = _classify_lead(lead, missing_flags)
    canonical_label = _canonical_dataset_label(label)
    return {
        "lead_id": lead.lead_id,
        "title": lead.title,
        "material_family": lead.material_family,
        "intended_use": lead.intended_use,
        "source_type": lead.source_type,
        "source_refs": lead.source_refs,
        "source_urls": lead.source_urls,
        "exact_files_or_records": lead.exact_files_or_records,
        "priority_rank": lead.priority_rank,
        "computed_intake_label": label,
        "canonical_dataset_label": canonical_label,
        "hard_gate_pass": hard_gate_pass,
        "phase3f2_intake_candidate": hard_gate_pass,
        "residual_modeling_allowed_now": False,
        "phase4_candidate_ready_now": False,
        "missing_required_flags": missing_flags,
        "gate_blockers": _gate_blockers(lead.evidence),
        "evidence_states": _gate_states(lead.evidence),
        "known_failure_memory": lead.known_failure_memory,
        "notes": lead.notes,
        "exact_next_action": lead.exact_next_action,
    }


def _selection_key(evaluation: dict[str, Any]) -> tuple[int, int, str]:
    return (
        evaluation["priority_rank"],
        len(evaluation["missing_required_flags"]),
        evaluation["lead_id"],
    )


def _load_phase3f1f_memory(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "available": False,
            "path": str(path),
            "warning": "Phase 3F.1F decision artifact not found.",
        }
    payload = json.loads(path.read_text(encoding="utf-8"))
    evidence_basis = payload.get("evidence_basis", [])
    lead_count = sum(
        int(item.get("candidate_count", 0))
        for item in evidence_basis
        if "candidate_count" in item
    )
    return {
        "available": True,
        "path": str(path),
        "decision_status": payload.get("decision", {}).get("status"),
        "measured_data_scouting_paused": payload.get("decision", {}).get(
            "measured_data_scouting_paused"
        ),
        "phase3f2_intake_allowed": payload.get("decision", {}).get(
            "phase3f2_intake_allowed"
        ),
        "residual_modeling_allowed": payload.get("decision", {}).get(
            "residual_modeling_allowed"
        ),
        "phase4_candidate": payload.get("decision", {}).get("phase4_candidate"),
        "prior_measured_data_leads": lead_count,
        "evidence_basis": evidence_basis,
        "resume_conditions": payload.get("resume_conditions", []),
    }


def _assistant_command_contract() -> dict[str, Any]:
    return {
        "primary_cli": "eternity phase3g1-intake-queue",
        "commands": {
            "summarize_current_blockers": "eternity phase3g1-summarize-blockers",
            "rank_next_public_data_leads": "eternity phase3g1-rank-leads",
            "generate_pro_prompt": "eternity phase3g1-pro-prompt",
            "make_no_overclaim_status_report": "eternity phase3g1-no-overclaim-report",
            "compare_new_dataset_against_gate": (
                "eternity phase3g1-compare-lead --lead-card <lead.yaml>"
            ),
        },
        "supported_workflows": [
            {
                "name": "summarize_current_blockers",
                "output": "No-overclaim status plus top missing hard gates.",
            },
            {
                "name": "rank_next_public_data_leads",
                "output": "Sorted lead table by priority rank and missing hard-gate count.",
            },
            {
                "name": "generate_pro_prompt",
                "output": (
                    "A compact 5.5 Pro prompt asking for source-backed missing "
                    "evidence only."
                ),
            },
            {
                "name": "make_no_overclaim_status_report",
                "output": "Markdown report with claim ceiling, stop rules, and next action.",
            },
            {
                "name": "compare_new_dataset_against_gate",
                "output": "Add a lead card to the queue YAML and rerun the same command.",
            },
        ],
        "forbidden_workflows": [
            "running measured residuals from a queue lead",
            "opening Phase 3F.2 without every hard gate passing",
            "using residual shape to choose constants, thickness, or backside assumptions",
            "promoting Phase 3F.1E code parity to measured validation",
        ],
    }


def _lead_intake_template() -> dict[str, Any]:
    return {
        "lead_id": "new_source_data_lead",
        "title": "Paper or dataset title",
        "material_family": "material / stack",
        "intended_use": "simulator_validation",
        "source_type": "paper_dataset_repository",
        "source_refs": ["DOI or citation"],
        "source_urls": ["https://..."],
        "exact_files_or_records": ["data.csv", "nk.xlsx"],
        "evidence": {flag: "unknown" for flag in HARD_GATE_FLAGS},
        "priority_rank": 3,
        "known_failure_memory": [],
        "notes": ["Do not mark pass until source files are inspected."],
        "exact_next_action": "Inspect source files and hash machine-readable data.",
    }


def _pro_prompt(packet: dict[str, Any]) -> str:
    selected = packet["decision"]["selected_next_lead_id"] or "none"
    return "\n".join(
        [
            "You are reviewing candidate public thin-film measured-data leads for Eternity.",
            (
                "Do not relax the evidence bar. Find only source-backed evidence "
                "for missing hard gates."
            ),
            f"Current selected lead: {selected}.",
            (
                "Required gates: public access; source-qualified constants/model; "
                "independent measured holdout; machine-readable files; geometry; "
                "stack/thickness; substrate/backside/coherence; leakage-safe no-fit "
                "split; planar linear TMM suitability; source/hash readiness."
            ),
            (
                "Return a table with pass/unknown/fail for each gate, exact source "
                "files, and a conservative claim ceiling. Do not propose residual "
                "modeling unless every hard gate is source-backed before fitting."
            ),
        ]
    )


def build_phase3g1_packet(
    queue_path: Path = DEFAULT_QUEUE_PATH,
    phase3f1f_decision_path: Path = DEFAULT_PHASE3F1F_DECISION_PATH,
) -> dict[str, Any]:
    queue = load_phase3g1_queue(queue_path)
    evaluations = [evaluate_phase3g1_lead(lead) for lead in queue.leads]
    passing = [item for item in evaluations if item["hard_gate_pass"]]
    selected = sorted(passing, key=_selection_key)[0] if passing else None
    label_counts = Counter(item["computed_intake_label"] for item in evaluations)
    canonical_label_counts = Counter(item["canonical_dataset_label"] for item in evaluations)
    blocker_counts = Counter(
        blocker["flag"] for item in evaluations for blocker in item["gate_blockers"]
    )
    phase3f1f_memory = _load_phase3f1f_memory(phase3f1f_decision_path)
    packet: dict[str, Any] = {
        "phase_id": queue.phase_id,
        "title": queue.report_title,
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "inputs": {
            "queue_path": str(queue_path),
            "phase3f1f_decision_path": str(phase3f1f_decision_path),
        },
        "queue": {
            "queue_version": queue.queue_version,
            "updated_at": queue.updated_at,
            "queue_scope": queue.queue_scope,
            "candidates_note": queue.candidates_note,
            "lead_limit": queue.lead_limit,
            "lead_count": len(queue.leads),
        },
        "hard_gate_flags": HARD_GATE_FLAGS,
        "failure_memory": phase3f1f_memory,
        "searchable_failure_records": SEARCHABLE_FAILURE_RECORDS,
        "lead_evaluations": evaluations,
        "summary": {
            "lead_count": len(evaluations),
            "hard_gate_pass_count": len(passing),
            "selected_next_lead_id": selected["lead_id"] if selected else None,
            "intake_label_counts": dict(sorted(label_counts.items())),
            "canonical_dataset_label_counts": dict(sorted(canonical_label_counts.items())),
            "blocker_counts": dict(sorted(blocker_counts.items())),
        },
        "decision": {
            "status": (
                "phase3g1_candidate_ready_for_phase3f2_source_intake"
                if selected
                else "phase3g1_intake_queue_ready_no_candidate"
            ),
            "selected_next_lead_id": selected["lead_id"] if selected else None,
            "phase3f2_intake_allowed": selected is not None,
            "residual_modeling_allowed_now": False,
            "phase4_candidate_ready_now": False,
            "claim_standard_changed": False,
            "recommended_next_phase": (
                "Phase 3F.2 - source-file intake for selected measured-data lead"
                if selected
                else "Phase 3G.2 - assistant intake ergonomics and research-memory record promotion"
            ),
        },
        "assistant_command_contract": _assistant_command_contract(),
        "lead_intake_template": _lead_intake_template(),
        "stop_rules": [
            "A queue lead is not validation evidence.",
            "Phase 3F.2 can open only after every hard gate is pass.",
            "Measured residual modeling remains forbidden in Phase 3G.1.",
            (
                "No claim label may be promoted from code parity, constants-only data, "
                "or leakage-risk holdouts."
            ),
        ],
    }
    packet["assistant_command_contract"]["pro_prompt"] = _pro_prompt(packet)
    return packet


def phase3g1_blocker_summary(packet: dict[str, Any]) -> dict[str, Any]:
    blocker_counts = packet["summary"]["blocker_counts"]
    top_blockers = [
        {
            "flag": flag,
            "count": count,
            "criterion": HARD_GATE_FLAGS[flag],
        }
        for flag, count in sorted(
            blocker_counts.items(),
            key=lambda item: (-item[1], item[0]),
        )
    ]
    return {
        "phase_id": packet["phase_id"],
        "status": packet["decision"]["status"],
        "phase3f2_intake_allowed": packet["decision"]["phase3f2_intake_allowed"],
        "residual_modeling_allowed_now": packet["decision"][
            "residual_modeling_allowed_now"
        ],
        "phase4_candidate_ready_now": packet["decision"]["phase4_candidate_ready_now"],
        "lead_count": packet["summary"]["lead_count"],
        "hard_gate_pass_count": packet["summary"]["hard_gate_pass_count"],
        "top_blockers": top_blockers,
        "stop_rules": packet["stop_rules"],
    }


def phase3g1_ranked_leads(packet: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "lead_id": item["lead_id"],
            "title": item["title"],
            "label": item["computed_intake_label"],
            "canonical_dataset_label": item["canonical_dataset_label"],
            "hard_gate_pass": item["hard_gate_pass"],
            "priority_rank": item["priority_rank"],
            "missing_required_flags": item["missing_required_flags"],
            "missing_count": len(item["missing_required_flags"]),
            "exact_next_action": item["exact_next_action"],
        }
        for item in sorted(packet["lead_evaluations"], key=_selection_key)
    ]


def phase3g1_no_overclaim_markdown(packet: dict[str, Any]) -> str:
    blocker_summary = phase3g1_blocker_summary(packet)
    lines = [
        "# Phase 3G.1 No-Overclaim Status",
        "",
        f"- Status: `{blocker_summary['status']}`",
        (
            "- Phase 3F.2 intake allowed: "
            f"`{str(blocker_summary['phase3f2_intake_allowed']).lower()}`"
        ),
        (
            "- Residual modeling allowed now: "
            f"`{str(blocker_summary['residual_modeling_allowed_now']).lower()}`"
        ),
        (
            "- Phase 4 candidate ready now: "
            f"`{str(blocker_summary['phase4_candidate_ready_now']).lower()}`"
        ),
        f"- Queue lead count: `{blocker_summary['lead_count']}`",
        f"- Hard-gate pass count: `{blocker_summary['hard_gate_pass_count']}`",
        "",
        "## Top Blockers",
        "",
    ]
    if blocker_summary["top_blockers"]:
        lines.extend(
            (
                f"- `{item['flag']}`: {item['count']} lead(s). "
                f"{item['criterion']}"
            )
            for item in blocker_summary["top_blockers"]
        )
    else:
        lines.append("- None.")
    lines.extend(["", "## Stop Rules", ""])
    lines.extend(f"- {rule}" for rule in blocker_summary["stop_rules"])
    lines.append("")
    return "\n".join(lines)


def build_phase3g1_compare_packet(lead_path: Path) -> dict[str, Any]:
    lead = load_phase3g1_lead(lead_path)
    evaluation = evaluate_phase3g1_lead(lead)
    return {
        "phase_id": "Phase 3G.1",
        "title": "Single Lead Hard-Gate Comparison",
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "inputs": {"lead_path": str(lead_path)},
        "hard_gate_flags": HARD_GATE_FLAGS,
        "evaluation": evaluation,
        "decision": {
            "computed_intake_label": evaluation["computed_intake_label"],
            "canonical_dataset_label": evaluation["canonical_dataset_label"],
            "phase3f2_intake_allowed": evaluation["hard_gate_pass"],
            "residual_modeling_allowed_now": False,
            "phase4_candidate_ready_now": False,
            "exact_next_action": evaluation["exact_next_action"],
        },
        "stop_rules": [
            "This comparison does not download files or inspect residuals.",
            "Phase 3F.2 can open only if every hard gate is pass.",
            "Residual modeling remains forbidden until a frozen no-fit contract exists.",
        ],
    }


def phase3g1_compare_markdown(packet: dict[str, Any]) -> str:
    evaluation = packet["evaluation"]
    decision = packet["decision"]
    rows = [
        "| Gate | State | Criterion |",
        "| --- | --- | --- |",
    ]
    for flag, criterion in packet["hard_gate_flags"].items():
        rows.append(
            "| "
            + flag
            + " | `"
            + evaluation["evidence_states"][flag]
            + "` | "
            + criterion
            + " |"
        )
    return "\n".join(
        [
            "# Phase 3G.1 - Single Lead Hard-Gate Comparison",
            "",
            f"- Lead: `{evaluation['lead_id']}`",
            f"- Label: `{decision['computed_intake_label']}`",
            f"- Canonical dataset label: `{decision['canonical_dataset_label']}`",
            (
                "- Phase 3F.2 intake allowed: "
                f"`{str(decision['phase3f2_intake_allowed']).lower()}`"
            ),
            (
                "- Residual modeling allowed now: "
                f"`{str(decision['residual_modeling_allowed_now']).lower()}`"
            ),
            f"- Exact next action: {decision['exact_next_action'] or 'none'}",
            "",
            "## Gate Table",
            "",
            *rows,
            "",
            "## Stop Rules",
            "",
            *[f"- {rule}" for rule in packet["stop_rules"]],
            "",
        ]
    )


def phase3g1_markdown(packet: dict[str, Any]) -> str:
    decision = packet["decision"]
    summary = packet["summary"]
    selected = decision["selected_next_lead_id"] or "none"
    rows = [
        "| Lead | Label | Gate Pass? | Missing / Risk Flags | Next Action |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in sorted(packet["lead_evaluations"], key=_selection_key):
        missing = ", ".join(item["missing_required_flags"][:5])
        if len(item["missing_required_flags"]) > 5:
            missing += ", ..."
        rows.append(
            "| "
            + item["lead_id"]
            + " | `"
            + item["canonical_dataset_label"]
            + "` | "
            + ("yes" if item["hard_gate_pass"] else "no")
            + " | "
            + (missing or "none")
            + " | "
            + (item["exact_next_action"] or "none")
            + " |"
        )

    failure_memory = packet["failure_memory"]
    assistant = packet["assistant_command_contract"]
    lines = [
        f"# {packet['phase_id']} - {packet['title']}",
        "",
        "## Decision",
        "",
        f"- Status: `{decision['status']}`",
        f"- Selected next lead: `{selected}`",
        f"- Phase 3F.2 intake allowed: `{str(decision['phase3f2_intake_allowed']).lower()}`",
        (
            "- Residual modeling allowed now: "
            f"`{str(decision['residual_modeling_allowed_now']).lower()}`"
        ),
        (
            "- Phase 4 candidate ready now: "
            f"`{str(decision['phase4_candidate_ready_now']).lower()}`"
        ),
        f"- Recommended next phase: `{decision['recommended_next_phase']}`",
        "",
        "Phase 3G.1 is an assistant-facing queue. It ranks leads and preserves",
        "missing evidence, but it does not download files, fit parameters, inspect",
        "measured residuals, or promote claim status.",
        "",
        "## Prior Failure Memory",
        "",
        f"- Phase 3F.1F memory available: `{str(failure_memory['available']).lower()}`",
        (
            "- Prior measured-data leads recorded: "
            f"`{failure_memory.get('prior_measured_data_leads', 0)}`"
        ),
        (
            "- Phase 3F.2 allowed by prior memory: "
            f"`{str(failure_memory.get('phase3f2_intake_allowed')).lower()}`"
        ),
        "",
        "## Searchable Failure Memory",
        "",
        *[f"- `{record}`" for record in packet["searchable_failure_records"]],
        "",
        "## Queue Summary",
        "",
        f"- Lead count: `{summary['lead_count']}`",
        f"- Hard-gate pass count: `{summary['hard_gate_pass_count']}`",
        "",
        "## Lead Gate Table",
        "",
        *rows,
        "",
        "## Assistant Workflows",
        "",
        f"- Primary CLI: `{assistant['primary_cli']}`",
        *[
            f"- Command `{name}`: `{command}`"
            for name, command in assistant["commands"].items()
        ],
        *[
            f"- {workflow['name']}: {workflow['output']}"
            for workflow in assistant["supported_workflows"]
        ],
        "",
        "## 5.5 Pro Prompt",
        "",
        "```text",
        assistant["pro_prompt"],
        "```",
        "",
        "## Stop Rules",
        "",
        *[f"- {rule}" for rule in packet["stop_rules"]],
        "",
    ]
    return "\n".join(lines)


def write_phase3g1_packet(
    output_dir: Path,
    packet: dict[str, Any],
    report_stem: str = "phase3g_measured_data_intake_queue",
) -> tuple[Path, Path]:
    if report_stem != Path(report_stem).name or not report_stem:
        raise ValueError("report_stem must be a non-empty filename stem")
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{report_stem}.json"
    md_path = output_dir / f"{report_stem}.md"
    json_path.write_text(json.dumps(packet, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(phase3g1_markdown(packet), encoding="utf-8")
    return json_path, md_path
