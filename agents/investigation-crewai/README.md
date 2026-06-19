# Investigator CrewAI variant

A **drop-in alternative** to the LangGraph [Investigator](../investigation/), built
with **CrewAI** instead. Same `InvestigationInput`/`InvestigationOutput` contract,
so UiPath Maestro can swap one for the other at the Investigation stage with **no
change to the rest of the case**. This is the "external frameworks under UiPath
governance" story made concrete.

## The crew
A role-based team that mirrors a real financial-intelligence unit:

| Agent | Role | Tool |
|---|---|---|
| KYC & Sanctions Analyst | Resolve customer + owners, screen sanctions/PEP | `resolve_entity_tool` |
| Transaction Analyst | Detect structuring/layering/geography/profile deviation | `analyze_transactions_tool` |
| OSINT Analyst | Adverse-media screen | `adverse_media_tool` |
| Lead Investigator | Weigh evidence → recommendation + rationale | (synthesizes) |

The **tools carry the auditable logic** ([`analysis.py`](src/analysis.py)); the LLM
agents orchestrate and narrate they never invent the risk score. Same scoring
weights as the LangGraph variant, so decisions match.

## Two execution modes (automatic)
- **Crew mode** with `ANTHROPIC_API_KEY` (or `OPENAI_API_KEY`) set and `crewai`
  installed, the real role-based crew runs.
- **Deterministic mode** otherwise the same tools run in sequence directly.
  Identical contract, fully offline, zero credentials. If a crew run errors, it
  falls back to deterministic so a case is never left without a result.

## Run / test (offline)
```bash
python -m venv .venv && . .venv/Scripts/activate
pip install pydantic pytest        # crewai only needed for real crew mode
python run_local.py ALT-2026-0512-002   # -> ESCALATE, framework=crewai-deterministic
pytest -q                                # 3 contract-parity tests
```
Real crew: also `pip install crewai` and set `ANTHROPIC_API_KEY`.

## Deploy to UiPath
Entry point is `src/runner.py:run(input_dict) -> dict` (see [uipath.json](uipath.json)).
Package and publish with the UiPath CLI exactly like the LangGraph agent
([../../docs/deploy-coded-agents.md](../../docs/deploy-coded-agents.md)); then point
the Maestro Investigation stage at whichever variant you want to run.
