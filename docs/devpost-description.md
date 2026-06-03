# Devpost project description — copy/paste ready

> Paste the **Elevator pitch** into the short tagline field, and the **About the
> project** body (the `##` sections) into the main description editor — they match
> Devpost's default headers exactly. Set **Track = UiPath Maestro Case**.

---

## Elevator pitch (≤ 200 chars)
An agentic financial-crime investigation desk on UiPath Maestro Case: AI agents investigate AML alerts, robots act on systems of record, and a compliance officer signs off every filing — fully audited.

---

# About the project

## Inspiration

Banks generate millions of AML transaction-monitoring alerts a year, and roughly **95% are false positives**. Every single one is still investigated by hand: an analyst pulls transactions from core banking, resolves the customer and its counterparties, screens sanctions and PEP lists, searches adverse media, writes a Suspicious Activity Report (SAR) narrative, and routes it for compliance sign-off. It is slow, expensive, inconsistent from one analyst to the next, and the final filing decision is legally required to stay with an accountable human.

That is the definition of work that needs **agentic case management**: the goal is fixed (decide and document every alert correctly and on time), but the path is not. Each investigation branches as evidence emerges, loops back when a case is thin, and escalates the moment sanctions or an SLA deadline comes into play. A fixed flowchart can't model that, but a case can. That gap is what I set out to close with Sentinel.

## What it does

Sentinel turns every alert into a governed **case** in UiPath Maestro that moves through five stages, with the right kind of worker on each task:

- **Triage:** a low-code Agent Builder agent deduplicates, classifies the typology, sets priority and SLA, and routes (duplicates auto-close instantly).
- **Investigation:** a coded LangGraph agent resolves the entity, runs transaction-typology detection (sub-threshold structuring, same-day layering, high-risk geography), screens sanctions/PEP, and checks adverse media. It outputs a transparent risk score and a recommendation where **every finding cites its source**.
- **Narrative:** a second coded agent drafts a FinCEN "5 Ws" SAR narrative from that evidence.
- **Quality Review:** a low-code agent checks that every claim is evidence-backed and **loops the case back to Investigation** with specific gaps if it's thin.
- **Disposition:** the case suspends for a human **MLRO** in UiPath Action Center. Approve and a robot files the SAR; reject and it's dismissed with a rationale. **No SAR is ever filed without a human decision.**

The behavior is deliberately exception-heavy: duplicates close themselves, sanctions hits fast-track to a senior MLRO, weak cases loop back with a guard against infinite cycles, and SLA breaches escalate. Every step is recorded against the case, so a regulator can follow exactly how each decision was made.

## How we built it

UiPath Maestro Case is the control plane. On top of it I combined:

- **Coded agents** (Python + LangGraph via `uipath-langchain`) for the Investigator and Narrator, deployed to Orchestrator. The Narrator's `interrupt()` maps natively to an Action Center task for human sign-off.
- **Low-code agents** (Agent Builder) for Triage and Quality Review.
- **API Workflows + RPA** for the deterministic, system-of-record work (pull data, file the SAR, send escalations) and **Document Understanding** for KYC extraction.
- A second **CrewAI** build of the Investigator with the same input/output contract, so it drops in behind the same Maestro stage, letting external frameworks run under one governance layer.

The risk score is a transparent weighted sum over evidence severity, so it can be reconstructed by a reviewer; the LLM writes the rationale, never the score. I built and deployed the coded agents using **Claude Code through the UiPath `uip` CLI** ("UiPath for Coding Agents"), and the agents run offline with a deterministic fallback so anyone can test the repo with no credentials.

## Challenges we ran into

- **Learning UiPath from zero.** This was my first UiPath project, so wiring Maestro Case stages, Action Center, and coded-agent deployment was a real climb.
- **Human-in-the-loop across a coded agent.** Getting a LangGraph `interrupt()` to surface as an Action Center task and then resume the suspended graph with the officer's decision took careful design of the resume payload and a checkpointer.
- **Keeping decisions defensible.** AML is regulated, so I had to make sure the LLM never invents the score. It only narrates a score the code computed transparently.
- **Making it testable.** I wanted judges to run it without a UiPath tenant or an API key, which meant building a deterministic fallback path that mirrors the real one.
- **A genuine bug.** A LangGraph state reducer was duplicating evidence on the final projection; I caught it by running the agent and reading the output, and fixed it.

## Accomplishments that we're proud of

- A working, **tested**, end-to-end solution with 8 passing automated tests across the coded agents, and it runs fully offline.
- **Two agent frameworks (LangGraph and CrewAI) behind one UiPath contract**, producing identical decisions, swappable at the Maestro stage.
- A human-in-the-loop gate that is real and binding, not decorative: it legally controls whether a SAR is filed.
- **Transparent, reconstructable risk scoring** instead of a black box, which is what a regulated domain actually needs.
- Built solo, as a first-time UiPath builder, with coding agents doing the heavy lifting on the coded components.

## What we learned

- The practical difference between **BPMN and agentic case management** (flow complexity versus context complexity, path versus goal), and how to tell which one a problem needs.
- How to assign the **right actor to each task**: reasoning to agents, exact actions to robots, accountability to a human.
- How UiPath can govern **external frameworks** (LangChain/LangGraph, CrewAI) while keeping credentials, logging, and policy centralized.
- How to package and deploy coded agents with the `uip` CLI, and how coding agents fit into the UiPath SDLC.
- Designing for **auditability and graceful degradation** from the start, rather than bolting them on.

## What's next for Sentinel AML

- More typologies: trade-based laundering, funnel accounts, and smurfing networks.
- **Context Grounding** over a bank's AML policy so the agents cite the exact thresholds they apply.
- Swapping the mocked connectors for real ones: core banking, a sanctions provider, and the FinCEN BSA E-Filing portal.
- A live A/B between the LangGraph and CrewAI investigators, and production hardening (retries, rate limits, queue-based intake at scale).

---

## Built With
`uipath` · `uipath-maestro` · `maestro-case-management` · `agent-builder` ·
`action-center` · `document-understanding` · `orchestrator` · `coded-agents` ·
`python` · `langgraph` · `langchain` · `crewai` · `claude` · `claude-code` · `anthropic` · `aml` · `regtech`

## Links
- **GitHub:** https://github.com/<you>/sentinel-aml
- **Demo video:** <YouTube/Vimeo link>
- **Presentation deck:** <Drive/OneDrive link, public>
