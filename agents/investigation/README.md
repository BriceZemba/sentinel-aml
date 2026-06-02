# Investigator — coded agent (LangGraph)

Turns one AML alert into auditable evidence + a scored recommendation. Deployed to
UiPath as a coded agent; runs offline for development/testing.

## Graph
`ingest → entity_resolution → transaction_analysis → adverse_media → synthesize`

- **entity_resolution** — resolve customer + beneficial owners; screen sanctions/PEP; KYC freshness.
- **transaction_analysis** — deterministic typologies: sub-threshold structuring, same-day layering, high-risk geography, profile deviation.
- **adverse_media** — negative-news screen over subject + counterparties.
- **synthesize** — transparent weighted risk score (0–100) + recommendation (`FILE_SAR` / `DISMISS` / `ESCALATE` / `REQUEST_INFO`). The LLM writes the rationale only; the score is reconstructable.

## Contract
- Input: `InvestigationInput` (`alert_id, customer_id, account_id, rule, priority`).
- Output: `InvestigationOutput` (`risk_score, recommendation, rationale, red_flags[], evidence[], sla_breach_risk`).

## Run / test (offline)
```bash
python -m venv .venv && . .venv/Scripts/activate
pip install langgraph langchain-core pydantic pytest
python run_local.py ALT-2026-0512-002   # ESCALATE, score 100
pytest -q                                # 3 passing
```
Set `ANTHROPIC_API_KEY` for LLM-written rationale (optional).

## Deploy
See [../../docs/deploy-coded-agents.md](../../docs/deploy-coded-agents.md).
