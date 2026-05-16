# Phase 3A.6 CompleteEASE Re-export / Measurement Packet Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]` / `- [x]`) syntax for tracking.

**Goal:** Build the exact source-evidence packet needed to either recover/export absolute RC2 reflectance for thesis `d_10nm` / `3L2`, or keep Phase 3A permanently relative-only until new evidence appears.

**Architecture:** This is a documentation-and-contract phase, not a data-promotion phase. The implementation should create a packet template, machine-readable acceptance policy, and optional intake path for future files while leaving all current runs capped below `calibrated_linear_evidence`.

**Tech Stack:** Markdown policy docs, YAML decision schema, existing Eternity registry/validation commands, local shell tools (`shasum`, `pdftotext`, `strings`), GPD mirror docs, optional Consensus MCP for literature context before threshold policy.

---

## Phase Contract

Phase ID: `Phase 3A.6`

Phase name: `CompleteEASE Re-export / Measurement Packet`

Phase status while this plan is executed: `active/planning`.

Authoritative claim boundary:

- Do not promote `run_f35a15cef565fb15`.
- Do not change `claim_status.json` semantics.
- Do not treat `Intensity` as absolute `%R` unless the packet includes source-backed proof of channel, units, calibration state, angle, polarization, sample identity, and export provenance.
- Do not set numeric pass/fail residual thresholds from already-inspected residuals.
- Do allow a future run to be prepared once evidence and thresholds are approved before that future run.

## Files

- Create: `docs/phase3a6_completeease_reexport_packet.md` - human-facing packet to send to an experimentalist or use during local re-export.
- Create: `docs/phase3a6_acceptance_policy.yaml` - machine-readable decision fields and current blocked/default values.
- Modify: `docs/phase3a1_threshold_policy.yaml` - reference the Phase 3A.6 packet/policy as future-only evidence, without approving thresholds.
- Modify: `docs/phase_index.md` - mark Phase 3A.6 active/planning and keep Phase 3A.5 completed/blocked.
- Modify: `CURRENT_REALISTIC_ROADMAP.md` and `GOALS.md` - record the Phase 3A.6 planning route and unresolved blockers.
- Modify: `docs/PROJECT_ATLAS.md` and `docs/project_atlas/index.html` - show Phase 3A.6 as the active planning phase and preserve the conflict board.
- Modify: `GPD/ROADMAP.md`, `GPD/STATE.md`, and `GPD/state.json` - mirror the plan with Eternity docs remaining authoritative.

## Task 1: Create The Human Re-export Packet

**Files:**

- Create: `docs/phase3a6_completeease_reexport_packet.md`

- [x] **Step 1: Add the packet header and decision boundary**

Create `docs/phase3a6_completeease_reexport_packet.md` with:

```markdown
# Phase 3A.6 CompleteEASE Re-export / Measurement Packet

Date: 2026-05-16

## Purpose

This packet defines the minimum source evidence needed to use thesis
`d_10nm` / `3L2` RC2 traces as absolute reflectance in a future Eternity
validation run.

Current decision before this packet is satisfied:

- normalization basis: `relative_intensity_only`;
- claim ceiling: `weak_within_dataset_holdout`;
- existing run `run_f35a15cef565fb15`: historical only;
- calibrated promotion: blocked.

This packet is not approval to promote any existing run. It is a checklist for
future source recovery, re-export, or re-measurement.
```

- [x] **Step 2: Add the required sample identity section**

Append:

```markdown
## Required Sample Identity

The source record must identify the sample without relying on filename
guesswork.

Required fields:

- sample label: `3L2` or explicitly mapped equivalent;
- substrate: `Quartz`;
- incident-order stack: `air / 20 nm TiN / 10 nm SiO2 / 30 nm TiN / quartz`;
- thesis table or lab-note reference tying the label to the stack;
- whether the record refers to `d_10nm_initial`, `d_10nm_12V`, both, or a new
  measurement.

Acceptance rule:

- Pass only if the sample label and stack are explicit in the source record or
  in an attached source note with path/hash.
- Fail if the only link is a filename such as `30_20_10`.
```

- [x] **Step 3: Add the required acquisition geometry section**

Append:

```markdown
## Required Acquisition Geometry

Required fields:

- instrument: J.A. Woollam RC2 or equivalent source;
- software/source environment: CompleteEASE, Woollam project, exported table,
  debug bundle, lab note, or new measurement note;
- angle of incidence: `60 deg`;
- polarization: `S`, `TE`, or source-backed equivalent;
- wavelength grid and units;
- acquisition mode: static spectrum, in-situ dynamic trace, or both;
- bias state: initial/no-bias, `12 V`, or explicit new condition.

Acceptance rule:

- Pass only if angle and polarization are source-backed.
- Fail if angle or polarization is inferred only from neighboring thesis text.
```

- [x] **Step 4: Add the required normalization/calibration section**

Append:

```markdown
## Required Normalization And Units

Required fields:

- exported channel name exactly as shown by the source system;
- exported units exactly as shown by the source system;
- whether values are absolute reflectance fraction, percent reflectance, raw
  detector intensity, normalized intensity, or arbitrary-unit intensity;
- calibration/baseline state used by the RC2/CompleteEASE workflow;
- any reference scan, baseline, mirror, dark correction, or sample alignment
  procedure needed to interpret the exported values;
- whether the exported table is directly comparable to TMM reflectance.

Acceptance rule for absolute reflectance:

- Pass only if the source says the exported values are absolute reflectance or
  gives enough calibration/baseline metadata to justify direct comparison to
  TMM reflectance.
- Fail if the source only says `Intensity`, `p-Intensity`, `s-Intensity`, or
  reflective intensity without units/calibration state.
```

- [x] **Step 5: Add the required artifact provenance section**

Append:

```markdown
## Required Artifact Provenance

For every recovered or newly produced file, record:

- original absolute path;
- copied immutable raw path, if copied into `lab_data/raw`;
- SHA-256 hash;
- byte count;
- export timestamp or measurement date, if available;
- operator/source note;
- relation to existing artifacts:
  - `thesis_reflectance_d_10nm_initial`;
  - `thesis_reflectance_d_10nm_12V`;
  - `phase3a_30_20_10_candidate`;
  - new artifact ID.

Acceptance rule:

- Pass only if the source file identity can be frozen with hash and path.
- Fail if the source is only a screenshot or plot unless it is explicitly
  registered as `digitized_from_plot` and kept out of absolute-calibrated
  promotion.
```

- [x] **Step 6: Add the decision outcomes section**

Append:

```markdown
## Decision Outcomes

Allowed outcomes:

- `absolute_reflectance_evidence_found`: a future absolute-reflectance run may
  be prepared after thresholds are approved before the run.
- `relative_intensity_policy_only`: source evidence supports relative/shape
  diagnostics but not absolute reflectance.
- `blocked_needs_new_export`: no source-backed interpretation exists; request a
  new export or measurement.
- `new_measurement_required`: source data cannot be trusted or recovered.

No outcome from this packet may retroactively promote
`run_f35a15cef565fb15`.
```

- [x] **Step 7: Add the requester checklist**

Append:

```markdown
## Request To Experimentalist Or Future Self

Please provide one of:

1. The original CompleteEASE/Woollam project or snapshot for the `3L2` / `d_10nm`
   spectra.
2. A fresh CompleteEASE export of S-polarized 60-degree reflectance for the
   `3L2` / 10 nm SiO2 sample, with channel name and units visible.
3. A lab note or export recipe stating how the existing `Intensity` column was
   produced and whether it is absolute reflectance, normalized reflectance, or
   raw/relative intensity.
4. A new measured reflectance table with incident/reference measurement notes.

Required accompanying note:

```text
Sample:
Stack:
Substrate:
Instrument/software:
Measurement date:
Operator:
Angle:
Polarization:
Bias state:
Channel name:
Units:
Calibration/baseline procedure:
Does this table represent absolute reflectance directly comparable to TMM?:
Original file path:
Any export settings:
```
```

## Task 2: Create The Machine-Readable Acceptance Policy

**Files:**

- Create: `docs/phase3a6_acceptance_policy.yaml`
- Modify: `docs/phase3a1_threshold_policy.yaml`

- [x] **Step 1: Add the default blocked policy**

Create `docs/phase3a6_acceptance_policy.yaml` with:

```yaml
phase_id: Phase 3A.6
status: active_planning
decision: blocked_needs_new_export
applies_to_existing_run: false
existing_run_refs:
  - results/runs/run_f35a15cef565fb15
current_normalization_basis: relative_intensity_only
future_absolute_reflectance_allowed: false
future_threshold_policy_allowed: false
required_evidence_fields:
  sample_identity:
    - sample_label
    - substrate
    - incident_order_stack
    - stack_source_ref
  acquisition_geometry:
    - instrument
    - software_or_source_environment
    - incidence_angle_deg
    - polarization
    - wavelength_units
    - bias_state
  normalization:
    - exported_channel_name
    - exported_units
    - calibration_or_baseline_state
    - direct_tmm_comparability_statement
  provenance:
    - original_absolute_path
    - sha256
    - byte_count
    - source_note
acceptance_rules:
  absolute_reflectance_evidence_found:
    requires_source_backed_units: true
    requires_calibration_state: true
    may_apply_to_existing_run: false
    next_required_phase: Phase 3A.7
  relative_intensity_policy_only:
    may_promote_calibrated_linear_evidence: false
    allowed_use: shape_or_provenance_diagnostic
  blocked_needs_new_export:
    allowed_use: provenance_only
    next_required_action: recover_project_or_reexport
  new_measurement_required:
    allowed_use: none_for_calibrated_validation
prohibited_actions:
  - promote_run_f35a15cef565fb15
  - set_thresholds_from_inspected_residuals
  - treat_intensity_header_as_absolute_reflectance_without_source_proof
```

- [x] **Step 2: Link Phase 3A.6 policy from Phase 3A.1**

Modify `docs/phase3a1_threshold_policy.yaml` so `normalization_evidence_refs`
contains:

```yaml
- docs/phase3a6_completeease_reexport_packet.md
- docs/phase3a6_acceptance_policy.yaml
```

Do not change:

```yaml
status: blocked_pending_pro_checkpoint
thresholds_ref: null
approver: null
approved_at: null
applies_to_existing_run: false
policy_may_promote_calibrated_evidence: false
```

## Task 3: Sync Roadmap, Atlas, And GPD Mirror

**Files:**

- Modify: `CURRENT_REALISTIC_ROADMAP.md`
- Modify: `GOALS.md`
- Modify: `docs/phase_index.md`
- Modify: `docs/PROJECT_ATLAS.md`
- Modify: `docs/project_atlas/index.html`
- Modify: `GPD/ROADMAP.md`
- Modify: `GPD/STATE.md`
- Modify: `GPD/state.json`

- [x] **Step 1: Mark Phase 3A.6 active/planning**

Update `docs/phase_index.md` so the Phase 3A.6 row status is:

```text
Active/planning
```

Update the active recommendation to:

```text
Current phase: Phase 3A.6 - CompleteEASE re-export / measurement packet.
```

- [x] **Step 2: Preserve the skipped blockers**

Ensure every updated roadmap surface still lists:

```text
TiON_48/TiON_49 raw R/T remain missing.
30_20_10 filename-to-thesis provenance remains unresolved.
Phase 3A absolute normalization remains unresolved until source-backed evidence appears.
No already-inspected run may be promoted.
```

- [x] **Step 3: Update the atlas conflict board**

Update atlas text so it says Phase 3A.6 is active and its current work is:

```text
Prepare the exact re-export/measurement packet. The conflict is not whether
the spectra are useful; the conflict is whether their exported units and
calibration state support absolute reflectance.
```

- [x] **Step 4: Update GPD mirror without changing authority**

Update `GPD/state.json` with:

```json
{
  "current_phase": "3A.6",
  "current_phase_name": "CompleteEASE Re-export / Measurement Packet",
  "last_activity_desc": "Planning the source-evidence packet required before any future absolute-reflectance Phase 3A run."
}
```

Keep the GPD contract language that Eternity docs and claim-status code are
authoritative.

## Task 4: Verification And Commit

**Files:**

- No new source files beyond docs/policy files.

- [x] **Step 1: Validate YAML and JSON**

Run:

```bash
python3 - <<'PY'
import json
from pathlib import Path
import yaml
for path in [
    Path("docs/phase3a1_threshold_policy.yaml"),
    Path("docs/phase3a6_acceptance_policy.yaml"),
]:
    yaml.safe_load(path.read_text())
json.loads(Path("GPD/state.json").read_text())
print("policy_yaml_and_gpd_json_ok")
PY
```

Expected output:

```text
policy_yaml_and_gpd_json_ok
```

- [x] **Step 2: Run registry and experiment checks**

Run:

```bash
uv run --no-editable eternity validate-registry lab_data/registry.yaml
uv run --no-editable eternity validate experiments/examples/linear_tin_sio2_d10nm_validation_candidate.yaml
uv run --no-editable eternity run experiments/examples/linear_tin_sio2_d10nm_validation_candidate.yaml
uv run --no-editable eternity phase3a1-audit --run-dir results/runs/run_f35a15cef565fb15 --output-dir results/runs/run_f35a15cef565fb15/phase3a1_audit
```

Expected results:

- registry validates;
- validation candidate spec validates;
- run completes to `results/runs/run_f35a15cef565fb15`;
- Phase 3A.1 audit still reports normalization and threshold blockers.

- [x] **Step 3: Run tests and lint**

Run:

```bash
uv run --no-editable pytest -q
uv run --no-editable ruff check .
git diff --check
```

Expected results:

- pytest passes;
- ruff passes;
- no whitespace errors.

- [x] **Step 4: Smoke-check atlas**

Run the existing Playwright file smoke pattern against:

```text
file:///Users/joegarbarino/Desktop/Eternity/docs/project_atlas/index.html
```

Expected checks:

- body text includes `Phase 3A.6`;
- body text includes `CompleteEASE`;
- body text includes `blocked_needs_new_export`;
- conflict board exists.

- [x] **Step 5: Review claim status remains fail-closed**

Run:

```bash
cat results/runs/run_f35a15cef565fb15/claim_status.json
cat results/runs/run_f35a15cef565fb15/phase3a1_audit/phase3a1_audit.json
```

Expected findings:

- `can_feed_serious_core` is `false`;
- `claim_status` remains `weak_within_dataset_holdout`;
- `normalization_gate_blocked` remains present;
- `thresholds_predeclared_gate_blocked` remains present.

- [x] **Step 6: Commit only Phase 3A.6 planning files**

Run:

```bash
git status --short
git add CURRENT_REALISTIC_ROADMAP.md GOALS.md GPD/ROADMAP.md GPD/STATE.md GPD/state.json docs/PROJECT_ATLAS.md docs/phase3a1_threshold_policy.yaml docs/phase3a6_acceptance_policy.yaml docs/phase3a6_completeease_reexport_packet.md docs/phase_index.md docs/project_atlas/index.html docs/superpowers/plans/2026-05-16-phase3a6-completeease-reexport-measurement-packet.md
git commit -m "Plan Phase 3A.6 re-export packet"
git push origin codex/research-memory-v0
```

Expected:

- unrelated untracked files remain unstaged;
- commit contains only Phase 3A.6 planning work;
- branch push succeeds.

## Self-Review

Spec coverage:

- Covers the re-export/measurement packet.
- Preserves Phase 3A.5 `blocked_needs_new_export`.
- Keeps existing inspected residuals historical.
- Keeps TiON and `30_20_10` blockers visible.
- Defines exact verification commands.

Placeholder scan:

- No `TBD` or open-ended placeholder fields are used as final content.
- Missing future values are represented as explicit required fields or blocked defaults.

Type consistency:

- Phase IDs use `Phase 3A.6`.
- Policy statuses use snake-case values aligned with prior docs.
- Existing run ID is consistently `run_f35a15cef565fb15`.
