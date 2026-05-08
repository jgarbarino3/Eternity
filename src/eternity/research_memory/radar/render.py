"""Markdown rendering for radar digests."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from eternity.research_memory.ids import content_hash_for_record
from eternity.research_memory.radar.models import RankedRadarCandidate


def _candidate_link(item: RankedRadarCandidate) -> str:
    candidate = item.candidate
    if candidate.url:
        return f"[{candidate.title}]({candidate.url})"
    return candidate.title


def _short_meta(item: RankedRadarCandidate) -> str:
    candidate = item.candidate
    values = [
        f"source={candidate.source_id}",
        f"type={candidate.source_type}",
        f"score={item.score}",
    ]
    if item.themes:
        values.append(f"themes={', '.join(item.themes)}")
    if candidate.venue:
        values.append(f"venue={candidate.venue}")
    if candidate.year:
        values.append(f"year={candidate.year}")
    if candidate.arxiv_id:
        values.append(f"arxiv={candidate.arxiv_id}")
    if candidate.doi:
        values.append(f"doi={candidate.doi}")
    return "; ".join(values)


def _render_full_item(index: int, item: RankedRadarCandidate) -> list[str]:
    candidate = item.candidate
    lines = [
        f"### {index}. {item.grade}: {_candidate_link(item)}",
        "",
        f"- Metadata: {_short_meta(item)}",
        f"- Reasons: {'; '.join(item.reasons)}",
        f"- Why this matters for Eternity: {item.why_this_matters}",
        f"- Possible experiment: {item.possible_experiment}",
        f"- Possible code module: {item.possible_code_module}",
        f"- Risk / limitation: {item.risk_or_limitation}",
        f"- Should we act now? {item.should_we_act_now}",
    ]
    if candidate.abstract:
        lines.append(f"- Abstract signal: {' '.join(candidate.abstract.split())[:500]}")
    lines.append("")
    return lines


def _render_compact_section(title: str, items: list[RankedRadarCandidate]) -> list[str]:
    lines = [f"## {title}"]
    if not items:
        lines.extend(["- None.", ""])
        return lines
    for item in items:
        lines.append(f"- `{item.grade}` {_candidate_link(item)} ({_short_meta(item)})")
    lines.append("")
    return lines


def build_radar_markdown(
    ranked: list[RankedRadarCandidate],
    *,
    generated_at: datetime | None = None,
    dry_run: bool = False,
    warnings: list[str] | None = None,
    recurring_queries: list[str] | None = None,
    arxiv_categories: list[str] | None = None,
) -> str:
    """Build an Eternity-specific radar digest."""

    generated_at = generated_at or datetime.now(UTC)
    warnings = warnings or []
    recurring_queries = recurring_queries or []
    arxiv_categories = arxiv_categories or []
    act_now = [item for item in ranked if item.grade == "A"]
    strong_b = [item for item in ranked if item.grade == "B" and item.strong_b]
    architecture = [item for item in ranked if item.grade == "B" and not item.strong_b]
    relevant = [item for item in ranked if item.grade == "C"]
    noise = [item for item in ranked if item.grade == "D"]
    read_later = [item for item in ranked if item.grade == "E"]

    lines = [
        f"# Eternity Weekly Research Radar - {generated_at.date().isoformat()}",
        "",
        "This radar is a review queue, not validated evidence.",
        "It uses deterministic rules and source metadata to prioritize papers for human review. "
        "No item may feed the serious core without explicit validation artifacts.",
        "",
        f"Dry run: `{str(dry_run).lower()}`",
        "",
    ]
    if warnings:
        lines.append("## Warnings")
        lines.extend(f"- {warning}" for warning in warnings)
        lines.append("")

    lines.append("## Act-now and strong architecture leads")
    high_signal = act_now + strong_b
    if high_signal:
        for index, item in enumerate(high_signal, start=1):
            lines.extend(_render_full_item(index, item))
    else:
        lines.extend(["- None.", ""])

    lines.extend(_render_compact_section("Architecture ideas", architecture[:20]))
    lines.extend(_render_compact_section("Relevant but not actionable", relevant[:20]))
    lines.extend(_render_compact_section("Hype / noise", noise[:20]))
    lines.extend(_render_compact_section("Read later", read_later[:20]))

    lines.append("## Recurring Queries")
    lines.extend(f"- {query}" for query in recurring_queries)
    lines.append("")

    lines.append("## arXiv Categories")
    if arxiv_categories:
        lines.extend(f"- `{category}`" for category in arxiv_categories)
    else:
        lines.append("- None configured.")
    lines.append("")

    lines.append("## Provenance")
    if ranked:
        for item in ranked:
            candidate = item.candidate
            locator = candidate.url or candidate.canonical_url or candidate.title
            lines.append(
                f"- {candidate.source_id}: {locator} "
                f"(grade={item.grade}, score={item.score}, themes={', '.join(item.themes)})"
            )
    else:
        lines.append("- No candidates.")
    lines.append("")
    return "\n".join(lines)


def write_radar_digest(
    ranked: list[RankedRadarCandidate],
    *,
    output_root: Path = Path("results/research_memory/radar"),
    generated_at: datetime | None = None,
    dry_run: bool = False,
    warnings: list[str] | None = None,
    recurring_queries: list[str] | None = None,
    arxiv_categories: list[str] | None = None,
) -> Path:
    """Write a dated radar digest and update latest.md."""

    generated_at = generated_at or datetime.now(UTC)
    markdown = build_radar_markdown(
        ranked,
        generated_at=generated_at,
        dry_run=dry_run,
        warnings=warnings,
        recurring_queries=recurring_queries,
        arxiv_categories=arxiv_categories,
    )
    digest_hash = content_hash_for_record(
        {
            "ranked": [item.model_dump(mode="json", exclude_none=True) for item in ranked],
            "warnings": warnings or [],
            "markdown": markdown,
        }
    )[:12]
    run_dir = output_root / f"{generated_at.date().isoformat()}_{digest_hash}"
    run_dir.mkdir(parents=True, exist_ok=True)
    digest_path = run_dir / "digest.md"
    digest_path.write_text(markdown)
    (output_root / "latest.md").write_text(markdown)
    (run_dir / "ranked.json").write_text(
        json.dumps([item.model_dump(mode="json", exclude_none=True) for item in ranked], indent=2)
    )
    return digest_path
