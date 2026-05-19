# Phase 3D.1 - Exeter/Bohn ITO Package Intake

Date: 2026-05-19

## Decision

- Status: `package_downloaded_first_pass_intake_ready`
- Can feed serious core: `false`
- Can promote calibrated evidence: `false`
- Phase 4 ready: `false`
- Recommended next phase: `Phase 3D.1A - Exeter/Bohn calibration-holdout split audit`

## Source

- Paper: Bohn et al., "All-optical switching of an epsilon-near-zero plasmon resonance in indium tin oxide"
- Paper DOI: `10.1038/s41467-021-21332-y`
- Dataset DOI: `10.24378/exe.3004`
- Dataset article id: `29776322`
- Package: `OpenData.zip`
- File id: `56807864`
- Rights in metadata: `CC BY 4.0`

## Local Snapshot

- Raw folder: `lab_data/raw/public_exeter_bohn_ito_2021/`
- Metadata: `lab_data/raw/public_exeter_bohn_ito_2021/figshare_article_29776322.json`
- Package: `lab_data/raw/public_exeter_bohn_ito_2021/OpenData.zip`
- File manifest: `lab_data/raw/public_exeter_bohn_ito_2021/file_manifest_paths.txt`
- File tree: `lab_data/raw/public_exeter_bohn_ito_2021/file_tree.txt`
- Supplied/computed MD5: `0d9c1a1b720795aa09f51a7aad4b51e4`
- Local MD5: `0d9c1a1b720795aa09f51a7aad4b51e4`
- Local SHA-256: `9d04f668ec13586093963cef5a9cbea930dd5690eb30e64fc9619a53c9fc1215`
- ZIP test: no errors detected.

## First-Pass File Findings

The package is a real data/code archive, not only a paper landing page. It has
53 members and includes CSVs, notebooks, Mathematica code, EPS/SVG figures, and
plain-text Figure 1 optical data.

Candidate calibration/model inputs:

- `Figure1/DATA_ellipsometer_fit.txt`: 188 lines. Header says `Opt. Const. of Gen-Osc vs. nm` with columns `nm`, `e1 Gen-Osc`, `e2 Gen-Osc`, `e1 Ref.`, and `e2 Ref.`.
- `Figure1/dispersion_export_w.dat`: 99 lines.
- `Figure1/dispersion_export_k.dat`: 99 lines.
- `Figure2/JUPYTER_Figure2a,b,c.ipynb`: contains model code with `t_ITO = 60`.

Candidate reflection/calibration files:

- `Figure2/DATA/DATA_Figure2a,b,c_calibration_probe_TIR.csv`: 373 lines.
- `Figure2/DATA/DATA_Figure2a,b,c_experiment.csv`: 65,287 lines.
- `Figure3/DATA/DATA_Figure3_calibration_probe_TIR.csv`: 541 lines.
- `Figure3/DATA/DATA_Figure3_experiment.csv`: 12,241 lines.
- `Figure4/DATA/DATA_Figure4_calibration_probe_TIR.csv`: 541 lines.
- `Figure4/DATA/DATA_Figure4a_experiment.csv`: 31,876 lines.
- `Figure4/DATA/DATA_Figure4b,c_experiment.csv`: 31,876 lines.

The Figure 2 notebook explicitly labels a section `Probe (TIR reflection)` and
uses the calibration file as a `TIR Reference = 100% Reflection`. That is
promising for absolute reflection reconstruction, but it still needs a leakage
and static-linear-holdout audit.

## Current Risks

- The experiment CSVs are pump/probe dynamic experiment tables, not yet proven
  to contain a clean static linear unpumped reflection holdout.
- Notebook code may include model parameters or processing choices tuned to the
  reflection data. That must be audited before any claim-status promotion.
- The angle conversion and prism/coverslip stack handling need to be mapped
  from notebook variables into an explicit Eternity geometry contract.
- The Figure 1 permittivity table may be enough for a frozen ITO material model,
  but it is not yet linked to a leak-free holdout split.

## Allowed Next

- Extract only the relevant Figure 1 optical constants and Figure 2/3/4
  calibration/experiment CSVs into a candidate manifest.
- Audit the notebooks for static-unpumped reflection reconstruction, fitted
  parameters, and allowed nuisance parameters.
- Draft a `calibration_holdout_split.yaml` only if the split is source-backed.

## Forbidden Next

- Do not mark this dataset as `calibrated_linear_evidence`.
- Do not fit ITO parameters, thickness, angle, scaling, or threshold choices
  after inspecting the reflection residuals.
- Do not treat pump-probe dynamic rows as a linear holdout until static
  unpumped reconstruction is proven.
- Do not proceed to Phase 4 from this package intake alone.
