"""I/O contracts for the Narrator coded agent."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class NarrativeInput(BaseModel):
    """Handed in by the Maestro Narrative-Drafting stage, built from case data."""

    alert_id: str
    customer_id: str
    customer_name: str
    risk_score: int
    recommendation: Literal["FILE_SAR", "DISMISS", "ESCALATE", "REQUEST_INFO"]
    red_flags: list[str] = Field(default_factory=list)
    rationale: str = ""


class NarrativeOutput(BaseModel):
    """Disposition package returned to the case after human sign-off."""

    alert_id: str
    disposition: Literal["FILED", "DISMISSED", "RETURNED_FOR_REWORK"]
    sar_narrative: str
    decided_by: str
    decision_notes: str = ""
