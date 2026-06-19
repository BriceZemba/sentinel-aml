# Build the case in UiPath Maestro (Studio Web)

This wires the actors you've deployed into a single governed case. UI labels can
shift between platform versions follow the *intent* of each step and consult the
[Maestro docs](https://docs.uipath.com/maestro) for exact menus. Do the
[coded-agent deploy](deploy-coded-agents.md) and [Agent Builder](agent-builder-setup.md)
steps first so the agents exist to reference.

## 0. Model the case data
Create the case object (Data Service entity or Maestro case data schema) with at
least these fields they are the shared memory every stage reads/writes:

```
case_id, alert_id, customer_id, account_id, rule, typology, priority,
is_duplicate, linked_case_id,
risk_score, recommendation, rationale, red_flags[], evidence[],
sar_narrative, qa_result, gaps[], rework_count,
disposition, decided_by, decision_notes, filing_reference,
stage, sla_due_at, status
```

## 1. Create the case definition
1. In Studio Web open **Maestro → Case** and create **"AML Investigation Case"**.
2. Add the five **stages**: `Triage`, `Investigation`, `Narrative Drafting`,
   `Quality Review`, `Disposition`.
3. Add terminal outcomes: `Closed – Duplicate`, `Closed – No Action`,
   `Closed – Dismissed`, `Closed – SAR Filed`.

## 2. Trigger
Start a case when a transaction-monitoring alert arrives. For the hackathon, the
simplest reliable trigger is an **API Workflow / queue** seeded from
`data/alerts.json` (or a Maestro API call). Each alert → one new case.

## 3. Wire each stage

### Stage 1 Triage
- **Task:** invoke the **Triage Agent** (Agent Builder). Map alert fields in;
  map `is_duplicate`, `linked_case_id`, `typology`, `priority` out.
- **Routing rules:**
  - `is_duplicate == true` → **Closed – Duplicate** (record `linked_case_id`).
  - `typology == ROUTINE && priority == low` → **Closed – No Action**.
  - else → **Investigation**.
- **SLA:** set Investigation SLA from `priority` (high 4h / medium 1d / low 3d).

### Stage 2 Investigation
- **Task A (robot):** `DataFetcher` API Workflow → fills `customer`, `transactions`.
- **Task B (coded agent):** `Investigator` process. Input: `alert_id, customer_id,
  account_id, rule, priority`. Output → `risk_score, recommendation, rationale,
  red_flags, evidence, sla_breach_risk`.
- **Routing:**
  - any evidence item `category == sanctions` → **Escalate** (raise priority,
    assign senior MLRO) then → Disposition.
  - `recommendation == REQUEST_INFO` → create an analyst RFI task, then re-enter
    Investigation when info returns.
  - else → **Narrative Drafting**.

### Stage 3 Narrative Drafting
- **Task (coded agent):** `Narrator` process. Input: the investigation output +
  `customer_name`. **Note:** the Narrator suspends at its human-review interrupt
  in the *full* design you can either (a) let the Narrator own the Action Center
  task, or (b) split drafting (Stage 3) from approval (Stage 5). This repo ships
  option (a) for a tight demo; for cleaner stage separation, configure the
  Narrator to return the draft and place the Action Center approval in Stage 5.
- Output → `sar_narrative`.

### Stage 4 Quality Review
- **Task (agent):** `QA Agent` (Agent Builder). Input: `sar_narrative, evidence,
  red_flags, recommendation`. Output → `qa_result, gaps`.
- **Routing:**
  - `qa_result == FAIL && rework_count < 2` → back to **Investigation**, pass
    `gaps` as `follow_up_requests`, increment `rework_count`.
  - `qa_result == FAIL && rework_count >= 2` → assign **human analyst** task.
  - `qa_result == PASS` → **Disposition**.

### Stage 5 Disposition (human-in-the-loop)
- **Task (human):** **Action Center** action assigned to the MLRO. Show
  `sar_narrative`, `risk_score`, `red_flags`, `evidence`. Buttons: **Approve /
  Edit & Approve / Reject**.
- **Routing:**
  - Approve → `Filer` robot submits SAR → `Closed – SAR Filed` (store `filing_reference`).
  - Reject → dismiss (`Closed – Dismissed`, capture `decision_notes`) or send to
    rework (→ Investigation).

## 4. Escalation & SLA rules (Maestro)
- On `sla_due_at` breach for any stage → notify supervisor (`Notifier`) and raise priority.
- On sanctions hit → immediate escalation path to senior MLRO.

## 5. Verify the audit trail
Open a completed case and confirm Maestro shows: every stage transition, each
agent/robot job (with Orchestrator logs), and the MLRO's Action Center decision
with timestamp and identity. **This audit view is what you screen-record for the
demo** it's the strongest Track-1 evidence.
