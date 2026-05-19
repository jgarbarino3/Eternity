# Phase 3E.2C - Wang Bounded De-Offseted Reproduction Fixture

## Decision

- Status: `bounded_deoffset_reproduction_fixture_ready`
- Claim-status ceiling: `literature_reproduction_fixture`
- Full no-fit TMM validation allowed: `False`
- Recommended next phase: `Phase 3E.2D - Wang lane claim-boundary and assistant handoff`

This fixture lets the assistant parse stacked source-data plots, record inferred line semantics, and compute bounded diagnostics while preserving the calibrated-evidence gate.

## Fixture Contract

- Fixture kind: `source_data_reproduction_not_validation`
- De-offset rule: add 420, 350, 280, 210, 140, 70, and 0 percent offsets across the stacked thickness groups
- Measured column rule: first y column per thickness pair is inferred measured
- Simulated column rule: second y column per thickness pair is inferred simulated

## Diagnostics

- Row count: `3017`
- Global MAE: `3.118` percent
- Global RMSE: `4.039` percent
- Global max absolute residual: `21.897` percent

| Thickness nm | Points | MAE percent | RMSE percent | Max abs percent |
| --- | ---: | ---: | ---: | ---: |
| 152 | 431 | 3.225 | 4.007 | 20.131 |
| 163 | 431 | 3.805 | 4.733 | 17.740 |
| 185 | 431 | 2.953 | 3.582 | 8.674 |
| 200 | 431 | 3.004 | 3.564 | 12.488 |
| 215 | 431 | 2.829 | 3.607 | 18.180 |
| 233 | 431 | 2.114 | 3.688 | 21.897 |
| 250 | 431 | 3.898 | 4.857 | 16.047 |

## Forbidden Uses

- calibrated_linear_evidence
- ENZ evidence
- absolute reflectance validation
- proof that the source simulation was independent of Fig. 2f tuning
