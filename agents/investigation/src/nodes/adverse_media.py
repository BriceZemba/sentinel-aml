"""Adverse Media node.

OSINT-style negative-news screen over the subject and its key counterparties.
In production this calls a media-intelligence API (or an RPA robot that drives a
web search); offline it reads the curated adverse_media fixtures.
"""
from __future__ import annotations

import data_access as dao
from state import InvestigationState


def adverse_media(state: InvestigationState) -> dict:
    customer = state.get("customer", {})
    txns = state.get("transactions", [])
    evidence: list[dict] = []
    red_flags: list[str] = []

    # Build the set of entities worth screening: subject + distinct counterparties.
    entities = {customer.get("legal_name", "")}
    entities |= {t.get("counterparty", "") for t in txns}
    entities.discard("")

    for entity in sorted(entities):
        for hit in dao.search_adverse_media(entity):
            sev = "high" if any(t in hit["tags"] for t in ("money-laundering", "trade-based-laundering")) else "medium"
            red_flags.append(f"Adverse media on {entity}: \"{hit['headline']}\" ({hit['source']}).")
            evidence.append({
                "category": "adverse_media",
                "summary": f"Negative news: {entity}",
                "detail": f"{hit['headline']} - {hit['source']}, {hit['date']} [tags: {', '.join(hit['tags'])}]",
                "source": f"osint:{hit['source']}",
                "severity": sev,
            })

    return {"evidence": evidence, "red_flags": red_flags}
