"""Typed I/O contracts for the Investigator coded agent.

These Pydantic models are the public schema of the agent. UiPath uses the input
model to render the trigger form and the output model to pass structured results
back into the Maestro case as case data for the next stage (Narrative Drafting).
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class InvestigationInput(BaseModel):
    """Input handed to the agent by the Maestro Investigation stage."""

    alert_id: str = Field(description="Triggering transaction-monitoring alert id")
    customer_id: str = Field(description="Subject customer id")
    account_id: str = Field(description="Subject account id")
    rule: str = Field(description="Detection rule that fired the alert")
    priority: Literal["low", "medium", "high"] = "medium"


class EvidenceItem(BaseModel):
    """A single, citable piece of evidence. Every finding must trace to a source."""

    category: Literal[
        "entity", "transaction", "sanctions", "pep", "adverse_media", "kyc"
    ]
    summary: str
    detail: str
    source: str
    severity: Literal["info", "low", "medium", "high", "critical"] = "info"


class InvestigationOutput(BaseModel):
    """Structured result merged back into the case at the end of Investigation."""

    alert_id: str
    customer_id: str
    risk_score: int = Field(ge=0, le=100)
    recommendation: Literal["FILE_SAR", "DISMISS", "ESCALATE", "REQUEST_INFO"]
    rationale: str
    red_flags: list[str] = Field(default_factory=list)
    evidence: list[EvidenceItem] = Field(default_factory=list)
    sla_breach_risk: bool = False
