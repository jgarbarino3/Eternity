"""Phase 3E.2D Wang claim-boundary and assistant handoff."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from eternity.phase3e2a import DEFAULT_RAW_DIR
from eternity.phase3e2b import build_phase3e2b_packet
from eternity.phase3e2c import build_phase3e2c_packet


def build_phase3e2d_packet(raw_dir: Path = DEFAULT_RAW_DIR) -> dict[str, Any]:
    semantics = build_phase3e2b_packet(raw_dir)
    fixture = build_phase3e2c_packet(raw_dir)
    return {
        "phase_id": "Phase 3E.2D",
        "title": "Wang Lane Claim Boundary And Assistant Handoff",
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "inputs": {
            "raw_dir": str(raw_dir),
            "semantics_status": semantics["decision"]["status"],
            "fixture_status": fixture["decision"]["status"],
        },
        "lane_decision": {
            "status": "wang_lane_fixture_complete_not_validation",
            "candidate_label": "literature_reproduction_fixture",
            "phase4_candidate": False,
            "phase4_enz_ready": False,
            "serious_core_allowed": False,
            "why_not_validation": [
                "Wang is W/WO3, not ENZ/TCO/TiN/AZO evidence.",
                (
                    "Fig2f-R.xlsx contains stacked plotted traces rather than plain "
                    "absolute reflectance columns."
                ),
                (
                    "Measured/simulated assignment is inferred from source caption "
                    "plus trace character, not workbook labels."
                ),
                (
                    "The source simulated curve may already include author modeling "
                    "choices and is not an independent holdout contract."
                ),
            ],
        },
        "assistant_capabilities_added": [
            "public source-data package intake",
            "XLSX chart/label absence detection",
            "stacked-plot de-offset fixture generation",
            "claim-label downgrade when semantics are incomplete",
            "machine-readable residual diagnostics for non-promoting source reproduction",
        ],
        "artifacts_expected": [
            "docs/phase3e2b_wang_fig2f_semantics_audit.json",
            "docs/phase3e2b_wang_fig2f_semantics_audit.md",
            "docs/phase3e2c_wang_deoffset_reproduction_fixture.json",
            "docs/phase3e2c_wang_deoffset_reproduction_fixture.md",
            "docs/phase3e2c_wang_deoffset_reproduction_fixture.csv",
            "docs/phase3e2d_wang_claim_boundary_handoff.json",
            "docs/phase3e2d_wang_claim_boundary_handoff.md",
        ],
        "next_search_policy": {
            "status": "resume_enz_data_search_or_opju_conversion_only_with_new_lead",
            "preferred_next_phase": (
                "Phase 3E.3 - ENZ public-data lead intake or Saha OPJU conversion "
                "if a real conversion path appears"
            ),
            "do_now_without_new_data": [
                "Use Wang only as a parser/fixture regression input.",
                "Keep Saha TiN/AZO parked until OPJU conversion becomes available.",
                "Accept a new Phase 4 candidate only when all public-dataset gate flags pass.",
            ],
            "stop_conditions": [
                "No new ENZ table-ready source-data package is available.",
                "Only plot/PDF/request-only data remain.",
                "A proposed next step would require weakening calibrated-linear standards.",
            ],
        },
        "decision": {
            "status": "phase3e2b_through_3e2d_complete",
            "goal_progress": (
                "requested Wang 3E.2B-3E.2D work is complete once artifacts are "
                "written and verified"
            ),
            "claim_standard_changed": False,
            "recommended_next_phase": (
                "Phase 3E.3 - gated ENZ data lead intake when new source data exists"
            ),
        },
    }


def phase3e2d_markdown(packet: dict[str, Any]) -> str:
    lane = packet["lane_decision"]
    next_policy = packet["next_search_policy"]
    decision = packet["decision"]
    return "\n".join(
        [
            "# Phase 3E.2D - Wang Claim Boundary And Assistant Handoff",
            "",
            "## Decision",
            "",
            f"- Status: `{decision['status']}`",
            f"- Candidate label: `{lane['candidate_label']}`",
            f"- Phase 4 candidate: `{lane['phase4_candidate']}`",
            f"- Serious core allowed: `{lane['serious_core_allowed']}`",
            f"- Claim standard changed: `{decision['claim_standard_changed']}`",
            f"- Recommended next phase: `{decision['recommended_next_phase']}`",
            "",
            "Wang now helps the project as a non-promoting public-data fixture. It improves "
            "the research assistant substrate, but it does not create calibrated linear evidence.",
            "",
            "## Why This Is Not Validation",
            "",
            *["- " + item for item in lane["why_not_validation"]],
            "",
            "## Assistant Capabilities Added",
            "",
            *["- " + item for item in packet["assistant_capabilities_added"]],
            "",
            "## Next Search Policy",
            "",
            f"- Status: `{next_policy['status']}`",
            f"- Preferred next phase: `{next_policy['preferred_next_phase']}`",
            "",
            "Do now without new data:",
            "",
            *["- " + item for item in next_policy["do_now_without_new_data"]],
            "",
            "Stop conditions:",
            "",
            *["- " + item for item in next_policy["stop_conditions"]],
            "",
        ]
    )


def write_phase3e2d_packet(output_dir: Path, packet: dict[str, Any]) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase3e2d_wang_claim_boundary_handoff.json"
    md_path = output_dir / "phase3e2d_wang_claim_boundary_handoff.md"
    json_path.write_text(json.dumps(packet, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(phase3e2d_markdown(packet), encoding="utf-8")
    return json_path, md_path
