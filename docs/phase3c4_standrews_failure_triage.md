# Phase 3C.4 - St Andrews Failure Triage

## Decision

- Status: `failure_triaged_no_promotion`
- Leading failure mode: `source_model_or_material_pairing_mismatch`
- Can feed serious core: `False`
- Can promote calibrated evidence: `False`
- Phase 4 ready: `False`
- Next phase: `Phase 3C.5 - St Andrews source-model parity diagnostic`

## Current Failure

- Run: `run_f6ea582618328f44`
- Selected material member: `TiN-data_Pure/Ellipsometry/50nm-MTiN-50c.txt`
- Metrics: MAE `0.0847482`, RMSE `0.178247`, max residual `0.697624`, dip offset `-141.93` nm, shape corr `-0.111454`
- Failed metrics: `mean_absolute_error`, `root_mean_square_error`, `max_absolute_residual`, `dip_wavelength_offset_nm`, `shape_correlation_minmax`

## Dominant Residual Windows

- `400-450 nm`: MAE `0.573834`, bias `-0.573834`, prediction mean `0.199401`, measurement mean `0.773234`.
- `450-500 nm`: MAE `0.202755`, bias `-0.202755`, prediction mean `0.216202`, measurement mean `0.418958`.

## Diagnostic Sweeps

- Best RMSE material-table diagnostic: `TiN-data_Pure/Ellipsometry/50nm TiN-RoomTemp.txt` with MAE `0.116124`, RMSE `0.175763`, max residual `0.616257`, dip offset `-141.93` nm, shape corr `-0.765624`.
- Best selected-table thickness diagnostic: `55 nm` with MAE `0.0857787`, RMSE `0.177973`, max residual `0.701976`, dip offset `-141.93` nm, shape corr `-0.12786`.
- Best selected-table substrate-index diagnostic: `n=1.7` with MAE `0.0876396`, RMSE `0.177379`, max residual `0.700546`, dip offset `-141.93` nm, shape corr `-0.157764`.

### Alternate Material Tables

| Candidate | RMSE | MAE | Dip offset nm | Shape corr | Threshold status |
| --- | ---: | ---: | ---: | ---: | --- |
| `TiN-data_Pure/Ellipsometry/50nm TiN-RoomTemp.txt` | `0.175763` | `0.116124` | `-141.93` | `-0.765624` | `fail` |
| `TiN-data_Pure/Ellipsometry/50nm-MTiN-50c.txt` | `0.178247` | `0.0847483` | `-141.93` | `-0.111455` | `fail` |
| `TiN-data_Pure/Ellipsometry/50 nm-MTiN-Anntemp-50C.txt` | `0.18228` | `0.0875438` | `-91.63` | `0.0264106` | `fail` |
| `TiN-data_Pure/Ellipsometry/50nm-MTiN-40c.txt` | `0.192254` | `0.155827` | `-141.93` | `-0.0713093` | `fail` |
| `TiN-data_Pure/Ellipsometry/50nm-MTiN-60c.txt` | `0.221442` | `0.177482` | `60.24` | `0.540821` | `fail` |

### Thickness Sweep

| Candidate | RMSE | MAE | Dip offset nm | Shape corr | Threshold status |
| --- | ---: | ---: | ---: | ---: | --- |
| `55 nm` | `0.177973` | `0.0857787` | `-141.93` | `-0.12786` | `fail` |
| `50 nm` | `0.178247` | `0.0847483` | `-141.93` | `-0.111455` | `fail` |
| `60 nm` | `0.179369` | `0.0889978` | `-141.93` | `-0.140777` | `fail` |
| `45 nm` | `0.181001` | `0.0902157` | `-141.93` | `-0.0918177` | `fail` |
| `65 nm` | `0.181751` | `0.0926351` | `-141.93` | `-0.150152` | `fail` |
| `70 nm` | `0.184591` | `0.0957464` | `-141.93` | `-0.156098` | `fail` |

### Substrate-Index Sweep

| Candidate | RMSE | MAE | Dip offset nm | Shape corr | Threshold status |
| --- | ---: | ---: | ---: | ---: | --- |
| `n=1.7` | `0.177379` | `0.0876396` | `-141.93` | `-0.157764` | `fail` |
| `n=1.8` | `0.177412` | `0.0900153` | `-141.93` | `-0.172815` | `fail` |
| `n=1.6` | `0.177551` | `0.0858423` | `-141.93` | `-0.140875` | `fail` |
| `n=1.52` | `0.177853` | `0.0850099` | `-141.93` | `-0.12585` | `fail` |
| `n=1.5` | `0.177952` | `0.0848873` | `-141.93` | `-0.121862` | `fail` |
| `n=1.45` | `0.178247` | `0.0847483` | `-141.93` | `-0.111455` | `fail` |

## Findings

- `failure_is_not_a_near_miss`: All Phase 3C.3 thresholds failed, including shape correlation and dip offset. The strongest residual concentration is at the blue edge.
- `blue_edge_residual_dominates`: The 400-450 nm segment has the largest mean absolute residual, while the 500-850 nm middle bands are much closer.
- `alternate_tables_do_not_repair_the_lane`: No candidate St Andrews epsilon table passes the locked thresholds. Some alternatives improve one diagnostic, but degrade others.
- `simple_substrate_or_thickness_changes_are_not_decisive`: The selected-table thickness and substrate-index sweeps do not move the predicted dip to the measured dip or restore the required shape correlation.
- `source_model_parity_is_the_next_clean_question`: The paper and archive point to Woollam ellipsometry modeling with glass substrate and roughness information, while the current clean run uses a single flat TiN layer on lossless n=1.45 glass.

## Boundary

Phase 3C.4 is a diagnostic failure triage. It may rank likely failure causes, but it cannot tune thresholds, select a replacement model using the holdout, feed the serious core, or promote calibrated_linear_evidence.
