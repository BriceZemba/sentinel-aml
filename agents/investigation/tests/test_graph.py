"""Smoke + behavior tests for the Investigator graph (offline, no API key)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from data_access import _load  # noqa: E402
from graph import graph  # noqa: E402


def _run(alert_id: str) -> dict:
    alert = {a["alert_id"]: a for a in _load("alerts.json")}[alert_id]
    return graph.invoke({
        "alert_id": alert["alert_id"],
        "customer_id": alert["customer_id"],
        "account_id": alert["account_id"],
        "rule": alert["rule"],
        "priority": alert.get("priority_hint", "medium"),
    })


def test_sanctions_case_escalates():
    out = _run("ALT-2026-0512-002")  # Halcyon -> Blue Lagoon (OFAC) + adverse media
    assert out["recommendation"] == "ESCALATE"
    assert any(e["category"] == "sanctions" for e in out["evidence"])
    assert out["risk_score"] >= 55


def test_structuring_case_flags_sar():
    out = _run("ALT-2026-0512-001")  # Northbridge sub-threshold credits
    assert any("Structuring" in f for f in out["red_flags"])
    assert out["recommendation"] in {"FILE_SAR", "REQUEST_INFO", "ESCALATE"}


def test_routine_payroll_dismisses():
    out = _run("ALT-2026-0512-004")  # teacher payroll, clean
    assert out["recommendation"] == "DISMISS"
    assert out["risk_score"] < 30
