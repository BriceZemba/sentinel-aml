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

from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt

from .models import NarrativeInput, NarrativeOutput
from .narrative import draft_narrative
from .state import NarrativeState


def draft(state: NarrativeState) -> dict:
    inp = NarrativeInput(**{k: state[k] for k in NarrativeInput.model_fields if k in state})
    return {"draft": draft_narrative(inp)}


def human_review(state: NarrativeState) -> dict:
    """Suspend for MLRO sign-off via Action Center; resume with their decision."""
    decision = interrupt(
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
    # In UiPath, `decision` is the submitted Action Center form. Locally it is the
    # value passed to Command(resume=...).
    return {
        "decided_by": decision.get("decided_by", "unknown"),
        "decision_notes": decision.get("notes", ""),
        "sar_narrative": decision.get("edited_narrative") or state.get("draft", ""),
        "disposition": {
            "approve": "FILED",
            "edit": "FILED",
            "reject": "RETURNED_FOR_REWORK",
        }.get(decision.get("action", "reject"), "RETURNED_FOR_REWORK"),
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
