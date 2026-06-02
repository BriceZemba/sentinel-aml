# Deploy the coded agents to UiPath

This deploys the **Investigator** and **Narrator** LangGraph agents to UiPath
Orchestrator using the UiPath Python SDK / CLI. Do this once per agent.

## Prerequisites
- A UiPath Automation Cloud / Labs tenant (from your AgentHack lab access email).
- Python 3.11–3.13 and `pip`.
- (Recommended) `uv` for fast installs: `pip install uv`.
- The UiPath CLI for coding agents: `npm i -g @uipath/cli` (provides `uip`).

## 1. Install the Python SDK packages
```bash
cd agents/investigation
python -m venv .venv && . .venv/Scripts/activate    # Linux/mac: source .venv/bin/activate
pip install uipath uipath-langchain langgraph langchain-core langchain-anthropic pydantic python-dotenv
```

## 2. Authenticate to your tenant
```bash
uipath auth
```
Opens a browser, then writes `UIPATH_URL` and `UIPATH_ACCESS_TOKEN` into `.env`.
Copy `.env.example` to `.env` first and add `ANTHROPIC_API_KEY` if you want
LLM-written rationale/narrative.

## 3. Generate entry points
```bash
uipath init
```
Reads `langgraph.json` (graph `investigator` → `./src/graph.py:graph`) and
generates `entry-points.json`. The Pydantic `InvestigationInput`/`Output` models
become the agent's input/output contract in UiPath.

## 4. Package and publish
```bash
uipath pack            # -> sentinel-investigator.<version>.nupkg
uipath publish         # uploads the package to your Orchestrator tenant
```

## 5. Run / verify
- In **Orchestrator**, find the published process in your folder, create a job,
  and pass a test input:
  ```json
  { "alert_id": "ALT-2026-0512-002", "customer_id": "CUST-30555",
    "account_id": "ACC-770233", "rule": "RAPID_MOVEMENT_FUNDS", "priority": "high" }
  ```
- Or test locally first: `uipath run investigator '{"alert_id":"ALT-2026-0512-002","customer_id":"CUST-30555","account_id":"ACC-770233","rule":"RAPID_MOVEMENT_FUNDS","priority":"high"}'`

## 6. Repeat for the Narrator
```bash
cd ../narrative
# steps 1–5 again. graph name is `narrator`.
```
The Narrator contains a human-in-the-loop `interrupt()`. On UiPath this creates an
**Action Center task** and the job suspends until the MLRO submits the decision —
no extra code needed; the `uipath-langchain` runtime maps the interrupt to Action
Center and supplies the checkpointer.

## 7. (Bonus) Do all of this through Claude Code
Once `uip skills install --agent claude` is run, you can drive every command above
from Claude Code in natural language ("pack and publish this agent to the Shared
folder"). Capture that session for the coding-agent bonus — see
[../CODING_AGENTS.md](../CODING_AGENTS.md).

## Troubleshooting
| Symptom | Fix |
|---|---|
| `uipath init` finds no graph | Check `langgraph.json` path matches `src/graph.py:graph` |
| Auth fails | Re-run `uipath auth`; confirm tenant URL from the lab email |
| Interrupt never resumes | Ensure the Action Center app is mapped to the Narrator's task type and assigned to a user/queue |
| Package version conflict | Bump `version` in `pyproject.toml` before `uipath pack` |
