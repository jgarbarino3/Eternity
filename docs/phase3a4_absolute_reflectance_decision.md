# Phase 3A.4 Absolute Reflectance Decision

Date: 2026-05-16

## Decision

Status: `relative_intensity_only`.

The thesis `d_10nm_initial.txt` and `d_10nm_12V.txt` exports remain useful
measured spectra for shape/provenance checks, but Phase 3A.4 does not find
source-backed proof that their exported `Intensity` columns are calibrated
absolute reflectance. They must not be used to promote any run to
`calibrated_linear_evidence`.

This decision preserves the Phase 3A.3 finding:

- `d_10nm` remains source-backed to thesis sample `3L2/Quartz` and Figure 4.1.
- The figure and thesis text describe S-polarized reflectance measured by the
  RC2 at 60 degrees.
- The copied raw tables are byte-identical to the original thesis data files.
- The exported table headers still say `Intensity`, and no local source proves
  the exact export represents calibrated absolute `%R`.

## Evidence Checked

Strong evidence for measured reflectance provenance:

- `/Users/joegarbarino/Desktop/Research Optics/Thesis Last copy.pdf` describes
  RC2 measurements of reflectance spectra at 60 degrees and labels Figure 4.1
  as in-situ reflectance for the 10 nm SiO2 three-layer sample.
- `/Users/joegarbarino/Desktop/Research Optics/Thesis/Figures/10 nm SiO2 Reflectance.png`
  visually matches the `d_10nm` initial and 12 V text-table scale.
- `/Users/joegarbarino/Desktop/Research Optics/Thesis/Figures/photo 10 nm SiO2 in situ.png`
  shows CompleteEASE in-situ reflective-intensity behavior near the same
  wavelength/value regime.

Direct artifact identity:

| Artifact | SHA-256 |
| --- | --- |
| `lab_data/raw/thesis_reflectance/d_10nm_initial.txt` | `c093c27d277841140f7655da72372e9ffc90b2abf030c5e358cd0c01d2b3bc21` |
| `/Users/joegarbarino/Desktop/Research Optics/Thesis/Data/d_10nm_initial.txt` | `c093c27d277841140f7655da72372e9ffc90b2abf030c5e358cd0c01d2b3bc21` |
| `lab_data/raw/thesis_reflectance/d_10nm_12V.txt` | `0b4890786cbebe76d723447592ed67549a826e563a8d4a4c4970d33919be4819` |
| `/Users/joegarbarino/Desktop/Research Optics/Thesis/Data/d_10nm_12V.txt` | `0b4890786cbebe76d723447592ed67549a826e563a8d4a4c4970d33919be4819` |
| `/Users/joegarbarino/Desktop/Research Optics/Thesis Last copy.pdf` | `9f6649f777f50aa52cbb46348b0617d860d4b663ab80659fa68474aa134ac40b` |
| `/Users/joegarbarino/Desktop/Research Optics/Thesis/Figures/10 nm SiO2 Reflectance.png` | `93032f23773dafbb7b933b3dade1d5722e9b3e93908f3bc33b3b2877c1e1d5f5` |
| `/Users/joegarbarino/Desktop/Research Optics/Thesis/Figures/photo 10 nm SiO2 in situ.png` | `2b7301850a47f4ade4abee44d72e54fc66ff8b3fc8f9098a23c66ec2a7b71665` |
| `/Users/joegarbarino/Desktop/Research Optics/Thesis/References/Ellipsometry_manual.pdf` | `f9797c832c4e8761a5a1e24f2ba9015fc824c22842e3ae70ad2a3d159016d00c` |

Evidence that prevents absolute promotion:

- Both `d_10nm` exports begin with `Wavelength (nm)` and `Intensity`, not
  `Reflectance`, `%R`, or a calibration-normalized quantity.
- Other thesis data exports use `s-Intensity` for S-polarized channels, so
  `Intensity` is a real CompleteEASE channel label in this data family.
- The local CompleteEASE manual confirms that intensity data are recorded by
  the software, but the checked passages do not prove that these exported
  `Intensity` columns are calibrated absolute reflectance for this measurement.
- `/Users/joegarbarino/Optics Research/Thesis SiO2 experimental thickness optimization.ipynb`
  reads a related thesis plot column as `Intensity` / `Reflective Intensity`,
  not calibrated absolute reflectance.
- No local Woollam project file, recipe, export setting, plotting script, or
  lab note was found that maps this exact export column to absolute `%R`.

## Phase 3A.5 Follow-up

Phase 3A.5 extended the source search across the likely Research Optics, Optics
Research, targeted Downloads, desktop SDSU Google Drive, targeted Google Drive
thesis/defense hits, SDSU slides/reports, and the scanned lab notebook. It found
related RC2 reflectivity/reflection-intensity files plus stronger `3L2/Quartz`
sample provenance, but no exact CompleteEASE/Woollam source record proving that
the thesis `d_10nm` `Intensity` exports are calibrated absolute `%R`.

Follow-up status: `blocked_needs_new_export`.

See `docs/phase3a5_export_provenance_retrieval.md`.

## Future Policy

Existing residuals remain historical context only. Because
`run_f35a15cef565fb15` has already been inspected, Phase 3A.4 does not set
pass/fail thresholds for it.

A future Phase 3A run may only move beyond `weak_within_dataset_holdout` if all
of the following are recorded before the run:

- `absolute_reflectance_confirmed` normalization with source-backed evidence;
- wavelength window, residual metrics, numeric thresholds, approver, and date;
- explicit `applies_to_existing_run: false` for any policy created after
  already-inspected residuals;
- gate outputs showing stack mapping, no-fit leakage, normalization,
  thresholds, and claim-status policy all pass.

Acceptable future evidence would include one of:

- a CompleteEASE/Woollam export or recipe record whose channel is explicitly
  reflectance or `%R`;
- a project/snapshot file or lab note tying the `Intensity` export to calibrated
  reflectance normalization for this RC2 measurement;
- a newly exported reflectance table with geometry, polarization, calibration,
  and sample mapping recorded before residual inspection;
- a Pro/user-approved policy that keeps the data relative-only and defines only
  shape/provenance diagnostics, not calibrated evidence.

## Pro Checkpoint

Pro checkpoint recommended

```text
Review Eternity Phase 3A.4: thesis d_10nm/3L2 reflectance validation has text
exports labeled Intensity, thesis plots labeled Reflectance, and no hard proof
yet that the exported values are calibrated absolute reflectance. Decide whether
this supports absolute reflectance, relative-only shape validation, or requires
new measurement/export evidence before calibrated_linear_evidence. If future
thresholds are allowed, specify wavelength window, metrics, and evidence gates
without using already-inspected residuals to tune thresholds.
```
