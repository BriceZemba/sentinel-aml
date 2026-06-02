"""Contract-parity tests: the CrewAI variant must produce the same decisions as
the LangGraph variant (deterministic mode, offline, no CrewAI/LLM needed)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.data_access import _load  # noqa: E402
from src.runner import run  # noqa: E402


def _run(alert_id: str) -> dict:
    a = {x["alert_id"]: x for x in _load("alerts.json")}[alert_id]
    return run({"alert_id": a["alert_id"], "customer_id": a["customer_id"],
                "account_id": a["account_id"], "rule": a["rule"], "priority": a.get("priority_hint", "medium")})


def test_sanctions_escalates():
    out = _run("ALT-2026-0512-002")
    assert out["recommendation"] == "ESCALATE"
    assert any(e["category"] == "sanctions" for e in out["evidence"])
    assert out["framework"].startswith("crewai")


def test_structuring_flagged():
    out = _run("ALT-2026-0512-001")
    assert any("Structuring" in f for f in out["red_flags"])


def test_routine_dismissed():
    out = _run("ALT-2026-0512-004")
    assert out["recommendation"] == "DISMISS"
    assert out["risk_score"] < 30
