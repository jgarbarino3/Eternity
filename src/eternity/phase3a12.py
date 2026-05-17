"""Phase 3A.12 manual source review result utilities."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

PASS = "passed"


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _candidate_summary(candidate: dict[str, Any]) -> dict[str, Any]:
    gates = candidate.get("proof_gate_results", {})
    passed = sorted(gate for gate, status in gates.items() if status == PASS)
    unresolved_or_failed = sorted(gate for gate, status in gates.items() if status != PASS)
    return {
        "candidate_id": candidate.get("candidate_id"),
        "sha256": candidate.get("sha256"),
        "path": candidate.get("path"),
        "candidate_decision": candidate.get("candidate_decision"),
        "passed_gates": passed,
        "failed_or_unresolved_gates": unresolved_or_failed,
        "positive_evidence": candidate.get("positive_evidence", []),
        "negative_evidence": candidate.get("negative_evidence", []),
    }


def build_phase3a12_result(review_input: dict[str, Any]) -> dict[str, Any]:
    if review_input.get("phase_id") != "Phase 3A.12":
        raise ValueError("Phase 3A.12 requires Phase 3A.12 review input")
    candidates = review_input.get("reviewed_candidates", [])
    if not candidates:
        raise ValueError("Phase 3A.12 requires at least one reviewed candidate")

    summaries = [_candidate_summary(candidate) for candidate in candidates]
    any_all_gates_passed = any(not summary["failed_or_unresolved_gates"] for summary in summaries)
    if any_all_gates_passed:
        final_decision = "source_proof_found_requires_xhigh_policy_checkpoint"
        next_phase = "Phase 3A.13 - Future-only absolute-reflectance policy"
    else:
        final_decision = "manual_source_followup_exhausted"
        next_phase = "Phase 3B - TiON evidence gathering or Phase 3A.6 clean export"

    return {
        "phase_id": "Phase 3A.12",
        "title": "Manual Source Review Result or Clean Export Pivot",
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "review_input_ref": "docs/phase3a12_manual_source_review_input.json",
        "source_packet_ref": review_input.get("source_packet"),
        "decision": {
            "status": final_decision,
            "candidate_count": len(summaries),
            "source_proof_found": any_all_gates_passed,
            "can_feed_serious_core": False,
            "can_promote_calibrated_linear_evidence": False,
            "normalization_basis": "relative_intensity_only",
            "claim_status_ceiling": "weak_within_dataset_holdout",
            "phase3a_manual_followup_continuation_recommended": False,
            "recommended_next_phase": next_phase,
        },
        "candidate_results": summaries,
        "bottom_line": (
            "The three bounded source candidates strengthen related provenance "
            "but do not prove exact 3L2/Quartz source identity, the 30/10/20 "
            "stack, absolute reflectance calibration, or lineage to the d_10nm "
            "text trace."
            if not any_all_gates_passed
            else "At least one candidate passed every proof gate; policy review is required."
        ),
        "allowed_next_actions": [
            "Use Phase 3A.6 to request a clean CompleteEASE export or new measurement.",
            "Return to Phase 3B only if raw sample-matched TiON R/T appears.",
            "Use TiON plots only if explicitly digitized as plot-derived evidence.",
            "Keep Phase 3A relative-only until source-backed absolute data exists.",
        ],
        "forbidden_next_actions": [
            "continue open-ended Phase 3A source searching without new user-supplied evidence",
            "treat thesis Intensity columns as absolute reflectance",
            "promote run_f35a15cef565fb15",
            "feed Phase 3A relative-only diagnostics into the serious core",
        ],
    }


def build_phase3a12_result_from_path(review_input_path: Path) -> dict[str, Any]:
    return build_phase3a12_result(_load_json(review_input_path))


def result_markdown(result: dict[str, Any]) -> str:
    decision = result["decision"]
    lines = [
        "# Phase 3A.12 Manual Source Review Result",
        "",
        "## Decision",
        "",
        f"- Status: `{decision['status']}`",
        f"- Source proof found: `{decision['source_proof_found']}`",
        f"- Can feed serious core: `{decision['can_feed_serious_core']}`",
        (
            "- Can promote calibrated evidence: "
            f"`{decision['can_promote_calibrated_linear_evidence']}`"
        ),
        f"- Normalization basis: `{decision['normalization_basis']}`",
        f"- Claim-status ceiling: `{decision['claim_status_ceiling']}`",
        (
            "- Continue Phase 3A manual source follow-up: "
            f"`{decision['phase3a_manual_followup_continuation_recommended']}`"
        ),
        f"- Recommended next phase: `{decision['recommended_next_phase']}`",
        "",
        "## Bottom Line",
        "",
        result["bottom_line"],
        "",
        "## Candidate Results",
        "",
    ]
    for candidate in result["candidate_results"]:
        lines.extend(
            [
                f"### {candidate['candidate_id']}",
                "",
                f"- Decision: `{candidate['candidate_decision']}`",
                f"- SHA-256: `{candidate['sha256']}`",
                f"- Path: `{candidate['path']}`",
                (
                    "- Passed gates: "
                    + (
                        ", ".join(f"`{gate}`" for gate in candidate["passed_gates"])
                        if candidate["passed_gates"]
                        else "`none`"
                    )
                ),
                (
                    "- Failed or unresolved gates: "
                    + ", ".join(f"`{gate}`" for gate in candidate["failed_or_unresolved_gates"])
                ),
                "",
                "Positive evidence:",
            ]
        )
        lines.extend(f"- {item}" for item in candidate["positive_evidence"])
        lines.extend(["", "Negative evidence:"])
        lines.extend(f"- {item}" for item in candidate["negative_evidence"])
        lines.append("")
    lines.extend(["## Allowed Next Actions", ""])
    lines.extend(f"- {item}" for item in result["allowed_next_actions"])
    lines.extend(["", "## Forbidden Next Actions", ""])
    lines.extend(f"- {item}" for item in result["forbidden_next_actions"])
    lines.append("")
    return "\n".join(lines)


def write_phase3a12_result(output_dir: Path, result: dict[str, Any]) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "phase3a12_manual_source_review_result.json"
    md_path = output_dir / "phase3a12_manual_source_review_result.md"
    json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(result_markdown(result), encoding="utf-8")
    return json_path, md_path
