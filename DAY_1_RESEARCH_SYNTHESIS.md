# Day 1 Research Synthesis

Date: 2026-05-07

## Honest Position

Eternity is feasible today as a calibrated ultrafast ENZ optics research environment with AI assistance. It is not feasible today as a fully autonomous scientist that can reliably discover new physics, certify novelty, diagnose all artifacts, and write publishable papers without expert review.

The useful near-term project is not "AI discovers physics from scratch." It is:

> Build a reproducible ENZ digital twin and lab-memory system that an AI can use to run bounded theoretical experiments, compare models, track uncertainty, and propose next tests.

That is ambitious enough. If the foundation is rigorous, future AI model improvements can become better reasoning layers on top of the same data, solvers, and validation history.

## What Seems Truly Buildable Now

We can build a strong first version with current tools:

- A Python research package for ENZ thin-film experiments.
- YAML experiment specs with schema validation.
- A lab-data registry with immutable file hashes.
- Drude and Drude-Lorentz material models.
- Linear thin-film transfer-matrix simulation.
- Ellipsometry and transmission/reflection fitting workflows.
- Deterministic run artifacts and a SQLite run ledger.
- Markdown reports generated from recorded artifacts.
- Regression tests for units, energy bookkeeping, deterministic replay, and low-fluence limits.
- Literature/lab-memory ingestion for papers, notes, datasets, and failed hypotheses.
- AI-assisted hypothesis generation with hard human review gates.

This would already be useful even if no autonomous researcher exists yet.

## What Is Not Buildable Reliably Today

Current AI assistance should not be trusted to:

- Certify that a simulated effect is genuinely new physics.
- Know whether a lab artifact has been modeled unless the artifact is explicitly encoded.
- Build a fully trustworthy hot-electron ENZ solver from prose alone without careful physics validation.
- Decide that a paper should be written from simulation output alone.
- Treat polished plots and fluent explanations as evidence.
- Run physical lab instruments without strict human gating.
- Use surrogate models outside their calibrated domain.

The system must be designed to slow down overclaiming.

## Simulation Stack Takeaway

No surveyed open-source package appears to provide turnkey ultrafast ENZ/TCO hot-electron pump-probe dynamics for ITO/AZO/CdO thin films.

The right stack is multi-fidelity:

1. **Day 1 baseline**
   - `tmm` or `TMMax` for thin-film transfer matrix.
   - `refractiveindex.info` seed data where useful.
   - `pyElli` or `refellips` as references for ellipsometry modeling.
   - Project-owned Drude/Drude-Lorentz fitting and result contracts.

2. **Validation backends**
   - Meep as the most credible open-source FDTD backend.
   - Tidy3D as a possible paid/cloud comparison backend later.
   - openEMS, S4, Meent, Ceviche, FDTDX, Palace, MFEM, FEniCSx, or NGSolve only when a specific modeling need justifies them.

3. **Custom core**
   - The ENZ hot-electron material dynamics layer should be project-owned.
   - It should start static, then add time-dependent plasma frequency, damping, electron/lattice temperature, effective mass, and validity envelopes.

## Useful Repos And Libraries

Highest-priority practical dependencies:

- `sbyrnes321/tmm`: linear thin-film transfer matrix.
- `TMMax`: JAX transfer matrix for fast sweeps and fitting.
- `refractiveindex.info` Python interfaces: seed optical constants with provenance.
- `pyElli` / `refellips`: ellipsometry modeling references.
- `Meep`: first serious open-source FDTD validation backend.
- `SciPy`, `lmfit`, `xarray`, `pandas`, `numpy`, `matplotlib`, `pydantic`, `pint`, `typer`, `pytest`, `ruff`.

Useful later:

- `gnlse-python`, `py-fmas`, `Luna.jl`, `PyNLO`: pulse-propagation references.
- `Meent` / `S4`: periodic or metasurface RCWA.
- `NTMpy`: thermal pump-probe modeling reference.
- `DVC`: once real raw datasets become too large or important for plain Git.
- `DuckDB`: once analysis queries outgrow SQLite.

## MCP And Tooling Takeaway

Do not start with a huge MCP pile. The first month needs a disciplined local research codebase more than a swarm of integrations.

Useful now:

- OpenAI developer docs MCP for OpenAI/Codex/API docs.
- Consensus for fast scientific literature search.
- Git/GitHub once the repo is initialized.
- Local Python execution and shell tooling.
- Google Drive only if lab data or papers live there.

Useful soon:

- arXiv, PubMed, Semantic Scholar, Crossref, and OpenAlex ingestion, probably through direct APIs first.
- Zotero MCP or Zotero export once the literature library becomes central.
- Jupyter MCP only after notebooks are supporting views, not the source of truth.
- Qdrant/Chroma only after there is enough curated literature/lab memory to justify vector search.

Useful much later:

- Docker/HPC job MCPs for simulation queues.
- PyVISA/serial/DAQ instrument-control MCPs with strict human confirmation.
- Slack/Gmail/Calendar only if collaboration and lab scheduling become part of the workflow.

Low priority now:

- Autonomous multi-agent frameworks.
- Browser automation.
- Vector database first.
- Direct instrument control.
- Heavy workflow engines before the first validated optical result.

## First-Month Technical Direction

Recommended foundation:

1. Initialize a Python package, not an agent.
2. Use `uv`, `pyproject.toml`, `ruff`, `pytest`, and `src/eternity`.
3. Define `ExperimentSpec v0.1` with Pydantic and generated JSON Schema.
4. Add Pint-backed units and strict wavelength/frequency/energy conversions.
5. Create a SHA-256 lab-data registry.
6. Create a SQLite run ledger.
7. Implement Drude and Drude-Lorentz material models.
8. Implement linear thin-film transfer matrix.
9. Generate deterministic artifacts and Markdown reports.
10. Add tests before nonlinear modeling.

Only after that should the project add Meep, hot-electron dynamics, surrogates, or autonomous hypothesis generation.

## Scientific Guardrails

Every result should include:

- Simulator level.
- Input data hashes.
- Code version.
- Material model and fitted parameters.
- Numerical convergence status.
- Energy bookkeeping.
- Calibration domain.
- Holdout comparison when available.
- Known unmodeled artifacts.
- Validity envelope.
- Required follow-up.

No claim should be allowed without these fields.

## What We Can Do Together Before Big Model Updates

With current Codex and current AI tools, we can realistically:

- Build the full V0 digital-twin infrastructure.
- Reproduce basic thin-film spectra from known optical constants.
- Fit Drude/Drude-Lorentz models to ellipsometry-like data.
- Ingest your real sample and laser data when you have it.
- Make reports that compare prediction and measurement.
- Build a careful model-disagreement workflow.
- Build literature memory with citations and provenance.
- Draft bounded research notes that clearly state uncertainty.
- Add Meep validation for selected simple cases.
- Start implementing and testing custom hot-electron material dynamics, but slowly and with published benchmarks.

The best use of our current state is to build the machinery that prevents false discovery. The discovery layer comes later.
