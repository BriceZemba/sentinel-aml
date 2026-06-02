# Architecture

Sentinel is an **agentic case-management** system. UiPath Maestro Case is the
control plane; agents (low-code + coded), robots, and a human are the actors it
orchestrates. Nothing acts outside Maestro's governance and audit trail.

## Actor map

| Actor | Built with | Type | Why this actor |
|---|---|---|---|
| Case Manager Agent | Maestro Case (native) | Orchestrator | Owns case state/lifecycle, decides paths |
| Stage Manager Agents | Maestro Case (native) | Orchestrator | Drive each stage to completion + SLAs |
| Triage Agent | Agent Builder | Low-code agent | Dedup/classify/route — fast, policy-grounded |
| Investigator | Python + LangGraph (`uipath-langchain`) | Coded agent | Multi-step reasoning over messy evidence |
| Narrator | Python + LangGraph (`uipath-langchain`) | Coded agent | Drafts regulator-grade narrative; HITL gate |
| QA Agent | Agent Builder | Low-code agent | Strict, schema-checkable sufficiency review |
| DataFetcher / Filer / Notifier | Studio Web (API Workflows + RPA) | Robot | Deterministic system-of-record actions |
| DocIntake | Document Understanding (IDP) | Robot | Structured extraction from KYC docs |
| MLRO / Compliance Officer | Action Center task | **Human** | Legally accountable for filing/dismissal |

## Case lifecycle

```mermaid
flowchart TD
    A([Alert from Transaction Monitoring]) --> T

    subgraph S1[Stage 1 · Triage]
        T[Triage Agent<br/>low-code]
    end
    T -->|duplicate| DUP([Closed – Duplicate])
    T -->|routine low-value| DIS0([Closed – No Action])
    T -->|investigate| INV

    subgraph S2[Stage 2 · Investigation]
        DF[DataFetcher robot<br/>pull txns + KYC] --> INV[Investigator agent<br/>coded · LangGraph]
        INV --> EVID[(Evidence + risk score<br/>+ recommendation)]
    end
    EVID -->|sanctions hit| ESC[[Escalate: senior MLRO<br/>fast-track]]
    EVID --> NAR

    subgraph S3[Stage 3 · Narrative Drafting]
        NAR[Narrator agent<br/>coded · LangGraph]
    end
    NAR --> QA

    subgraph S4[Stage 4 · Quality Review]
        QA[QA Agent<br/>low-code]
    end
    QA -->|FAIL: gaps| INV
    QA -->|PASS| DISP

    subgraph S5[Stage 5 · Disposition]
        HUM{{MLRO review<br/>Action Center · HUMAN}}
        HUM -->|approve| FILE[Filer robot<br/>submit SAR]
        HUM -->|reject → dismiss| DISMISS([Closed – Dismissed])
        HUM -->|reject → rework| INV
    end
    DISP --> HUM
    FILE --> FILED([Closed – SAR Filed])
    ESC --> HUM

    classDef human fill:#ffe8cc,stroke:#d9480f;
    classDef agent fill:#d0ebff,stroke:#1971c2;
    classDef robot fill:#d3f9d8,stroke:#2f9e44;
    class HUM human;
    class T,INV,NAR,QA agent;
    class DF,FILE robot;
```

## Where humans stay in charge
- **Disposition (mandatory):** no SAR is filed and no alert dismissed without an
  MLRO decision in Action Center. The Narrator graph literally **suspends** at
  `interrupt()` until the human submits.
- **Escalation:** sanctions exposure and SLA breaches route to a supervisor.
- **Loop guard:** after 2 QA rework cycles a human analyst takes over.

## Exception & failure handling
| Situation | Handling |
|---|---|
| Duplicate alert | Triage links + auto-closes |
| Sanctions/PEP hit | Fast-track escalation, priority raised |
| Thin evidence (QA FAIL) | Loop back to Investigation with targeted `gaps` |
| Repeated QA failure | Loop guard → human analyst |
| SLA breach | Maestro auto-escalates to supervisor + Notifier |
| Source system / API error | Robot retry policy in Orchestrator; case parks in "Blocked" with a follow-up task |
| LLM unavailable | Agents fall back to deterministic logic (never hard-fail the case) |

## How decisions stay auditable
Every evidence item carries a `source`. The risk score is a **transparent
weighted sum** over evidence severity (see `synthesize.py`) — the LLM writes the
rationale, never the score, so a reviewer can reconstruct the decision. Maestro
records every stage transition, agent run (Orchestrator job logs), and the human
decision (Action Center) against the case.

## Technology boundaries (governance)
Agents never touch source systems directly — robots/API Workflows do, and hand
clean data to agents. This keeps credentials in the UiPath vault, keeps actions
logged, and means swapping a connector never touches agent logic.

## External frameworks under UiPath governance
The Investigator and Narrator are **LangGraph** graphs (LangChain ecosystem),
packaged with the **UiPath Python SDK** and run as Orchestrator processes. The
design also supports a **CrewAI** variant of the Investigator (role-based crew:
Entity Analyst, Transaction Analyst, OSINT Analyst, Lead Investigator) — same
inputs/outputs, swappable behind the Maestro stage. UiPath remains the
orchestration and governance layer regardless of framework.
