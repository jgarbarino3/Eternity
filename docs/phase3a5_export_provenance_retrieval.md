# Phase 3A.5 Source-Backed Export / Provenance Retrieval

Date: 2026-05-16

## Decision

Status: `blocked_needs_new_export`.

Phase 3A.5 did not find source-backed local evidence tying the exact thesis
`d_10nm_initial.txt` and `d_10nm_12V.txt` dynamic traces to calibrated absolute
reflectance or `%R`. The operational normalization basis therefore remains
`relative_intensity_only`, and no Phase 3A run may promote to
`calibrated_linear_evidence` from these exports.

This is an evidence-retrieval decision, not a scientific rejection of the
measurement. The local record supports that the traces are measured RC2
reflectance-provenance data for the thesis `3L2/Quartz` path. It does not prove
that the exported `Intensity` columns are absolute-calibrated reflectance.

## Search Scope

Bounded read-only sources checked:

- `/Users/joegarbarino/Desktop/Research Optics`
- `/Users/joegarbarino/Desktop/SDSU Google Drive`
- `/Users/joegarbarino/Optics Research`
- targeted `/Users/joegarbarino/Downloads` hits whose filenames suggested
  Woollam, CompleteEASE, RC2, `d_10nm`, `3L2`, `Intensity`, `%R`, or
  reflectance provenance.
- targeted Google Drive searches for SDSU thesis drafts, thesis defense
  slides, lab-notebook language, `3L2`, and reflective-intensity provenance.

Tools used:

- `find`, `mdfind`, and `rg` for candidate discovery;
- `pdftotext` and `textutil` for thesis/report text inspection;
- `strings` and `unzip -l/-p` for Woollam binary/snapshot/archive inspection;
- slide-aware `.pptx` XML extraction for SDSU and thesis presentation decks;
- contact-sheet visual inspection of the image-only lab-notebook PDF;
- `shasum -a 256` for exact artifact identity checks.

## Candidate Hits

| Evidence path | SHA-256 | Classification | Finding |
| --- | --- | --- | --- |
| `/Users/joegarbarino/Desktop/Research Optics/Thesis/Data/d_10nm_initial.txt` | `c093c27d277841140f7655da72372e9ffc90b2abf030c5e358cd0c01d2b3bc21` | relative/intensity-only source table | Header is `Wavelength (nm)` / `Intensity`; no absolute `%R` metadata. |
| `/Users/joegarbarino/Desktop/Research Optics/Thesis/Data/d_10nm_12V.txt` | `0b4890786cbebe76d723447592ed67549a826e563a8d4a4c4970d33919be4819` | relative/intensity-only source table | Header is `Wavelength (nm)` / `Intensity`; no absolute `%R` metadata. |
| `/Users/joegarbarino/Optics Research/d_10nm_initial.txt` | `c093c27d277841140f7655da72372e9ffc90b2abf030c5e358cd0c01d2b3bc21` | duplicate source table | Byte-identical to the thesis data copy. |
| `/Users/joegarbarino/Optics Research/d_10nm_12V.txt` | `0b4890786cbebe76d723447592ed67549a826e563a8d4a4c4970d33919be4819` | duplicate source table | Byte-identical to the thesis data copy. |
| `/Users/joegarbarino/Desktop/Research Optics/Coding/txt/30_20_10 reflectance.txt` | `f708bf4abd2efe49a131f423aabcccd4f669d0a16a9a9d16de44ead3100bb9a8` | unresolved related export | Header uses `Intensity`; not source-linked to thesis `d_10nm` / `3L2`. |
| `/Users/joegarbarino/Desktop/Research Optics/Coding/txt/30_20_10 p_s intensity.txt` | `c47f552a0b166775ecfb1bfe700e3911738f43056e17b53bb91508cd94a665d7` | unresolved related export | Uses `p-Intensity` / `s-Intensity`, confirming intensity-channel labeling in this data family. |
| `/Users/joegarbarino/Desktop/Research Optics/Thesis/References/rc2-brochure.pdf` | `9787bf967d720d36eac0f31cc6b1076bbe69a538ffc4ce1ae42f727fcc98a780` | instrument capability context | Supports that RC2/CompleteEASE can acquire intensity/reflectance-style data; does not identify these exports as calibrated `%R`. |
| `/Users/joegarbarino/Desktop/Research Optics/Thesis/Checkpoints/Thesis Final.pdf` | `336e4ef902e7cc334e9dedc279143da653f218a5f444a85686eed60280ca752f` | thesis provenance | Supports RC2 reflectance/reflective-intensity thesis context, but not the exact export calibration state. |
| `/Users/joegarbarino/Optics Research/Thesis Multilayer experimental.ipynb` | `ce4ac7bc981160ba80cc577831015d6ca7238c825bf2a1e9c765a400178f4975` | notebook provenance | Reads local intensity-like spectra and plotting/modeling context; does not provide absolute `%R` export proof. |
| `/Users/joegarbarino/Desktop/Research Optics/AFRL/DoD/DoD SAFE-aCyVf5zQGhuzpg6f/RC-2.zip` | `02f9abec386e431d8b17897867144b4b6034c68683a64b1148a8b63aeeeebfad` | related Woollam archive | Contains many RC2 `.SE`/`.SEsnap` reflectivity and reflection-intensity files, including 3-layer cap tests; no exact `d_10nm` / `3L2/Quartz` export proof was found. |
| `/Users/joegarbarino/Desktop/SDSU Google Drive/drive-download-20241101T181943Z-001/AFRL TiN.pptx` | `eae10394853b62f51ca6103644e022369ce262f7036f44f255bb1100839a96cf` | SDSU slide provenance | Contains the long SDSU research-slide sequence. Slides include `30 nm TiN -> 10 nm SiO2 -> 20 nm TiN`, 3-layer reflectance modeling, and note that later model/data files used previous-sample TiN/SiO2 constants; no exact `d_10nm` absolute `%R` export proof. |
| `/Users/joegarbarino/Desktop/SDSU Google Drive/drive-download-20241101T181943Z-001/AFRL Final Report.docx` | `45f927ff7faf216e67700ecac4fc4a1f4afab40b60ef3c3514ca3bc638ce8b6f` | SDSU report provenance | States that the RC2 measured reflectance/permittivity and records Puck 4 Quartz as `30 nm TiN / 10 nm SiO2 / 20 nm TiN`; no exact export calibration metadata. |
| `/Users/joegarbarino/Desktop/SDSU Google Drive/drive-download-20241101T181943Z-001/Thesis Defense notes.docx` | `3f5a11960ab55586282b2526fd33c26fd1b5d5b42661c52d24a7bca5ec4df1d6` | SDSU notes provenance | Supports thesis-defense framing around RC2 ellipsometry and reflective-intensity measurements; no exact `%R` export proof. |
| `/Users/joegarbarino/Desktop/SDSU Google Drive/drive-download-20241101T181943Z-001/Optics Research.pptx` | `973d85012c74cb0449ae8cd50e9c744f1368ca8e3098ef5dc391051d353e5431` | unrelated/low-value slide hit | Six-slide local deck; no targeted `3L2`, RC2, reflective-intensity, or absolute-reflectance hits. |
| `/Users/joegarbarino/Desktop/Research Optics/Research notebook full.pdf` | `a84328bf068bba9bd0752855e5c8c349bb488c20ecee71d30417bcfd8386cbe5` | scanned lab notebook provenance | Image-only 101-page notebook. Visual scan found Puck/sample tables, reflective-intensity notes, later 3-layer thesis-correction notes, and explicit `Rs` / reflectance-model reminders, but no source-backed statement that the exact thesis `Intensity` exports are calibrated absolute `%R`. |
| `/Users/joegarbarino/Desktop/SDSU Google Drive/drive-download-20241101T181943Z-001/DoNotRepl_Sharpcopy@sdsu.edu_20240604_154120.pdf` | `f60f0dfaf9d054ea32fa21533a9d2d2dfd08daa7bdc1fa212a629ae9ba97f9a8` | image-only low-value PDF | One-page Sharpcopy PDF; text extraction produced no searchable provenance and it did not resolve the calibration question. |
| Google Drive search hits: `Thesis Draft 1 April 7 copy (dragged) (dragged) 1:2.pdf/.docx`, `Thesis Defense v12 June 4.pdf` | not copied into repo | cloud provenance | Search hits confirm thesis Table 4.1 `3L2/Quartz 30 nm TiN / 10 nm SiO2 / 20 nm TiN`, Figure 4.1 language as reflective intensity, and defense slide language as experimental S-polarized reflectance; no exact absolute `%R` export proof. |

## Supporting Evidence

Evidence supporting measured reflectance provenance:

- Thesis/report text says the J.A. Woollam RC2 was used to measure reflectance
  and permittivity over a wide wavelength range.
- The AFRL report records a quartz sample with `30 nm TiN / 10 nm SiO2 /
  20 nm TiN` and describes measured reflectance changes under 12 V.
- SDSU Google Drive thesis/report/deck hits independently support the same
  `3L2/Quartz` stack and thesis-defense framing as experimental S-polarized
  reflectance / reflective-intensity RC2 measurements.
- Visual inspection of the scanned lab notebook found relevant handwritten
  Puck/sample tables and later thesis-correction notes for three-layer
  reflectance modeling, including that some model files used older TiN/SiO2
  constants.
- Local thesis figures and Phase 3A.3 already align `d_10nm` with thesis
  Figure 4.1 and the `3L2/Quartz` stack.
- `RC-2.zip` contains nearby Woollam reflectivity/reflection-intensity project
  artifacts, showing the local folder family really does include RC2 source
  files.

Evidence blocking absolute `%R` promotion:

- The exact `d_10nm` exports label the measured channel `Intensity`, not
  `Reflectance` or `%R`.
- Nearby local exports use `p-Intensity` and `s-Intensity`, so `Intensity` is a
  genuine channel name rather than a harmless synonym introduced by the loader.
- Notebook code reads the tables as intensity-like columns and does not record
  calibration or export settings.
- The checked `.SE`/`.SEsnap`/archive hits are related to RC2 reflectivity work,
  but no recovered file ties the exact thesis `d_10nm` dynamic traces to an
  absolute reflectance export.
- The SDSU Google Drive slides, report, thesis drafts, and lab notebook add
  sample/stack and RC2-measurement provenance, but still do not state the
  export channel, units, calibration state, or CompleteEASE recipe for the
  exact `d_10nm` text files.

## Consequence For Phase 3A

Existing run `run_f35a15cef565fb15` remains historical and capped at
`weak_within_dataset_holdout`. It must not be judged by thresholds written after
its residuals were inspected.

Future Phase 3A validation can continue in two ways:

1. Recover or create source-backed absolute-reflectance evidence before a new
   run. Acceptable evidence includes a CompleteEASE/Woollam project file, export
   recipe, debug bundle, lab note, or newly exported table that records sample
   ID, angle, polarization, calibration state, channel name, and units.
2. Define a Pro/user-approved relative-only diagnostic policy. This can support
   shape/provenance diagnostics, but not `calibrated_linear_evidence`.

## Next Recommended Phase

Recommended next phase: `Phase 3A.6 - CompleteEASE Re-export / Measurement
Packet`.

Information sufficiency:

- Enough information exists to write the exact evidence request and keep the
  current validation candidate fail-closed.
- Not enough information exists to complete calibrated Phase 3A promotion.
- Not enough information exists to use `30_20_10` as thesis `d_10nm`
  validation evidence.

Reasoning recommendation under the current GPT-5.5 assumption:

- Planning: `high`, because the packet should prevent another ambiguous export.
- Implementation: `medium`, because it is mostly docs, checklists, and optional
  source-file intake if the export appears.
- Use `xhigh` before approving any absolute-normalization or residual-threshold
  policy.

Helpful tools:

- Available: local shell, `pdftotext`, `strings`, `shasum`, GPD
  planner/checker/verifier, and Consensus MCP for literature context on
  reflectance validation policy.
- Already checked in Phase 3A.5: local SDSU Google Drive folder, targeted
  Google Drive search hits, SDSU slides, thesis/report docs, and visual
  lab-notebook scan.
- Candidate only if local evidence remains insufficient: direct CompleteEASE
  re-export or recovery of the original Woollam project/debug bundle.
