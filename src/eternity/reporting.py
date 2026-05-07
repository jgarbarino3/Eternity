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

    report_path.write_text(
        f"""# {spec.experiment_id} Report

## Summary

Question: {spec.question}

Hypothesis: {spec.hypothesis}

This is a synthetic V0 linear thin-film run. It is useful for exercising the
Eternity research pipeline, but it is not evidence of nonlinear ENZ dynamics or
new physics.

## Model

- Simulator: `{spec.simulator.name}` version `{spec.simulator.version}`
- Model level: `{result.metrics["model_level"]}`
- Material: synthetic `{spec.sample.material}`
- Film thickness: `{spec.sample.thickness.value} {spec.sample.thickness.unit}`
- Spec hash: `{spec_hash}`

## Metrics

```json
{metrics_json}
```

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

- Replace the synthetic ITO model with fitted ellipsometry data.
- Compare this linear baseline against measured transmission/reflection.
- Keep nonlinear ENZ, hot-electron, roughness, detector, and pump-probe effects out of V0 claims.
""",
        encoding="utf-8",
    )
    return report_path
