"""Mock core-banking / watchlist data access (shared logic with the LangGraph variant).

Reads the JSON fixtures in /data so the crew runs offline. In production these are
replaced by UiPath API Workflows / RPA robots calling real systems.
"""
from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any


def _data_dir() -> Path:
    override = os.getenv("SENTINEL_DATA_DIR")
    if override:
        return Path(override)
    # Prefer the copy bundled inside the package (src/data) so it travels with the
    # agent when deployed to UiPath; fall back to the repo-root data/ for local dev.
    bundled = Path(__file__).resolve().parent / "data"
    if bundled.exists():
        return bundled
    return Path(__file__).resolve().parents[3] / "data"


@lru_cache(maxsize=None)
def _load(name: str) -> Any:
    with (_data_dir() / name).open("r", encoding="utf-8") as fh:
        return json.load(fh)


def get_customer(customer_id: str) -> dict[str, Any] | None:
    return _load("customers.json").get(customer_id)


def get_transactions(account_id: str) -> list[dict[str, Any]]:
    return _load("transactions.json").get(account_id, [])


def screen_watchlists(name: str) -> dict[str, list[dict[str, Any]]]:
    wl = _load("watchlists.json")
    needle = name.lower().strip()
    match = lambda recs: [r for r in recs if needle and needle in r["name"].lower()]
    return {"sanctions": match(wl.get("sanctions", [])), "pep": match(wl.get("pep", []))}


def search_adverse_media(entity: str) -> list[dict[str, Any]]:
    needle = entity.lower().strip()
    return [a for a in _load("watchlists.json").get("adverse_media", []) if needle and needle in a["entity"].lower()]


def high_risk_jurisdictions() -> set[str]:
    return set(_load("watchlists.json").get("high_risk_jurisdictions", []))
