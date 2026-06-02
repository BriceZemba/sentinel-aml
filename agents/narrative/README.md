# Narrator — coded agent (LangGraph + Action Center HITL)

Drafts a FinCEN "5 Ws" SAR narrative from the investigation evidence, then
**suspends for an MLRO decision** before any filing.

## Graph
`draft → human_review (INTERRUPT) → finalize`

The `human_review` node calls LangGraph `interrupt()`. On UiPath this becomes an
**Action Center task** assigned to the compliance officer; the job suspends and
resumes only when they submit. No SAR is filed without this human decision.

### Human response shape
```json
{ "action": "approve|edit|reject", "decided_by": "mlro@bank.com",
  "edited_narrative": "<text, for edit>", "notes": "<for reject>" }
```
- `approve` / `edit` → `disposition = FILED`
- `reject` → `disposition = RETURNED_FOR_REWORK`

## Contract
- Input: `NarrativeInput` (investigation output + `customer_name`).
- Output: `NarrativeOutput` (`disposition, sar_narrative, decided_by, decision_notes`).

## Run / test (offline — walks the interrupt/resume cycle)
```bash
python -m venv .venv && . .venv/Scripts/activate
pip install langgraph langchain-core pydantic pytest
python run_local.py approve   # -> FILED
python run_local.py reject    # -> RETURNED_FOR_REWORK
pytest -q                     # 2 passing
```

## Deploy
See [../../docs/deploy-coded-agents.md](../../docs/deploy-coded-agents.md).
