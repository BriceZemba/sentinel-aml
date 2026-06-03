"""Entity Resolution node.

Resolves the subject customer and its beneficial owners, screens every resolved
party against sanctions / PEP lists, and flags KYC freshness problems. Emits
evidence and red flags into shared state.
"""
from __future__ import annotations

import data_access as dao
from state import InvestigationState


def entity_resolution(state: InvestigationState) -> dict:
    customer = dao.get_customer(state["customer_id"]) or {}
    evidence: list[dict] = []
    red_flags: list[str] = []
    expedite = False

    if not customer:
        red_flags.append("Subject customer could not be resolved in core banking.")
        return {"customer": {}, "evidence": evidence, "red_flags": red_flags}

    evidence.append({
        "category": "entity",
        "summary": f"Resolved subject: {customer.get('legal_name')} ({customer['customer_id']})",
        "detail": (
            f"Type={customer.get('type')}, inc_country={customer.get('incorporation_country')}, "
            f"risk_rating={customer.get('risk_rating')}, business={customer.get('business_description')}"
        ),
        "source": "core-banking:customers",
        "severity": "info",
    })

    # KYC freshness
    if customer.get("kyc_status") != "verified":
        red_flags.append(f"KYC status is '{customer.get('kyc_status')}' (not verified).")
        evidence.append({
            "category": "kyc",
            "summary": "KYC not in good standing",
            "detail": f"kyc_status={customer.get('kyc_status')}, last_reviewed={customer.get('kyc_last_reviewed')}",
            "source": "core-banking:kyc",
            "severity": "high",
        })
        expedite = True

    # Screen the entity and every beneficial owner
    parties = [customer.get("legal_name", "")]
    parties += [bo["name"] for bo in customer.get("beneficial_owners", [])]

    for party in filter(None, parties):
        hits = dao.screen_watchlists(party)
        for s in hits["sanctions"]:
            red_flags.append(f"SANCTIONS hit on {party}: {s['list']} ({s['program']}).")
            evidence.append({
                "category": "sanctions",
                "summary": f"Sanctions match: {party}",
                "detail": f"{s['list']} / {s['program']} / country={s['country']}",
                "source": "screening:sanctions",
                "severity": "critical",
            })
            expedite = True
        for p in hits["pep"]:
            evidence.append({
                "category": "pep",
                "summary": f"PEP match: {party}",
                "detail": f"{p['role']} ({p['country']})",
                "source": "screening:pep",
                "severity": "medium",
            })
            red_flags.append(f"PEP exposure via {party}: {p['role']}.")

    return {
        "customer": customer,
        "evidence": evidence,
        "red_flags": red_flags,
        "expedite": expedite,
    }
