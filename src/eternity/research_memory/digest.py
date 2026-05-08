"""Conservative Markdown digests for research-memory records."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from eternity.research_memory.ids import content_hash_for_record
from eternity.research_memory.records import ResearchRecord


def _matches_project_area(record: ResearchRecord, project_area: str | None) -> bool:
    return project_area is None or project_area in record.project_areas


def _bullet(record: ResearchRecord) -> str:
    source_refs = "; ".join(
        f"{source.source_type}:{source.locator}" for source in record.source_refs
    )
    return (
        f"- `{record.record_id}` {record.title} "
        f"(type={record.record_type}, evidence={record.evidence_state}, "
        f"source_refs={source_refs})"
    )


def _section(title: str, records: list[ResearchRecord]) -> list[str]:
    lines = [f"## {title}"]
    if records:
        lines.extend(_bullet(record) for record in records)
    else:
        lines.append("- None.")
    lines.append("")
    return lines


def build_digest_markdown(
    records: list[ResearchRecord],
    *,
    project_area: str | None = None,
    generated_at: datetime | None = None,
) -> str:
    """Build a deterministic, non-validating research-memory digest."""

    generated_at = generated_at or datetime.now(UTC)
    scoped = sorted(
        [record for record in records if _matches_project_area(record, project_area)],
        key=lambda record: (record.created_at, record.record_id or ""),
        reverse=True,
    )

    must_review = [
        record
        for record in scoped
        if record.record_type in {"paper_card", "source", "method_transfer"}
        or record.review_state == "needs_human_review"
    ]
    codex_tasks = [
        record
        for record in scoped
        if record.record_type == "codex_task_draft"
        or any("codex" in action.lower() for action in record.next_actions)
    ]
    experiment_ideas = [
        record
        for record in scoped
        if record.record_type in {"hypothesis", "lab_failure_mode"}
        or any(
            "experiment" in action.lower() or "lab" in action.lower()
            for action in record.next_actions
        )
    ]
    weak_claims = [
        record
        for record in scoped
        if record.evidence_state
        in {"unknown", "speculative", "literature_supported", "observed_lab", "simulated"}
    ]
    surprising = [
        record
        for record in scoped
        if record.record_type in {"method_transfer", "contradiction"}
        or "surprising_connection" in record.tags
    ]

    lines = [
        f"# Eternity Research Memory Digest - {generated_at.date().isoformat()}",
        "",
        "This digest is a review queue, not validated evidence.",
        "Research memory proposes hypotheses, tasks, and weak-claim checks; serious-core "
        "validation remains separate.",
        "",
    ]
    if project_area:
        lines.extend([f"Project area: `{project_area}`", ""])

    lines.extend(_section("Must-read / must-review", must_review[:8]))
    lines.extend(_section("Possible Codex tasks", codex_tasks[:8]))
    lines.extend(_section("Possible experiment ideas", experiment_ideas[:8]))
    lines.extend(_section("Weak claims / needs validation", weak_claims[:8]))
    lines.extend(_section("Surprising connections", surprising[:8]))
    lines.extend(_section("Recent records", scoped[:8]))
    lines.append("## Provenance")
    if scoped:
        for record in scoped:
            refs = "; ".join(
                f"{source.source_type}:{source.locator} ({source.description})"
                for source in record.source_refs
            )
            lines.append(f"- `{record.record_id}` {refs}")
    else:
        lines.append("- None.")
    lines.append("")
    return "\n".join(lines)


def write_digest(
    records: list[ResearchRecord],
    *,
    output_root: Path = Path("results/research_memory/digests"),
    project_area: str | None = None,
) -> Path:
    """Write a Markdown digest artifact and return its path."""

    digest_markdown = build_digest_markdown(records, project_area=project_area)
    digest_hash = content_hash_for_record(
        {
            "record_ids": [record.record_id for record in records],
            "project_area": project_area,
            "digest": digest_markdown,
        }
    )[:12]
    today = datetime.now(UTC).date().isoformat()
    output_dir = output_root / f"{today}_{digest_hash}"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "digest.md"
    output_path.write_text(digest_markdown)
    return output_path
