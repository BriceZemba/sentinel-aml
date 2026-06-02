"""Synthesis node.

Combines all evidence into an auditable risk score and a recommendation. The
score is a transparent weighted sum over evidence severity so a reviewer can
reconstruct it; the LLM (if available) only writes the human-readable rationale,
never the score itself. This separation keeps the decision defensible.
"""
from __future__ import annotations

from ..llm import get_llm
from ..state import InvestigationState

_SEVERITY_WEIGHT = {"info": 0, "low": 5, "medium": 12, "high": 22, "critical": 40}


def _score(evidence: list[dict]) -> int:
    raw = sum(_SEVERITY_WEIGHT.get(e.get("severity", "info"), 0) for e in evidence)
    return min(100, raw)


def _recommend(score: int, evidence: list[dict], expedite: bool) -> str:
    has_sanctions = any(e["category"] == "sanctions" for e in evidence)
    if has_sanctions:
        return "ESCALATE"  # sanctions exposure always goes to senior MLRO fast-track
    if score >= 55:
        return "FILE_SAR"
    if score >= 30:
        return "REQUEST_INFO"  # borderline -> gather more before deciding
    return "DISMISS"


def _fallback_rationale(score: int, rec: str, red_flags: list[str]) -> str:
    bullets = "\n".join(f"- {f}" for f in red_flags) or "- No material red flags identified."
    return (
        f"Composite risk score {score}/100 -> recommendation {rec}.\n"
        f"Key drivers:\n{bullets}"
    )


def synthesize(state: InvestigationState) -> dict:
    evidence = state.get("evidence", [])
    red_flags = state.get("red_flags", [])
    score = _score(evidence)
    rec = _recommend(score, evidence, state.get("expedite", False))

    llm = get_llm()
    if llm is None:
        rationale = _fallback_rationale(score, rec, red_flags)
    else:
        flags_txt = "\n".join(f"- {f}" for f in red_flags) or "- none"
        prompt = (
            "You are a senior AML investigator. Write a concise, regulator-ready "
            "rationale (max 120 words) for the recommendation below. Be factual, "
            "cite the red flags, do not invent facts.\n\n"
            f"Customer: {state.get('customer', {}).get('legal_name')}\n"
            f"Alert rule: {state.get('rule')}\n"
            f"Composite risk score: {score}/100\n"
            f"Recommendation: {rec}\n"
            f"Red flags:\n{flags_txt}\n"
        )
        try:
            rationale = llm.invoke(prompt).content
        except Exception as exc:  # never fail the case on an LLM error
            rationale = _fallback_rationale(score, rec, red_flags) + f"\n(LLM unavailable: {exc})"

    sla_breach_risk = state.get("priority") == "high" and rec != "DISMISS"
    return {
        "risk_score": score,
        "recommendation": rec,
        "rationale": rationale,
        "sla_breach_risk": sla_breach_risk,
    }
