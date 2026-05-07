# Eternity

Eternity is a long-term AI-assisted ultrafast ENZ optics research project. V0 is a reproducible synthetic thin-film experiment runner, not an autonomous scientist.

## V0 Commands

```bash
uv sync
uv run --no-editable eternity validate experiments/examples/linear_ito_toy.yaml
uv run --no-editable eternity run experiments/examples/linear_ito_toy.yaml
```

Direct console-script targets after installation:

```bash
eternity validate experiments/examples/linear_ito_toy.yaml
eternity run experiments/examples/linear_ito_toy.yaml
```

The first run writes deterministic artifacts under `results/runs/<run_id>/`, including a resolved spec, provenance, metrics, warnings, plots, and a Markdown report.
