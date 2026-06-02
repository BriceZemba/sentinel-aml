# RPA robots & API Workflows

These are the **deterministic, system-of-record actions** in the case — the work
that should be done by a robot, not an LLM. Built in **UiPath Studio Web** as
API Workflows (and where UI automation is needed, RPA). They are invoked by
Maestro stages as tasks.

> In this repo the connected systems (core banking, FinCEN portal) are mocked by
> the JSON fixtures in `/data` so the solution is runnable end-to-end. The
> workflow contracts below are what you wire to real connectors in production.

## 1. `DataFetcher` (API Workflow) — Investigation stage
Pulls the raw material the Investigator agent reasons over, so the agent never
touches source systems directly (governance + auditability).

| In | Out |
|---|---|
| `customer_id`, `account_id` | `customer` record, `transactions[]`, `kyc_documents[]` |

- Connectors in production: core-banking API, KYC/CDD system, sanctions provider (e.g. Dow Jones / WorldCheck).
- Emits a UiPath Orchestrator job log entry → part of the case audit trail.

## 2. `DocIntake` (Document Understanding) — Triage/Investigation
Runs **UiPath Document Understanding (IDP)** over KYC documents (passport,
incorporation certificate, proof of address) to extract structured fields when a
case requires fresh CDD (e.g. KYC expired). Output is added to case evidence with
the `kyc` category.

## 3. `Filer` (API Workflow + RPA) — Disposition stage, after human approval
The binding action. Only ever runs **after the MLRO approves** in Action Center.

| In | Out |
|---|---|
| `sar_narrative`, `customer_id`, `decided_by`, `case_id` | `filing_reference`, `filed_at` |

- Production: submits the SAR to the FinCEN BSA E-Filing portal (RPA UI automation
  or API), then writes the `filing_reference` back to the case and the case
  management system.
- On `disposition == DISMISSED`: writes the dismissal rationale to the case and
  closes it (no filing).

## 4. `Notifier` (API Workflow) — cross-cutting
Posts case status changes / SLA-breach escalations to the compliance team
(email / Teams / Slack connector). Triggered by Maestro escalation rules.

## Why robots and not agents for these
| Action | Actor | Reason |
|---|---|---|
| Read transactions, run IDP, file SAR | **Robot** | Deterministic, must be exact, system-of-record |
| Score risk, draft narrative, judge sufficiency | **Agent** | Requires reasoning over ambiguous evidence |
| Approve filing / dismissal | **Human (MLRO)** | Legal accountability |

This mapping is the heart of the Track-1 story: the **right actor doing the right
task**, orchestrated by Maestro.
