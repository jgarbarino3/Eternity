# Phase 3A.2 Stack Mapping Correction

Date: 2026-05-16

## Decision

Keep the thesis `d_10nm` validation candidate mapped to `3L2/Quartz`, but remove
the separate `30_20_10` Coding/txt exports from that candidate.

The thesis supports:

- Table 4.1: `3L2/Quartz = 30 nm TiN / 10 nm SiO2 / 20 nm TiN`.
- Figure 4.1: in-situ S-polarized reflectance for the 10 nm SiO2 three-layer
  sample, with and without 12 V bias.
- Chapter 2 setup text: RC2 optical measurements at 60 degrees.

The thesis and appendix do not source-confirm that the local
`Research Optics/Coding/txt/30_20_10 ...` files are the exact `d_10nm` thesis
plot exports. Those files remain registered, but under
`phase3a_30_20_10_candidate`.

## Consequences

- `thesis_d_10nm_phase3a_validation_candidate` now uses only the thesis
  `d_10nm_initial` holdout plus `d_10nm_12V` as biased-state auxiliary data.
- `30_20_10` reflectance, p/s intensity, Psi/Delta, and e1/e2 files are
  provenance artifacts, not validation evidence for `thesis_d_10nm`.
- The validation candidate is still blocked from calibrated promotion by
  normalization and threshold gates.

## Open Questions

- Are the `d_10nm_initial` and `d_10nm_12V` text files direct exports from the
  thesis Figure 4.1 spectra?
- Are the `Intensity` columns absolute reflectance, normalized reflectance, or
  instrument intensity?
- Can any Woollam project file or plotting script connect `30_20_10` filenames
  to a specific sample, substrate, and layer order?
