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
  as candidate raw artifacts if their provenance mapping holds.
- Decide the measurement geometry, polarization, normalization, and holdout
  split policy before any residual thresholds are set.
- Keep TiON_48/TiON_49 in a parked Phase 3B path unless raw R/T or
  source-tabulated reflectance appears.

Implemented Phase 3A should emit a fail-closed validation candidate using the
`thesis_d_10nm` / `3L2` stack:

- frozen TiN and SiO2 epsilon tables;
- incident-order stack `air / 20 nm TiN / 10 nm SiO2 / 30 nm TiN / quartz`;
- TE/S-polarized, 60-degree comparison against the d=10 nm initial spectrum;
- `30_20_10` reflectance, p/s intensity, Psi/Delta, and e1/e2 exports as
  auxiliary audit evidence.

Phase 3A may emit `weak_within_dataset_holdout`, but it cannot claim
`calibrated_linear_evidence` while normalization and residual-threshold gates
remain blocked.

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
