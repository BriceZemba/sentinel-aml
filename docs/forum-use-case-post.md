# UiPath Community Forum use-case post (finalist deliverable)

> Finalists must publish their solution as a use case on the UiPath Community
> Forum. This is a ready-to-post draft. Paste it into a new topic in the
> **Maestro / Agentic Automation** category, add your screenshots, and update the
> links. Keep it practical the community values reproducibility.

---

## Title
**Sentinel Agentic AML Investigation Case Manager on UiPath Maestro Case**

## Category & tags
Maestro · Case Management · Agentic Automation · Coded Agents · Agent Builder ·
Action Center · Document Understanding · LangGraph · CrewAI · Financial Services · AML

---

## TL;DR
Sentinel turns every AML transaction-monitoring alert into a governed **case** in
UiPath Maestro that flows through **Triage → Investigation → Narrative → Quality
Review → Disposition**. AI agents (low-code + coded) do the reasoning, robots do
the system-of-record work, and a compliance officer (MLRO) signs off every SAR
filing in Action Center. The whole lifecycle is orchestrated and audited by
Maestro. Built for UiPath AgentHack 2026, Track 1.

---

## The business problem
~95% of AML alerts are false positives, yet each one is investigated by hand and
must be signed off by an accountable human. It's slow, inconsistent, and costly.
The work is also unpredictable: each investigation branches differently as
evidence emerges. That combination a fixed goal but an emergent path, with
mandatory human accountability is exactly what **agentic case management** is for.

## Why Maestro Case
The path isn't knowable up front: a duplicate auto-closes, a sanctions hit
fast-tracks to a senior MLRO, a thin case loops back from QA to Investigation, an
SLA breach escalates. Maestro Case lets the **Case Manager Agent** hold state and
context across stages and decide paths dynamically, while **Stage Manager Agents**
drive each phase instead of forcing the work into a fixed flowchart.

## Architecture
```
  Triage ─▶ Investigation ─▶ Narrative Drafting ─▶ Quality Review ─▶ Disposition
```

| Actor | Built with | Type | Job |
|---|---|---|---|
| Case / Stage Managers | Maestro Case (native) | Orchestrator | Lifecycle, SLAs, escalation, audit |
| Triage | Agent Builder | Low-code agent | Dedup, classify, prioritize, route |
| Investigator | Python + LangGraph (`uipath-langchain`) | Coded agent | Entity resolution, transaction typologies, sanctions/PEP, adverse media → scored recommendation |
| Narrator | Python + LangGraph | Coded agent | Draft FinCEN 5-Ws SAR narrative; HITL gate |
| Quality Review | Agent Builder | Low-code agent | Evidence-sufficiency check; loop-back |
| DataFetcher / Filer / Notifier | Studio Web (API Workflows + RPA) | Robots | Pull data, file SAR, escalate |
| DocIntake | Document Understanding | Robot | KYC extraction |
| MLRO / Compliance Officer | Action Center | **Human** | Approve filing / dismissal |

A second **CrewAI** implementation of the Investigator ships in the repo with the
*same* input/output contract it drops in behind the Maestro Investigation stage
in place of the LangGraph one, demonstrating external frameworks running under one
UiPath governance layer.

## How it works (a real case)
1. An alert on **Halcyon Capital Partners** enters → Triage sets priority *high*,
   no duplicate → Investigation.
2. The Investigator resolves the entity (KYC expired), screens its owner (OFAC/EU
   **sanctions hit**), detects same-day **layering** ($240k in / $238.5k out) and
   corroborating **adverse media** → **risk score 100 → ESCALATE**, every finding
   citing a source.
3. The Narrator drafts a SAR narrative; QA confirms each claim is evidence-backed.
4. The case **suspends** at an Action Center task — the MLRO reviews and approves;
   a robot files the SAR and the case closes **SAR Filed**, fully audited.

Contrast: a routine teacher-payroll alert scores < 30 and is auto-**dismissed**; a
duplicate alert auto-closes at Triage.

## Exception & failure handling
Duplicate auto-close · sanctions fast-track · QA→Investigation rework loop with a
2-cycle loop guard · SLA-breach escalation · robot retries via Orchestrator ·
agents degrade to deterministic logic if the LLM is unavailable (a case is never
left without a result).

## UiPath components used
Maestro Case · Agent Builder · Coded Agents (Python SDK + `uipath-langchain`) ·
Action Center · API Workflows + RPA · Document Understanding · Orchestrator. Plus
external LangGraph/CrewAI agents under UiPath governance, and the solution was
built/deployed with **Claude Code via the `uip` CLI** (UiPath for Coding Agents).

## Results / impact
Multi-hour manual investigations compress to minutes of agent work plus one
focused human decision, with consistent rigor and a complete, reconstructable
audit trail fewer late filings and lower cost per alert. Production path: swap
the mocked connectors for core-banking, sanctions, and FinCEN E-Filing.

## Reproduce it
The two coded agents run **offline with no API key** (deterministic fallback) and
ship with passing tests:
```bash
# Investigator (LangGraph)
cd agents/investigation && pip install langgraph langchain-core pydantic pytest
python run_local.py ALT-2026-0512-002   # ESCALATE, score 100
pytest -q

# Narrator (LangGraph + Action Center HITL)
cd ../narrative && python run_local.py approve   # FILED

# Investigator (CrewAI variant same contract)
cd ../investigation-crewai && python run_local.py ALT-2026-0512-002
```
Full deploy + Maestro wiring: see the repo's `docs/` (`deploy-coded-agents.md`,
`agent-builder-setup.md`, `maestro-case-setup.md`).

## Screenshots
*(add: Maestro case audit view · Action Center SAR task · Investigator evidence
output · architecture diagram · Claude Code deploying via `uip`)*

## What's next
More typologies (trade-based laundering, funnel accounts), Context Grounding over
the bank's AML policy, and a fuller CrewAI/LangGraph A/B behind the same stage.

---

*Questions welcome — happy to share the agent contracts and the Maestro case
definition. Licensed MIT.*
