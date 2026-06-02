"""SAR narrative drafting.

Produces a FinCEN-style "5 Ws" narrative (Who, What, When, Where, Why/How) from
the investigation evidence. Uses the LLM when ANTHROPIC_API_KEY is present;
otherwise emits a deterministic templated narrative so the agent runs offline.
"""
from __future__ import annotations

import os


def _llm():
    if not os.getenv("ANTHROPIC_API_KEY"):
        return None
    from langchain_anthropic import ChatAnthropic

    return ChatAnthropic(
        model=os.getenv("SENTINEL_LLM_MODEL", "claude-opus-4-8"),
        temperature=0.2,
        max_tokens=1200,
    )


def _template(inp) -> str:
    flags = "\n".join(f"  - {f}" for f in inp.red_flags) or "  - (none recorded)"
    return (
        f"SUSPICIOUS ACTIVITY REPORT — NARRATIVE (DRAFT)\n"
        f"Subject: {inp.customer_name} ({inp.customer_id})\n"
        f"Triggering alert: {inp.alert_id}\n"
        f"Composite risk score: {inp.risk_score}/100\n\n"
        f"WHO: {inp.customer_name}, a customer of the institution.\n"
        f"WHAT/WHY: The institution identified activity consistent with possible "
        f"money laundering based on the following indicators:\n{flags}\n\n"
        f"ANALYST RATIONALE:\n{inp.rationale}\n\n"
        f"The institution is filing this report to document the activity for "
        f"regulatory review. This narrative is a draft pending compliance approval."
    )


def draft_narrative(inp) -> str:
    llm = _llm()
    if llm is None:
        return _template(inp)
    flags = "\n".join(f"- {f}" for f in inp.red_flags) or "- none"
    prompt = (
        "Draft a concise, factual FinCEN SAR narrative using the 5 Ws (Who, What, "
        "When, Where, Why/How). Use only the facts provided; do not fabricate "
        "names, dates, or amounts beyond what is given. Max 250 words.\n\n"
        f"Subject: {inp.customer_name} ({inp.customer_id})\n"
        f"Alert: {inp.alert_id}\n"
        f"Risk score: {inp.risk_score}/100\n"
        f"Red flags:\n{flags}\n"
        f"Investigator rationale: {inp.rationale}\n"
    )
    try:
        return llm.invoke(prompt).content
    except Exception as exc:
        return _template(inp) + f"\n\n(LLM unavailable, used template: {exc})"
