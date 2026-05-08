"""Scan/digest orchestration for the research radar."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from eternity.research_memory.ids import content_hash_for_record
from eternity.research_memory.radar.adapters import (
    Clock,
    fetch_json,
    fetch_text,
    scan_enabled_sources,
)
from eternity.research_memory.radar.config import RadarConfig, load_radar_config
from eternity.research_memory.radar.dedupe import dedupe_candidates
from eternity.research_memory.radar.models import RadarCandidate, RadarRunManifest
from eternity.research_memory.radar.render import build_radar_markdown
from eternity.research_memory.radar.scoring import rank_candidates


def _run_id(payload: object) -> str:
    return f"radar_{content_hash_for_record(payload)[:12]}"


def _write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str))


def scan_radar(
    *,
    config_path: Path,
    output_root: Path = Path("results/research_memory/radar"),
    dry_run: bool = True,
    clock: Clock | None = None,
) -> Path:
    """Scan enabled configured sources, rank candidates, and write a run directory."""

    config = load_radar_config(config_path)
    raw_candidates, warnings = scan_enabled_sources(
        config,
        text_fetcher=fetch_text,
        json_fetcher=fetch_json,
        clock=clock,
    )
    if dry_run and not raw_candidates:
        raw_candidates = seed_candidates_from_queries(config)
        warnings.append(
            "No enabled external sources returned candidates; dry-run used recurring query seeds."
        )
    deduped = dedupe_candidates(raw_candidates)
    ranked = rank_candidates(deduped, scoring=config.scoring)
    generated_at = datetime.now(UTC)
    identity = {
        "generated_at": generated_at.isoformat(),
        "config_path": str(config_path),
        "candidate_titles": [candidate.title for candidate in deduped],
        "warnings": warnings,
    }
    run_id = _run_id(identity)
    run_dir = output_root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    manifest = RadarRunManifest(
        run_id=run_id,
        generated_at=generated_at,
        config_path=str(config_path),
        dry_run=dry_run,
        source_count=len([source for source in config.sources if source.enabled]),
        raw_candidate_count=len(raw_candidates),
        deduped_candidate_count=len(deduped),
        warnings=warnings,
        recurring_queries=config.recurring_queries,
        arxiv_categories=config.arxiv_categories,
        themes=config.themes,
    )
    _write_json(
        run_dir / "candidates.json",
        [candidate.model_dump(mode="json", exclude_none=True) for candidate in deduped],
    )
    _write_json(
        run_dir / "ranked.json",
        [item.model_dump(mode="json", exclude_none=True) for item in ranked],
    )
    _write_json(run_dir / "manifest.json", manifest.model_dump(mode="json"))
    return run_dir


def load_ranked_run(run_dir: Path) -> tuple[RadarConfig | None, list[dict], dict]:
    """Load a previously scanned radar run."""

    manifest = json.loads((run_dir / "manifest.json").read_text())
    ranked_payload = json.loads((run_dir / "ranked.json").read_text())
    config_path = Path(manifest["config_path"])
    config = load_radar_config(config_path) if config_path.exists() else None
    return config, ranked_payload, manifest


def digest_radar_run(run_dir: Path) -> Path:
    """Render a digest from a scanned radar run."""

    config, ranked_payload, manifest = load_ranked_run(run_dir)
    from eternity.research_memory.radar.models import RankedRadarCandidate

    ranked = [RankedRadarCandidate.model_validate(item) for item in ranked_payload]
    markdown = build_radar_markdown(
        ranked,
        generated_at=datetime.fromisoformat(manifest["generated_at"]),
        dry_run=manifest["dry_run"],
        warnings=manifest["warnings"],
        recurring_queries=(
            config.recurring_queries if config else manifest.get("recurring_queries", [])
        ),
        arxiv_categories=(
            config.arxiv_categories if config else manifest.get("arxiv_categories", [])
        ),
    )
    digest_path = run_dir / "digest.md"
    digest_path.write_text(markdown)
    (run_dir.parent / "latest.md").write_text(markdown)
    return digest_path


def seed_candidates_from_queries(config: RadarConfig) -> list[RadarCandidate]:
    """Create deterministic placeholder leads from recurring queries for dry-run visibility."""

    return [
        RadarCandidate(
            source_id="recurring_query_seed",
            source_type="rss_feed",
            title=query,
            abstract="Recurring query seed for Codex/OpenClaw web radar; not a fetched paper.",
            query=query,
            tags=["recurring_query", "codex_web_radar"],
            project_areas=["literature_radar"],
        )
        for query in config.recurring_queries
    ]
