# ENZ Material Dynamics Reuse Research

Date: 2026-05-07

Question: what existing ultrafast optics, ENZ/TCO/ITO/AZO/CdO, Drude-Lorentz, hot-electron, pump-probe, and nonlinear optical material-response work can inform custom ENZ material dynamics and validation for Eternity?

Bottom line: I did not find a single ready-made Python package that already implements and validates custom ENZ hot-electron material dynamics for ITO/AZO/CdO pump-probe thin films. The practical path is to reuse existing Python for linear multilayer optics, ellipsometry/fitting, thermal relaxation scaffolding, pulse utilities, and FDTD validation, while implementing Eternity's ENZ material-state model as project-owned code.

## Best Practical Reuse Targets

| Priority | Item | URL | Code status | Practical reuse for Eternity | Caveats |
|---|---|---|---|---|---|
| 1 | `sbyrnes321/tmm` | https://github.com/sbyrnes321/tmm | Code exists. Python/NumPy, MIT. | Best immediate baseline for Layer 1: coherent/incoherent transfer matrix, R/T/A, field/absorption profiles, ellipsometry quantities. Use to validate Eternity's own thin-film solver or depend on it directly. | Linear optics only. No native time-dependent ENZ hot-electron dynamics. |
| 1 | Bohn et al., "All-optical switching of an epsilon-near-zero plasmon resonance in indium tin oxide" | Paper: https://www.nature.com/articles/s41467-021-21332-y ; dataset/code: https://doi.org/10.24378/exe.3004 | Data and analysis code exist. Nature says Python and Mathematica analysis/plotting code are included. | Very strong validation target for ITO thin-film pump-probe / Kretschmann geometry. Includes 60 nm ITO, ellipsometry-derived permittivity, pump/probe geometry, dynamic three-layer model, and measured switching. | Analysis code is not necessarily a reusable package. Still valuable as benchmark data and reference equations. |
| 1 | NTMpy | Paper: https://arxiv.org/abs/2002.04559 ; repo: https://github.com/udcm-su/NTMpy ; CPC record: https://doi.org/10.1016/j.cpc.2021.107990 | Code exists. Python, MIT. | Reuse ideas/API for two-/three-temperature diffusion in multilayer pump-probe experiments. Good reference for source deposition, thermal relaxation, and validation against transient reflectivity. | It models thermal response, not ENZ permittivity from nonparabolic TCO bands. Likely use as reference or optional adapter, not as the core material law. |
| 1 | Silaeva/Saddier/Colombier, "Drude-Lorentz Model for Optical Properties of Photoexcited Transition Metals under Electron-Phonon Nonequilibrium" | https://www.mdpi.com/2076-3417/11/21/9902 | Supplementary Python code and tabulated data exist. | Reuse the fitting pattern: basin-hopping / optimization of Drude-Lorentz coefficients vs hot-electron-temperature optical data. Useful for Eternity's fitting pipeline and tests. | Transition metals, not TCO/ITO/AZO/CdO. Do not copy material constants as ENZ truth. |
| 2 | pyElli | https://github.com/PyEllips/pyElli | Code exists. Python, GPL-3.0. | Useful reference for ellipsometry analysis, 2x2/4x4 solvers, custom dispersion models, fitting measurement data, refractiveindex.info ingestion. | GPL makes direct embedding into a permissive/proprietary core awkward. Prefer as dev tool/reference unless Eternity accepts GPL-compatible licensing. |
| 2 | Meep | https://github.com/NanoComp/meep ; docs: https://meep.readthedocs.io/en/latest/Materials | Code exists. Python API, GPL. | Best open FDTD validation backend. Supports dispersive Drude/Lorentz-style media, conductivity, Kerr/Pockels nonlinearities, and programmable field analysis. | Generic nonlinear material models do not equal ENZ hot-electron dynamics. Custom time-dependent Drude parameters may require workarounds or a separate solver. GPL matters. |
| 2 | gnlse-python | Paper: https://arxiv.org/abs/2110.00298 ; repo: https://github.com/WUST-FOG/gnlse-python | Code exists. Python, MIT. | Reuse pulse/frequency-grid/SSFM ideas for chirped Gaussian pulses, measured spectra, and quick propagation sanity checks. | Fiber GNLSE package, not thin-film ENZ. Treat as utility inspiration, not physical authority for ENZ slabs. |
| 2 | `flaport/fdtd` | https://github.com/flaport/fdtd | Code exists. Python with optional GPU support. | Hackable FDTD scaffold if Eternity needs project-owned ADE/time-dependent material experiments before committing to Meep. | Not a mature ENZ dispersive-hot-electron solver out of the box. Would require significant custom material work. |
| 3 | PyNLO | https://github.com/pyNLO/PyNLO | Code exists. Python. | Pulse/beam/nonlinear optics abstractions and examples for chi2/chi3 processes. | Mostly fiber/crystal nonlinear optics. Not ENZ hot-electron TCO dynamics. Check current maintenance and license before reuse. |
| 3 | Lightwave Explorer | https://github.com/NickKarpowicz/LightwaveExplorer | Code exists, but not Python-first. | Good reference for ultrashort nonlinear light-matter simulation UX and convergence thinking. | Not directly reusable in a Python codebase. |
| 3 | Luna.jl | https://github.com/LupoLab/Luna.jl | Code exists, Julia. | Strong reference for UPPE/GNLSE-style propagation architecture. | Not Python. More relevant to Layer 2 than thin-film ENZ material response. |

## ENZ/TCO Papers That Should Inform the Custom Material Model

These are not drop-in codebases. They are physics/model/validation sources.

| Item | URL | Code status | What to extract |
|---|---|---|---|
| Un/Sarkar/Sivan, "Electronic-Based Model of the Optical Nonlinearity of Low-Electron-Density Drude Materials" | APS: https://journals.aps.org/prapplied/abstract/10.1103/PhysRevApplied.19.044043 ; arXiv: https://arxiv.org/abs/2210.08504 | I did not find public code. | Central model source for LEDD/TCO nonlinearity. Important because it argues ENZ/TCO response should not be treated as simple Kerr or saturable nonlinearity. Use for time-dependent permittivity, nonthermal electron distribution, effective chemical potential, nonparabolicity, and validity assumptions. |
| Sarkar/Un/Sivan, "Electronic and Thermal Response of Low-Electron-Density Drude Materials to Ultrafast Optical Illumination" | https://arxiv.org/search/?query=%22Electronic+and+Thermal+Response+of+Low-Electron-Density+Drude+Materials%22&searchtype=all | I did not find public code. | Companion theory for electron dynamics and thermal response in LEDD materials. Useful for state variables and relaxation model structure. |
| Secondo/Khurgin/Kinsey, "Absorptive loss and band non-parabolicity as a physical origin of large nonlinearity in epsilon-near-zero materials" | https://opg.optica.org/ome/abstract.cfm?uri=ome-10-7-1545 ; arXiv: https://arxiv.org/abs/2004.00134 | I did not find public code. | Practical theory for intensity-dependent index in heavily doped semiconductors. Extract band nonparabolicity/effective-mass/plasma-frequency relationships and material tradeoff metrics. |
| Secondo et al., "Deterministic Modeling of Hybrid Nonlinear Effects in Epsilon-Near-Zero Thin Films" | https://www.anl.gov/argonne-scientific-publications/pub/172842 ; DOI: https://doi.org/10.1063/5.0077116 | I did not find public code. | Framework for predicting nonlinear ENZ performance from E-k diagram, linear optical properties, and experimental conditions. Useful later for material screening and model-based experiment design. |
| Rahmeier/Smy/Gupta, "Nonlinear FDTD Simulation of Optical Thin Films with Intensity-Dependent Drude-Lorentz Parameters" | IEEE: https://ieeexplore.ieee.org/document/10133543 ; TechRxiv/ResearchGate entry: https://www.researchgate.net/publication/364708524_Nonlinear_FDTD_Simulation_of_Optical_Thin_Films_with_Intensity-Dependent_Drude-Lorentz_Parameters | I did not find public code. | Very relevant algorithmic direction: extend FDTD/ADE Drude-Lorentz updates with local intensity-dependent parameters and low-pass/memory response. Good blueprint for Eternity's custom Maxwell-Drude solver. |
| Scalora et al., "Electrodynamics of Conductive Oxides: Intensity-dependent anisotropy..." | arXiv: https://arxiv.org/abs/2003.01059 | I did not find public code. | Important warning that longitudinal/transverse dielectric response and nonlocal effects can diverge in ITO nanolayers, especially at intensity. Use as future validity-envelope pressure test. |
| Alam/De Leon/Boyd, "Large optical nonlinearity of indium tin oxide in its epsilon-near-zero region" | https://www.science.org/doi/10.1126/science.aae0330 | I did not find public code. | Foundational ITO ENZ nonlinear benchmark. Extract reported n2/beta, pump-probe conditions, and near-unity refractive-index-change expectations for sanity checks. |
| Kinsey et al., "Epsilon-near-zero Al-doped ZnO for ultrafast switching at telecom wavelengths" | https://opg.optica.org/optica/abstract.cfm?uri=optica-2-7-616 ; DOI: https://doi.org/10.1364/OPTICA.2.000616 | I did not find public code. Supplement exists. | AZO validation source: sub-ps recovery and large reflectance/transmittance modulation at telecom wavelengths. Use to avoid overfitting Eternity only to ITO. |
| Tyborski et al., "Ultrafast nonlinear response of bulk plasmons in highly doped ZnO layers" | DOI: https://doi.org/10.1103/PhysRevLett.115.147401 | I did not find public code. | ZnO/AZO-adjacent validation for ultrafast bulk-plasmon nonlinear response. |
| Caspani et al., "Enhanced nonlinear refractive index in epsilon-near-zero materials" | DOI: https://doi.org/10.1103/PhysRevLett.116.233901 | I did not find public code. | Useful for comparing reported nonlinear refractive index enhancement near ENZ. |
| Yang et al., "Femtosecond optical polarization switching using a cadmium oxide-based perfect absorber" | Nature: https://www.nature.com/articles/nphoton.2017.64 ; OSTI: https://www.osti.gov/pages/biblio/1361213 | I did not find public code. | Key CdO validation target. Extract CdO perfect absorber geometry, sub-bandgap pumping, effective-mass increase, reflectance swing, and 800 fs switching. |
| Saha/Rashed/Yildiz/Ayyagari/Caglayan, "Hot Electron Dynamics in Ultrafast Multilayer Epsilon-Near-Zero Metamaterial" | https://arxiv.org/abs/2003.04540 | I did not find public code. | Useful two-temperature-model interpretation of hot-electron dynamics in multilayer ENZ metamaterial. |
| Khurgin et al., "Adiabatic frequency shifting in epsilon-near-zero materials: the role of group velocity" | https://opg.optica.org/optica/abstract.cfm?uri=optica-7-3-226 ; DOI: https://doi.org/10.1364/OPTICA.374788 | I did not find public code. | Use for time-varying medium/frequency-shift validation and to avoid overclaiming ENZ enhancement mechanisms. |
| "Broadband frequency translation through time refraction in an epsilon-near-zero material" | https://www.nature.com/articles/s41467-020-15682-2 | I did not find public code. | Experimental validation for time-varying ITO frequency translation. Useful later for chirp/delay experiments. |
| Bohn et al. references around ITO/AZO/CdO TCOs | https://www.nature.com/articles/s41467-021-21332-y | Paper with dataset/code, plus curated reference list. | Useful literature map. The introduction explicitly ties ITO, doped ZnO/AZO, and CdO nonlinearities to electron heating, nonparabolic dispersion, and effective-mass changes. |

## Architecture Implications For Eternity

Own these parts in Eternity:

- `MaterialModel` interface: `epsilon(omega, state)` and `update_state(absorbed_power, t, z, params)`.
- Static models: Drude, Drude-Lorentz, tabulated n/k, fitted ellipsometry model.
- Dynamic state variables: electron temperature, lattice temperature, plasma frequency, damping/scattering rate, carrier density, effective mass, pump-probe delay, local absorbed energy.
- Validation envelope on every model: wavelength range, fluence range, film thickness, material, geometry, pulse duration, fit data source.
- Result contract: include assumptions, calibration dataset hash, holdout dataset, warnings, and convergence metrics.

Reuse or adapt these parts:

- Linear TMM: start with `tmm` as a correctness oracle; decide later whether to vendor/rewrite the small core for full control.
- Ellipsometry fitting: use pyElli/refellips as references and maybe dev tools; implement Eternity-owned Drude-Lorentz fitting with SciPy/lmfit if licensing matters.
- Thermal dynamics: use NTMpy as a tested reference for multilayer two-/three-temperature dynamics.
- Pulse utilities: borrow patterns from gnlse-python/PyNLO for grids, chirp, measured spectra, FFT conventions, and reproducibility tests.
- FDTD validation: use Meep as an external validation backend, not as the first source of truth for custom hot-electron material response.

## Recommended Build Sequence

1. Build V0 linear stack:
   - Drude and Drude-Lorentz permittivity functions.
   - Transfer matrix R/T/A and ellipsometry quantities.
   - Fit Drude-Lorentz parameters to ellipsometry CSV.
   - Cross-check outputs against `sbyrnes321/tmm` and pyElli examples.

2. Add validation datasets:
   - Load Bohn et al. ITO dataset/code from https://doi.org/10.24378/exe.3004.
   - Add paper-derived benchmark fixtures for Alam 2016 ITO, Kinsey 2015 AZO, and Yang 2017 CdO.

3. Add V1 dynamic material model:
   - Start with phenomenological time-dependent `omega_p(t)` and `gamma(t)` fit to pump-probe data.
   - Add a two-temperature or three-temperature state evolution path inspired by NTMpy.
   - Then add nonparabolic/effective-mass physics from Secondo/Khurgin/Kinsey and Un/Sarkar/Sivan.

4. Add higher-fidelity checks:
   - Compare dynamic TMM predictions against Bohn's static/dynamic three-layer model.
   - Use Meep for fixed-parameter dispersive FDTD checks.
   - Prototype project-owned 1D Maxwell-Drude/ADE only when the dynamic TMM layer is validated.

## Direct Answer To The Research Question

Existing work can strongly inform Eternity, but mostly as pieces:

- There is reusable Python for linear multilayer optics, ellipsometry, pulse propagation, and thermal pump-probe dynamics.
- There are excellent ENZ/TCO papers for ITO, AZO, and CdO model validation.
- There are some paper-specific datasets and analysis code, especially Bohn et al. 2021 for ITO ENZ plasmon switching.
- There is no obvious maintained Python library that already provides the exact custom ENZ material dynamics Eternity wants: time-dependent Drude-Lorentz/hot-electron/nonparabolic TCO response coupled to pump-probe thin-film validation.

Therefore the core scientific value should be Eternity-owned: a modular, testable material-dynamics layer calibrated against lab/literature datasets, with existing libraries used as reference backends and validation oracles.
