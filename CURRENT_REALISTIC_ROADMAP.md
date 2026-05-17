# Eternity Current Realistic Roadmap

Date: 2026-05-07

## Framing

Eternity is a long-term personal research/build project, not a short-term product sprint.

The goal is to see how far one person plus current and future AI systems can go toward building an AI researcher for ultrafast ENZ optics over the next few years. The project should be useful, scientifically grounded, and fun. It does not need to become a fully autonomous scientist immediately. The right standard is compounding progress.

The long-term destination is:

> An AI researcher that can read literature and lab memory, form hypotheses, design theoretical ENZ/ultrafast optics experiments, run simulations, compare against real lab data, critique its own conclusions, propose next experiments, and eventually help draft research notes or papers.

The realistic starting point is:

> Build the experimental world that a future AI researcher can think and act inside.

That world is the ENZ digital twin: simulation infrastructure, lab data, material models, validation records, uncertainty tracking, and reproducible experiment runs.

## Why Start With The Digital Twin

The digital twin is still the best start, but not because the AI researcher idea is being dismissed.

It is the best start because it is the most direct path to making the AI researcher meaningful.

If the project starts with autonomous agents first, the result will probably be a smart-sounding chatbot with weak contact with physical reality. If the project starts with the digital twin, every later AI upgrade can plug into a real substrate:

- Data it can inspect.
- Simulators it can run.
- Results it can compare.
- Assumptions it must state.
- Validity envelopes it must respect.
- Failed hypotheses it can remember.
- Experimental artifacts it can learn to avoid.

The digital twin is the body, lab bench, notebook, and reality-check layer for the future AI researcher.

## Two-Track Strategy

Because this is a long-term personal project, Eternity should not be overly conservative. It should have a serious physics core and a more experimental AI researcher playground.

### Track A: Serious Core

This is the validated ENZ digital twin.

Principles:

- Slow and careful.
- Test-driven where possible.
- Physically explicit.
- Reproducible.
- Versioned.
- Skeptical about claims.
- Grounded in real lab data and known literature.

This track owns:

- Experiment specs.
- Lab-data registry.
- Material models.
- Transfer-matrix simulation.
- FDTD adapters.
- Fitting and calibration.
- Run provenance.
- Reports.
- Validity envelopes.
- Regression tests.

### Track B: Researcher Playground

This is where we explore the AI researcher idea early.

Principles:

- Fun and speculative.
- Allowed to be wrong.
- Clearly labeled as exploratory.
- Never allowed to overwrite or contaminate validated core results.
- Useful for learning what future AI workflows might look like.

This track can include:

- Hypothesis generation.
- Literature-question answering.
- Proposed simulation sweeps.
- Research-note drafting.
- Critique agents.
- Mechanism comparison.
- Paper-outline generation.
- Weird search strategies.
- Multi-agent debate.

The rule is simple: the playground may suggest; the serious core verifies.

## First Real Loop

The first important milestone is not a complete simulator. It is a complete research loop:

```text
question
  -> experiment spec
  -> simulation
  -> result
  -> critique
  -> proposed next experiment
```

This is the seed of the autonomous researcher.

At first, the loop can use toy data and a simple linear simulator. Later, each piece becomes more real:

- Toy material -> fitted Drude/Drude-Lorentz material.
- Synthetic pulse -> measured laser spectrum/FROG/autocorrelation data.
- Linear TMM -> nonlinear ENZ dynamics and FDTD validation.
- Human-written question -> AI-generated hypothesis.
- Simple report -> research notebook entry with uncertainty and literature context.

## V0: First Vertical Slice

Build a minimal but real ENZ thin-film experiment runner.

V0 should include:

- Python package foundation.
- One YAML experiment spec.
- One lab-data registry.
- One material model.
- One transfer-matrix simulator.
- One deterministic run command.
- One generated Markdown report.
- Tests proving deterministic behavior and basic energy bookkeeping.

The first V0 experiment can use:

- Synthetic ITO/AZO material parameters.
- Synthetic Gaussian or chirped Gaussian pulse.
- Simple thin-film stack.
- Transmission/reflection output.
- Plots of epsilon, n/k, transmission, and reflection.

The point is to make the entire system shape real, even before the physics is deep.

## V1: Real Inputs

After V0 works, add real data one path at a time.

Priority order:

1. Ellipsometry import.
2. Linear transmission/reflection import.
3. Measured laser spectrum import.
4. Pulse duration/chirp metadata.
5. Sample thickness and uncertainty.
6. Incidence angle and polarization metadata.

V1 goal:

> Given one measured sample and one measured optical setup, predict linear transmission/reflection and compare against measurement.

This is the first serious digital-twin checkpoint.

### Active V1 Phase 3: TiN/TiON + Thesis Reflectance Grounding

The immediate core move is not yet a calibrated claim. It is to make the
available real data safe for the Serious Core:

- Snapshot the 50 nm TiN optical constants, TiON_48/TiON_49 40 nm epsilon
  tables, and thesis reflectance spectra under `lab_data/raw/...`.
- Register every artifact with SHA-256, byte size, source notes, sample/stack
  refs, and claim-status boundaries.
- Load tabulated epsilon as a frozen linear material model for deterministic
  TMM grounding runs.
- Preserve thesis initial/12V reflectance spectra as measured provenance and
  possible holdout candidates.
- Emit explicit R/T provenance audits and gaps when TiON sample-matched
  reflection/transmission data is missing.

Allowed status for optical-constants-only TiN/TiON runs:

```text
calibration_only_no_holdout
```

Forbidden language until an independent holdout exists:

```text
calibrated TiN/TiON evidence
validated nonlinear ENZ response
sample-matched R/T agreement
```

#### Phase 3A: TiN/SiO2 Thesis Reflectance Reconciliation

Active core move:

- Reconcile the thesis/paper TiN/SiO2 measured spectra with the sample labels
  and stack records already in the registry.
- Add the `30_20_10` reflectance, Psi/Delta, p/s intensity, and e1/e2 exports
  as candidate raw artifacts, but do not treat them as thesis `d_10nm`
  validation evidence until the filename-to-thesis mapping is source-confirmed.
- Decide the measurement geometry, polarization, normalization, and holdout
  split policy before any residual thresholds are set.
- Keep TiON_48/TiON_49 in a parked Phase 3B path unless raw R/T or
  source-tabulated reflectance appears.

Implemented Phase 3A should emit a fail-closed validation candidate using the
`thesis_d_10nm` / `3L2` stack:

- frozen TiN and SiO2 epsilon tables;
- incident-order stack `air / 20 nm TiN / 10 nm SiO2 / 30 nm TiN / quartz`;
- TE/S-polarized, 60-degree comparison against the d=10 nm initial spectrum;
- `30_20_10` reflectance, p/s intensity, Psi/Delta, and e1/e2 exports as a
  separate unresolved candidate bundle, not auxiliary evidence for the
  `d_10nm` holdout.

Phase 3A may emit `weak_within_dataset_holdout`, but it cannot claim
`calibrated_linear_evidence` while normalization and residual-threshold gates
remain blocked.

#### Phase 3A.1: Normalization And Threshold Gate Hardening

Active follow-up:

- Keep the already-inspected Phase 3A residuals as historical context only.
- Record the normalization decision as a machine-readable gate policy with the
  current state `relative_intensity_only`.
- Record that no residual thresholds are approved for the existing run.
- Provide an audit command that reports whether the current run can be promoted
  and why it remains blocked.

Phase 3A.1 is not a calibration phase. It may prepare future gate policy, but
it must not convert `run_f35a15cef565fb15` into
`calibrated_linear_evidence`.

#### Phase 3A.2: Stack Mapping Correction

Active correction:

- Keep thesis `d_10nm` mapped to `3L2/Quartz` because the thesis Table 4.1 and
  Figure 4.1 support the 30 nm TiN / 10 nm SiO2 / 20 nm TiN stack.
- Demote separate `30_20_10` Coding/txt exports to
  `phase3a_30_20_10_candidate` because the thesis/appendix do not prove those
  filenames are the plotted `d_10nm` spectra.
- Keep calibrated promotion blocked by normalization and threshold gates.

#### Phase 3A.3: Thesis Figure/Data Provenance Reconciliation

Active provenance closure:

- Align `d_10nm_initial.txt` and `d_10nm_12V.txt` with thesis Figure 4.1 and
  the local `10 nm SiO2 Reflectance.png` plot.
- Record that the values are plotted as reflectance but exported as
  `Intensity`, so the current normalization basis is `relative_intensity_only`,
  not absolute calibrated reflectance.
- Keep `30_20_10` as a separate candidate bundle. AFRL 6E notebook evidence
  supports a 30 nm TiN / 10 nm SiO2 / 20 nm TiN quartz model, but not identity
  with the thesis Figure 4.1 export.
- Keep calibrated promotion blocked by normalization and threshold gates.

#### Phase 3A.4: Absolute Reflectance Decision And Threshold Policy Prep

Active decision:

- Treat the thesis `d_10nm` exports as `relative_intensity_only` after checking
  thesis text, local figures, byte-identical raw tables, local CompleteEASE
  manual passages, and nearby Woollam/CompleteEASE artifacts.
- Preserve the stronger Phase 3A.3 provenance result: `d_10nm` is source-backed
  to thesis Figure 4.1 and sample `3L2/Quartz`, with 60-degree S-polarized RC2
  reflectance context.
- Do not treat the exported `Intensity` columns as absolute `%R` until a
  source-backed export/recipe/project/lab-note record proves that calibration.
- Keep `run_f35a15cef565fb15` historical only. No pass/fail thresholds may be
  chosen from already-inspected residuals, and no current Phase 3A run may
  promote to `calibrated_linear_evidence`.
- Prepare future policy only: absolute-normalization evidence, wavelength
  window, residual metrics, numeric thresholds, approver, and date must all be
  recorded before a future residual-gated run.

#### Phase 3A.5: Source-Backed Export/Provenance Retrieval

Decision: `blocked_needs_new_export`.

The bounded local/SDSU/Google Drive search found strong RC2/CompleteEASE,
thesis, SDSU slide, AFRL report, and scanned lab-notebook provenance, including
related reflectivity/reflection-intensity files and the `3L2/Quartz` sample
narrative. It still did not find a source-backed export, recipe, project, debug
bundle, or lab-note statement proving that the exact `d_10nm_initial.txt` and
`d_10nm_12V.txt` `Intensity` columns are calibrated absolute `%R`.

The Phase 3A normalization basis therefore stays `relative_intensity_only`.
`run_f35a15cef565fb15` remains historical and capped below calibrated evidence.

Next best core move:

- `Phase 3A.6 - CompleteEASE re-export / measurement packet`: write the exact
  source-evidence request needed for a clean future run, or define a
  Pro/user-approved relative-only diagnostic policy that cannot promote to
  `calibrated_linear_evidence`.

#### Phase 3A.6: CompleteEASE Re-export / Measurement Packet

Implementation artifacts:

- `docs/phase3a6_completeease_reexport_packet.md`
- `docs/phase3a6_acceptance_policy.yaml`
- `docs/superpowers/plans/2026-05-16-phase3a6-completeease-reexport-measurement-packet.md`

Planning file:
`docs/superpowers/plans/2026-05-16-phase3a6-completeease-reexport-measurement-packet.md`.

Purpose:

- Turn the Phase 3A.5 blocked result into a precise evidence request for the
  original CompleteEASE/Woollam project, a fresh re-export, an export recipe,
  or a new measurement note.
- Require sample identity, stack, angle, polarization, channel name, units,
  calibration/baseline state, source file identity, hash, and future-only
  threshold boundaries before any absolute-reflectance run.
- Keep all existing inspected runs below `calibrated_linear_evidence`.

Not enough information exists yet to complete calibrated Phase 3A promotion.
Enough information exists to use the source-evidence packet and prevent another
ambiguous export from entering the serious core.

#### Phase 3A.7: CompleteEASE Source Recovery + 3L2 Provenance Lock

Decision: `related_source_candidates_found`, with `absolute_reflectance_blocked`.

Implementation artifacts:

- `src/eternity/phase3a7.py`
- `docs/phase3a7_completeease_source_recovery.md`
- `docs/phase3a7_completeease_source_recovery.json`

Phase 3A.7 adds a read-only recovery scanner for local CompleteEASE/Woollam
`.SE`, `.SEsnap`, and `.iSE` files, including matching members inside DoD SAFE
zip containers. It records hashes, archive/member paths, `_FitLog` snippets,
and candidate scores without copying large binary source files into the repo.

Result:

- Thesis-backed `3L2/Quartz` mapping is stronger: 30 nm TiN / 10 nm SiO2 /
  20 nm TiN on quartz, S-polarized RC2 in-situ reflectance/reflective intensity
  at 60 degrees, Figure 4.1.
- The strongest recovered local candidates are related CompleteEASE/Woollam
  source snapshots for quartz cap-test and 10 nm SiO2 pulsed/dynamic runs.
- No readable source metadata proves that the exported `Intensity` columns are
  calibrated absolute `%R`. Generic CompleteEASE strings such as `% 1st
  Reflection` or `Absolute MSE` are not normalization proof.
- `run_f35a15cef565fb15` remains historical, capped at
  `weak_within_dataset_holdout`, and blocked by normalization and
  predeclared-threshold gates.

Enough information exists to continue relative-intensity diagnostics and source
triage. Not enough information exists to approve absolute normalization,
thresholds, or `calibrated_linear_evidence`.

#### Phase 3A.8: Source Candidate Triage + Relative-Only Diagnostic Decision

Decision: `pivot_to_relative_only_diagnostic`, with `absolute_reflectance_blocked`.

Implementation artifacts:

- `src/eternity/phase3a8.py`
- `docs/phase3a8_source_candidate_triage.md`
- `docs/phase3a8_source_candidate_triage.json`
- `docs/phase3a8_relative_only_diagnostic_policy.yaml`

Phase 3A.8 consumes the Phase 3A.7 recovery manifest without rescanning local
source files. It deduplicates source candidates by SHA-256, separates the
quartz 10 nm dynamic/manual-follow-up candidates from Si-control candidates,
and records the relative-only lane explicitly.

Result:

- The highest manual-follow-up candidates are the DoD SAFE zip-contained quartz
  10 nm SiO2 pulsed/dynamic `.SEsnap` files.
- Related quartz cap-test files remain provenance context, not exact source
  identity records.
- Si 100 files are classified as controls or wrong-substrate candidates for the
  thesis `3L2/Quartz` path.
- Future Phase 3A diagnostics may compare spectral shape, dip position, trend
  direction, and figure provenance only.
- Serious-core ingestion, calibrated-linear-evidence promotion, absolute
  reflectance claims, and retroactive threshold tuning remain forbidden.

Enough information exists to run relative-only diagnostics honestly. Not enough
information exists to approve absolute normalization, thresholds, or
`calibrated_linear_evidence`.

#### Phase 3A.9: Relative-Only Diagnostic Run Packet

Decision: `relative_only_diagnostic_packet_ready`, with serious-core ingestion
and calibrated promotion still forbidden.

Implementation artifacts:

- `src/eternity/phase3a9.py`
- `docs/phase3a9_relative_only_diagnostic_packet.md`
- `docs/phase3a9_relative_only_diagnostic_packet.json`
- `docs/phase3a9_relative_only_diagnostic_table.csv`

Phase 3A.9 consumes the existing Phase 3A validation-candidate run and the
Phase 3A.8 relative-only policy. It reports normalized shape, dip-position, and
trend-direction diagnostics without treating them as thresholds or calibrated
validation.

Result for `run_f35a15cef565fb15`:

- Window: 400-900 nm, 501 points.
- Min-max shape correlation: about 0.986.
- Prediction and measurement dips both occur at 400 nm in the inspected window.
- Both normalized spectra trend upward over the inspected window.
- Historical absolute residual context remains visible, but it is not used for
  threshold setting or promotion.

Enough information exists to say the relative spectral shape is worth keeping
as a diagnostic clue. Not enough information exists to claim absolute
reflectance agreement, pass/fail validation, or `calibrated_linear_evidence`.

## Near-Term Reach With Current Tools

With the V0 skeleton in place, the project can go meaningfully further before
waiting for future model releases.

Realistic current-tool milestones:

1. **Real linear ENZ digital twin**
   - Ingest ellipsometry or exported `n,k` data.
   - Fit Drude and Drude-Lorentz parameters.
   - Simulate real ITO/AZO thin films.
   - Compare predicted and measured transmission/reflection.
   - Produce reproducible reports with warnings and validity envelopes.

2. **First calibration loop**
   - Take one sample.
   - Fit material parameters from one dataset.
   - Predict another dataset.
   - Show where the model works and where it fails.
   - Track uncertainty and model limits.

3. **Pump-probe / nonlinear prototype**
   - Add simple time-dependent Drude parameters.
   - Add fluence and delay as experiment dimensions.
   - Fit relaxation times from synthetic or real pump-probe traces.
   - Compare mechanisms such as plasma-frequency modulation vs damping
     modulation.

4. **Researcher playground**
   - Let an AI read a result manifest.
   - Ask it to explain what happened.
   - Ask it to propose next simulations.
   - Ask it to identify missing physics and possible artifacts.
   - Keep it separate from validated claims.

5. **Literature and lab memory**
   - Build a local paper library around ENZ, ITO, AZO, hot electrons, temporal
     refraction, pump-probe methods, and FDTD.
   - Extract model equations, parameter ranges, and experimental conditions.
   - Connect papers to simulations and results.

6. **Higher-fidelity validation**
   - Add Meep/FDTD for selected simple cases.
   - Compare TMM vs FDTD in limits where both should agree.
   - Use FDTD when it adds scientific value, not as the foundation for
     everything.

The honest limit is that current tools should not be trusted as a fully
autonomous scientist. The useful target is a research copilot with a real
physics substrate.

The most exciting next scientific checkpoint is:

> Eternity takes one identified ENZ film dataset, currently the local TiN/TiON
> family if sample provenance is strong enough, loads or fits a constrained
> linear material model, predicts an independent measured spectrum, compares
> against holdout data, and writes a report saying exactly where it agrees and
> fails.

## V2: First Researcher Behavior

Once V0 or early V1 exists, add a small AI researcher command or notebook.

It should not claim discovery. It should do bounded reasoning:

- Read one result manifest.
- Summarize what was simulated.
- State assumptions.
- State what was not modeled.
- Compare against baseline.
- Suggest three follow-up simulations.
- Write a cautious research note.

This keeps the AI researcher dream visible from the beginning while preserving scientific discipline.

## V3: Nonlinear ENZ Dynamics

After the linear setup is validated, begin adding nonlinear material response.

Start with simple, explicit models:

- Fluence-dependent Drude parameters.
- Time-dependent plasma frequency.
- Time-dependent damping/scattering rate.
- Simple relaxation time.
- Electron-temperature-inspired response.

Then move toward richer models:

- Two-temperature-style dynamics.
- Effective mass changes.
- Nonparabolic band corrections.
- Hot-electron scattering mechanisms.
- Pump-probe delay dependence.

Every nonlinear feature must include:

- Literature provenance.
- Parameter source.
- Validity envelope.
- Baseline comparison.
- Failure modes.
- Tests against known or synthetic limits.

## V4: Higher-Fidelity Simulation

Add Meep or another FDTD backend only after the project has a clean lower-fidelity baseline.

FDTD should be used for:

- Boundary-condition-sensitive effects.
- Angle-dependent behavior.
- Subwavelength field enhancement.
- Pump-probe geometry tests.
- Multilayer or metasurface expansion.

It should not replace the simple models. It should sit above them and be forced to agree with them in limits where the simple models are valid.

## V5: Mechanism-Separating Researcher

This is where the AI researcher starts becoming more interesting.

The system should compare mechanisms, not just sweep parameters.

Example:

- Mechanism A: spectral shift from bulk temporal refraction.
- Mechanism B: spectral shift from time-dependent boundary conditions.
- Mechanism C: apparent shift from detector/spectral-window artifact.

The AI researcher should propose simulations or lab experiments that distinguish these mechanisms.

This is the first version that feels like a research collaborator rather than a plotting assistant.

## V6: Long-Term Autonomous Researcher Direction

Over the 2.5-year horizon, the AI researcher can gradually gain more autonomy:

- Read new papers and add them to lab memory.
- Extract model equations and parameter ranges.
- Generate experiment specs.
- Run cheap models.
- Queue expensive simulations.
- Compare simulation levels.
- Identify disagreement between literature, simple theory, high-fidelity simulation, and lab data.
- Propose next experiments.
- Draft research notes.
- Maintain a failed-hypothesis archive.
- Build a case for possible novelty.

Even at this stage, human review remains central. The AI can accelerate search and synthesis, but the project should keep scientific claims gated by validation.

## Later Model-Customization Track

Down the line, Eternity may benefit from model customization tools such as
Unsloth Studio or Thinking Machines Lab's Tinker-style managed fine-tuning. They
should not be used to train the physics simulator itself. Their likely value is
training or adapting smaller specialist models around Eternity's accumulated
research process.

Possible later uses:

- A local experiment-spec drafting model trained on accepted Eternity specs.
- A result-critique model trained to flag missing assumptions, bad units,
  unsupported claims, and validity-envelope violations.
- A literature triage model trained on promoted vs rejected ENZ papers.
- A report-drafting assistant that follows Eternity's cautious reporting style.
- A mechanism-comparison assistant that proposes alternative explanations from
  structured result manifests.

Use this track only after the project has enough high-quality internal data:

- Accepted and rejected experiment specs.
- Result manifests with human critiques.
- Literature notes with quality labels.
- Failed-hypothesis records.
- Reports that clearly separate evidence from speculation.

Unsloth Studio is likely most useful for local no-code or low-code fine-tuning
and side-by-side model comparison. Thinking Machines credits would be most useful
for managed post-training or reinforcement-style fine-tuning if Tinker access is
available and the project has a clean training/evaluation dataset.

This track should stay downstream of the serious core:

```text
validated registry -> curated training examples -> fine-tuned helper model ->
held-out evaluation -> optional use in researcher playground
```

Do not fine-tune on raw papers, raw lab data, or unreviewed AI outputs and then
trust the result. For Eternity, customization should teach process discipline,
not invent physics authority.

## What Success Could Look Like By The End Of The PhD Window

An ambitious but realistic 2.5-year outcome:

- A working ENZ digital-twin codebase.
- Several real lab datasets ingested.
- Material parameters fit for specific samples.
- Linear and nonlinear simulations with provenance.
- Meep/FDTD validation for selected cases.
- A lab-memory system with papers, notes, datasets, and failed ideas.
- An AI researcher prototype that proposes mechanism-separating simulations.
- Optional fine-tuned helper models for spec drafting, result critique,
  literature triage, or report style.
- Reproducible research reports that could support thesis work or paper ideation.
- A clear record of where the model succeeded, failed, and suggested useful experiments.

The win is not necessarily "AI independently discovers new physics."

The win is:

> We built a system that makes AI meaningfully participate in ultrafast ENZ research instead of merely talking about it.

## Immediate Next Step

Initialize the repo and build V0.

Recommended starting implementation:

```text
src/eternity/
  specs/
  data/
  materials/
  pulses/
  simulators/
  results/
  reports/
  cli/

experiments/
  examples/

lab_data/
  README.md

results/
  .gitkeep

tests/
```

First command target:

```text
eternity run experiments/examples/linear_ito_toy.yaml
```

First output:

```text
results/<run_id>/
  spec.yaml
  manifest.json
  metrics.json
  plots/
  report.md
```

The first report should already include:

- What was simulated.
- Which model was used.
- What assumptions were made.
- What data was synthetic.
- What the simulator predicts.
- What is not trusted yet.
- What follow-up would make it more real.

That is the first brick on the direct path toward the AI researcher.

## Pro Model Checkpoints

Eternity should periodically ask for outside input from 5.5 Pro, or whatever the
current best Pro reasoning model is, when the project enters hard or unknown
territory. This is not for routine implementation. It is for checkpoint gates
where better abstract reasoning could materially change the path.

Use this process before:

- Unknown physics or material-modeling choices.
- Major architecture decisions that will be hard to reverse.
- Surprising simulation results.
- Possible novelty claims.
- Failed validation loops where the reason is unclear.
- Phase transitions such as V0 to V1, linear to nonlinear, or local simulator to
  FDTD.

When a checkpoint is warranted, the assistant should say:

```text
Pro checkpoint recommended
```

Then it should explain why in 2-4 bullets and provide a compact prompt the user
can paste into the current Pro model.
