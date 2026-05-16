# Phase 3A.3 Thesis Data Provenance

Date: 2026-05-16

## Result

The `d_10nm_initial.txt` and `d_10nm_12V.txt` tables are strong thesis Figure 4.1
provenance candidates, but they still do not prove absolute calibrated
reflectance.

Current decision:

- Treat thesis `d_10nm` as source-backed to sample `3L2/Quartz`.
- Treat the exported y-axis as `relative_intensity_only` for gate policy.
- Keep calibrated promotion blocked until absolute normalization and future
  residual thresholds are approved before a future run.
- Keep `30_20_10` separate from thesis `d_10nm` unless a file-level export link
  is found.

## Evidence

Local thesis evidence:

- `/Users/joegarbarino/Desktop/Research Optics/Thesis Last copy.pdf` Table 4.1
  maps `3L2/Quartz` to `30 nm TiN / 10 nm SiO2 / 20 nm TiN`.
- The same thesis Figure 4.1 describes S-polarized reflectance of the 10 nm
  SiO2 three-layer sample with initial and 12 V traces.
- `/Users/joegarbarino/Desktop/Research Optics/Thesis/Figures/10 nm SiO2 Reflectance.png`
  plots `d=10 nm`, `initial`, `12 V`, y-axis `Reflectance`, and values matching
  the `d_10nm` text tables.
- `/Users/joegarbarino/Desktop/Research Optics/Thesis/Figures/photo 10 nm SiO2 in situ.png`
  shows CompleteEASE in-situ dynamic data at 529.0 nm on the same approximate
  value scale as the text export.

Text-table checks:

| File | Timestamp Header | Value at 529 nm | Value at 550 nm |
| --- | --- | ---: | ---: |
| `d_10nm_initial.txt` | `Spectroscopic Data at 3.081 min.` | 0.260890 | 0.272113 |
| `d_10nm_12V.txt` | `Spectroscopic Data at 5.041 min.` | 0.265188 | 0.276447 |
| `30_20_10 reflectance.txt` | `Spectroscopic Data at 13.069 min.` | 0.265175 | 0.276347 |

The `d_10nm` initial and 12 V traces over 400-900 nm have a mean absolute
difference of about `0.00618`, max absolute difference about `0.009999`, and
correlation `0.999990`.

The `30_20_10 reflectance.txt` trace is extremely close to `d_10nm_12V` over
400-900 nm, with mean absolute difference about `0.000516` and correlation
`0.999968`, but the timestamp and folder provenance differ. This is similarity
evidence, not identity evidence.

Notebook evidence for `30_20_10`:

- `/Users/joegarbarino/Desktop/Research Optics/Coding/notebooks/AFRL 6E - Reflectance using p- s-.ipynb`
  reads `30_20_10 p_s intensity.txt`.
- A later code/comment cell describes the modeled structure as a three-layer
  quartz substrate stack with layer 1 `30 nm TiN`, layer 2 `10 nm SiO2`, and
  layer 3 `20 nm TiN`.

## Remaining Blockers

- The text exports still label the y-axis column as `Intensity`.
- No source found yet states that the text `Intensity` column is absolute
  calibrated reflectance.
- No source found yet proves `30_20_10 reflectance.txt` is the exact thesis
  Figure 4.1 / `d_10nm_12V` export.
- No future threshold policy has been approved before residual inspection.
