# Measurement Schema Contract

Measurements must declare raw artifact reference, sample, stack, axis quantity,
axis unit, y quantity, y unit, uncertainty type, incidence angle, polarization,
instrument or source notes, preprocessing, and whether the data are forbidden
for fitting.

Ellipsometry records should store measured psi and delta separately from any
derived `n,k`.

Multi-channel tables must name every channel explicitly. `epsilon_table`
records use `epsilon_real` and `epsilon_imag` channel mappings. `nk_table`
records use `n` and `k`. `ellipsometry_psi_delta` records use `psi` and
`delta`. Single-channel reflectance/transmission records may still use one
primary y column.

TiN/TiON optical constants are derived material-response inputs unless raw
ellipsometry psi/delta provenance is present. Thesis reflectance exports are
measured spectra, but their geometry, normalization, polarization, and stack
notes must be reconciled before they can serve as calibrated holdout evidence.

For Phase 3A, d=10 nm TiN/SiO2 thesis measurements are mapped to
`3L2/Quartz` with 60-degree TE/S-polarized geometry. Their exported
`Intensity` columns are `reflectance_intensity` with unit `arb` until absolute
reflectance calibration is source-confirmed. The `30_20_10` reflectance, p/s
intensity, Psi/Delta, and e1/e2 exports are unresolved candidate-bundle records
and must remain forbidden for fitting.

Phase 3A.7 may register CompleteEASE/Woollam source candidates by path, hash,
archive member, and readable metadata. Those records strengthen provenance, but
they do not change measurement units or normalization unless the source
explicitly proves calibrated absolute reflectance.
