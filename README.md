# Sentinel — Agentic AML Investigation Case Manager

> **UiPath AgentHack 2026 · Track 1: UiPath Maestro Case**
> An agentic financial-crime investigation desk that turns transaction-monitoring
> alerts into regulator-ready dispositions — orchestrated end to end by UiPath
> Maestro Case, with a compliance officer accountable for every filing.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## The business problem

Banks generate enormous volumes of AML transaction-monitoring alerts, and roughly
**95% are false positives**. Each one is still triaged, investigated, and
documented by hand: an analyst pulls transactions from the core banking system,
resolves the customer and counterparties, screens sanctions/PEP lists, searches
adverse media, writes a Suspicious Activity Report (SAR) narrative, and routes it
for compliance sign-off. It is slow, expensive, inconsistent, and **mandated by
law to keep a human accountable** for the final filing decision.

This is the textbook case for **agentic case management**: the *goal* is fixed
(decide and document each alert correctly), but the *path is not* — every
investigation branches differently as evidence emerges, loops back when a case is
thin, and escalates when sanctions or SLAs are in play.

## What Sentinel does

Each alert becomes a **case** in UiPath Maestro that moves through five stages.
Agents, robots, and people each do the part they are best at; Maestro coordinates
them and keeps a complete audit trail.

```
  Triage ─▶ Investigation ─▶ Narrative Drafting ─▶ Quality Review ─▶ Disposition
   (1)          (2)                (3)                  (4)              (5)
```

| Stage | Actor | What happens |
|---|---|---|
| **1. Triage** | Triage Agent *(low-code)* | Dedup, classify typology, set priority/SLA, route |
| **2. Investigation** | Investigator *(coded, LangGraph)* + DataFetcher robot | Resolve entities, analyze transactions, screen sanctions/PEP, adverse media → scored recommendation with citable evidence |
| **3. Narrative** | Narrator *(coded, LangGraph)* | Draft a FinCEN "5 Ws" SAR narrative from the evidence |
| **4. Quality Review** | QA Agent *(low-code)* | Verify every claim is evidence-backed; **loop back to (2)** if thin |
| **5. Disposition** | **MLRO / Compliance Officer (human)** via Action Center; then Filer robot | Approve → file SAR; reject → dismiss or rework. **No filing without human sign-off.** |

### Dynamic, exception-heavy behavior (why this is a *Case*, not a BPMN flow)
- **Duplicate alerts** auto-close at Triage and link to the open case.
- **Sanctions hit** → case fast-tracks to senior MLRO (skips ahead, raises priority).
- **Thin investigation** → QA bounces it back to Investigation with specific `gaps`; the Investigator re-runs *only* the requested checks (with a 2-cycle loop guard).
- **SLA breach** → Maestro escalates to a supervisor automatically.
- **Missing KYC** → Document Understanding + an RFI follow-up task.

## UiPath components used

| Component | Role in Sentinel |
|---|---|
| **UiPath Maestro — Case Management** | Orchestrates the 5-stage case lifecycle, SLAs, escalation, audit trail (Case Manager + Stage Manager agents) |
| **Agent Builder (low-code agents)** | Triage Agent, Quality Review Agent |
| **Coded Agents (Python SDK + `uipath-langchain`)** | Investigator and Narrator LangGraph agents |
| **Action Center** | Human-in-the-loop MLRO sign-off (the Narrator's interrupt) |
| **Studio Web / API Workflows + RPA** | DataFetcher, Filer, Notifier robots |
| **Document Understanding (IDP)** | KYC document extraction |
| **Orchestrator** | Hosts/schedules the coded agents and robots; job logs feed the audit trail |
| **UiPath for Coding Agents (`uip` CLI + skills)** | This solution was **built and deployed with Claude Code** — see [CODING_AGENTS.md](CODING_AGENTS.md) |

## Agent type

**Both.** Sentinel deliberately blends **low-code agents** (Triage, QA — Agent
Builder) with **coded agents** (Investigator, Narrator — Python/LangGraph deployed
via the UiPath Python SDK), plus deterministic **RPA/API robots**, all governed by
Maestro. This hybrid is intentional: reasoning tasks go to agents, exact
system-of-record tasks go to robots, and the legally accountable decision goes to
a human.

## Coding agents (bonus)

This entire repository — the LangGraph crews, the risk-scoring logic, the tests,
and the deployment scripts — was built using **Claude Code** driving the **UiPath
`uip` CLI and skills** ("UiPath for Coding Agents"). Evidence (prompt log,
screenshots, the exact CLI flow) is in **[CODING_AGENTS.md](CODING_AGENTS.md)**.

---

## Repository layout

```
sentinel-aml/
├── agents/
│   ├── triage/              Triage Agent spec (Agent Builder, low-code)
│   ├── investigation/       Investigator — LangGraph coded agent (tested, runnable offline)
│   ├── investigation-crewai/ Investigator — CrewAI variant, SAME contract (drop-in swap)
│   ├── narrative/           Narrator — LangGraph coded agent w/ Action Center HITL
│   └── qa/                  Quality Review Agent spec (Agent Builder, low-code)
├── rpa/                DataFetcher / Filer / Notifier workflow contracts + IDP
├── data/              Mock core-banking, transactions, alerts, watchlists (offline demo)
├── docs/
│   ├── architecture.md         Full architecture + case-flow diagram
│   ├── maestro-case-setup.md   Click-path to build the case in Studio Web/Maestro
│   ├── agent-builder-setup.md  Build the low-code agents
│   ├── deploy-coded-agents.md  uip CLI: init → pack → publish → deploy
│   ├── demo-script.md          5-minute video script (shot list)
│   ├── deck-outline.md         Presentation deck outline
│   ├── deck/                   Sentinel-Deck.pptx + build_deck.js (generated, editable)
│   ├── devpost-description.md  Copy/paste-ready Devpost project description
│   ├── build-plan.md           Week-by-week plan to submission
│   ├── devpost-submission.md   Step-by-step Devpost submission guide
│   ├── forum-use-case-post.md  Finalist UiPath Community Forum write-up
│   └── feedback-notes.md       Notes for the Best Product Feedback prize
└── CODING_AGENTS.md   How Claude Code built this (bonus-point evidence)
```

## Quickstart (run the agents offline — no UiPath account needed)

Prerequisites: **Python 3.11–3.13**, `git`.

```bash
# 1) Investigator — turn an alert into a scored, evidence-backed recommendation
cd agents/investigation
python -m venv .venv && . .venv/Scripts/activate     # macOS/Linux: source .venv/bin/activate
pip install langgraph langchain-core pydantic pytest
python run_local.py ALT-2026-0512-002                # sanctions+layering case -> ESCALATE
pytest -q                                            # 3 passing tests

# 2) Narrator — draft a SAR and walk the human-in-the-loop interrupt/resume
cd ../narrative
python -m venv .venv && . .venv/Scripts/activate
pip install langgraph langchain-core pydantic pytest
python run_local.py approve                          # MLRO approves -> FILED
python run_local.py reject                           # MLRO rejects  -> RETURNED_FOR_REWORK
pytest -q
```

Optional: set `ANTHROPIC_API_KEY` in a `.env` to have Claude write the rationale
and SAR narrative (the agents run with a deterministic template if it's absent,
so judges can test with zero credentials).

## Deploy to UiPath (full solution)

Follow, in order:
1. **[docs/deploy-coded-agents.md](docs/deploy-coded-agents.md)** — `uip auth → init → pack → publish`, run on Orchestrator.
2. **[docs/agent-builder-setup.md](docs/agent-builder-setup.md)** — build Triage + QA agents.
3. **[docs/maestro-case-setup.md](docs/maestro-case-setup.md)** — define the case, stages, SLAs, escalation, and wire every actor.

## License

[MIT](LICENSE). Applies to this repo's original code only; UiPath platform
components and SDK packages remain under their own licenses.
