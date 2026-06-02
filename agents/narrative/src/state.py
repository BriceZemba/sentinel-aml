"""Graph state for the Narrator agent."""
from __future__ import annotations

from typing import TypedDict


class NarrativeState(TypedDict, total=False):
    alert_id: str
    customer_id: str
    customer_name: str
    risk_score: int
    recommendation: str
    red_flags: list[str]
    rationale: str

    draft: str
    disposition: str
    sar_narrative: str
    decided_by: str
    decision_notes: str
