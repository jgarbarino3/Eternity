# Phase 3A.6 CompleteEASE Re-export / Measurement Packet

Date: 2026-05-16

## Purpose

This packet defines the minimum source evidence needed to use thesis
`d_10nm` / `3L2` RC2 traces as absolute reflectance in a future Eternity
validation run.

Current decision before this packet is satisfied:

- normalization basis: `relative_intensity_only`;
- claim ceiling: `weak_within_dataset_holdout`;
- existing run `run_f35a15cef565fb15`: historical only;
- calibrated promotion: blocked.

This packet is not approval to promote any existing run. It is a checklist for
future source recovery, re-export, or re-measurement.

## Required Sample Identity

The source record must identify the sample without relying on filename
guesswork.

Required fields:

- sample label: `3L2` or explicitly mapped equivalent;
- substrate: `Quartz`;
- incident-order stack: `air / 20 nm TiN / 10 nm SiO2 / 30 nm TiN / quartz`;
- thesis table or lab-note reference tying the label to the stack;
- whether the record refers to `d_10nm_initial`, `d_10nm_12V`, both, or a new
  measurement.

Acceptance rule:

- Pass only if the sample label and stack are explicit in the source record or
  in an attached source note with path/hash.
- Fail if the only link is a filename such as `30_20_10`.

## Required Acquisition Geometry

Required fields:

- instrument: J.A. Woollam RC2 or equivalent source;
- software/source environment: CompleteEASE, Woollam project, exported table,
  debug bundle, lab note, or new measurement note;
- angle of incidence: `60 deg`;
- polarization: `S`, `TE`, or source-backed equivalent;
- wavelength grid and units;
- acquisition mode: static spectrum, in-situ dynamic trace, or both;
- bias state: initial/no-bias, `12 V`, or explicit new condition.

Acceptance rule:

- Pass only if angle and polarization are source-backed.
- Fail if angle or polarization is inferred only from neighboring thesis text.

## Required Normalization And Units

Required fields:

- exported channel name exactly as shown by the source system;
- exported units exactly as shown by the source system;
- whether values are absolute reflectance fraction, percent reflectance, raw
  detector intensity, normalized intensity, or arbitrary-unit intensity;
- calibration/baseline state used by the RC2/CompleteEASE workflow;
- any reference scan, baseline, mirror, dark correction, or sample alignment
  procedure needed to interpret the exported values;
- whether the exported table is directly comparable to TMM reflectance.

Acceptance rule for absolute reflectance:

- Pass only if the source says the exported values are absolute reflectance or
  gives enough calibration/baseline metadata to justify direct comparison to
  TMM reflectance.
- Fail if the source only says `Intensity`, `p-Intensity`, `s-Intensity`, or
  reflective intensity without units/calibration state.

## Required Artifact Provenance

For every recovered or newly produced file, record:

- original absolute path;
- copied immutable raw path, if copied into `lab_data/raw`;
- SHA-256 hash;
- byte count;
- export timestamp or measurement date, if available;
- operator/source note;
- relation to existing artifacts:
  - `thesis_reflectance_d_10nm_initial`;
  - `thesis_reflectance_d_10nm_12V`;
  - `phase3a_30_20_10_candidate`;
  - new artifact ID.

Acceptance rule:

- Pass only if the source file identity can be frozen with hash and path.
- Fail if the source is only a screenshot or plot unless it is explicitly
  registered as `digitized_from_plot` and kept out of absolute-calibrated
  promotion.

## Decision Outcomes

Allowed outcomes:

- `absolute_reflectance_evidence_found`: a future absolute-reflectance run may
  be prepared after thresholds are approved before the run.
- `relative_intensity_policy_only`: source evidence supports relative/shape
  diagnostics but not absolute reflectance.
- `blocked_needs_new_export`: no source-backed interpretation exists; request a
  new export or measurement.
- `new_measurement_required`: source data cannot be trusted or recovered.

No outcome from this packet may retroactively promote
`run_f35a15cef565fb15`.

## Request To Experimentalist Or Future Self

Please provide one of:

1. The original CompleteEASE/Woollam project or snapshot for the `3L2` / `d_10nm`
   spectra.
2. A fresh CompleteEASE export of S-polarized 60-degree reflectance for the
   `3L2` / 10 nm SiO2 sample, with channel name and units visible.
3. A lab note or export recipe stating how the existing `Intensity` column was
   produced and whether it is absolute reflectance, normalized reflectance, or
   raw/relative intensity.
4. A new measured reflectance table with incident/reference measurement notes.

Required accompanying note:

```text
Sample:
Stack:
Substrate:
Instrument/software:
Measurement date:
Operator:
Angle:
Polarization:
Bias state:
Channel name:
Units:
Calibration/baseline procedure:
Does this table represent absolute reflectance directly comparable to TMM?:
Original file path:
Any export settings:
```
