# Eternity

Eternity is a long-term AI-assisted ultrafast ENZ optics research project. V0 is a reproducible synthetic thin-film experiment runner, not an autonomous scientist.

## V0 Commands

```bash
uv sync
uv run --no-editable eternity validate experiments/examples/linear_ito_toy.yaml
uv run --no-editable eternity validate-registry lab_data/registry.yaml
uv run --no-editable eternity hash-artifact lab_data/raw/synthetic_v0/transmission_fixture.csv
uv run --no-editable eternity run experiments/examples/linear_ito_toy.yaml
```

Direct console-script targets after installation:

```bash
eternity validate experiments/examples/linear_ito_toy.yaml
eternity validate-registry lab_data/registry.yaml
eternity hash-artifact lab_data/raw/synthetic_v0/transmission_fixture.csv
eternity run experiments/examples/linear_ito_toy.yaml
```

The first run writes deterministic artifacts under `results/runs/<run_id>/`, including a resolved spec, provenance, metrics, warnings, plots, and a Markdown report.

V1.0 contract artifacts add claim status, input manifest, artifact hashes, and
validation gate files. Synthetic V0 runs remain labeled
`synthetic_software_fixture`; they are software fixtures, not calibrated linear
evidence.

## Research Memory

Stage 0/1 adds a local, file-backed research-memory layer for reviewable paper
cards, method-transfer notes, lab failure modes, hypotheses, contradictions,
Codex task drafts, and digest items. These records are Researcher Playground
artifacts: they can propose next work, but they do not validate scientific
claims.

```bash
uv run --no-editable eternity memory validate research_memory/examples
uv run --no-editable eternity memory list research_memory/examples --tag frog
uv run --no-editable eternity memory search research_memory/examples "scalar GDD TiN FROG"
uv run --no-editable eternity memory digest research_memory/examples --project-area tin_frog
uv run --no-editable eternity memory radar scan --config config/research_radar.example.yaml --dry-run
```

See `docs/research_memory.md` for schema boundaries, evidence-state rules, and
how to add records.
