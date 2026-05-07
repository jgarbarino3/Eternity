# Eternity Day 1 Future Roadmap

## Project Vision

Eternity is a long-horizon project to build an AI researcher for ultrafast optics and ENZ material physics. The goal is not simply to have an AI write physics papers. The real target is an AI researcher connected to a calibrated simulation and lab-data environment that can:

- Form hypotheses about new ultrafast/ENZ optical behavior.
- Convert hypotheses into theoretical experiment specifications.
- Run those experiments through appropriate simulation backends.
- Compare predictions against real lab data.
- Estimate uncertainty, model bias, and failure modes.
- Propose next experiments that distinguish competing physical mechanisms.
- Eventually draft research notes and papers from validated results.

The strongest version of the project is a research digital twin of an ultrafast ENZ optics lab: a simulation environment continuously constrained by measured laser, sample, detector, and experiment data.

## Core Principle

Do not build "one giant physically accurate simulator" first.

Build a multi-fidelity research environment where different model layers answer different kinds of questions, and where real lab data constantly pulls the system back toward reality.

A normal simulator says:

> Given parameters, here is what theory predicts.

Eternity should say:

> Given the actual laser, pulse, sample, measured material response, detector limits, and experimental noise, here is the most trustworthy prediction available, with uncertainty, assumptions, failure modes, and proposed next tests.

The AI researcher should not ask only:

> What does the simulator say?

It should ask:

> Which simulator level says this? What assumptions were used? Does it match lab data? What is the uncertainty? What simpler model fails? What real experiment would disprove this?

## Why This Matters For ENZ Ultrafast Optics

For ENZ ultrafast optics, "truth" is not just Maxwell's equations. It is Maxwell's equations plus uncertain material dynamics and lab-specific effects:

- Hot-electron response.
- Pump/probe alignment.
- Pulse chirp.
- Detector response.
- Thermal history.
- Fabrication variation.
- Film thickness variation.
- Roughness and interface effects.
- Surface and boundary-condition effects.
- Scattering-rate changes.
- Carrier-density and effective-mass changes.
- Unknown artifacts that are not yet in the model.

If the project does not explicitly track model bias, it can become confidently wrong. Every simulation result should carry its validity envelope and known limitations.

## System Separation

Build the project as three systems that talk to each other but stay separable:

1. **ENZ Digital Twin**
   - The simulator, calibration stack, uncertainty engine, and data registry.
   - This should remain useful even if the AI researcher is weak.

2. **AI Researcher**
   - Hypothesis generation, experiment planning, result interpretation, critique, and research-note generation.
   - This should be replaceable as better AI models arrive.

3. **Lab Memory**
   - Literature, lab notebooks, raw and processed data, failed experiments, known artifacts, and prior model comparisons.
   - This should remain useful even before the simulator is complete.

The simulator should be trustworthy even if the AI researcher is dumb. The lab memory should be useful even if the simulator is incomplete. The AI researcher should be replaceable when better models arrive.

## Simulation Environment Layers

### Layer 0: Lab Data Layer

This is where real experimental data lives. It should store machine-readable data, not only plots.

Example structure:

```text
lab_data/
  lasers/
    spectra/
    frog_traces/
    autocorrelation/
    pulse_energy/
    beam_profile/
    rep_rate/
    pointing_stability/
    polarization/
    chirp_estimates/

  samples/
    ellipsometry/
    thickness/
    roughness/
    AFM_SEM/
    carrier_density/
    mobility/
    fabrication_notes/
    temperature_history/

  experiments/
    pump_probe/
    transmission_spectra/
    reflection_spectra/
    phase_measurements/
    harmonic_generation/
    delay_scans/
    detector_calibration/
```

This layer is the project advantage over generic AI scientist systems. General systems may have papers. Eternity should have the user's actual laser and sample reality.

### Layer 1: Fast Analytic Models

Cheap models are essential for sanity checks and baseline comparisons.

Initial models:

- Linear transfer matrix.
- Thin-film reflection and transmission.
- Drude permittivity.
- Drude-Lorentz fitting.
- Static ENZ resonance location.
- Basic phase and group-delay calculations.

This layer will not discover deep effects by itself, but it prevents the system from mistaking ordinary dispersion, absorption, or cavity behavior for new physics.

### Layer 2: Pulse Propagation Models

Envelope-style propagation models can screen hypotheses quickly when the geometry allows them.

Candidate model families:

- Generalized nonlinear Schrodinger equation style models.
- UPPE-style propagation models.
- Chirped Gaussian and measured-spectrum pulse propagation.
- Fast pulse-shaping and spectral-evolution models.

Questions this layer can answer:

- How does chirp change the spectrum?
- How does pulse duration affect broadening?
- What happens to spectral centroid?
- What happens to temporal phase?
- Which regimes are worth sending to higher-fidelity solvers?

For ENZ thin-film cases, this layer may not be the final authority. It is mainly a fast screening layer.

### Layer 3: Maxwell / FDTD Simulations

Higher-fidelity electromagnetic solvers are needed for field dynamics, subwavelength film effects, and boundary-condition-sensitive mechanisms.

Candidate capabilities:

- 1D, 2D, and eventually 3D FDTD.
- Dispersive permittivity.
- Custom sources.
- PML boundaries.
- Nonlinear material terms where supported.
- Angle-dependent response.
- TM vs TE behavior.
- Multilayer stacks.
- Pump-probe geometries.
- Transient field enhancement.

Meep is an important candidate, but should not be blindly trusted for every ENZ nonlinear problem. Ultrafast ENZ material dynamics may require custom material equations that do not map cleanly onto generic Kerr/Pockels abstractions.

### Layer 4: Custom ENZ Material Dynamics

This is likely where the project becomes scientifically distinctive.

Eventually, Eternity should support custom material-response models such as:

- Drude and Drude-Lorentz dispersion.
- Time-dependent plasma frequency.
- Time-dependent damping or scattering rate.
- Hot-electron temperature.
- Two-temperature-style relaxation.
- Carrier-density-dependent permittivity.
- Effective-mass changes.
- Nonlocal response or hydrodynamic corrections if needed.
- Experimental parameter fitting.
- Fluence-dependent response.
- Pump-probe delay-dependent response.

This does not need to be perfect at first. It must be modular, testable, and calibratable.

### Layer 5: Surrogate Models

Once high-fidelity simulations become expensive, train fast approximators.

Example surrogate inputs:

- Material parameters.
- Pulse duration.
- Chirp.
- Fluence.
- Film thickness.
- Incidence angle.
- Polarization.
- Pump/probe delay.

Example surrogate outputs:

- Reflection spectrum.
- Transmission spectrum.
- Phase shift.
- Spectral centroid shift.
- Harmonic yield.
- Absorption.
- Uncertainty.

The surrogate must always know when it is extrapolating. The AI researcher should not be allowed to treat surrogate predictions outside the calibrated domain as discoveries.

## Simulation Result Contract

The simulator should not return only numbers or plots. Every result should include confidence, warnings, and required follow-up.

Example:

```json
{
  "result": {
    "spectral_centroid_shift_THz": -3.2,
    "transmission_change_percent": 18.4,
    "phase_shift_rad": 0.71
  },
  "confidence": {
    "numerical_convergence": 0.92,
    "material_model_validity": 0.61,
    "experimental_parameter_certainty": 0.74,
    "within_calibrated_domain": true
  },
  "warnings": [
    "Hot-electron relaxation time extrapolated beyond fitted fluence range",
    "Film roughness not included",
    "Detector response not modeled",
    "Only 1D propagation used"
  ],
  "required_followup": [
    "Run higher-resolution FDTD",
    "Compare to Kerr-only baseline",
    "Fit against pump-probe delay scan",
    "Test positive and negative chirp experimentally"
  ]
}
```

This is how the project avoids becoming a hallucination engine with plots.

## How Real Laser And Lab Data Enter The System

### 1. Calibrating Inputs

Instead of assuming perfect Gaussian pulses, the simulator should use measured lab pulses when possible.

Useful inputs:

- Measured spectrum.
- Measured temporal duration.
- Measured chirp.
- Measured pulse energy distribution.
- Beam waist.
- Spatial mode.
- Polarization purity.
- Pulse-to-pulse fluctuation.
- Rep-rate heating effects.

Many simulated ultrafast optics papers quietly assume ideal pulses. Eternity should not.

### 2. Fitting Material Parameters

The user's samples are not generic ITO, AZO, CdO, or other literature samples. They are specific fabricated samples with specific material parameters.

Fit material models from:

- Ellipsometry.
- Linear transmission/reflection.
- Film thickness and roughness measurements.
- Pump-probe traces.
- Fluence-dependent spectra.
- Temperature-dependent data.
- Fabrication notes.

### 3. Validating Predictions

The system should use calibration data and holdout data.

Example split:

- Calibration data:
  - Normal-incidence transmission.
  - One pump fluence.
  - One chirp setting.
  - One sample thickness.

- Holdout data:
  - Different chirp.
  - Different angle.
  - Different pump/probe delay.
  - Different fluence.

The AI can fit calibration data. Then it must predict holdout data. If it fails, it does not get to write a paper; it must update the model or state what physics is missing.

### 4. Proposing Next Experiments

Once the model has uncertainty, the AI can design experiments that reduce uncertainty or distinguish mechanisms.

Example:

- Mechanism A: frequency shift comes mostly from bulk temporal refraction.
- Mechanism B: frequency shift comes mostly from time-dependent boundary conditions.
- Proposed experiment: sweep incidence angle and film thickness while keeping fluence fixed, because the mechanisms predict different angle/thickness scaling.

The goal is not random parameter search. The goal is mechanism-separating experiment design.

## Formal Experiment Language

Every theoretical experiment should be a structured file, not just prose.

Example:

```yaml
experiment_id: enz_chirp_boundary_001

question:
  Can chirp reverse the sign of pump-induced frequency shift in a subwavelength ENZ film?

hypothesis:
  Negative and positive chirp change the temporal ordering of spectral components
  relative to the pump-induced ENZ shift, causing opposite spectral centroid shifts.

sample:
  material: ITO
  thickness_nm: 60
  source: lab_sample_ITO_2026_02_A
  material_model:
    type: drude_lorentz_hot_electron
    parameters_from: ellipsometry_fit_2026_02_A

input_pulse:
  source: measured_frog_trace_2026_02_11
  center_wavelength_nm: 1550
  duration_fs: 35
  chirp_fs2: [-500, -250, 0, 250, 500]
  fluence_mJ_cm2: [0.1, 0.5, 1.0, 2.0]

geometry:
  incidence_angle_deg: [0, 30, 45, 60]
  polarization: TM

simulators:
  - linear_transfer_matrix
  - maxwell_1d_drude_hot_electron
  - fdtd_meep_validation

observables:
  - transmitted_spectrum
  - reflected_spectrum
  - spectral_centroid_shift
  - phase_shift
  - absorption
  - temporal_delay

baselines:
  - linear_no_pump
  - instantaneous_kerr_only
  - drude_no_hot_electron
  - no_boundary_modulation

acceptance_tests:
  - convergence_with_grid
  - convergence_with_time_step
  - energy_accounting
  - agrees_with_linear_model_in_low_fluence_limit
  - predicts_holdout_lab_data_within_uncertainty
```

The AI researcher can generate, mutate, critique, run, and compare these specs.

## AI Researcher Loop

The research loop should be:

1. Read literature and lab memory.
2. Find open questions, contradictions, or model disagreements.
3. Generate candidate hypotheses.
4. Convert each hypothesis into experiment specs.
5. Run cheap analytic models.
6. Reject obvious, trivial, or already-known effects.
7. Run higher-fidelity simulations.
8. Compare with real lab data.
9. Estimate uncertainty and model bias.
10. Ask what mechanism explains the result.
11. Design follow-up simulations.
12. Only then write a research note or paper draft.

The paper-writing part is downstream. The most valuable first product is the closed-loop lab notebook.

## Starting Scope

Do not begin with every possible nonlinear optics experiment.

Start with one real experimental setup:

> Digital twin of an ITO/AZO ENZ thin-film pump-probe experiment.

The V0 target should reproduce one setup well before expanding.

## Milestones

### V0: Linear Digital Twin

Inputs:

- Measured laser spectrum.
- Measured pulse duration/chirp.
- Measured sample ellipsometry.
- Measured film thickness.
- Measured incidence angle.
- Measured polarization.

Simulation:

- Linear transfer matrix.
- Drude-Lorentz fit.
- Low-fluence transmission/reflection prediction.

Outputs:

- Predicted vs measured spectrum.
- Fitted material parameters.
- Uncertainty.
- Markdown report.

### V1: Fluence And Delay

Add:

- Fluence-dependent material response.
- Pump-probe relaxation-time fitting.
- Delay-scan prediction.
- Comparison to measured pump-probe data.

### V2: Hypothesis Generation

Add:

- Candidate hypothesis generation.
- Model-disagreement search.
- Automatic baseline comparison.
- Structured experiment spec generation.

### V3: Next-Experiment Planner

Add:

- Mechanism-separating experiment design.
- Uncertainty reduction scoring.
- Proposed real lab experiments.
- Human review gates before execution or publication.

### Later: Paper Drafting

Only after the system can reproduce and validate a real setup should it draft papers. Drafting should be grounded in:

- Reproducible simulation records.
- Versioned data.
- Explicit model assumptions.
- Holdout validation.
- Failed hypotheses.
- Known artifacts.
- Confidence and validity envelopes.

## First Codex Build Target

The first project should be infrastructure, not discovery.

Working name:

```text
enz-digital-twin
```

Goal:

```text
Build a reproducible simulation and data-calibration environment for ultrafast
pulse propagation in ENZ thin films.
```

Initial implementation checklist:

1. YAML experiment specifications.
2. Lab-data registry for laser, sample, and measurement data.
3. Drude and Drude-Lorentz material models.
4. Linear thin-film transfer-matrix simulation.
5. Pulse objects:
   - Gaussian pulse.
   - Chirped Gaussian pulse.
   - Measured-spectrum pulse loaded from CSV.
6. Fitting tools:
   - Fit Drude-Lorentz parameters to ellipsometry data.
   - Fit film-thickness correction from linear transmission/reflection.
7. Plotting:
   - n,k vs wavelength.
   - epsilon real/imaginary vs wavelength.
   - Transmission/reflection spectra.
   - Predicted vs measured plots.
8. Results database that stores:
   - Experiment spec.
   - Input data hashes.
   - Fitted parameters.
   - Simulator version.
   - Git commit.
   - Plots.
   - Metrics.
9. Markdown report generator.
10. Tests for:
   - Material model behavior.
   - Deterministic simulation.
   - Low-loss limits.
   - Energy bookkeeping.
   - Reproducibility of fits.

Do not implement autonomous agents yet.

Make the code modular so future solvers can be added:

- 1D Maxwell-Drude solver.
- Meep/FDTD backend.
- Hot-electron material model.
- Surrogate model.
- Hypothesis generator.

## Validity Envelope

Every model should state where it is trusted and not trusted.

Example trusted region:

```text
wavelength: 1300-1700 nm
fluence: 0-1.5 mJ/cm^2
pulse duration: 30-100 fs
film thickness: 40-100 nm
material: lab ITO samples A-C
geometry: single-layer thin film, TM incidence
```

Example untrusted region:

```text
damage threshold regimes
unknown sample heating
nanostructured metasurfaces
few-cycle carrier-envelope-sensitive pulses
nonlocal effects
roughness-dominated scattering
```

The AI researcher should be forced to state the validity envelope every time it makes a scientific claim.

## Biggest Trap

"As physically accurate as possible" can become a trap.

The correct sequence is:

1. Accurate enough for one setup.
2. Validated against one dataset.
3. Expanded to one nonlinear effect.
4. Validated again.
5. Expanded to one new geometry.
6. Validated again.

Accuracy should be earned experimentally.

## How Novelty Could Emerge

The project should search for disagreement between:

- Known literature.
- Simple theory.
- High-fidelity simulation.
- Real lab data.

Possible research questions:

- Find parameter regions where a measured ITO sample behaves unlike the published model.
- Determine whether chirp or incidence angle better separates hot-electron relaxation from instantaneous Kerr response.
- Find the smallest set of experiments needed to distinguish Drude damping modulation from plasma-frequency modulation.
- Find pulse shapes that maximize phase shift while minimizing absorption.
- Find where simple transfer-matrix predictions fail most strongly.
- Find where nonlinear response is robust to realistic laser noise.
- Find whether sample-to-sample variation kills or preserves the effect.

The goal is not to ask the AI to be creative in a vacuum. The goal is to make it search scientifically meaningful disagreement regions.

## Day 1 Working Position

The first useful artifact is not a complete AI scientist. It is a clean, versioned foundation for:

- Lab data ingestion.
- Material-model fitting.
- Transfer-matrix simulation.
- Experiment specs.
- Reproducible runs.
- Reports.
- Tests.
- Clear validity envelopes.

If this foundation is done well, future AI models can become better "brains" on top of it. The enduring asset is the calibrated optics research environment.

## References From Initial Research Note

- Bayesian digital-twin calibration and data quality: https://publications.tno.nl/publication/34641731/PnCubA/titscher-2023-bayesian.pdf
- Model bias in digital twins: https://arxiv.org/html/2312.00664v2
- GNLSE Python documentation: https://gnlse.readthedocs.io/en/latest/gnlse_intro.html
- Meep documentation: https://meep.readthedocs.io/
- Meep material modeling: https://meep.readthedocs.io/en/latest/Materials
- 2025 hot-electron ENZ dynamics paper: https://pubmed.ncbi.nlm.nih.gov/40397738/
- Large optical nonlinearity of ITO near ENZ: https://www.science.org/doi/10.1126/science.aae0330

## Open-Source Simulation Stack Scan

Web scan current as of 2026-05-07. The practical Day 1 stack should stay multi-fidelity: fast TMM/material fitting first, then Meep validation, then custom ENZ dynamics. No surveyed open-source package appears to directly solve ultrafast ENZ hot-electron Drude dynamics as a turnkey feature.

| Project | Class | Use in Eternity | ENZ / hot-electron limitation | License | Priority |
| --- | --- | --- | --- | --- | --- |
| [tmm](https://github.com/sbyrnes321/tmm) | Thin-film TMM | Baseline R/T/A, ellipsometry-style sanity checks, V0 linear model. | Linear, planar, frequency-domain; no femtosecond carrier dynamics. | MIT | Day 1 |
| [TMMax](https://github.com/bahremsd/tmmax) | JAX TMM | Faster batched TMM sweeps, differentiable fitting, surrogate-data generation. | Still layered linear optics; nonlinear pump response must be external. | MIT | Day 1 |
| [refractiveindex.info database](https://refractiveindex.info/about.php) | Optical constants | Seed n,k datasets and provenance for Drude-Lorentz fitting. | Literature data may not match lab films; ENZ samples must be measured/fitted. | CC0 database | Day 1 |
| [Meep](https://github.com/NanoComp/meep) | FDTD | Main credible open-source Maxwell backend: Python, dispersive, anisotropic, Kerr/Pockels, PML, MPI, adjoint. | Hot-electron/two-temperature Drude dynamics are not turnkey; custom material updates may be needed. | GPL-2.0 | Day 1 / later |
| [Solcore](https://github.com/qpv-research-group/solcore5) | Solar/semiconductor optics | Material + optical stack tooling; TMM and S4/RCWA interface useful for cross-checks. | PV-oriented, not ultrafast ENZ; likely supporting library, not core truth model. | LGPL-style repo license | Later |
| [Meent](https://github.com/kc-ml2/meent) | RCWA + JAX/PyTorch | Differentiable periodic/metasurface sweeps if Eternity expands beyond flat films. | Frequency-domain, linear RCWA; no transient pump-probe dynamics. | MIT | Later |
| [S4](https://web.stanford.edu/group/fan/S4/) | RCWA/FMM | Credible Stanford RCWA for layered periodic structures, Python extension. | Linear frequency-domain; older interface; license not obvious from docs scan. | Not found quickly | Later |
| [openEMS](https://docs.openems.de/intro.html) | FDTD/EC-FDTD | Alternative FDTD with Python/Octave, graded mesh, Drude/Lorentz/Debye materials. | RF/microwave heritage; less photonics/ultrafast-focused than Meep. | GPL-3.0+ | Later |
| [FDTDX](https://ymahlau.github.io/fdtdx/) | JAX FDTD | Interesting GPU/autodiff path for inverse design and future ML integration. | 2026 JOSS paper says only linear, non-dispersive materials at publication. | Check before adopting | Maybe |
| [Ceviche](https://github.com/fancompute/ceviche) | FDFD/FDTD + autograd | Lightweight differentiable EM experiments and inverse-design prototypes. | Last release is old; limited material physics; not ENZ transient-ready. | MIT | Maybe |
| [Palace](https://github.com/awslabs/palace) | 3D FEM EM | Large-scale full-wave FEM, time/frequency/eigenmode; credible HPC backend. | Heavy C++/MFEM stack; not a Day 1 Python thin-film simulator. | Apache-2.0 | Maybe / later |
| [MFEM / PyMFEM](https://mfem.org/electromagnetics/) | FEM library | Custom Maxwell/FEM research backend if bespoke material PDEs become necessary. | High engineering cost; not turnkey optics workflow. | BSD-3 via PyMFEM | Maybe |
| [FEniCSx/DOLFINx](https://docs.fenicsproject.org/) | FEM/PDE | General PDE platform for custom coupled material/thermal/carrier models. | Maxwell examples exist, but full EM/material stack must be built. | LGPL-3.0+ | Maybe |
| [NGSolve](https://ngsolve.org/ngsolve/docs/i-tutorials/wta/maxwell.html) | FEM | Python-accessible Maxwell FEM tutorials; useful for custom formulations. | Solver-framework work, not ENZ optics product out of the box. | LGPL family | Maybe |
| [py-fmas](https://omelchert.github.io/py-fmas/) | Ultrafast pulse propagation | Few-cycle/analytic-signal propagation concepts and test cases. | Single-mode waveguide propagation, not thin-film Maxwell boundary physics. | MIT | Later |
| [gnlse-python](https://gnlse.readthedocs.io/) | GNLSE pulse propagation | Quick envelope-level nonlinear pulse screening and pulse-object tests. | Fiber/waveguide GNLSE; ENZ film response must be represented separately. | MIT | Later |
| [PyNLO](https://github.com/pyNLO/PyNLO) | Nonlinear optics | Reference ideas for pulse/material abstractions and chi2/chi3 workflows. | Python 2 requirement in README; not a modern Day 1 dependency. | GPL-3.0 | Maybe |
| [Prismo](https://pypi.org/project/pyprismo/) | Python FDTD | New alpha photonics FDTD claims Drude/Lorentz/Debye/Sellmeier and ITO material library. | Alpha project; verify accuracy before scientific use. | MIT | Maybe |
| [rfx-fdtd](https://pypi.org/project/rfx-fdtd/) | JAX FDTD | Active differentiable FDTD with Drude/Lorentz/Kerr claims; possible experiment lane. | RF-oriented and new; independently validate before trusting optics output. | MIT | Maybe |
| [pyGDM](https://pypi.org/project/pyGDM2/1.0.7/) | Green dyadic method | Nano-object frequency-domain scattering/near-field alternative. | Monochromatic GDM; not transient hot-electron ENZ. | GPL-3.0+ | Maybe |

Day 1 recommendation: implement the internal abstraction around `tmm` or `TMMax`, `refractiveindex.info` data ingestion, Drude/Drude-Lorentz fitting, and result contracts. Treat Meep as the first high-fidelity validation backend, not the foundation for every model. Keep newer differentiable FDTD packages in a sandbox until they reproduce known TMM/Meep cases and energy bookkeeping.
