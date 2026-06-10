"""Narrator graph — drafts the SAR and pauses for human sign-off.

Flow:  draft -> human_review (INTERRUPT) -> finalize

`human_review` calls LangGraph's ``interrupt()``. When this graph runs on UiPath
via uipath-langchain, that interrupt is materialized as a **UiPath Action Center
task** assigned to the MLRO / compliance officer: the job suspends, the case in
Maestro shows "Awaiting human decision", and the graph resumes only when the
officer submits the action. This is the binding, accountable, human-in-the-loop
gate — no SAR is filed and no alert is dismissed without it.

The human's response shape:
    {
      "action": "approve" | "edit" | "reject",
      "decided_by": "j.okafor@bank.com",
      "edited_narrative": "<full text>",   # only for "edit"
      "notes": "..."                        # required for "reject"
    }
"""
from __future__ import annotations

import json
import os
import sys

# UiPath's graph loader imports this file standalone (no parent package), which
# breaks relative imports. Put this agent's own src/ dir on sys.path and use
# absolute imports so the SAME code runs locally, in tests, and on UiPath.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt

from models import NarrativeInput, NarrativeOutput
from narrative import draft_narrative
from state import NarrativeState


def draft(state: NarrativeState) -> dict:
    inp = NarrativeInput(**{k: state[k] for k in NarrativeInput.model_fields if k in state})
    return {"draft": draft_narrative(inp)}


def _as_decision(raw) -> dict:
    """Normalize the human's response into a dict.

    Action Center can hand the resume value back as a structured dict OR as a plain
    string (e.g. an outcome word, or JSON typed into a text field). Accept all of
    these so the graph never crashes on the human's input.
    """
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str):
        s = raw.strip()
        try:
            parsed = json.loads(s)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            pass
        return {"action": s}  # a bare word like "approve" / "reject"
    return {}  # unknown shape -> no explicit rejection -> files by default


def human_review(state: NarrativeState) -> dict:
    """Suspend for MLRO sign-off via Action Center; resume with their decision."""
    raw = interrupt(
        {
            "task_type": "SAR_DISPOSITION_REVIEW",
            "title": f"Approve SAR filing for {state.get('customer_name')} "
                     f"(alert {state.get('alert_id')})",
            "instructions": "Review the AI-drafted SAR narrative and the evidence. "
                            "Approve to file, edit then approve, or reject to dismiss/rework.",
            "customer": state.get("customer_name"),
            "risk_score": state.get("risk_score"),
            "recommendation": state.get("recommendation"),
            "red_flags": state.get("red_flags", []),
            "draft_narrative": state.get("draft", ""),
        }
    )
    decision = _as_decision(raw)
    action = str(decision.get("action", "")).strip().lower()
    # File by default. Only an EXPLICIT rejection sends it back / dismisses.
    # This keeps Action Center robust: an approval in any form results in FILED.
    rejected = action in {"reject", "rejected", "deny", "denied", "dismiss", "dismissed", "no", "rework"}
    return {
        "decided_by": decision.get("decided_by", "unknown"),
        "decision_notes": decision.get("notes", ""),
        "sar_narrative": decision.get("edited_narrative") or state.get("draft", ""),
        "disposition": "RETURNED_FOR_REWORK" if rejected else "FILED",
    }


def finalize(state: NarrativeState) -> dict:
    out = NarrativeOutput(
        alert_id=state["alert_id"],
        disposition=state.get("disposition", "RETURNED_FOR_REWORK"),
        sar_narrative=state.get("sar_narrative", ""),
        decided_by=state.get("decided_by", "unknown"),
        decision_notes=state.get("decision_notes", ""),
    )
    return out.model_dump()


def build_graph():
    g = StateGraph(NarrativeState, input_schema=NarrativeInput, output_schema=NarrativeOutput)
    g.add_node("draft", draft)
    g.add_node("human_review", human_review)
    g.add_node("finalize", finalize)
    g.add_edge(START, "draft")
    g.add_edge("draft", "human_review")
    g.add_edge("human_review", "finalize")
    g.add_edge("finalize", END)
    # A checkpointer is required so the graph can suspend at the interrupt and
    # resume later. UiPath supplies a managed checkpointer at runtime; locally we
    # use an in-memory one (see run_local.py).
    return g


graph = build_graph().compile()
