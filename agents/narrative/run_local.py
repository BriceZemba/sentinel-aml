"""Demonstrate the Narrator's human-in-the-loop interrupt/resume cycle locally.

    python run_local.py            # simulates MLRO approving
    python run_local.py reject     # simulates MLRO rejecting -> rework

Shows the exact payload that becomes an Action Center task on UiPath, then
resumes the suspended graph with the human decision.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from langgraph.checkpoint.memory import MemorySaver  # noqa: E402
from langgraph.types import Command  # noqa: E402

from graph import build_graph  # noqa: E402

SAMPLE = {
    "alert_id": "ALT-2026-0512-002",
    "customer_id": "CUST-30555",
    "customer_name": "Halcyon Capital Partners",
    "risk_score": 100,
    "recommendation": "ESCALATE",
    "red_flags": [
        "SANCTIONS hit on Dmitri Sokolov: EU-CONSOLIDATED (RUSSIA).",
        "Rapid in/out fund movement (layering indicator) on 2026-05-01 and 2026-05-08.",
        "Adverse media: regulator probes Halcyon Capital over layering allegations.",
    ],
    "rationale": "Sanctioned counterparty, same-day pass-through layering, and "
                 "corroborating adverse media indicate probable laundering.",
}


def main() -> None:
    action = sys.argv[1] if len(sys.argv) > 1 else "approve"
    app = build_graph().compile(checkpointer=MemorySaver())
    config = {"configurable": {"thread_id": "demo-1"}}

    paused = app.invoke(SAMPLE, config)
    task = paused["__interrupt__"][0].value
    print("=== Action Center task created (graph suspended) ===")
    print(json.dumps({k: task[k] for k in ("title", "instructions", "recommendation")}, indent=2))
    print("\n--- Drafted SAR narrative ---\n" + task["draft_narrative"][:600] + " ...\n")

    decision = {
        "approve": {"action": "approve", "decided_by": "j.okafor@bank.com",
                    "notes": "Concur. File immediately."},
        "reject": {"action": "reject", "decided_by": "j.okafor@bank.com",
                   "notes": "Need source-of-funds docs before filing."},
    }[action]

    print(f"=== MLRO submits decision: {decision['action']} ===")
    final = app.invoke(Command(resume=decision), config)
    print(json.dumps(final, indent=2))


if __name__ == "__main__":
    main()
