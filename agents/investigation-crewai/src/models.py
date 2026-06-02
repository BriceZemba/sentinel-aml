"""I/O contracts — identical to the LangGraph Investigator.

The whole point of this variant: a different agent framework (CrewAI) behind the
*same* UiPath contract. Maestro can swap one for the other at the Investigation
stage with no change to the rest of the case.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class InvestigationInput(BaseModel):
    alert_id: str
    customer_id: str
    account_id: str
    rule: str
    priority: Literal["low", "medium", "high"] = "medium"


class EvidenceItem(BaseModel):
    category: Literal["entity", "transaction", "sanctions", "pep", "adverse_media", "kyc"]
    summary: str
    detail: str
    source: str
    severity: Literal["info", "low", "medium", "high", "critical"] = "info"


class InvestigationOutput(BaseModel):
    alert_id: str
    customer_id: str
    risk_score: int = Field(ge=0, le=100)
    recommendation: Literal["FILE_SAR", "DISMISS", "ESCALATE", "REQUEST_INFO"]
    rationale: str
    red_flags: list[str] = Field(default_factory=list)
    evidence: list[EvidenceItem] = Field(default_factory=list)
    sla_breach_risk: bool = False
    framework: str = "crewai"
