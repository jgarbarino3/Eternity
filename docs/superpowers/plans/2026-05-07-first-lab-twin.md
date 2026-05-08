# First Lab Twin Contracts And Registry Plumbing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the contracts, claim-status labels, registry records, split rules, and validation gates required before Eternity may ingest real or literature data as evidence.

**Architecture:** Keep the existing V0 CLI and synthetic TMM runner, but add a contract layer before scientific expansion. The next slice should validate registry records, raw artifact hashes, calibration/holdout splits, fit/validation plans, and claim status without adding nonlinear physics or claiming real calibration.

**Tech Stack:** Python 3.11, `uv`, Pydantic v2, Pint, PyYAML, NumPy, Pytest, Ruff, existing Typer CLI.

---

## Scope

This plan supersedes the earlier minimal registry-plumbing plan. The current
target is not yet "first calibrated lab twin." The target is:

```text
V1.0 contract-backed synthetic fixture
```

After this plan, Eternity should be able to exercise the same contracts that
real/literature data will use, but the only allowed claim status remains
`synthetic_software_fixture`.

Do not implement:

- nonlinear ENZ dynamics
- hot-electron or two-temperature models
- pump-probe delay scans
- FDTD
- autonomous researcher commands
- novelty or paper claims
- real/literature data ingestion

## Evidence Hierarchy

Every run must carry exactly one claim status:

- `synthetic_software_fixture`: software contract test only.
- `literature_reproduction_fixture`: reproduces a published curve or parameters
  without independent validation.
- `calibration_only_no_holdout`: fit or reproduction exists, but no holdout was
  evaluated.
- `weak_within_dataset_holdout`: held-out wavelength blocks or rows from the
  same raw spectrum.
- `calibrated_linear_evidence`: calibration-only model predicts an independent
  linear observable or measurement.
- `failed_validation`: validation gate failed.

Only `calibrated_linear_evidence` may feed serious-core scientific conclusions.

## File Map

- Create: `docs/contracts/data_registry.md` - human-readable registry contract.
- Create: `docs/contracts/measurement_schema.md` - measurement schema contract.
- Create: `docs/contracts/material_model_schema.md` - material model contract.
- Create: `docs/contracts/calibration_holdout.md` - split and leakage rules.
- Create: `docs/contracts/run_artifact_contract.md` - run directory contract.
- Create: `docs/contracts/claim_status.md` - claim labels and allowed uses.
- Create: `src/eternity/contracts.py` - Pydantic records for V1 contracts.
- Create: `src/eternity/registry.py` - registry loader and validation helpers.
- Create: `src/eternity/artifacts.py` - SHA-256 helpers and artifact records.
- Create: `src/eternity/claim_status.py` - claim status enum and gate helpers.
- Modify: `src/eternity/cli.py` - add `validate-registry` and `hash-artifact`.
- Modify: `src/eternity/runner.py` - write `input_manifest.json`,
  `claim_status.json`, `artifact_hashes.json`, and `validation_gates/*.json`.
- Leave: `src/eternity/simulation.py` - the synthetic V0 simulator keeps its
  current hardcoded media until the registry adds typed sample/stack/media
  records in a later slice.
- Modify: `src/eternity/reporting.py` - render claim status, comparison status,
  gate outcomes, and synthetic-vs-measured status.
- Create: `lab_data/registry.yaml` - tracked synthetic fixture registry.
- Create: `lab_data/raw/synthetic_v0/transmission_fixture.csv` - tiny synthetic
  measurement fixture used only to exercise contracts.
- Modify: `experiments/examples/linear_ito_toy.yaml` - reference registry ids
  and declare claim status.
- Create: `tests/unit/test_contracts.py` - contract validation tests.
- Create: `tests/unit/test_artifacts.py` - hash helper tests.
- Create: `tests/unit/test_registry.py` - registry validation tests.
- Create: `tests/unit/test_claim_status.py` - claim label tests.
- Modify: `tests/integration/test_cli.py` - artifact and gate assertions.

## Task 1: Define Claim Status And Contract Records

**Files:**
- Create: `src/eternity/claim_status.py`
- Create: `src/eternity/contracts.py`
- Create: `tests/unit/test_claim_status.py`
- Create: `tests/unit/test_contracts.py`

- [ ] **Step 1: Write claim-status tests**

Create `tests/unit/test_claim_status.py`:

```python
from eternity.claim_status import ClaimStatus, can_feed_serious_core


def test_only_calibrated_linear_evidence_feeds_serious_core() -> None:
    assert can_feed_serious_core(ClaimStatus.CALIBRATED_LINEAR_EVIDENCE)
    assert not can_feed_serious_core(ClaimStatus.SYNTHETIC_SOFTWARE_FIXTURE)
    assert not can_feed_serious_core(ClaimStatus.LITERATURE_REPRODUCTION_FIXTURE)
    assert not can_feed_serious_core(ClaimStatus.CALIBRATION_ONLY_NO_HOLDOUT)
    assert not can_feed_serious_core(ClaimStatus.WEAK_WITHIN_DATASET_HOLDOUT)
    assert not can_feed_serious_core(ClaimStatus.FAILED_VALIDATION)
```

- [ ] **Step 2: Write contract validation tests**

Create `tests/unit/test_contracts.py`:

```python
import pytest
from pydantic import ValidationError

from eternity.contracts import (
    AxisSpec,
    DataSplitRecord,
    MeasurementRecord,
    QuantityWithUncertainty,
    RawArtifactRecord,
)


def test_raw_artifact_record_requires_sha256_and_source_type() -> None:
    record = RawArtifactRecord(
        raw_artifact_id="synthetic_transmission_csv",
        kind="csv",
        path="lab_data/raw/synthetic_v0/transmission_fixture.csv",
        sha256="a" * 64,
        bytes=100,
        source_type="synthetic",
        immutable=True,
    )

    assert record.sha256 == "a" * 64
    assert record.source_type == "synthetic"


def test_raw_artifact_record_rejects_bad_sha256() -> None:
    with pytest.raises(ValidationError):
        RawArtifactRecord(
            raw_artifact_id="bad",
            kind="csv",
            path="bad.csv",
            sha256="not-a-hash",
            bytes=1,
            source_type="synthetic",
            immutable=True,
        )


def test_measurement_record_requires_geometry_and_uncertainty_label() -> None:
    record = MeasurementRecord(
        measurement_id="synthetic_t_001",
        kind="transmission_spectrum",
        raw_artifact_ref="synthetic_transmission_csv",
        sample_ref="synthetic_ito_001",
        stack_ref="synthetic_air_ito_glass",
        x_axis=AxisSpec(
            quantity="vacuum_wavelength",
            unit="nm",
            values_column="wavelength_nm",
        ),
        y_quantity="transmission",
        y_unit="fraction",
        y_values_column="transmission",
        uncertainty_type="scalar",
        geometry_incidence_angle=QuantityWithUncertainty(value=0, unit="deg"),
        geometry_polarization="TM",
        preprocessing=["synthetic fixture generated from V0 model"],
        forbidden_for_fitting=False,
    )

    assert record.geometry_polarization == "TM"
    assert record.uncertainty_type == "scalar"


def test_split_declares_evidence_strength_and_no_holdout_access() -> None:
    split = DataSplitRecord(
        split_id="synthetic_contract_split",
        raw_data_refs=["synthetic_transmission_csv"],
        created_before_fit=True,
        method="explicit_indices",
        calibration_measurement_refs=["synthetic_t_001"],
        holdout_measurement_refs=[],
        fitting_may_access_holdout_y=False,
        ai_playground_may_access_holdout_y_before_fit=False,
        evidence_strength="synthetic_fixture",
    )

    assert split.created_before_fit
    assert not split.fitting_may_access_holdout_y
```

- [ ] **Step 3: Run tests and confirm failure**

Run:

```bash
uv run --no-editable pytest tests/unit/test_claim_status.py tests/unit/test_contracts.py -q
```

Expected: failure because `eternity.claim_status` and `eternity.contracts` do
not exist.

- [ ] **Step 4: Implement claim status**

Create `src/eternity/claim_status.py`:

```python
"""Claim-status labels for Eternity run outputs."""

from __future__ import annotations

from enum import StrEnum


class ClaimStatus(StrEnum):
    SYNTHETIC_SOFTWARE_FIXTURE = "synthetic_software_fixture"
    LITERATURE_REPRODUCTION_FIXTURE = "literature_reproduction_fixture"
    CALIBRATION_ONLY_NO_HOLDOUT = "calibration_only_no_holdout"
    WEAK_WITHIN_DATASET_HOLDOUT = "weak_within_dataset_holdout"
    CALIBRATED_LINEAR_EVIDENCE = "calibrated_linear_evidence"
    FAILED_VALIDATION = "failed_validation"


def can_feed_serious_core(status: ClaimStatus) -> bool:
    return status is ClaimStatus.CALIBRATED_LINEAR_EVIDENCE
```

- [ ] **Step 5: Implement contract models**

Create `src/eternity/contracts.py`:

```python
"""Typed V1 data contracts for lab-twin inputs and evidence gates."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class QuantityWithUncertainty(BaseModel):
    value: float
    unit: str
    uncertainty: float | None = Field(default=None, ge=0)

    model_config = ConfigDict(extra="forbid")


class AxisSpec(BaseModel):
    quantity: Literal["vacuum_wavelength", "photon_energy", "frequency"]
    unit: str
    values_column: str

    model_config = ConfigDict(extra="forbid")


class RawArtifactRecord(BaseModel):
    raw_artifact_id: str
    kind: Literal["csv", "hdf5", "json", "image_digitization", "vendor_export"]
    path: str
    sha256: str
    bytes: int = Field(gt=0)
    source_type: Literal["lab", "literature_table", "literature_digitized", "synthetic"]
    immutable: bool

    model_config = ConfigDict(extra="forbid")

    @field_validator("sha256")
    @classmethod
    def validate_sha256(cls, value: str) -> str:
        if len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
            raise ValueError("sha256 must be a lowercase 64-character hex digest")
        return value


class MeasurementRecord(BaseModel):
    measurement_id: str
    kind: Literal[
        "transmission_spectrum",
        "reflection_spectrum",
        "ellipsometry_psi_delta",
        "nk_table",
        "epsilon_table",
    ]
    raw_artifact_ref: str
    sample_ref: str
    stack_ref: str
    x_axis: AxisSpec
    y_quantity: str
    y_unit: str
    y_values_column: str
    uncertainty_type: Literal["per_point", "scalar", "unknown"]
    geometry_incidence_angle: QuantityWithUncertainty
    geometry_polarization: Literal["TE", "TM", "unpolarized", "mixed", "unknown"]
    preprocessing: list[str] = Field(default_factory=list)
    forbidden_for_fitting: bool

    model_config = ConfigDict(extra="forbid")


class DataSplitRecord(BaseModel):
    split_id: str
    raw_data_refs: list[str]
    created_before_fit: bool
    method: Literal["explicit_indices", "wavelength_blocks", "measurement_ids", "random_seeded"]
    calibration_measurement_refs: list[str]
    holdout_measurement_refs: list[str]
    fitting_may_access_holdout_y: bool
    ai_playground_may_access_holdout_y_before_fit: bool
    evidence_strength: Literal[
        "independent_measurement",
        "same_raw_spectrum_holdout",
        "literature_reproduction",
        "synthetic_fixture",
    ]

    model_config = ConfigDict(extra="forbid")
```

- [ ] **Step 6: Verify Task 1**

Run:

```bash
uv run --no-editable pytest tests/unit/test_claim_status.py tests/unit/test_contracts.py -q
```

Expected: `5 passed`.

## Task 2: Add Artifact Hashing And Registry Validation

**Files:**
- Create: `src/eternity/artifacts.py`
- Create: `src/eternity/registry.py`
- Create: `lab_data/raw/synthetic_v0/transmission_fixture.csv`
- Create: `lab_data/registry.yaml`
- Create: `tests/unit/test_artifacts.py`
- Create: `tests/unit/test_registry.py`

- [ ] **Step 1: Write artifact hash tests**

Create `tests/unit/test_artifacts.py`:

```python
from pathlib import Path

from eternity.artifacts import sha256_file


def test_sha256_file_is_stable(tmp_path: Path) -> None:
    path = tmp_path / "artifact.txt"
    path.write_text("eternity\n", encoding="utf-8")

    assert sha256_file(path) == "a62b6b005047be416432acf08445606cd803ee0bce5f290b63a011dd9d91c150"
```

- [ ] **Step 2: Write registry tests**

Create `tests/unit/test_registry.py`:

```python
from pathlib import Path

from eternity.registry import load_registry


def test_registry_loads_contract_fixture() -> None:
    registry = load_registry(Path("lab_data/registry.yaml"))

    assert registry.raw_artifacts["synthetic_v0_transmission"].source_type == "synthetic"
    assert registry.measurements["synthetic_v0_transmission_measurement"].kind == (
        "transmission_spectrum"
    )
    assert registry.splits["synthetic_v0_contract_split"].evidence_strength == "synthetic_fixture"
```

- [ ] **Step 3: Run tests and confirm failure**

Run:

```bash
uv run --no-editable pytest tests/unit/test_artifacts.py tests/unit/test_registry.py -q
```

Expected: failure because artifact and registry modules do not exist.

- [ ] **Step 4: Create the synthetic measurement fixture**

Create `lab_data/raw/synthetic_v0/transmission_fixture.csv`:

```csv
wavelength_nm,transmission,uncertainty
1300,0.42,0.02
1400,0.47,0.02
1500,0.51,0.02
1600,0.56,0.02
1700,0.60,0.02
```

This exact fixture has 114 bytes and SHA-256:

```bash
40d8593fb72cf7df1eecccfe87e46d8b5e2f9ced6932ee2efadbae97d02ec2a8
```

- [ ] **Step 5: Implement artifact hashing**

Create `src/eternity/artifacts.py`:

```python
"""Artifact hashing helpers."""

from __future__ import annotations

import hashlib
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
```

- [ ] **Step 6: Create the registry file**

Create `lab_data/registry.yaml`:

```yaml
schema_version: "0.1"

raw_artifacts:
  synthetic_v0_transmission:
    raw_artifact_id: synthetic_v0_transmission
    kind: csv
    path: lab_data/raw/synthetic_v0/transmission_fixture.csv
    sha256: 40d8593fb72cf7df1eecccfe87e46d8b5e2f9ced6932ee2efadbae97d02ec2a8
    bytes: 114
    source_type: synthetic
    immutable: true

measurements:
  synthetic_v0_transmission_measurement:
    measurement_id: synthetic_v0_transmission_measurement
    kind: transmission_spectrum
    raw_artifact_ref: synthetic_v0_transmission
    sample_ref: synthetic_ito_001
    stack_ref: synthetic_air_ito_glass
    x_axis:
      quantity: vacuum_wavelength
      unit: nm
      values_column: wavelength_nm
    y_quantity: transmission
    y_unit: fraction
    y_values_column: transmission
    uncertainty_type: scalar
    geometry_incidence_angle:
      value: 0
      unit: deg
    geometry_polarization: TM
    preprocessing:
      - synthetic fixture generated for V1 contract testing
    forbidden_for_fitting: false

splits:
  synthetic_v0_contract_split:
    split_id: synthetic_v0_contract_split
    raw_data_refs:
      - synthetic_v0_transmission
    created_before_fit: true
    method: explicit_indices
    calibration_measurement_refs:
      - synthetic_v0_transmission_measurement
    holdout_measurement_refs: []
    fitting_may_access_holdout_y: false
    ai_playground_may_access_holdout_y_before_fit: false
    evidence_strength: synthetic_fixture
```

- [ ] **Step 7: Implement registry loader**

Create `src/eternity/registry.py`:

```python
"""Registry loading for lab-twin contracts."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field

from eternity.contracts import DataSplitRecord, MeasurementRecord, RawArtifactRecord


class LabDataRegistry(BaseModel):
    schema_version: Literal["0.1"]
    raw_artifacts: dict[str, RawArtifactRecord] = Field(default_factory=dict)
    measurements: dict[str, MeasurementRecord] = Field(default_factory=dict)
    splits: dict[str, DataSplitRecord] = Field(default_factory=dict)

    model_config = ConfigDict(extra="forbid")


def load_registry(path: Path = Path("lab_data/registry.yaml")) -> LabDataRegistry:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return LabDataRegistry.model_validate(payload)
```

- [ ] **Step 8: Verify Task 2**

Run:

```bash
uv run --no-editable pytest tests/unit/test_artifacts.py tests/unit/test_registry.py -q
```

Expected: `2 passed`.

## Task 3: Add CLI Commands For Registry And Artifact Inspection

**Files:**
- Modify: `src/eternity/cli.py`
- Modify: `tests/integration/test_cli.py`

- [ ] **Step 1: Write CLI tests**

Append to `tests/integration/test_cli.py`:

```python
def test_hash_artifact_command_outputs_digest() -> None:
    result = runner.invoke(
        app,
        ["hash-artifact", "lab_data/raw/synthetic_v0/transmission_fixture.csv"],
    )

    assert result.exit_code == 0, result.output
    assert len(result.output.strip()) == 64


def test_validate_registry_command_accepts_fixture_registry() -> None:
    result = runner.invoke(app, ["validate-registry", "lab_data/registry.yaml"])

    assert result.exit_code == 0, result.output
    assert "valid registry" in result.output
```

- [ ] **Step 2: Run tests and confirm failure**

Run:

```bash
uv run --no-editable pytest tests/integration/test_cli.py::test_hash_artifact_command_outputs_digest tests/integration/test_cli.py::test_validate_registry_command_accepts_fixture_registry -q
```

Expected: failure because the commands do not exist.

- [ ] **Step 3: Implement CLI commands**

Add imports to `src/eternity/cli.py`:

```python
from eternity.artifacts import sha256_file
from eternity.registry import load_registry
```

Add commands:

```python
@app.command("hash-artifact")
def hash_artifact(path: Path) -> None:
    """Print the SHA-256 digest for an artifact."""

    if not path.exists():
        typer.echo(f"Artifact not found: {path}", err=True)
        raise typer.Exit(1)
    typer.echo(sha256_file(path))


@app.command("validate-registry")
def validate_registry(path: Path) -> None:
    """Validate the lab-data registry."""

    try:
        registry = load_registry(path)
    except FileNotFoundError:
        typer.echo(f"Registry not found: {path}", err=True)
        raise typer.Exit(1) from None
    except ValidationError as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(1) from error

    typer.echo(
        "valid registry: "
        f"{len(registry.raw_artifacts)} artifacts, "
        f"{len(registry.measurements)} measurements, "
        f"{len(registry.splits)} splits"
    )
```

- [ ] **Step 4: Verify Task 3**

Run:

```bash
uv run --no-editable pytest tests/integration/test_cli.py::test_hash_artifact_command_outputs_digest tests/integration/test_cli.py::test_validate_registry_command_accepts_fixture_registry -q
```

Expected: `2 passed`.

## Task 4: Emit Claim Status And Gate Artifacts For V0 Runs

**Files:**
- Modify: `src/eternity/runner.py`
- Modify: `src/eternity/reporting.py`
- Modify: `tests/integration/test_cli.py`

- [ ] **Step 1: Write artifact assertions**

Append to `tests/integration/test_cli.py`:

```python
def test_run_writes_claim_status_and_gate_artifacts() -> None:
    result = runner.invoke(app, ["run", "experiments/examples/linear_ito_toy.yaml"])
    assert result.exit_code == 0, result.output
    run_dir = Path(result.output.strip().splitlines()[-1])

    assert (run_dir / "input_manifest.json").exists()
    assert (run_dir / "claim_status.json").exists()
    assert (run_dir / "artifact_hashes.json").exists()
    assert (run_dir / "validation_gates" / "input_integrity.json").exists()
    assert (run_dir / "validation_gates" / "split_integrity.json").exists()

    report = (run_dir / "report.md").read_text()
    assert "## Claim Status" in report
    assert "synthetic_software_fixture" in report
```

- [ ] **Step 2: Run test and confirm failure**

Run:

```bash
uv run --no-editable pytest tests/integration/test_cli.py::test_run_writes_claim_status_and_gate_artifacts -q
```

Expected: failure because these artifacts do not exist.

- [ ] **Step 3: Add V0 claim and gate writes**

In `src/eternity/runner.py`, import:

```python
from eternity.claim_status import ClaimStatus
```

After existing artifact writes, add:

```python
    gates_dir = run_dir / "validation_gates"
    gates_dir.mkdir(exist_ok=True)
    write_json(
        run_dir / "input_manifest.json",
        {
            "claim_scope": "synthetic V0 run",
            "source_type": "synthetic",
            "measurements": [],
            "registry_snapshot_sha256": None,
        },
    )
    write_json(
        run_dir / "claim_status.json",
        {
            "status": ClaimStatus.SYNTHETIC_SOFTWARE_FIXTURE.value,
            "can_feed_serious_core": False,
            "reason": "Synthetic fixture only; no measured or holdout data were used.",
        },
    )
    write_json(
        gates_dir / "input_integrity.json",
        {"status": "pass", "scope": "synthetic inline V0 inputs"},
    )
    write_json(
        gates_dir / "split_integrity.json",
        {"status": "not_applicable", "reason": "No calibration or holdout split in V0."},
    )
```

Build `artifact_hashes.json` after all artifacts are written:

```python
    artifact_hashes = {}
    for artifact_path in sorted(run_dir.rglob("*")):
        if artifact_path.is_file() and artifact_path.name != "artifact_hashes.json":
            artifact_hashes[str(artifact_path.relative_to(run_dir))] = sha256_file(artifact_path)
    write_json(run_dir / "artifact_hashes.json", artifact_hashes)
```

This needs:

```python
from eternity.artifacts import sha256_file
```

- [ ] **Step 4: Render claim status in the report**

In `src/eternity/reporting.py`, add a section:

```markdown
## Claim Status

`synthetic_software_fixture`

This run cannot feed serious-core conclusions because it uses synthetic inputs
and no measured comparison or holdout data.
```

- [ ] **Step 5: Verify Task 4**

Run:

```bash
uv run --no-editable pytest tests/integration/test_cli.py::test_run_writes_claim_status_and_gate_artifacts -q
```

Expected: `1 passed`.

## Task 5: Add Human-Readable Contract Docs

**Files:**
- Create: `docs/contracts/data_registry.md`
- Create: `docs/contracts/measurement_schema.md`
- Create: `docs/contracts/material_model_schema.md`
- Create: `docs/contracts/calibration_holdout.md`
- Create: `docs/contracts/run_artifact_contract.md`
- Create: `docs/contracts/claim_status.md`

- [ ] **Step 1: Create `docs/contracts/claim_status.md`**

```markdown
# Claim Status Contract

Every Eternity run must emit `claim_status.json` and render the same status in
`report.md`.

Allowed statuses:

- `synthetic_software_fixture`
- `literature_reproduction_fixture`
- `calibration_only_no_holdout`
- `weak_within_dataset_holdout`
- `calibrated_linear_evidence`
- `failed_validation`

Only `calibrated_linear_evidence` may feed serious-core scientific conclusions.
All other statuses may be used for software testing, reproduction, planning, or
researcher-playground critique only.
```

- [ ] **Step 2: Create `docs/contracts/calibration_holdout.md`**

```markdown
# Calibration And Holdout Contract

Calibration and holdout splits are explicit records, not conventions.

A split must be created and hashed before fitting. Fitting code may receive only
calibration views. Holdout measurements and holdout y-values must not appear in
fit inputs or AI researcher-playground prompts before the model is frozen.

Validation must fail if any holdout measurement or index hash appears in
`fit_result.used_data`.
```

- [ ] **Step 3: Create `docs/contracts/run_artifact_contract.md`**

```markdown
# Run Artifact Contract

V1 runs must include the V0 artifacts plus:

- `input_manifest.json`
- `registry_snapshot.json`
- `registry_snapshot.sha256`
- `raw_artifacts.json`
- `data_splits.json`
- `material_model.json`
- `fit_plan.json`
- `fit_result.json`
- `fit_diagnostics.json`
- `prediction_table.csv`
- `comparison_table.csv`
- `holdout_residuals.csv`
- `validation_gates/*.json`
- `claim_status.json`
- `assumptions.json`
- `validity_envelope.json`
- `artifact_hashes.json`
- `environment.json`

The manifest must record artifact hashes, semantic artifact kinds, and whether
each artifact comes from calibration, holdout, or neither.
```

- [ ] **Step 4: Create the remaining contract docs**

Create `docs/contracts/data_registry.md`:

```markdown
# Data Registry Contract

The lab-data registry is the canonical map from ids to immutable raw artifacts,
samples, stacks, media, measurements, material models, data splits, calibration
plans, and validation plans.

Real or literature data must not enter through loose paths. Every raw artifact
requires a SHA-256 digest, source label, byte size, and immutable path.
```

Create `docs/contracts/measurement_schema.md`:

```markdown
# Measurement Schema Contract

Measurements must declare raw artifact reference, sample, stack, axis quantity,
axis unit, y quantity, y unit, uncertainty type, incidence angle, polarization,
instrument or source notes, preprocessing, and whether the data are forbidden
for fitting.

Ellipsometry records should store measured psi and delta separately from any
derived `n,k`.
```

Create `docs/contracts/material_model_schema.md`:

```markdown
# Material Model Schema Contract

Material models must declare sample id, model kind, equation convention,
parameters, uncertainty where available, fit provenance, validity envelope, and
source type.

Passive linear models must declare sign convention and passivity checks. ENZ
wavelength definitions must be explicit.
```

- [ ] **Step 5: Verify contract docs exist**

Run:

```bash
test -f docs/contracts/data_registry.md
test -f docs/contracts/measurement_schema.md
test -f docs/contracts/material_model_schema.md
test -f docs/contracts/calibration_holdout.md
test -f docs/contracts/run_artifact_contract.md
test -f docs/contracts/claim_status.md
```

Expected: all commands exit `0`.

## Task 6: Full Verification

**Files:**
- Read: `GOALS.md`
- Read: `docs/pro_checkpoints/2026-05-07-v0-to-v1.md`
- Read: `docs/superpowers/plans/2026-05-07-first-lab-twin.md`
- Read: generated `results/runs/run_47d4e2d9baa7f574/report.md`

- [ ] **Step 1: Run the full suite**

Run:

```bash
uv run --no-editable pytest
uv run --no-editable ruff check .
uv run --no-editable eternity validate experiments/examples/linear_ito_toy.yaml
uv run --no-editable eternity run experiments/examples/linear_ito_toy.yaml
```

Expected:

```text
All tests pass.
All checks passed!
valid: linear_ito_toy_001
run complete
results/runs/run_47d4e2d9baa7f574
```

- [ ] **Step 2: Inspect required V0.1 artifacts**

Confirm the generated run directory includes:

- `input_manifest.json`
- `claim_status.json`
- `artifact_hashes.json`
- `validation_gates/input_integrity.json`
- `validation_gates/split_integrity.json`
- `report.md` with `synthetic_software_fixture`

- [ ] **Step 3: Confirm no overclaiming**

Search:

```bash
rg -n "calibrated_linear_evidence|new physics|novel" results/runs/run_47d4e2d9baa7f574 GOALS.md docs
```

Expected: `calibrated_linear_evidence` may appear only in contracts/goals as a
future gated label. Generated synthetic V0 reports must not claim calibrated
linear evidence, new physics, or novelty.

- [ ] **Step 4: Confirm git scope**

Run:

```bash
git diff --stat
git status --short
```

Expected: source, tests, and docs changes match this plan. The zip handoff
artifact may remain untracked for user upload, but it should not be committed
unless explicitly requested.
