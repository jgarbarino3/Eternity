"""Phase 3E.4 renewed public-data search through the stack-contract gate."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

DEFAULT_REGISTRY_PATH = Path("docs/phase3e1_dataset_candidate_registry.yaml")


STACK_CONTRACT_FLAGS = {
    "source_backed_material_constants": (
        "optical constants or model parameters are public and tied to the sample"
    ),
    "independent_measured_holdout": (
        "measured R/T/A or ellipsometry holdout is separable from calibration data"
    ),
    "machine_readable_tables": "numerical data are tables, arrays, or scripts, not plots only",
    "measurement_geometry": "angle, polarization, side, and units are source-backed",
    "stack_order_and_thickness": "layer order, thicknesses, and sample identity are source-backed",
    "substrate_optical_contract": "substrate optical constants/model are source-backed",
    "backside_coherence_contract": (
        "substrate backside, thickness, wedge/roughness, and coherence treatment are source-backed"
    ),
    "leakage_boundary": (
        "source model and measured holdout can be used without residual-driven tuning"
    ),
    "planar_tmm_regime": "the measurement is physically suitable for the current linear planar TMM",
}


def _lead_cards() -> list[dict[str, Any]]:
    return [
        {
            "lead_id": "acs_intracavity_ito_2025_zenodo_data",
            "title": "Intracavity Epsilon-Near-Zero Dual-Range Frequency Switch",
            "material_family": "ITO",
            "source_urls": [
                "https://zenodo.org/records/14236212",
                "https://pubs.acs.org/doi/10.1021/acsphotonics.4c01322",
            ],
            "source_refs": [
                "DOI 10.1021/acsphotonics.4c01322",
                "Zenodo DOI 10.5281/zenodo.14236212",
            ],
            "inspection": [
                "Zenodo exposes Zenodo_Data.zip with MD5 41d93af8f27d62a2474ee06fbc9b1ce8.",
                (
                    "The ZIP has 31 MATLAB-oriented members, including article figure scripts, "
                    "Data_ellipsometer_FP_2um.mat, Data_TMM_TRA_diff_thickness.mat, and "
                    "Data_OSA_OSC.mat."
                ),
                (
                    "This corrects the older global registry wording that treated the ACS "
                    "intracavity lane as only public PDF/SI."
                ),
            ],
            "gate": {
                "source_backed_material_constants": "partial",
                "independent_measured_holdout": False,
                "machine_readable_tables": True,
                "measurement_geometry": "partial",
                "stack_order_and_thickness": "partial",
                "substrate_optical_contract": False,
                "backside_coherence_contract": False,
                "leakage_boundary": False,
                "planar_tmm_regime": False,
            },
            "decision": "zenodo_matlab_package_found_not_phase4_ready",
            "claim_label": "literature_reproduction_fixture",
            "reason": (
                "Useful source-code/data fixture, but not a clean independent static "
                "linear R/T/A holdout with frozen stack, substrate, backside, and "
                "leakage contracts."
            ),
        },
        {
            "lead_id": "linkoping_ito_pedot_2026",
            "title": (
                "Electrotunable coupling between an epsilon-near-zero thin film and "
                "conducting polymer nanoantennas"
            ),
            "material_family": "ITO/PEDOT metasurface",
            "source_urls": [
                "https://zenodo.org/records/18412236",
                "https://pubmed.ncbi.nlm.nih.gov/41671185/",
            ],
            "source_refs": [
                "DOI 10.1073/pnas.2517549123",
                "Zenodo DOI 10.5281/zenodo.18412236",
            ],
            "inspection": [
                (
                    "Zenodo exposes Figure 1/2/3/4 ZIPs; Figure 2 has measured and simulated "
                    "angle/polarization-dependent extinction spectra for a 50 nm ITO film on glass."
                ),
                (
                    "The final device lane is nanorod/ITO hybrid coupling, not a plain planar "
                    "thin-film validation target."
                ),
            ],
            "gate": {
                "source_backed_material_constants": "partial",
                "independent_measured_holdout": False,
                "machine_readable_tables": True,
                "measurement_geometry": True,
                "stack_order_and_thickness": "partial",
                "substrate_optical_contract": False,
                "backside_coherence_contract": False,
                "leakage_boundary": False,
                "planar_tmm_regime": False,
            },
            "decision": "table_ready_fixture_not_planar_phase4_candidate",
            "claim_label": "literature_reproduction_fixture",
            "reason": (
                "Good public source-data fixture for ENZ coupling and bare-film extinction, "
                "but the required material/holdout split and planar stack contract are not frozen."
            ),
        },
        {
            "lead_id": "ito_glass_sio2_optical_properties_2025",
            "title": "ITO, soda lime float glass and SiO2 buffer layer optical properties",
            "material_family": "ITO/glass/SiO2",
            "source_urls": ["https://zenodo.org/records/15055400"],
            "source_refs": [
                "DOI 10.5281/zenodo.15055400",
                "Documenting article DOI 10.1016/j.omx.2025.100408",
            ],
            "inspection": [
                (
                    "Zenodo exposes ITO, soda-lime glass, and SiO2 optical dispersion files; "
                    "ITO_20 Ohm_105 nm_e1e2.mat is a plain text e1/e2 table despite its extension."
                ),
                (
                    "No independent measured R/T/A holdout was found in the record "
                    "metadata or files inspected."
                ),
            ],
            "gate": {
                "source_backed_material_constants": True,
                "independent_measured_holdout": False,
                "machine_readable_tables": True,
                "measurement_geometry": False,
                "stack_order_and_thickness": "partial",
                "substrate_optical_contract": True,
                "backside_coherence_contract": False,
                "leakage_boundary": False,
                "planar_tmm_regime": True,
            },
            "decision": "constants_fixture_no_independent_holdout",
            "claim_label": "calibration_only_no_holdout",
            "reason": "Useful public optical-constants fixture; not a validation candidate.",
        },
        {
            "lead_id": "spacetime_synthetic_motion_ito_2025",
            "title": "Space-Time Optical Diffraction from Synthetic Motion",
            "material_family": "ITO",
            "source_urls": [
                "https://figshare.com/projects/Space-Time_Optical_Diffraction_from_Synthetic_Motion_-_Source_data/229662",
                "https://www.nature.com/articles/s41467-025-60159-9",
            ],
            "source_refs": [
                "DOI 10.1038/s41467-025-60159-9",
                "Figshare DOI 10.6084/m9.figshare.27925419.v3",
            ],
            "inspection": [
                (
                    "Figshare project 229662 contains article 27925419 with XLSX, NPZ, "
                    "and TXT source-data files for space-time diffraction measurements."
                ),
                (
                    "The inspected Fig. 2b workbook is diffraction efficiency versus "
                    "pump-probe delay, "
                    "and the NPZ/TXT files are nonlinear frequency-momentum data."
                ),
            ],
            "gate": {
                "source_backed_material_constants": False,
                "independent_measured_holdout": False,
                "machine_readable_tables": True,
                "measurement_geometry": True,
                "stack_order_and_thickness": "partial",
                "substrate_optical_contract": False,
                "backside_coherence_contract": False,
                "leakage_boundary": False,
                "planar_tmm_regime": False,
            },
            "decision": "nonlinear_source_data_fixture_no_static_holdout",
            "claim_label": "literature_reproduction_fixture",
            "reason": (
                "Public and table-ready, but it is a nonlinear diffraction package, "
                "not a static TMM holdout."
            ),
        },
        {
            "lead_id": "natural_enz_compendium_2025",
            "title": "Compendium of Natural Epsilon-Near-Zero Materials",
            "material_family": "mixed natural ENZ materials",
            "source_urls": [
                "https://acs.figshare.com/articles/dataset/Compendium_of_Natural_Epsilon-Near-Zero_Materials/29134854",
                "https://pubs.acs.org/doi/10.1021/acsphotonics.5c00199",
            ],
            "source_refs": [
                "DOI 10.1021/acsphotonics.5c00199",
                "Figshare DOI 10.1021/acsphotonics.5c00199.s002",
            ],
            "inspection": [
                (
                    "The Figshare source file is an XLSX compendium of n, k, Re(epsilon), "
                    "Im(epsilon), and quality metrics across spectral bands."
                ),
                "No sample-specific measured thin-film holdout or stack contract is present.",
            ],
            "gate": {
                "source_backed_material_constants": True,
                "independent_measured_holdout": False,
                "machine_readable_tables": True,
                "measurement_geometry": False,
                "stack_order_and_thickness": False,
                "substrate_optical_contract": False,
                "backside_coherence_contract": False,
                "leakage_boundary": False,
                "planar_tmm_regime": False,
            },
            "decision": "constants_compendium_not_validation_dataset",
            "claim_label": "calibration_only_no_holdout",
            "reason": "Good literature-memory fixture; not a sample-matched validation dataset.",
        },
        {
            "lead_id": "acs_lbsno_ferrell_berreman_2026",
            "title": "Active Tuning of the Ferrell-Berreman Mode of La-Doped BaSnO3",
            "material_family": "La-doped BaSnO3",
            "source_urls": [
                "https://acs.figshare.com/articles/journal_contribution/Active_Tuning_of_the_Ferrell-Berreman_Mode_of_La-Doped_BaSnO_sub_3_sub_/31618292"
            ],
            "source_refs": ["DOI 10.1021/acs.jpcc.5c07927"],
            "inspection": [
                "Figshare exposes only the ACS supporting-information PDF for this lead."
            ],
            "gate": {
                "source_backed_material_constants": "unknown",
                "independent_measured_holdout": False,
                "machine_readable_tables": False,
                "measurement_geometry": "unknown",
                "stack_order_and_thickness": "unknown",
                "substrate_optical_contract": False,
                "backside_coherence_contract": False,
                "leakage_boundary": False,
                "planar_tmm_regime": True,
            },
            "decision": "public_si_pdf_only",
            "claim_label": "blocked_source_data_lead",
            "reason": "Interesting ENZ/TCO-like lead, but not table-package-ready.",
        },
        {
            "lead_id": "enz_metal_oxide_reflectors_2024",
            "title": "Epsilon-Near-Zero Metal Oxide-Based Spectrally Selective Reflectors",
            "material_family": "metal oxide ENZ multilayer",
            "source_urls": [
                "https://acs.figshare.com/articles/journal_contribution/Epsilon-Near-Zero_Metal_Oxide-Based_Spectrally_Selective_Reflectors/26097966"
            ],
            "source_refs": ["DOI 10.1021/acsaom.4c00124"],
            "inspection": [
                "Figshare exposes only the ACS supporting-information PDF for this lead."
            ],
            "gate": {
                "source_backed_material_constants": "unknown",
                "independent_measured_holdout": False,
                "machine_readable_tables": False,
                "measurement_geometry": "unknown",
                "stack_order_and_thickness": "unknown",
                "substrate_optical_contract": False,
                "backside_coherence_contract": False,
                "leakage_boundary": False,
                "planar_tmm_regime": True,
            },
            "decision": "public_si_pdf_only",
            "claim_label": "blocked_source_data_lead",
            "reason": (
                "Potentially relevant reflector paper, but no public numerical source "
                "package was found."
            ),
        },
    ]


def _phase4_ready(lead: dict[str, Any]) -> bool:
    return all(value is True for value in lead["gate"].values())


def build_phase3e4_packet(registry_path: Path = DEFAULT_REGISTRY_PATH) -> dict[str, Any]:
    leads = _lead_cards()
    phase4_ready = [lead["lead_id"] for lead in leads if _phase4_ready(lead)]
    registry_candidate_count: int | None = None
    if registry_path.exists():
        try:
            import yaml

            payload = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
            registry_candidate_count = len(payload.get("candidates", []))
        except Exception:
            registry_candidate_count = None

    return {
        "phase_id": "Phase 3E.4",
        "title": "Renewed ENZ Public-Data Search Through Stack-Contract Gate",
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "inputs": {"registry_path": str(registry_path)},
        "objective": (
            "Find a public ENZ/TCO/TiN/AZO thin-film dataset that clears material, "
            "measured holdout, geometry, stack/substrate/backside, and leakage gates "
            "before residual inspection."
        ),
        "search_routes": [
            "Zenodo API query for epsilon-near-zero ITO reflectance optical constants",
            "Figshare API search for epsilon-near-zero reflectance ITO",
            "targeted Figshare project/API inspection for space-time ITO source data",
            (
                "targeted Zenodo record inspection for intracavity ITO, ITO/glass "
                "constants, and ITO/PEDOT"
            ),
            "targeted ACS Figshare metadata inspection for ENZ metal-oxide and LBSO leads",
        ],
        "stack_contract_flags": STACK_CONTRACT_FLAGS,
        "inspected_leads": leads,
        "summary": {
            "inspected_lead_count": len(leads),
            "phase4_candidate_count": len(phase4_ready),
            "phase4_candidate_ids": phase4_ready,
            "registry_candidate_count_at_generation": registry_candidate_count,
            "corrected_prior_leads": ["acs_intracavity_ito_2025_zenodo_data"],
            "strongest_new_nonpromoting_fixtures": [
                "acs_intracavity_ito_2025_zenodo_data",
                "linkoping_ito_pedot_2026",
                "ito_glass_sio2_optical_properties_2025",
            ],
        },
        "decision": {
            "status": "phase3e4_search_snapshot_no_phase4_candidate",
            "can_open_phase4_now": False,
            "can_feed_serious_core_now": False,
            "claim_standard_changed": False,
            "residual_modeling_performed": False,
            "tmm_adapter_started": False,
            "recommended_next_phase": (
                "Phase 3E.4 - continue renewed ENZ public-data search through "
                "the stack-contract gate"
            ),
        },
        "stop_rule": {
            "triggered": True,
            "reason": (
                "No inspected lead establishes the complete measured reflectance/geometry/"
                "stack/substrate/backside/leakage contract needed for no-fit TMM residual modeling."
            ),
        },
    }


def phase3e4_markdown(packet: dict[str, Any]) -> str:
    decision = packet["decision"]
    summary = packet["summary"]
    rows = [
        "| Lead | Label | Phase 4? | Decision |",
        "| --- | --- | --- | --- |",
    ]
    for lead in packet["inspected_leads"]:
        rows.append(
            "| "
            + lead["lead_id"]
            + " | `"
            + lead["claim_label"]
            + "` | "
            + ("yes" if _phase4_ready(lead) else "no")
            + " | `"
            + lead["decision"]
            + "` |"
        )

    lines = [
        "# Phase 3E.4 - Renewed ENZ Public-Data Search Through Stack-Contract Gate",
        "",
        "## Decision",
        "",
        f"- Status: `{decision['status']}`",
        f"- Can open Phase 4 now: `{str(decision['can_open_phase4_now']).lower()}`",
        f"- Can feed Serious Core now: `{str(decision['can_feed_serious_core_now']).lower()}`",
        f"- Claim standard changed: `{str(decision['claim_standard_changed']).lower()}`",
        f"- Residual modeling performed: `{str(decision['residual_modeling_performed']).lower()}`",
        f"- TMM adapter started: `{str(decision['tmm_adapter_started']).lower()}`",
        f"- Recommended next phase: `{decision['recommended_next_phase']}`",
        "",
        packet["objective"],
        "",
        "## Search Summary",
        "",
        f"- Inspected leads: `{summary['inspected_lead_count']}`",
        f"- Phase 4 candidates: `{summary['phase4_candidate_count']}`",
        (
            "- Corrected prior lead(s): "
            + ", ".join(f"`{item}`" for item in summary["corrected_prior_leads"])
        ),
        "",
        *rows,
        "",
        "## Stack-Contract Gate",
        "",
    ]
    lines.extend(
        f"- `{flag}`: {description}"
        for flag, description in packet["stack_contract_flags"].items()
    )
    lines.extend(["", "## Inspected Lead Notes", ""])
    for lead in packet["inspected_leads"]:
        lines.extend(
            [
                f"### {lead['lead_id']}",
                "",
                f"- Title: {lead['title']}",
                f"- Decision: `{lead['decision']}`",
                f"- Claim label: `{lead['claim_label']}`",
                f"- Reason: {lead['reason']}",
                "- Sources:",
            ]
        )
        lines.extend(f"  - {url}" for url in lead["source_urls"])
        lines.append("- Inspection:")
        lines.extend(f"  - {item}" for item in lead["inspection"])
        lines.append("")
    lines.extend(
        [
            "## Stop Rule",
            "",
            f"- Triggered: `{str(packet['stop_rule']['triggered']).lower()}`",
            f"- Reason: {packet['stop_rule']['reason']}",
            "",
        ]
    )
    return "\n".join(lines)


def write_phase3e4_packet(output_dir: Path, packet: dict[str, Any]) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase3e4_renewed_public_data_search.json"
    md_path = output_dir / "phase3e4_renewed_public_data_search.md"
    json_path.write_text(json.dumps(packet, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(phase3e4_markdown(packet), encoding="utf-8")
    return json_path, md_path
