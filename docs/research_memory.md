# Eternity Research Memory

The research-memory layer is a local, typed, reviewable record system for ideas,
papers, method-transfer notes, lab failure modes, hypotheses, contradictions,
Codex task drafts, and digest items.

It belongs to the Researcher Playground, not the Serious Core. It can preserve
context and propose next work, but it does not validate scientific claims.

## Boundary

The Serious Core owns experiment specs, material models, calibrated or holdout
validation, simulations, reports, uncertainty, and scientific conclusions.

Research memory owns review queues:

- literature and method-transfer notes,
- lab troubleshooting memory,
- hypothesis queues,
- contradiction and weak-claim notes,
- Codex task drafts,
- conservative digests.

Memory records may say "candidate explanation", "possible transfer", "needs
validation", or "consistent with". They must not claim novelty, mechanism proof,
validated material-model correctness, nonlinear isolation, or paper-ready
conclusions without serious-core validation artifacts.

## Commands

```bash
uv run --no-editable eternity memory validate research_memory/examples
uv run --no-editable eternity memory list research_memory/examples --tag frog
uv run --no-editable eternity memory show <record-id> --dir research_memory/examples --json
uv run --no-editable eternity memory search research_memory/examples "scalar GDD TiN FROG"
uv run --no-editable eternity memory digest research_memory/examples --project-area tin_frog
```

`digest` writes Markdown under `results/research_memory/digests/`. Runtime memory
data belongs under `data/research_memory/` or `results/research_memory/`, both of
which are ignored by git.

## Weekly Research Radar

The radar layer turns public metadata feeds and Codex web-search results into a
review queue. It is not a literature authority and cannot validate scientific
claims.

```bash
uv run --no-editable eternity memory radar validate-config config/research_radar.example.yaml
uv run --no-editable eternity memory radar scan --config config/research_radar.example.yaml --dry-run
uv run --no-editable eternity memory radar digest --run-dir results/research_memory/radar/<run_id>
uv run --no-editable eternity memory radar promote --run-dir results/research_memory/radar/<run_id> --min-grade A --record-dir data/research_memory/radar
```

`scan --dry-run` writes run artifacts under `results/research_memory/radar/` and
does not create research-memory records. `promote` is explicit and should only be
run after human review. Google Scholar is manual alert/export only; the radar
must not scrape it.

OpenClaw or Codex may orchestrate scheduled runs, but they should call the
allowlisted radar commands and write Markdown artifacts only. They should not
promote records, edit code, upgrade evidence states, or open lab-control
surfaces without a separate human review gate.

### Optional Browse.sh Support

Browserbase Browse is installed as an optional browser and Browse.sh skill
surface for agent-assisted discovery. The project-local skill
`.agents/skills/search-papers/SKILL.md` documents a read-only arXiv Atom API
workflow (`arxiv.org/search-papers-zv05w6`) that may be used for literature
scouting and arXiv metadata lookups before human review.

Browse results remain Research Memory/Radar inputs only. They do not promote
records, validate claims, replace source archives, or upgrade evidence states.
Google Scholar remains manual alert/export only. See
`docs/agents/browserbase_browse.md` for setup, commands, and safety boundaries.

### Optional Plasmate Support

Plasmate is available as an optional MCP surface for quick readable-text
extraction and lightweight browser inspection of public literature, repository,
dataset, supplement, and source-data pages. Use it more often with Browse.sh
when it improves source coverage or speeds candidate triage.

Plasmate results remain Research Memory/Radar inputs only. They can seed paper
cards, candidate cards, and follow-up tasks, but they do not replace downloaded
artifacts, checksums, machine-readable tables, repo-local scripts, or claim
review. See `docs/agents/plasmate.md` for setup notes and safety boundaries.

## Adding Records

Add curated, reviewable YAML or JSON files under a committed examples directory
or a local private directory. Each record must include:

- `record_type`
- `title`
- `summary`
- `evidence_state`
- `source_refs`
- `created_at`
- `tags`
- `related_record_ids`
- `claims`
- `limitations`
- `next_actions`

Omit `record_id` unless you intentionally want to pin it. The CLI computes a
stable ID from normalized record content.

### Paper Card

Use `record_type: paper_card` for a paper-to-action note. Keep paper claims
separate from what Eternity can reproduce or adapt. Use `evidence_state:
literature_supported` only for claims supported by the source, not for transfer
to Eternity.

### Lab Failure Mode

Use `record_type: lab_failure_mode` when a lab observation should be searchable
without overinterpreting it. `evidence_state: observed_lab` means the observation
was noted; it does not mean the interpretation is correct.

### Hypothesis

Use `record_type: hypothesis` for ranked candidate explanations. Use
`evidence_state: speculative` unless a serious-core validation artifact exists.
`evidence_state: validated` is rejected unless `validation_artifact_ref` is
present.

## Future Stages

Stage 2 should add paper-to-action translation and optional Codex task generation
from records. Later stages may add source adapters, graph/semantic indexing, or
agent access, but those systems must index these auditable records rather than
replace them as the source of truth.
