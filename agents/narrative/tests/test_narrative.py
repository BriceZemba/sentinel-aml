"""HITL interrupt/resume tests for the Narrator (offline)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from langgraph.checkpoint.memory import MemorySaver  # noqa: E402
from langgraph.types import Command  # noqa: E402

from graph import build_graph  # noqa: E402

SAMPLE = {
    "alert_id": "ALT-1", "customer_id": "C-1", "customer_name": "Acme Co",
    "risk_score": 80, "recommendation": "FILE_SAR",
    "red_flags": ["structuring"], "rationale": "test",
}


def _app():
    return build_graph().compile(checkpointer=MemorySaver())


def test_suspends_then_files_on_approval():
    app = _app()
    cfg = {"configurable": {"thread_id": "t1"}}
    paused = app.invoke(SAMPLE, cfg)
    assert "__interrupt__" in paused  # graph paused for a human
    final = app.invoke(Command(resume={"action": "approve", "decided_by": "mlro"}), cfg)
    assert final["disposition"] == "FILED"
    assert final["decided_by"] == "mlro"
    assert final["sar_narrative"]


def test_reject_returns_for_rework():
    app = _app()
    cfg = {"configurable": {"thread_id": "t2"}}
    app.invoke(SAMPLE, cfg)
    final = app.invoke(Command(resume={"action": "reject", "decided_by": "mlro", "notes": "need docs"}), cfg)
    assert final["disposition"] == "RETURNED_FOR_REWORK"
    assert final["decision_notes"] == "need docs"
