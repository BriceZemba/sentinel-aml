"""Pure analysis functions — no agent-framework dependency.

These are the same auditable detections as the LangGraph variant's nodes. They are
(a) wrapped as CrewAI tools in ``crew.py`` for the real crew, and (b) called
directly by the deterministic fallback in ``runner.py`` so the agent still runs
and tests pass with no LLM/CrewAI installed. Single source of truth either way.
"""
from __future__ import annotations

from collections import defaultdict

import data_access as dao

CTR_THRESHOLD = 10000
STRUCTURING_BAND = 0.90
SEVERITY_WEIGHT = {"info": 0, "low": 5, "medium": 12, "high": 22, "critical": 40}


def resolve_entity(customer_id: str) -> dict:
    customer = dao.get_customer(customer_id) or {}
    evidence: list[dict] = []
    red_flags: list[str] = []
    expedite = False
    if not customer:
        return {"customer": {}, "evidence": [], "red_flags": ["Customer could not be resolved."], "expedite": True}

    evidence.append({
        "category": "entity", "summary": f"Resolved subject: {customer.get('legal_name')} ({customer_id})",
        "detail": f"type={customer.get('type')}, inc_country={customer.get('incorporation_country')}, "
                  f"risk_rating={customer.get('risk_rating')}",
        "source": "core-banking:customers", "severity": "info",
    })
    if customer.get("kyc_status") != "verified":
        red_flags.append(f"KYC status is '{customer.get('kyc_status')}' (not verified).")
        evidence.append({"category": "kyc", "summary": "KYC not in good standing",
                         "detail": f"kyc_status={customer.get('kyc_status')}", "source": "core-banking:kyc", "severity": "high"})
        expedite = True

    parties = [customer.get("legal_name", "")] + [bo["name"] for bo in customer.get("beneficial_owners", [])]
    for party in filter(None, parties):
        hits = dao.screen_watchlists(party)
        for s in hits["sanctions"]:
            red_flags.append(f"SANCTIONS hit on {party}: {s['list']} ({s['program']}).")
            evidence.append({"category": "sanctions", "summary": f"Sanctions match: {party}",
                             "detail": f"{s['list']} / {s['program']} / {s['country']}", "source": "screening:sanctions", "severity": "critical"})
            expedite = True
        for p in hits["pep"]:
            red_flags.append(f"PEP exposure via {party}: {p['role']}.")
            evidence.append({"category": "pep", "summary": f"PEP match: {party}",
                             "detail": f"{p['role']} ({p['country']})", "source": "screening:pep", "severity": "medium"})
    return {"customer": customer, "evidence": evidence, "red_flags": red_flags, "expedite": expedite}


def analyze_transactions(account_id: str, customer: dict) -> dict:
    txns = dao.get_transactions(account_id)
    hrj = dao.high_risk_jurisdictions()
    evidence: list[dict] = []
    red_flags: list[str] = []
    if not txns:
        return {"transactions": [], "evidence": [], "red_flags": []}

    near = [t for t in txns if t["direction"] == "credit" and STRUCTURING_BAND * CTR_THRESHOLD <= t["amount_usd"] < CTR_THRESHOLD]
    if len(near) >= 2:
        total = sum(t["amount_usd"] for t in near)
        red_flags.append(f"Structuring pattern: {len(near)} credits just below ${CTR_THRESHOLD:,} totaling ${total:,}.")
        evidence.append({"category": "transaction", "summary": "Sub-threshold structuring detected",
                         "detail": "; ".join(f"{t['txn_id']} {t['date']} ${t['amount_usd']:,}" for t in near),
                         "source": "analysis:structuring", "severity": "high"})

    by_day: dict[str, list] = defaultdict(list)
    for t in txns:
        by_day[t["date"]].append(t)
    for day, group in by_day.items():
        for c in [t for t in group if t["direction"] == "credit"]:
            for d in [t for t in group if t["direction"] == "debit"]:
                if c["amount_usd"] > 50000 and abs(c["amount_usd"] - d["amount_usd"]) / c["amount_usd"] < 0.05:
                    red_flags.append(f"Rapid movement on {day}: ${c['amount_usd']:,} in -> ${d['amount_usd']:,} out (~equal, same day).")
                    evidence.append({"category": "transaction", "summary": "Rapid in/out fund movement (layering indicator)",
                                     "detail": f"{c['txn_id']} -> {d['txn_id']} on {day}", "source": "analysis:layering", "severity": "high"})

    hrj_txns = [t for t in txns if t.get("counterparty_country") in hrj]
    if hrj_txns:
        countries = sorted({t["counterparty_country"] for t in hrj_txns})
        evidence.append({"category": "transaction", "summary": f"High-risk jurisdiction exposure: {', '.join(countries)}",
                         "detail": f"{len(hrj_txns)}/{len(txns)} transactions touch high-risk jurisdictions.",
                         "source": "analysis:geography", "severity": "medium"})

    monthly = sum(t["amount_usd"] for t in txns if t["direction"] == "credit")
    expected = customer.get("expected_monthly_volume_usd")
    if expected and monthly > 1.5 * expected:
        red_flags.append(f"Credit volume ${monthly:,} exceeds expected ${expected:,} by {monthly / expected:.1f}x.")
        evidence.append({"category": "transaction", "summary": "Activity exceeds expected profile",
                         "detail": f"observed=${monthly:,}, expected=${expected:,}", "source": "analysis:profile-deviation", "severity": "medium"})
    return {"transactions": txns, "evidence": evidence, "red_flags": red_flags}


def screen_adverse_media(customer: dict, transactions: list[dict]) -> dict:
    entities = {customer.get("legal_name", "")} | {t.get("counterparty", "") for t in transactions}
    entities.discard("")
    evidence: list[dict] = []
    red_flags: list[str] = []
    for entity in sorted(entities):
        for hit in dao.search_adverse_media(entity):
            sev = "high" if any(t in hit["tags"] for t in ("money-laundering", "trade-based-laundering")) else "medium"
            red_flags.append(f"Adverse media on {entity}: \"{hit['headline']}\" ({hit['source']}).")
            evidence.append({"category": "adverse_media", "summary": f"Negative news: {entity}",
                             "detail": f"{hit['headline']} — {hit['source']}, {hit['date']}", "source": f"osint:{hit['source']}", "severity": sev})
    return {"evidence": evidence, "red_flags": red_flags}


def score(evidence: list[dict]) -> int:
    return min(100, sum(SEVERITY_WEIGHT.get(e.get("severity", "info"), 0) for e in evidence))


def recommend(evidence: list[dict], total_score: int) -> str:
    if any(e["category"] == "sanctions" for e in evidence):
        return "ESCALATE"
    if total_score >= 55:
        return "FILE_SAR"
    if total_score >= 30:
        return "REQUEST_INFO"
    return "DISMISS"
