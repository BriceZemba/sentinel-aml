"""Transaction Analysis node.

Deterministic typology detection over the subject account: structuring
(sub-threshold clustering), rapid in/out movement (layering), high-risk
jurisdiction exposure, and activity vs. expected-volume deviation. The logic is
explicit and auditable on purpose — regulators distrust opaque scoring.
"""
from __future__ import annotations

from collections import defaultdict
from datetime import date

import data_access as dao
from state import InvestigationState

CTR_THRESHOLD = 10000
STRUCTURING_BAND = 0.90  # transactions in [band*threshold, threshold)


def _parse(d: str) -> date:
    return date.fromisoformat(d)


def transaction_analysis(state: InvestigationState) -> dict:
    txns = dao.get_transactions(state["account_id"])
    customer = state.get("customer", {})
    hrj = dao.high_risk_jurisdictions()
    evidence: list[dict] = []
    red_flags: list[str] = []

    if not txns:
        return {"transactions": [], "evidence": [], "red_flags": []}

    # --- Structuring: clusters of credits just under the CTR threshold ---
    near_threshold = [
        t for t in txns
        if t["direction"] == "credit"
        and STRUCTURING_BAND * CTR_THRESHOLD <= t["amount_usd"] < CTR_THRESHOLD
    ]
    if len(near_threshold) >= 2:
        total = sum(t["amount_usd"] for t in near_threshold)
        red_flags.append(
            f"Structuring pattern: {len(near_threshold)} credits just below ${CTR_THRESHOLD:,} "
            f"totaling ${total:,}."
        )
        evidence.append({
            "category": "transaction",
            "summary": "Sub-threshold structuring detected",
            "detail": "; ".join(
                f"{t['txn_id']} {t['date']} ${t['amount_usd']:,} from {t['counterparty']}"
                for t in near_threshold
            ),
            "source": "analysis:structuring",
            "severity": "high",
        })

    # --- Rapid movement / layering: large credit followed by near-equal debit ---
    by_day: dict[str, list] = defaultdict(list)
    for t in txns:
        by_day[t["date"]].append(t)
    for day, group in by_day.items():
        credits = [t for t in group if t["direction"] == "credit"]
        debits = [t for t in group if t["direction"] == "debit"]
        for c in credits:
            for d in debits:
                if abs(c["amount_usd"] - d["amount_usd"]) / c["amount_usd"] < 0.05 and c["amount_usd"] > 50000:
                    red_flags.append(
                        f"Rapid movement on {day}: ${c['amount_usd']:,} in from {c['counterparty']} "
                        f"-> ${d['amount_usd']:,} out to {d['counterparty']} (same day, ~equal)."
                    )
                    evidence.append({
                        "category": "transaction",
                        "summary": "Rapid in/out fund movement (layering indicator)",
                        "detail": f"{c['txn_id']} -> {d['txn_id']} on {day}",
                        "source": "analysis:layering",
                        "severity": "high",
                    })

    # --- High-risk jurisdiction exposure ---
    hrj_txns = [t for t in txns if t.get("counterparty_country") in hrj]
    if hrj_txns:
        countries = sorted({t["counterparty_country"] for t in hrj_txns})
        evidence.append({
            "category": "transaction",
            "summary": f"Exposure to high-risk jurisdictions: {', '.join(countries)}",
            "detail": f"{len(hrj_txns)} of {len(txns)} transactions touch high-risk jurisdictions.",
            "source": "analysis:geography",
            "severity": "medium",
        })

    # --- Volume vs. expected ---
    monthly = sum(t["amount_usd"] for t in txns if t["direction"] == "credit")
    expected = customer.get("expected_monthly_volume_usd")
    if expected and monthly > 1.5 * expected:
        red_flags.append(
            f"Credit volume ${monthly:,} exceeds expected ${expected:,} by "
            f"{monthly / expected:.1f}x."
        )
        evidence.append({
            "category": "transaction",
            "summary": "Activity exceeds expected profile",
            "detail": f"observed_credits=${monthly:,}, expected=${expected:,}",
            "source": "analysis:profile-deviation",
            "severity": "medium",
        })

    return {"transactions": txns, "evidence": evidence, "red_flags": red_flags}
