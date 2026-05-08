"""Deterministic relevance scoring for radar candidates."""

from __future__ import annotations

import re

from eternity.research_memory.radar.config import RadarScoringConfig
from eternity.research_memory.radar.models import (
    RadarCandidate,
    RadarGrade,
    RankedRadarCandidate,
)

THEME_KEYWORDS: dict[str, tuple[str, ...]] = {
    "hypothesis_generation": (
        "hypothesis generation",
        "scientific discovery",
        "idea generation",
        "research hypothesis",
    ),
    "agent_memory": ("agent memory", "memory", "persistent context", "long-term memory"),
    "context_engineering": ("context engineering", "retrieval", "rag", "context window"),
    "scientific_evals": ("scientific eval", "benchmark", "evaluation", "failure mode"),
    "self_driving_labs": (
        "self-driving lab",
        "autonomous experiment",
        "closed-loop experiment",
        "robot scientist",
    ),
    "bayesian_experiment_design": (
        "bayesian experimental design",
        "bayesian optimization",
        "active learning",
        "experiment design",
    ),
    "photonic_agents": ("photonics", "optics agent", "photonic design", "nanophotonics"),
    "ultrafast_ml": (
        "ultrafast spectroscopy",
        "pump-probe",
        "transient absorption",
        "machine learning spectroscopy",
    ),
    "frog_retrieval": (
        "frog retrieval",
        "frequency-resolved optical gating",
        "pulse characterization",
        "phase retrieval",
    ),
    "materials_agents": ("materials science", "materials agent", "materials discovery"),
    "claim_verification": (
        "claim verification",
        "evidence verification",
        "fact verification",
        "citation verification",
    ),
}

ETERNITY_DOMAIN_KEYWORDS = (
    "epsilon-near-zero",
    "epsilon near zero",
    "enz",
    "tin",
    "ito",
    "azo",
    "frog",
    "ultrafast",
    "spectroscopy",
    "pump-probe",
    "thin film",
    "photonic",
    "optics",
    "materials",
)

IMPLEMENTATION_KEYWORDS = (
    "code",
    "repository",
    "benchmark",
    "dataset",
    "algorithm",
    "retrieval",
    "pipeline",
    "simulator",
    "agent",
)

EXPERIMENT_KEYWORDS = (
    "experiment",
    "measurement",
    "spectroscopy",
    "laboratory",
    "lab",
    "pulse",
    "retrieval",
    "optimization",
)

HYPE_KEYWORDS = (
    "revolutionary",
    "fully autonomous scientist",
    "human-level scientist",
    "breakthrough without validation",
    "agi scientist",
)


def _text(candidate: RadarCandidate) -> str:
    values = [
        candidate.title,
        candidate.abstract,
        candidate.venue or "",
        " ".join(candidate.tags),
        " ".join(candidate.project_areas),
    ]
    return " ".join(values).lower()


def _contains_phrase(text: str, phrase: str) -> bool:
    return phrase.lower() in text


def _keyword_hits(text: str, keywords: tuple[str, ...]) -> list[str]:
    return [keyword for keyword in keywords if _contains_phrase(text, keyword)]


def classify_themes(candidate: RadarCandidate) -> list[str]:
    """Classify a candidate into configured radar themes."""

    text = _text(candidate)
    themes = [
        theme
        for theme, keywords in THEME_KEYWORDS.items()
        if any(_contains_phrase(text, keyword) for keyword in keywords)
    ]
    return themes


def _source_quality_score(
    candidate: RadarCandidate, scoring: RadarScoringConfig
) -> tuple[int, str | None]:
    if candidate.source_type in {"arxiv_query", "arxiv_category", "openreview_search"}:
        return scoring.weights["source_quality"], "metadata from scholarly source"
    if candidate.source_type == "huggingface_daily_papers":
        return 1, "metadata from Hugging Face paper page"
    return 0, None


def _possible_experiment(themes: list[str]) -> str:
    if "frog_retrieval" in themes:
        return "Run a synthetic-only FROG retrieval stress test before touching lab data."
    if "ultrafast_ml" in themes:
        return (
            "Benchmark on synthetic ultrafast spectra or pump-probe fixtures "
            "with known ground truth."
        )
    if "self_driving_labs" in themes or "bayesian_experiment_design" in themes:
        return (
            "Prototype a simulated experiment-selection loop over existing "
            "synthetic Eternity specs."
        )
    if "photonic_agents" in themes or "materials_agents" in themes:
        return (
            "Evaluate against a static thin-film or material-selection task "
            "with explicit provenance."
        )
    return "No lab experiment yet; first convert the lead into a reviewed paper card."


def _possible_code_module(themes: list[str]) -> str:
    if "frog_retrieval" in themes:
        return "Potential future module: `eternity.pulse_retrieval` synthetic FROG fixtures."
    if "bayesian_experiment_design" in themes:
        return (
            "Potential future module: `eternity.experiment_design` for simulated "
            "acquisition policies."
        )
    if "agent_memory" in themes or "context_engineering" in themes:
        return "Potential future module: `eternity.research_memory` retrieval/ranking helpers."
    if "claim_verification" in themes or "scientific_evals" in themes:
        return "Potential future module: `eternity.evals` for evidence and claim-check fixtures."
    return "Potential future module: reviewed research-memory paper card plus Codex task draft."


def _why_matters(candidate: RadarCandidate, themes: list[str], reasons: list[str]) -> str:
    if themes:
        theme_text = ", ".join(themes)
        return (
            f"Matches Eternity radar themes `{theme_text}` through deterministic keyword hits. "
            f"This is a lead for review, not evidence of new physics."
        )
    if reasons:
        return (
            f"Matches low-level radar signals ({'; '.join(reasons[:2])}). "
            "This should stay in the read-later queue unless human review finds a concrete link."
        )
    return "No strong Eternity signal beyond source/query match; keep as read-later only."


def _risk(candidate: RadarCandidate) -> str:
    source = candidate.source_type
    return (
        f"Radar classification is keyword-based, source `{source}` has not been human reviewed, "
        "and no serious-core validation artifact supports transfer to Eternity."
    )


def _should_act(grade: RadarGrade, themes: list[str]) -> str:
    if grade == RadarGrade.ACT_NOW:
        return (
            "Yes: human-read the paper, then promote to a reviewed paper card "
            "or Codex task draft."
        )
    if grade == RadarGrade.ARCHITECTURE_IDEA:
        return (
            "Maybe: keep in the architecture backlog unless it maps to a "
            "near-term synthetic test."
        )
    if grade == RadarGrade.RELEVANT_NOT_ACTIONABLE:
        return "Not now: preserve as context, but do not spend implementation time yet."
    if grade == RadarGrade.HYPE_OR_NOISE:
        return "No: ignore unless a concrete method, dataset, or validation result appears."
    if themes:
        return "Later: revisit when related Eternity module work starts."
    return "Later: read only if the weekly queue is otherwise empty."


def grade_candidate(
    candidate: RadarCandidate,
    *,
    scoring: RadarScoringConfig | None = None,
) -> RankedRadarCandidate:
    """Assign a deterministic grade and Eternity opportunity fields."""

    scoring = scoring or RadarScoringConfig()
    text = _text(candidate)
    reasons: list[str] = []
    score = 0

    themes = classify_themes(candidate)
    for theme in themes:
        keywords = THEME_KEYWORDS[theme]
        exact_hits = [keyword for keyword in keywords if " " in keyword and keyword in text]
        keyword_hits = [keyword for keyword in keywords if keyword in text]
        if exact_hits:
            score += scoring.weights["exact_theme_phrase"]
            reasons.append(f"{theme}: {exact_hits[0]}")
        if keyword_hits:
            score += scoring.weights["theme_keyword"]

    domain_hits = _keyword_hits(text, ETERNITY_DOMAIN_KEYWORDS)
    if domain_hits:
        score += scoring.weights["eternity_domain_keyword"] * min(len(domain_hits), 3)
        reasons.append(f"Eternity domain: {', '.join(domain_hits[:3])}")

    implementation_hits = _keyword_hits(text, IMPLEMENTATION_KEYWORDS)
    if implementation_hits:
        score += scoring.weights["implementation_keyword"] * min(len(implementation_hits), 2)
        reasons.append(f"implementation signal: {', '.join(implementation_hits[:2])}")

    experiment_hits = _keyword_hits(text, EXPERIMENT_KEYWORDS)
    if experiment_hits:
        score += scoring.weights["experiment_keyword"] * min(len(experiment_hits), 2)
        reasons.append(f"experiment signal: {', '.join(experiment_hits[:2])}")

    quality_score, quality_reason = _source_quality_score(candidate, scoring)
    score += quality_score
    if quality_reason:
        reasons.append(quality_reason)

    hype_hits = _keyword_hits(text, HYPE_KEYWORDS)
    if hype_hits:
        score += scoring.weights["hype_penalty"] * len(hype_hits)
        reasons.append(f"hype warning: {', '.join(hype_hits[:2])}")

    if score >= scoring.grade_thresholds["A"]:
        grade = RadarGrade.ACT_NOW
    elif score >= scoring.grade_thresholds["B"]:
        grade = RadarGrade.ARCHITECTURE_IDEA
    elif score >= scoring.grade_thresholds["C"]:
        grade = RadarGrade.RELEVANT_NOT_ACTIONABLE
    elif hype_hits:
        grade = RadarGrade.HYPE_OR_NOISE
    else:
        grade = RadarGrade.READ_LATER

    strong_b = grade == RadarGrade.ARCHITECTURE_IDEA and score >= scoring.strong_b_threshold
    return RankedRadarCandidate(
        candidate=candidate,
        grade=grade,
        score=score,
        themes=themes,
        reasons=reasons or ["No strong deterministic relevance signal."],
        why_this_matters=_why_matters(candidate, themes, reasons),
        possible_experiment=_possible_experiment(themes),
        possible_code_module=_possible_code_module(themes),
        risk_or_limitation=_risk(candidate),
        should_we_act_now=_should_act(grade, themes),
        strong_b=strong_b,
    )


def rank_candidates(
    candidates: list[RadarCandidate],
    *,
    scoring: RadarScoringConfig | None = None,
) -> list[RankedRadarCandidate]:
    """Rank candidates by grade/score with deterministic tie-breaking."""

    ranked = [grade_candidate(candidate, scoring=scoring) for candidate in candidates]
    grade_order = {grade: index for index, grade in enumerate("ABCDE")}
    return sorted(
        ranked,
        key=lambda item: (
            grade_order[item.grade],
            -item.score,
            re.sub(r"\W+", " ", item.candidate.title).lower(),
        ),
    )
