# Eternity Day 1 Technical Foundation Plan

## Goal

Build a small, reproducible Python research codebase for the first Eternity target:
linear and early calibrated ENZ thin-film experiments, with structured specs,
traceable data, repeatable runs, queryable results, and generated reports.

This should support one researcher plus Codex. It should not become a platform,
workflow engine, autonomous agent stack, or full FDTD environment in month one.

## Recommended Day 1 Defaults

- Package name: `eternity`
- Python: develop on Python 3.12 initially; revisit after solver dependencies
  such as Meep and compiled scientific libraries are confirmed on newer Python.
- Environment/tooling: `uv` for dependency management and lockfile, Hatchling as
  a simple build backend, Ruff for lint/format, Pytest for tests.
- Config/spec format: YAML files validated by Pydantic models. Pydantic should
  generate JSON Schema for editor validation and future tool use.
- Units: store units explicitly in specs and parse them through Pint at the
  boundary. Internals should convert to canonical SI or optics-specific units.
- Data: keep raw data immutable and content-addressed by SHA-256. Use a simple
  manifest on day one; add DVC when real data files become too large or need a
  remote.
- Results: SQLite database for run metadata plus file artifacts under
  `results/runs/<run_id>/`. Use DuckDB for analytics over Parquet/CSV/Zarr
  artifacts, not as the only system of record.
- Reports: generate deterministic Markdown reports first. Add Quarto when
  executable reports, HTML/PDF publishing, or parameterized reporting matters.

## Proposed Repository Structure

```text
Eternity/
  DAY_1_FUTURE_ROADMAP.md
  DAY_1_TECHNICAL_FOUNDATION_PLAN.md
  README.md
  pyproject.toml
  uv.lock
  .python-version
  .gitignore

  docs/
    architecture.md
    data_contract.md
    experiment_spec.md
    reproducibility.md

  experiments/
    specs/
      linear_ito_tmm_smoke.yaml
    schemas/
      experiment.schema.json

  data/                         # gitignored except README/manifest pointers
    README.md
    registry.yaml
    raw/
    interim/
    processed/
    external/

  results/                      # gitignored except README
    eternity.sqlite
    runs/

  reports/                      # generated; usually gitignored

  src/
    eternity/
      __init__.py
      cli.py

      schemas/
        experiment.py
        data_registry.py
        result.py

      core/
        ids.py
        hashing.py
        provenance.py
        units.py

      data/
        registry.py
        loaders.py
        tabular.py
        arrays.py

      physics/
        materials/
          drude.py
          drude_lorentz.py
        optics/
          transfer_matrix.py
        pulses/
          gaussian.py
          measured.py

      fitting/
        ellipsometry.py
        transmission.py

      simulations/
        base.py
        linear_tmm.py

      runs/
        execute.py
        database.py
        artifacts.py

      reporting/
        plots.py
        markdown.py

  tests/
    unit/
    integration/
    regression/
    fixtures/
      specs/
      data/
```

Keep this modular, but do not create empty packages just to anticipate the whole
roadmap. The first implemented vertical slice should be:

```text
YAML spec -> validated ExperimentSpec -> load tiny fixture data ->
run linear transfer-matrix simulation -> write results DB row + artifacts ->
generate Markdown report -> tests pass
```

## Prioritized Plan

### P0 - Day 1: Create The Reproducible Skeleton

1. Initialize the package with `src/` layout, `pyproject.toml`, `uv.lock`,
   `.python-version`, Ruff, Pytest, and a Typer CLI.
2. Add a minimal `ExperimentSpec` Pydantic schema with fields for:
   `schema_version`, `experiment_id`, `question`, `hypothesis`, `sample`,
   `input_pulse`, `geometry`, `simulator`, `observables`, `baselines`,
   `acceptance_tests`, and `validity_envelope`.
3. Add `QuantitySpec` for all physical values:
   `{value: 1550, unit: "nm"}` for scalars and
   `{values: [0, 30, 45], unit: "deg"}` for sweeps.
4. Add `data/registry.yaml` with a tiny synthetic fixture dataset and a rule:
   raw data is append-only and referenced by SHA-256.
5. Add run provenance collection:
   git commit if available, dirty state, Python version, OS, dependency lock
   hash, spec hash, input data hashes, random seed, command args, start/end
   times.
6. Add an `eternity validate experiments/specs/...yaml` command.
7. Add an `eternity run experiments/specs/...yaml` command that creates:
   `results/runs/<run_id>/resolved_spec.json`,
   `results/runs/<run_id>/provenance.json`,
   `results/runs/<run_id>/metrics.json`,
   and a row in `results/eternity.sqlite`.
8. Add tests for spec validation, unit parsing, hashing determinism, and run
   directory creation.

Day 1 success condition: a clean repo can run one validated synthetic experiment
and reproduce the same run hash from the same spec and fixture inputs.

### P1 - First Week: First Scientific Vertical Slice

1. Implement Drude and Drude-Lorentz material models with tested units and
   numerical behavior.
2. Implement a linear transfer-matrix simulation for a single thin film.
   Either wrap `tmm` for correctness speed or keep a small local implementation
   with cross-check tests against `tmm`.
3. Add Gaussian, chirped Gaussian, and measured-spectrum pulse loaders, but keep
   the first simulation linear and simple.
4. Store tabular outputs as Parquet where useful and small scalar metrics in
   SQLite.
5. Generate a Markdown report with:
   resolved spec summary, input hashes, material parameters, plots, metrics,
   warnings, validity envelope, and acceptance-test outcomes.
6. Add regression fixtures:
   low-loss limit, energy bookkeeping, deterministic output, and at least one
   known thin-film comparison.
7. Add a minimal CI workflow after the repo is under git:
   Ruff check, Ruff format check, Pytest, and schema generation check.

First-week success condition: Eternity can run a transparent V0 linear digital
twin smoke case and produce a report that explains what was assumed and what is
not trusted.

### P2 - Weeks 2-3: Real Data And Calibration

1. Import one real lab export path at a time:
   ellipsometry first, then transmission/reflection, then pump-probe delay data.
2. Adopt `xarray` for labeled spectra/delay/angle datasets and write NetCDF or
   Zarr only when the data becomes genuinely multidimensional.
3. Add `lmfit` or SciPy least-squares fitting for Drude-Lorentz parameters.
4. Store fit outputs with parameter covariance, residuals, data split, and
   fit warnings.
5. Add `CalibrationSpec` or extend `ExperimentSpec` with an explicit
   calibration/holdout split.
6. Add comparison reports:
   predicted vs measured spectra, residual plots, parameter table, acceptance
   tests, and failure notes.
7. Add DVC with a local external-drive or cloud remote if real raw data should
   not live inside Git.

Weeks 2-3 success condition: one measured sample can be fitted, reproduced, and
compared against a holdout or at least a separately identified validation trace.

### P3 - Week 4: Harden Reproducibility And Prepare Solver Expansion

1. Freeze a first schema version: `ExperimentSpec v0.1`.
2. Add schema migrations only if a real breaking change appears. Do not build a
   migration framework early.
3. Add a simulator plugin boundary:
   all simulators return the same `SimulationResult` contract with metrics,
   artifacts, warnings, validity envelope, and acceptance-test results.
4. Add stubs, not full integrations, for future solvers:
   `maxwell_1d_drude_hot_electron`, `meep_fdtd_validation`,
   and `surrogate_model`.
5. Add a lightweight result-inspection command:
   `eternity runs list`, `eternity runs show <run_id>`,
   `eternity runs compare <run_a> <run_b>`.
6. Add `CITATION.cff` and a software/data citation note once external research
   results depend on the code.
7. Decide whether `signac`, MLflow, or a custom SQLite/result-artifact model is
   still the right tracking layer after real sweeps exist.

First-month success condition: the project has one trustworthy, reproducible
scientific path from structured hypothesis to validated report, and the next
solver can be added without rewriting data, specs, or run provenance.

## Results Database

Use SQLite as the authoritative run ledger:

```text
runs
  run_id text primary key
  experiment_id text
  schema_version text
  status text
  started_at text
  finished_at text
  git_commit text
  git_dirty boolean
  python_version text
  platform text
  spec_hash text
  lock_hash text
  result_dir text
  notes text

artifacts
  artifact_id text primary key
  run_id text
  kind text                 # spec, provenance, metric, plot, table, array, log
  path text
  sha256 text
  media_type text

input_data
  input_id text primary key
  run_id text
  registry_id text
  path text
  sha256 text
  role text                 # ellipsometry, pulse, measured_spectrum, holdout

metrics
  run_id text
  name text
  value real
  unit text
  uncertainty real
  step integer nullable

warnings
  run_id text
  severity text
  source text
  message text
```

Store bulky arrays and plots as artifacts. Store searchable scalars and hashes
in SQLite. Use DuckDB for ad hoc analysis across Parquet/CSV artifacts.

## Experiment Spec Rules

- Specs are declarative. They should not contain Python expressions.
- Specs include units on every physical value.
- Specs reference data by registry id and hash, not just by a loose filename.
- Specs separate assumptions from fitted parameters.
- Specs state the validity envelope before the run.
- The runner writes a resolved spec that expands defaults and records all
  resolved paths/hashes.
- Any AI-generated spec must pass validation before execution.

Minimal skeleton:

```yaml
schema_version: "0.1"
experiment_id: linear_ito_tmm_smoke_001
question: "Can the linear TMM baseline reproduce a synthetic ITO film spectrum?"
hypothesis: "The low-fluence linear response is explained by the fitted dielectric function and film thickness."

sample:
  sample_id: synthetic_ito_001
  material: ITO
  thickness: {value: 60, unit: "nm"}
  material_model:
    type: drude_lorentz
    parameters_ref: synthetic_drude_lorentz_001

input_pulse:
  kind: measured_spectrum
  data_ref: synthetic_pulse_spectrum_001
  center_wavelength: {value: 1550, unit: "nm"}

geometry:
  incidence_angle: {value: 0, unit: "deg"}
  polarization: TM

simulator:
  name: linear_transfer_matrix
  version: "0.1"

observables:
  - transmission_spectrum
  - reflection_spectrum
  - absorption

baselines:
  - lossless_limit

acceptance_tests:
  - energy_accounting
  - deterministic_replay

validity_envelope:
  wavelength: {min: 1300, max: 1700, unit: "nm"}
  fluence: {min: 0, max: 0.01, unit: "mJ/cm^2"}
  trusted_notes:
    - "Linear low-fluence baseline only."
  untrusted_notes:
    - "No pump-induced material dynamics."
    - "No roughness or detector response."
```

## Reproducibility Contract

Every run directory should contain:

```text
resolved_spec.json
provenance.json
data_manifest.json
metrics.json
warnings.json
stdout.log
artifacts/
  plots/
  tables/
  arrays/
report.md
```

The report should be regenerable from `resolved_spec.json`, `provenance.json`,
the results database row, and the recorded artifacts. If that is not true, the
report is a notebook snapshot, not a reproducible research result.

## Useful Libraries And Repositories

Core Python foundation:

- Scientific Python Development Guide:
  https://learn.scientific-python.org/development/guides/packaging-simple/
- Scientific Python SPEC 0:
  https://scientific-python.org/specs/spec-0000/
- PyPA packaging guide:
  https://packaging.python.org/
- uv:
  https://docs.astral.sh/uv/
- Ruff:
  https://docs.astral.sh/ruff/
- Pytest:
  https://docs.pytest.org/
- Typer:
  https://typer.tiangolo.com/
- Pydantic:
  https://docs.pydantic.dev/
- SQLModel:
  https://sqlmodel.tiangolo.com/

Scientific/data stack:

- NumPy:
  https://numpy.org/
- SciPy:
  https://scipy.org/
- xarray:
  https://docs.xarray.dev/
- Zarr:
  https://zarr.readthedocs.io/
- Pint:
  https://pint.readthedocs.io/
- DuckDB Python:
  https://duckdb.org/docs/stable/clients/python/overview
- DVC:
  https://dvc.org/doc/start
- DataLad:
  https://www.datalad.org/

Optics and fitting candidates:

- tmm:
  https://github.com/sbyrnes321/tmm
- TMM-Fast:
  https://arxiv.org/abs/2111.13667
- pyElli:
  https://pypi.org/project/pyelli/
- lmfit:
  https://lmfit.github.io/lmfit-py/
- Meep:
  https://meep.readthedocs.io/
- Meep material modeling:
  https://meep.readthedocs.io/en/latest/Materials/
- gnlse-python:
  https://gnlse.readthedocs.io/

Experiment tracking and reports:

- signac:
  https://signac-docs.readthedocs.io/
- Sacred:
  https://sacred.readthedocs.io/
- MLflow Tracking:
  https://www.mlflow.org/docs/latest/ml/tracking
- Quarto Python:
  https://quarto.org/docs/computations/python.html
- Papermill:
  https://papermill.readthedocs.io/
- nbmake:
  https://github.com/treebeardtech/nbmake

Reproducible research references:

- Good Enough Practices in Scientific Computing:
  https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005510
- Ten Simple Rules for Reproducible Computational Research:
  https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003285
- FAIR Guiding Principles:
  https://www.nature.com/articles/sdata201618
- Software Citation Principles:
  https://force11.org/info/software-citation-principles-published-2016/

## Key Risks

1. Overbuilding infrastructure before the first validated optical result.
   Mitigation: build one vertical slice first and only add tools when the slice
   becomes painful.
2. Raw data mutation or path-only data references.
   Mitigation: immutable raw data, SHA-256 hashes, registry ids, and recorded
   input manifests for every run.
3. Unit mistakes.
   Mitigation: unit-bearing schemas at boundaries and canonical internal units.
4. Specs becoming prose with YAML syntax.
   Mitigation: strict Pydantic validation, generated JSON Schema, and no Python
   expressions in specs.
5. Database/artifact drift.
   Mitigation: every DB artifact row includes a path and hash; reports are
   generated from resolved artifacts, not manual notebook state.
6. Notebook logic becoming the true codebase.
   Mitigation: notebooks and reports call package APIs; tested logic lives under
   `src/eternity/`.
7. FDTD dependency and installation drag.
   Mitigation: keep Meep behind a future simulator adapter; do not make it a day
   one dependency.
8. False physical confidence.
   Mitigation: every result has warnings, acceptance tests, and a validity
   envelope. Low-fidelity and high-fidelity models should be compared explicitly.
9. AI-generated experiments producing plausible but invalid specs.
   Mitigation: AI can draft specs, but validated schemas and human review gates
   control execution.
10. Too many experiment tracking tools.
    Mitigation: start with SQLite plus artifacts. Re-evaluate signac/MLflow only
    after real parameter sweeps exist.
