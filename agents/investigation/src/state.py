"""Shared graph state for the Investigator crew."""
from __future__ import annotations

from typing import Annotated, Any, TypedDict

from langgraph.graph.message import add_messages


def _extend(left: list, right: list) -> list:
    """Reducer that appends evidence/flags across nodes instead of overwriting."""
    return (left or []) + (right or [])


class InvestigationState(TypedDict, total=False):
    # --- inputs (set from InvestigationInput) ---
    alert_id: str
    customer_id: str
    account_id: str
    rule: str
    priority: str

    # --- accumulated working memory ---
    customer: dict[str, Any]
    transactions: list[dict[str, Any]]
    evidence: Annotated[list[dict[str, Any]], _extend]
    red_flags: Annotated[list[str], _extend]
    expedite: bool

    # --- final synthesis ---
    risk_score: int
    recommendation: str
    rationale: str
    sla_breach_risk: bool

    messages: Annotated[list, add_messages]
