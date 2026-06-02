# Devpost project description — copy/paste ready

> Paste the **Elevator pitch** into the short tagline field, and the **About the
> project** body into the main description editor (Devpost supports Markdown).
> Set **Track = UiPath Maestro Case**. Built With tags are at the bottom.

---

## Elevator pitch (≤ 200 chars)
An agentic financial-crime investigation desk on UiPath Maestro Case: AI agents investigate AML alerts, robots act on systems of record, and a compliance officer signs off every filing — fully audited.

---

## About the project

### 🚨 The problem
Banks generate millions of AML transaction-monitoring alerts a year, and roughly
**95% are false positives**. Every single one is still investigated by hand: an
analyst pulls transactions from core banking, resolves the customer and its
counterparties, screens sanctions and PEP lists, searches adverse media, writes a
Suspicious Activity Report (SAR) narrative, and routes it for compliance sign-off.
It's slow, expensive, inconsistent across analysts — and **the final filing
decision is legally required to stay with an accountable human**.

This is the definition of work that needs **agentic case management**: the *goal*
is fixed (decide and document every alert correctly and on time), but the *path is
not* — each investigation branches as evidence emerges, loops back when a case is
thin, and escalates the moment sanctions or SLA deadlines come into play.

### 🛡️ What Sentinel does
Sentinel turns every alert into a **case** in UiPath Maestro that moves through
five stages, with the right actor doing each task:

1. **Triage** — a low-code Agent Builder agent deduplicates, classifies the
   typology, sets priority/SLA, and routes (duplicates auto-close instantly).
2. **Investigation** — a coded LangGraph agent resolves entities, runs
   deterministic transaction-typology detection (sub-threshold structuring,
   same-day layering, high-risk geography), screens sanctions/PEP, and checks
   adverse media — producing a **transparent risk score** and a recommendation
   where **every finding cites its source**.
3. **Narrative Drafting** — a second coded agent drafts a FinCEN "5 Ws" SAR
   narrative from that evidence.
4. **Quality Review** — a low-code agent verifies every claim is evidence-backed
   and **loops the case back to Investigation** with specific gaps if it's thin
   (with a 2-cycle loop guard).
5. **Disposition** — the case suspends for a **human MLRO** in **UiPath Action
   Center**. Approve → a robot files the SAR; reject → dismiss with rationale or
   send to rework. **No SAR is ever filed without a human decision.**

### 🧠 Why it's a *Case*, not a fixed flow
The behavior is dynamic and exception-heavy by design: duplicate auto-close,
sanctions fast-track to a senior MLRO, QA→Investigation rework loops, SLA-breach
escalation, and missing-KYC follow-ups via Document Understanding. The path
emerges as the work unfolds — exactly what Maestro Case is built for.

### 🏗️ How we built it
- **UiPath Maestro — Case Management** orchestrates the five-stage lifecycle, SLAs,
  escalation, and the audit trail.
- **Coded agents (UiPath Python SDK + `uipath-langchain`)**: the **Investigator**
  and **Narrator** are LangGraph graphs deployed to Orchestrator. The Narrator's
  `interrupt()` maps natively to an **Action Center** task for human sign-off.
- **Low-code agents (Agent Builder)**: the **Triage** and **Quality Review** agents.
- **API Workflows + RPA**: DataFetcher (pull transactions/KYC), Filer (submit the
  SAR), Notifier (escalations).
- **Document Understanding (IDP)** extracts KYC fields when fresh CDD is needed.
- **Governance by design**: agents never touch source systems — robots do, behind
  the UiPath credential vault, with every step logged.

The risk score is a transparent weighted sum over evidence severity, so a reviewer
can reconstruct any decision — the LLM writes the *rationale*, never the score.
The agents run **offline with no API key** (deterministic fallback) so anyone can
test the repo instantly.

### 🤖 Built with coding agents (bonus)
The entire coded core — the LangGraph crews, the risk logic, the test suites, and
the deployment scripts — was built using **Claude Code** driving the **UiPath
`uip` CLI and skills** ("UiPath for Coding Agents"). The coded agents pass an
automated test suite and run live on Orchestrator as part of the case. Evidence
(CLI flow, screenshots, prompt log) is in the repo's `CODING_AGENTS.md`.

### 🧩 Agent type
**Both coded and low-code.** Reasoning over messy evidence goes to coded
LangGraph agents; fast, schema-checkable judgments go to low-code Agent Builder
agents; deterministic system-of-record actions go to robots; the accountable
decision goes to a human. All governed by Maestro.

### 📈 Impact
Sentinel compresses a multi-hour manual investigation into minutes of agent work
plus one focused human decision, with consistent quality and a complete audit
trail — fewer late filings, lower cost per alert, and decisions a regulator can
follow end to end.

### 🔭 What's next
A CrewAI variant of the Investigator (role-based crew, same contract, swappable
behind the Maestro stage), more typologies (trade-based laundering, funnel
accounts), and Context Grounding over the bank's AML policy so agents cite
thresholds directly.

---

## Built With
`uipath` · `uipath-maestro` · `maestro-case-management` · `agent-builder` ·
`action-center` · `document-understanding` · `orchestrator` · `coded-agents` ·
`python` · `langgraph` · `langchain` · `claude` · `claude-code` · `anthropic` · `aml` · `regtech`

## Links
- **GitHub:** https://github.com/<you>/sentinel-aml
- **Demo video:** <YouTube/Vimeo link>
- **Presentation deck:** <Drive/OneDrive link, public>
