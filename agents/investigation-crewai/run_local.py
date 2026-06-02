"""Run the CrewAI Investigator variant locally.

    python run_local.py ALT-2026-0512-002

Runs in deterministic mode with no key (CrewAI not required); set
ANTHROPIC_API_KEY (and `pip install crewai`) to run the real role-based crew.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.data_access import _load  # noqa: E402
from src.runner import run  # noqa: E402


def main() -> None:
    alert_id = sys.argv[1] if len(sys.argv) > 1 else "ALT-2026-0512-002"
    alert = {a["alert_id"]: a for a in _load("alerts.json")}.get(alert_id)
    if not alert:
        raise SystemExit(f"Unknown alert {alert_id}")
    out = run({
        "alert_id": alert["alert_id"], "customer_id": alert["customer_id"],
        "account_id": alert["account_id"], "rule": alert["rule"],
        "priority": alert.get("priority_hint", "medium"),
    })
    print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
