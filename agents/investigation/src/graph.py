"""Investigator graph — the LangGraph crew deployed to UiPath as a coded agent.

Flow:  entity_resolution -> transaction_analysis -> adverse_media -> synthesize

The graph is intentionally a focused investigation crew. The *dynamic, long-
running* part of the lifecycle (looping back for more info, bouncing a weak
narrative from QA, SLA escalation) is orchestrated one level up by UiPath Maestro
Case across stages — that is where case management belongs. This agent's job is
to turn one alert into auditable evidence + a scored recommendation.

`uipath init` reads ``graph`` (exported below) via langgraph.json and generates
the entry points UiPath uses to run it in the cloud. The typed input/output
models become the agent's UiPath contract (trigger form + case data out).
"""
from __future__ import annotations

import os
import sys

# UiPath's graph loader imports this file standalone (no parent package), which
# breaks relative imports. Put this agent's own src/ dir on sys.path and use
# absolute imports so the SAME code runs locally, in tests, and on UiPath.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langgraph.graph import END, START, StateGraph

from models import InvestigationInput, InvestigationOutput
from nodes.adverse_media import adverse_media
from nodes.entity_resolution import entity_resolution
from nodes.synthesize import synthesize
from nodes.transaction_analysis import transaction_analysis
from state import InvestigationState


def _ingest(state: InvestigationState) -> dict:
    """Seed working memory from the typed input."""
    return {"evidence": [], "red_flags": [], "expedite": False}


def build_graph():
    # input/output schemas define the agent's public UiPath contract. The internal
    # InvestigationState carries reducer-managed working memory (evidence, flags).
    g = StateGraph(
        InvestigationState,
        input_schema=InvestigationInput,
        output_schema=InvestigationOutput,
    )

    g.add_node("ingest", _ingest)
    g.add_node("entity_resolution", entity_resolution)
    g.add_node("transaction_analysis", transaction_analysis)
    g.add_node("adverse_media", adverse_media)
    g.add_node("synthesize", synthesize)

    g.add_edge(START, "ingest")
    g.add_edge("ingest", "entity_resolution")
    g.add_edge("entity_resolution", "transaction_analysis")
    g.add_edge("transaction_analysis", "adverse_media")
    g.add_edge("adverse_media", "synthesize")
    g.add_edge("synthesize", END)
    return g.compile()


graph = build_graph()
