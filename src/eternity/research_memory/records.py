"""Strict Pydantic schemas for local research-memory records."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, model_validator


class EvidenceState(StrEnum):
    UNKNOWN = "unknown"
    SPECULATIVE = "speculative"
    LITERATURE_SUPPORTED = "literature_supported"
    OBSERVED_LAB = "observed_lab"
    SIMULATED = "simulated"
    VALIDATED = "validated"
    CONTRADICTED = "contradicted"
    DEPRECATED = "deprecated"


class SourceType(StrEnum):
    PEER_REVIEWED_PAPER = "peer_reviewed_paper"
    PREPRINT = "preprint"
    INSTRUMENT_MANUAL = "instrument_manual"
    LAB_NOTE = "lab_note"
    SIMULATION_ARTIFACT = "simulation_artifact"
    CONFERENCE_TALK = "conference_talk"
    NEWSLETTER = "newsletter"
    SOCIAL_LEAD = "social_lead"
    AGENT_SUMMARY = "agent_summary"
    CODEX_TASK = "codex_task"
    LOCAL_NOTE = "local_note"
    OTHER = "other"


class ReviewState(StrEnum):
    NEEDS_HUMAN_REVIEW = "needs_human_review"
    REVIEWED = "reviewed"
    APPROVED_FOR_CODEX = "approved_for_codex"
    APPROVED_FOR_LAB_PLANNING = "approved_for_lab_planning"
    ARCHIVED = "archived"


class Confidence(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class HypothesisValidationStatus(StrEnum):
    UNTESTED = "untested"
    SYNTHETIC_ONLY = "synthetic_only"
    LAB_PARTIAL = "lab_partial"
    VALIDATED = "validated"
    WEAKENED = "weakened"
    REJECTED = "rejected"


class Severity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class DigestKind(StrEnum):
    WEEKLY = "weekly"
    HOME = "home"
    PROJECT_AREA = "project_area"
    ADVISOR_SUMMARY = "advisor_summary"


class SourceRef(BaseModel):
    """A provenance pointer for a research-memory record."""

    source_type: SourceType
    locator: str = Field(min_length=1)
    description: str = Field(min_length=1)
    content_hash: str | None = None
    retrieved_at: datetime | None = None

    model_config = ConfigDict(extra="forbid")


class ResearchRecord(BaseModel):
    """Common auditable fields shared by all research-memory records."""

    schema_version: Literal["0.1"] = "0.1"
    record_type: str
    record_id: str | None = None
    title: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    body: str = ""
    evidence_state: EvidenceState
    review_state: ReviewState = ReviewState.NEEDS_HUMAN_REVIEW
    source_refs: list[SourceRef] = Field(min_length=1)
    source_type: SourceType | None = None
    created_at: datetime
    updated_at: datetime | None = None
    tags: list[str] = Field(min_length=1)
    project_areas: list[str] = Field(default_factory=list)
    related_record_ids: list[str]
    claims: list[str] = Field(min_length=1)
    limitations: list[str] = Field(min_length=1)
    next_actions: list[str] = Field(min_length=1)
    assumptions: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    reviewer_notes: list[str] = Field(default_factory=list)
    validation_artifact_ref: str | None = None

    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    @model_validator(mode="after")
    def validated_requires_validation_artifact(self) -> ResearchRecord:
        if self.evidence_state == EvidenceState.VALIDATED and not self.validation_artifact_ref:
            raise ValueError("validation_artifact_ref is required for validated records")
        return self


class SourceRecord(ResearchRecord):
    record_type: Literal["source"]
    source_kind: str = Field(min_length=1)
    canonical_id: str = Field(min_length=1)
    raw_metadata_hash: str | None = None
    license_notes: str = ""
    trust_notes: str = ""


class PaperCardRecord(ResearchRecord):
    record_type: Literal["paper_card"]
    paper_title: str = Field(min_length=1)
    paper_authors: list[str] = Field(min_length=1)
    year: int | None = None
    doi: str | None = None
    arxiv_id: str | None = None
    paper_url: str | None = None
    main_claims: list[str] = Field(default_factory=list)
    methods: list[str] = Field(default_factory=list)
    parameters: dict[str, Any] = Field(default_factory=dict)
    measurements: list[str] = Field(default_factory=list)
    suggested_simulation_tasks: list[str] = Field(default_factory=list)
    suggested_lab_tests: list[str] = Field(default_factory=list)
    suggested_codex_tasks: list[str] = Field(default_factory=list)
    caveats: list[str] = Field(default_factory=list)


class MethodTransferRecord(ResearchRecord):
    record_type: Literal["method_transfer"]
    method_name: str = Field(min_length=1)
    original_field: str = Field(min_length=1)
    transfer_target: str = Field(min_length=1)
    why_it_might_help: list[str] = Field(min_length=1)
    first_synthetic_test: str = Field(min_length=1)
    lab_feasibility: str = Field(min_length=1)
    required_inputs: list[str] = Field(default_factory=list)
    risks_or_misfits: list[str] = Field(default_factory=list)
    suggested_codex_task: str = Field(min_length=1)


class LabFailureModeRecord(ResearchRecord):
    record_type: Literal["lab_failure_mode"]
    symptom: str = Field(min_length=1)
    known_observations: list[str] = Field(min_length=1)
    likely_causes: list[str] = Field(default_factory=list)
    ruled_out_or_weakened: list[str] = Field(default_factory=list)
    diagnostic_tests: list[str] = Field(default_factory=list)
    related_runs_or_samples: list[str] = Field(default_factory=list)
    advisor_safe_summary: str = Field(min_length=1)


class HypothesisRecord(ResearchRecord):
    record_type: Literal["hypothesis"]
    hypothesis_id: str = Field(min_length=1)
    hypothesis_statement: str = Field(min_length=1)
    why_plausible: list[str] = Field(min_length=1)
    what_would_support_it: list[str] = Field(min_length=1)
    what_would_weaken_it: list[str] = Field(min_length=1)
    next_simulation: str = Field(min_length=1)
    next_lab_test: str = Field(min_length=1)
    current_confidence: Confidence
    validation_status: HypothesisValidationStatus


class ContradictionRecord(ResearchRecord):
    record_type: Literal["contradiction"]
    record_a: str = Field(min_length=1)
    record_b: str = Field(min_length=1)
    tension_summary: str = Field(min_length=1)
    why_it_matters: str = Field(min_length=1)
    possible_resolution: str = Field(min_length=1)
    recommended_follow_up: str = Field(min_length=1)
    severity: Severity


class CodexTaskDraft(ResearchRecord):
    record_type: Literal["codex_task_draft"]
    goal: str = Field(min_length=1)
    context: str = Field(min_length=1)
    source_record_ids: list[str] = Field(min_length=1)
    inputs: list[str] = Field(default_factory=list)
    expected_outputs: list[str] = Field(min_length=1)
    success_criteria: list[str] = Field(min_length=1)
    do_not: list[str] = Field(min_length=1)
    scientific_guardrails: list[str] = Field(min_length=1)


class DigestItem(ResearchRecord):
    record_type: Literal["digest_item"]
    digest_kind: DigestKind
    included_record_ids: list[str] = Field(min_length=1)
    queue: Literal[
        "must_read",
        "experiment_ideas",
        "codex_tasks",
        "weak_claims",
        "surprising_connections",
        "recent_records",
    ]


RecordUnion = Annotated[
    SourceRecord
    | PaperCardRecord
    | MethodTransferRecord
    | LabFailureModeRecord
    | HypothesisRecord
    | ContradictionRecord
    | CodexTaskDraft
    | DigestItem,
    Field(discriminator="record_type"),
]

record_adapter = TypeAdapter(RecordUnion)


def validate_record_payload(payload: dict[str, Any]) -> ResearchRecord:
    """Validate a raw record payload and return the typed model."""

    return record_adapter.validate_python(payload)
