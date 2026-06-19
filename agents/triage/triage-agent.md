# Triage Agent (low-code UiPath Agent Builder)

The first agent in the case. Built in **Agent Builder** (Studio Web) so the
submission demonstrates *both* low-code and coded agents. It runs at the Triage
stage of the Maestro case and decides how each alert enters the pipeline.

## Responsibilities
1. **Deduplicate** against open cases for the same customer + rule + overlapping window.
2. **Classify** the alert typology (structuring, layering, sanctions-nexus, routine).
3. **Score initial priority** (low / medium / high) from the rule, customer risk rating, and amount.
4. **Route**: open a new Investigation, attach to an existing case, or auto-close as duplicate/low-value.

## Inputs (case data)
| Field | Type | Source |
|---|---|---|
| `alert_id` | string | alert |
| `customer_id` | string | alert |
| `account_id` | string | alert |
| `rule` | string | alert |
| `open_cases_for_customer` | array | Maestro case query / Data Service |

## Outputs (written back to case data)
| Field | Type | Used by |
|---|---|---|
| `is_duplicate` | bool | Maestro routing rule |
| `linked_case_id` | string\|null | Maestro |
| `typology` | enum | Investigator |
| `priority` | enum(low/medium/high) | SLA selection |
| `triage_notes` | string | audit trail |

## System prompt (paste into Agent Builder)
```
You are an AML alert triage officer at a regulated bank. For each transaction-
monitoring alert you receive, you must:

1. Determine if it is a DUPLICATE of an already-open case. An alert is a duplicate
   if open_cases_for_customer contains a case with the same rule and an overlapping
   time window. If so, set is_duplicate=true and linked_case_id to that case.
2. Classify the typology as one of: STRUCTURING, LAYERING, SANCTIONS_NEXUS,
   RAPID_MOVEMENT, or ROUTINE.
3. Assign priority: HIGH if the rule indicates sanctions/rapid movement or the
   customer risk_rating is high; LOW only for routine, low-value, low-risk cases;
   otherwise MEDIUM.
4. Write a one-paragraph triage_notes explaining your routing decision.

Be conservative: when unsure between two priorities, choose the higher one.
Never auto-close anything except clear duplicates or clearly routine low-value
activity. Output strictly in the provided schema.
```

## Tools to attach in Agent Builder
- **Maestro / Data Service lookup**: "Get open cases for customer" (returns `open_cases_for_customer`).
- (Optional) **Context Grounding** index over the bank's AML policy so triage cites policy thresholds.

## Maestro wiring
- Output `is_duplicate == true` → Maestro transitions the case directly to **Closed – Duplicate** (with `linked_case_id` recorded).
- `priority` selects the **SLA** on the Investigation stage (high = 4h, medium = 1 business day, low = 3 business days).
