"""Run the Investigator graph locally against the JSON fixtures.

    python run_local.py ALT-2026-0512-002

No UiPath connection or API key required (LLM rationale degrades to a template
when ANTHROPIC_API_KEY is unset). Useful for the demo and for judges.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Allow `python run_local.py` from the agent folder without installing the package.
sys.path.insert(0, str(Path(__file__).parent / "src"))

from data_access import _load  # noqa: E402
from graph import graph  # noqa: E402


def main() -> None:
    alert_id = sys.argv[1] if len(sys.argv) > 1 else "ALT-2026-0512-002"
    alerts = {a["alert_id"]: a for a in _load("alerts.json")}
    alert = alerts.get(alert_id)
    if not alert:
        raise SystemExit(f"Unknown alert {alert_id}. Options: {', '.join(alerts)}")

    result = graph.invoke({
        "alert_id": alert["alert_id"],
        "customer_id": alert["customer_id"],
        "account_id": alert["account_id"],
        "rule": alert["rule"],
        "priority": alert.get("priority_hint", "medium"),
    })

    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
