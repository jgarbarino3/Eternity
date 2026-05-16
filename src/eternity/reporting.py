"""Plot and Markdown report generation for V0 runs."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from eternity.simulation import SimulationResult
from eternity.specs import ExperimentSpec


def write_plots(result: SimulationResult, plots_dir: Path) -> list[Path]:
    plots_dir.mkdir(parents=True, exist_ok=True)

    epsilon_path = plots_dir / "epsilon.png"
    plt.figure(figsize=(7, 4))
    plt.plot(result.wavelengths_nm, result.epsilon.real, label="Re(epsilon)")
    plt.plot(result.wavelengths_nm, result.epsilon.imag, label="Im(epsilon)")
    plt.axhline(0, color="black", linewidth=0.8)
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Dielectric function")
    plt.legend()
    plt.tight_layout()
    plt.savefig(epsilon_path, dpi=160)
    plt.close()

    nk_path = plots_dir / "nk.png"
    plt.figure(figsize=(7, 4))
    plt.plot(result.wavelengths_nm, result.refractive_index.real, label="n")
    plt.plot(result.wavelengths_nm, result.refractive_index.imag, label="k")
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Refractive index")
    plt.legend()
    plt.tight_layout()
    plt.savefig(nk_path, dpi=160)
    plt.close()

    tra_path = plots_dir / "tra.png"
    plt.figure(figsize=(7, 4))
    plt.plot(result.wavelengths_nm, result.transmission, label="Transmission")
    plt.plot(result.wavelengths_nm, result.reflection, label="Reflection")
    plt.plot(result.wavelengths_nm, result.absorption, label="Absorption")
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Fraction")
    plt.ylim(-0.05, 1.05)
    plt.legend()
    plt.tight_layout()
    plt.savefig(tra_path, dpi=160)
    plt.close()

    return [epsilon_path, nk_path, tra_path]


def write_report(
    spec: ExperimentSpec,
    result: SimulationResult,
    run_dir: Path,
    spec_hash: str,
    plot_paths: list[Path],
) -> Path:
    report_path = run_dir / "report.md"
    warnings = "\n".join(
        f"- **{warning['severity']}** from `{warning['source']}`: {warning['message']}"
        for warning in result.warnings
    )
    assumptions = "\n".join(f"- {assumption}" for assumption in result.assumptions)
    trusted = "\n".join(f"- {note}" for note in result.validity_notes["trusted"])
    untrusted = "\n".join(f"- {note}" for note in result.validity_notes["untrusted"])
    plots = "\n".join(f"- `{path.relative_to(run_dir)}`" for path in plot_paths)
    metrics_json = json.dumps(result.metrics, indent=2, sort_keys=True)
    model_level = result.metrics["model_level"]
    is_phase3a = model_level == "linear_tmm_registry_multilayer_phase3a_validation_candidate"
    is_tabulated = model_level == "linear_tmm_tabulated_epsilon_v1_grounding"
    if is_phase3a:
        claim_status = "weak_within_dataset_holdout"
        summary_note = (
            "This is a Phase 3A TiN/SiO2 validation-candidate run. It compares a frozen "
            "registry-backed multilayer TMM prediction with measured thesis reflectance, "
            "but it is not calibrated linear evidence until normalization and residual "
            "threshold gates are approved."
        )
        claim_note = (
            "This run cannot feed serious-core conclusions yet because the measured export "
            "is intensity-labeled and calibrated pass/fail thresholds are not predeclared."
        )
        follow_up = (
            "- Decide whether the thesis intensity export is comparable to absolute reflectance.\n"
            "- Predeclare residual thresholds before promoting any calibrated evidence.\n"
            "- Keep 12V, nonlinear, FROG, and pump-probe interpretations outside this claim."
        )
    elif is_tabulated:
        claim_status = "calibration_only_no_holdout"
        summary_note = (
            "This is a V1 real-data grounding run using registry-backed tabulated optical "
            "constants. It is not calibrated linear evidence because no independent measured "
            "R/T holdout is validated in this run."
        )
        claim_note = (
            "This run cannot feed serious-core conclusions yet because optical constants alone "
            "do not provide an independent measured R/T holdout or residual validation."
        )
        follow_up = (
            "- Recover or measure independent R/T for the same TiN/TiON sample and geometry.\n"
            "- Freeze the tabulated material model before comparing against any holdout.\n"
            "- Keep nonlinear ENZ, FROG, and pump-probe interpretations outside this claim."
        )
    else:
        claim_status = "synthetic_software_fixture"
        summary_note = (
            "This is a synthetic V0 linear thin-film run. It is useful for exercising the "
            "Eternity research pipeline, but it is not evidence of nonlinear ENZ dynamics "
            "or new physics."
        )
        claim_note = (
            "This run cannot feed serious-core conclusions because it uses synthetic inputs "
            "and no measured comparison or holdout data."
        )
        follow_up = (
            "- Replace the synthetic ITO model with fitted ellipsometry data.\n"
            "- Compare this linear baseline against measured transmission/reflection.\n"
            "- Keep nonlinear ENZ, hot-electron, roughness, detector, and pump-probe effects "
            "out of V0 claims."
        )

    report_path.write_text(
        f"""# {spec.experiment_id} Report

## Summary

Question: {spec.question}

Hypothesis: {spec.hypothesis}

{summary_note}

## Model

- Simulator: `{spec.simulator.name}` version `{spec.simulator.version}`
- Model level: `{result.metrics["model_level"]}`
- Material: `{spec.sample.material}`
- Film thickness: `{spec.sample.thickness.value} {spec.sample.thickness.unit}`
- Spec hash: `{spec_hash}`

## Metrics

```json
{metrics_json}
```

## Claim Status

`{claim_status}`

{claim_note}

## Plots

{plots}

## Assumptions

{assumptions}

## Warnings

{warnings}

## Validity Envelope

Trusted:

{trusted}

Not trusted:

{untrusted}

## Follow-Up

{follow_up}
""",
        encoding="utf-8",
    )
    return report_path
