"""Entry point for the CrewAI Investigator.

`run(input_dict)` is what UiPath invokes when this coded agent runs. It returns the
same `InvestigationOutput` schema as the LangGraph variant.

Two execution modes, chosen automatically:
  • **Crew mode** — if an LLM key is configured AND CrewAI is installed, the
    role-based crew (KYC/Sanctions, Transaction, OSINT analysts + Lead) runs.
  • **Deterministic mode** — otherwise, the same analysis tools are executed in
    sequence directly. The contract is identical, so the case behaves the same and
    the repo stays testable with zero credentials.
"""
from __future__ import annotations

import os
import sys

# UiPath imports this entry file standalone (no parent package); put src/ on the
# path and use absolute imports so the same code runs locally and on UiPath.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import analysis
from models import InvestigationInput, InvestigationOutput


def _deterministic(inp: InvestigationInput) -> InvestigationOutput:
    ent = analysis.resolve_entity(inp.customer_id)
    txn = analysis.analyze_transactions(inp.account_id, ent["customer"])
    media = analysis.screen_adverse_media(ent["customer"], txn["transactions"])

    evidence = ent["evidence"] + txn["evidence"] + media["evidence"]
    red_flags = ent["red_flags"] + txn["red_flags"] + media["red_flags"]
    total = analysis.score(evidence)
    rec = analysis.recommend(evidence, total)
    rationale = (
        f"Composite risk score {total}/100 -> {rec}. Key drivers: "
        + ("; ".join(red_flags) if red_flags else "no material red flags.")
    )
    return InvestigationOutput(
        alert_id=inp.alert_id, customer_id=inp.customer_id, risk_score=total,
        recommendation=rec, rationale=rationale, red_flags=red_flags,
        evidence=evidence, sla_breach_risk=(inp.priority == "high" and rec != "DISMISS"),
        framework="crewai-deterministic",
    )


def _crew_enabled() -> bool:
    if not (os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY")):
        return False
    try:
        import crewai  # noqa: F401
        return True
    except Exception:
        return False


def run(input_dict: dict) -> dict:
    inp = InvestigationInput(**input_dict)

    if not _crew_enabled():
        return _deterministic(inp).model_dump()

    # Crew mode. If anything in the LLM run fails, fall back to deterministic so a
    # case is never left without a result.
    try:
        from crew import build_crew

        result = build_crew().kickoff(inputs=inp.model_dump())
        out = _parse_crew_output(str(result), inp)
        return out.model_dump()
    except Exception as exc:  # pragma: no cover - needs network/LLM
        det = _deterministic(inp)
        det.rationale += f"\n(crew run failed, used deterministic fallback: {exc})"
        det.framework = "crewai-fallback"
        return det.model_dump()


def _parse_crew_output(text: str, inp: InvestigationInput) -> InvestigationOutput:  # pragma: no cover
    """Best-effort parse of the lead investigator's JSON; deterministic on failure."""
    import json
    import re

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group(0))
            data.setdefault("alert_id", inp.alert_id)
            data.setdefault("customer_id", inp.customer_id)
            data.setdefault("framework", "crewai")
            return InvestigationOutput(**data)
        except Exception:
            pass
    return _deterministic(inp)
