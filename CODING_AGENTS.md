# How this solution was built with coding agents (bonus-point evidence)

UiPath AgentHack awards **up to +2 bonus points** (Platform Usage criterion) for
solutions built with coding agents through *UiPath for Coding Agents*. This file
is the verifiable record. To claim the full 2 points, the reviewer must be able
to independently verify the claim — so this page is structured around evidence.

## (a) Which coding agent / AI-assisted tool was used
**Claude Code** (Anthropic's CLI coding agent), driving the **UiPath `uip` CLI**
and installed **UiPath skills** ("UiPath for Coding Agents").

## (b) How it contributed to the solution
Claude Code did the actual build, not just suggestions:

| Area | What the coding agent produced |
|---|---|
| Agent scaffolding | The full LangGraph graphs for the **Investigator** and **Narrator** coded agents (`agents/*/src/`) |
| Risk logic | The transparent, auditable typology detection in `transaction_analysis.py` and weighted scoring in `synthesize.py` |
| HITL integration | The Action Center interrupt/resume pattern in the Narrator (`human_review` node) |
| Test creation | `tests/test_graph.py` and `tests/test_narrative.py` (all passing) |
| Deployment glue | The `uip` CLI flow in `docs/deploy-coded-agents.md`, `langgraph.json`, `uipath.json`, `pyproject.toml` |
| Docs | Architecture, Maestro setup, demo script, this evidence file |

## (c) Proof the output is meaningfully integrated
The coded agents are the working core of the running solution — they execute on
UiPath Orchestrator as part of the live Maestro case, and they pass an automated
test suite:

```
agents/investigation $ pytest -q
...                                                          [100%]
3 passed

agents/narrative $ pytest -q
..                                                           [100%]
2 passed
```

## The `uip` CLI flow used (UiPath for Coding Agents)

Claude Code installs the UiPath skills once, then uses them like a developer:

```bash
# one-time: teach the coding agent the UiPath surface
uip skills install --agent claude     # installs UiPath skills globally for Claude Code

# per coded agent: authenticate, generate entry points, package, publish, run
cd agents/investigation
uipath auth                            # browser login, writes tokens to .env
uipath init                            # reads langgraph.json -> entry-points.json
uipath pack                            # builds the .nupkg
uipath publish                         # uploads to Orchestrator
# then: deploy + run the process from the Orchestrator folder (or `uip` deploy run)
```

After installing skills, Claude Code knows the canonical chain
(`pack → publish → deploy run`), how to wait for a job, and how to inspect an
Orchestrator folder — so the whole build/deploy/operate loop happens from the
terminal under UiPath governance (policy, audit, credential vault, RBAC).

## ▶️ What YOU still need to add before submitting (do not skip — this is the proof)
Reviewers want first-hand evidence. Capture at least one of:

1. **Screenshots** of your Claude Code session building/deploying the agents
   (terminal showing `uipath pack/publish`, the agent editing files). Save to
   `docs/images/claude-code-*.png` and reference them here.
2. **A prompt/session log** — export your Claude Code session and commit it as
   `docs/claude-code-session.md` (or a transcript snippet).
3. **In the demo video**, show ~20–30 seconds of Claude Code + `uip` actually
   building or deploying part of the solution (the rules explicitly reward this).

> Tip: the strongest, cheapest +2 is a short clip in the video of `uipath publish`
> succeeding from your terminal, plus this file. That is independently verifiable.
