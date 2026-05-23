"""Phase 3E.3B Saha frozen-stack provenance and no-fit adapter gate."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from eternity.phase3e3a import DEFAULT_RAW_DIR

DEFAULT_PHASE3E3A_AUDIT_PATH = Path("docs/phase3e3a_saha_exported_table_audit.json")


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _source_evidence() -> dict[str, Any]:
    return {
        "article_url": "https://www.nature.com/articles/s41467-023-41377-5",
        "supplementary_pdf_url": (
            "https://static-content.springer.com/esm/"
            "art%3A10.1038%2Fs41467-023-41377-5/"
            "MediaObjects/41467_2023_41377_MOESM1_ESM.pdf"
        ),
        "figshare_api_url": "https://api.figshare.com/v2/articles/23734116",
        "paper_and_figshare_support": [
            (
                "The article/Fig. 2 source context supports a 250 nm AZO layer on "
                "130 nm TiN on silicon, with Fig. 2b measured and simulated 50 degree "
                "s/p reflectance spectra."
            ),
            (
                "Figshare describes Fig. 2b as simulated Rp/Rs and experimentally "
                "measured reflectance versus wavelength, and Fig. 2c/d as TiN/AZO "
                "permittivity tables with film thickness comments."
            ),
            (
                "The supplementary information says TiN films were measured by VASE "
                "at 50 and 70 degrees and modeled with a Drude-Lorentz form."
            ),
            (
                "The supplementary information says AZO was grown on TiN layers on "
                "silicon, and also discusses AZO on silicon/fused-silica comparison "
                "samples."
            ),
        ],
        "missing_for_frozen_tmm_contract": [
            "No source table or methods text found here freezes silicon optical constants.",
            (
                "No source table or methods text found here specifies silicon substrate "
                "thickness, backside polish/roughness/wedge, or coherent/incoherent "
                "backside treatment."
            ),
            (
                "No complete source TMM settings file is published with the Fig. 2b "
                "source-simulated curves."
            ),
        ],
    }


def build_phase3e3b_packet(
    phase3e3a_audit_path: Path = DEFAULT_PHASE3E3A_AUDIT_PATH,
    raw_dir: Path = DEFAULT_RAW_DIR,
) -> dict[str, Any]:
    if not phase3e3a_audit_path.exists():
        raise FileNotFoundError(phase3e3a_audit_path)
    phase3e3a = _load_json(phase3e3a_audit_path)
    decision = phase3e3a["decision"]
    if decision["status"] != "canonical_tables_ready_tmm_adapter_blocked":
        raise ValueError(
            "Phase 3E.3B requires the completed Phase 3E.3A Saha table audit"
        )

    artifacts = phase3e3a["artifacts"]
    required_artifacts = {
        "fig2b_measured_reflectance",
        "fig2b_source_simulated_reflectance",
        "fig2cd_tin_epsilon",
        "fig2cd_azo_epsilon",
    }
    missing_artifacts = sorted(required_artifacts - set(artifacts))
    if missing_artifacts:
        raise ValueError(f"Phase 3E.3A audit is missing artifacts: {missing_artifacts}")
    for artifact in artifacts.values():
        path = Path(artifact["path"])
        if not path.exists():
            raise FileNotFoundError(path)

    source_evidence = _source_evidence()
    contract_items = {
        "canonical_measured_reflectance": {
            "status": "pass",
            "basis": (
                "Phase 3E.3A produced a measured-only Fig. 2b Rp/Rs canonical CSV "
                "with source labels preserved."
            ),
        },
        "canonical_material_epsilon": {
            "status": "pass",
            "basis": (
                "Phase 3E.3A produced separate TiN and AZO epsilon canonical CSVs "
                "from the Fig. 2c/d source table."
            ),
        },
        "stack_order_and_thickness": {
            "status": "pass_for_source_semantics",
            "basis": (
                "Paper/source evidence supports air/AZO/TiN/silicon with 250 nm "
                "AZO and 130 nm TiN."
            ),
        },
        "incidence_and_polarization": {
            "status": "pass",
            "basis": "Fig. 2b source labels preserve 50 degree p/s reflectance channels.",
        },
        "silicon_substrate_material": {
            "status": "partial",
            "basis": (
                "The source identifies silicon as the substrate, but does not publish "
                "the silicon optical-constant table or model used for Fig. 2b."
            ),
        },
        "silicon_optical_constants": {
            "status": "blocked",
            "basis": (
                "Any choice of Palik/Green/Aspnes/crystalline-Si constants would be an "
                "external predeclared assumption, not a source-backed Saha Fig. 2 "
                "contract."
            ),
        },
        "substrate_backside_and_coherence": {
            "status": "blocked",
            "basis": (
                "The source does not freeze substrate thickness, backside condition, "
                "wedge/roughness, or coherent versus incoherent backside handling."
            ),
        },
        "interface_roughness_or_native_oxide": {
            "status": "not_source_backed",
            "basis": (
                "No source-backed interfacial roughness, native oxide, or EMA layer "
                "contract was found for a no-fit adapter."
            ),
        },
        "source_model_leakage_boundary": {
            "status": "partial_not_promotion_clean",
            "basis": (
                "Measured and source-simulated Fig. 2b curves are separable, but the "
                "article/source package includes author simulations and does not publish "
                "a full model-settings file or a promotion-clean calibration/holdout split."
            ),
        },
    }
    blocked_items = [
        item_id
        for item_id, item in contract_items.items()
        if item["status"] in {"blocked", "not_source_backed"}
    ]

    return {
        "phase_id": "Phase 3E.3B",
        "title": "Saha Frozen-Stack Model Provenance And No-Fit Adapter Gate",
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "inputs": {
            "phase3e3a_audit_path": str(phase3e3a_audit_path),
            "raw_dir": str(raw_dir),
            "phase3e3a_status": decision["status"],
            "phase3e3a_claim_status_ceiling": decision["claim_status_ceiling"],
        },
        "source_evidence": source_evidence,
        "phase3e3a_artifacts": artifacts,
        "contract_items": contract_items,
        "blocked_items": blocked_items,
        "decision": {
            "status": "frozen_stack_contract_not_source_backed_tmm_blocked",
            "claim_status_ceiling": "weak_within_dataset_holdout",
            "current_claim_label": "source_tables_audited_stack_contract_blocked",
            "adapter_contract_frozen": False,
            "full_no_fit_tmm_validation_allowed": False,
            "residual_modeling_performed": False,
            "phase4_candidate": False,
            "serious_core_allowed": False,
            "stop_rule_triggered": True,
            "stop_rule_reason": (
                "Stop before TMM residual modeling: silicon optical constants, "
                "substrate/backside/coherence handling, and source-model leakage "
                "boundaries are not source-backed tightly enough to freeze a no-fit "
                "adapter without guessing."
            ),
            "recommended_next_phase": (
                "Phase 3E.4 - renewed ENZ public-data search through stack-contract gate"
            ),
        },
        "forbidden_next": [
            "Do not run Saha TMM residuals from a convenience silicon optical-constant table.",
            "Do not tune substrate constants, backside handling, roughness, scale, or offsets.",
            "Do not use source-simulated Fig. 2b curves as an independent holdout.",
            (
                "Do not promote Saha above weak-within-dataset holdout without a future "
                "predeclared source-backed stack contract and uncertainty policy."
            ),
        ],
    }


def phase3e3b_markdown(packet: dict[str, Any]) -> str:
    decision = packet["decision"]
    lines = [
        "# Phase 3E.3B - Saha Frozen-Stack Model Provenance And No-Fit Adapter Gate",
        "",
        "## Decision",
        "",
        f"- Status: `{decision['status']}`",
        f"- Claim-status ceiling: `{decision['claim_status_ceiling']}`",
        f"- Current claim label: `{decision['current_claim_label']}`",
        f"- Adapter contract frozen: `{str(decision['adapter_contract_frozen']).lower()}`",
        (
            "- Full no-fit TMM validation allowed: "
            f"`{str(decision['full_no_fit_tmm_validation_allowed']).lower()}`"
        ),
        (
            "- Residual modeling performed: "
            f"`{str(decision['residual_modeling_performed']).lower()}`"
        ),
        f"- Stop rule triggered: `{str(decision['stop_rule_triggered']).lower()}`",
        f"- Recommended next phase: `{decision['recommended_next_phase']}`",
        "",
        decision["stop_rule_reason"],
        "",
        "## Stack-Contract Items",
        "",
    ]
    for item_id, item in packet["contract_items"].items():
        lines.extend(
            [
                f"- `{item_id}`: `{item['status']}`",
                f"  - {item['basis']}",
            ]
        )
    lines.extend(
        [
            "",
            "## Source Evidence",
            "",
            f"- Article: {packet['source_evidence']['article_url']}",
            f"- Supplementary information: {packet['source_evidence']['supplementary_pdf_url']}",
            f"- Figshare API: {packet['source_evidence']['figshare_api_url']}",
            "",
            "Source-backed support:",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in packet["source_evidence"]["paper_and_figshare_support"])
    lines.extend(["", "Missing for a frozen no-fit TMM contract:", ""])
    lines.extend(
        f"- {item}" for item in packet["source_evidence"]["missing_for_frozen_tmm_contract"]
    )
    lines.extend(["", "## Forbidden Next", ""])
    lines.extend(f"- {item}" for item in packet["forbidden_next"])
    lines.append("")
    return "\n".join(lines)


def write_phase3e3b_packet(output_dir: Path, packet: dict[str, Any]) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase3e3b_saha_stack_model_gate.json"
    md_path = output_dir / "phase3e3b_saha_stack_model_gate.md"
    json_path.write_text(json.dumps(packet, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(phase3e3b_markdown(packet), encoding="utf-8")
    return json_path, md_path
