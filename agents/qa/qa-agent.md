# Quality Review Agent (low-code — UiPath Agent Builder)

Runs at the **Quality Review** stage, *after* the SAR narrative is drafted and
*before* it reaches the MLRO. Its job is to catch weak cases automatically so a
human only ever reviews complete, defensible work — and to create a dynamic
exception loop back to Investigation when the case is thin.

## Responsibilities
1. Check the narrative covers all **5 Ws** (Who/What/When/Where/Why-How).
2. Verify **every claim in the narrative is backed by an evidence item** (no unsupported assertions).
3. Confirm required elements are present for the recommendation (e.g. FILE_SAR needs ≥1 high/critical red flag).
4. Emit a **pass / fail** with specific gaps.

## Inputs
| Field | Type |
|---|---|
| `sar_narrative` | string |
| `evidence` | array |
| `red_flags` | array |
| `recommendation` | enum |

## Outputs
| Field | Type | Effect in Maestro |
|---|---|---|
| `qa_result` | enum(PASS/FAIL) | PASS → advance to Disposition; FAIL → loop back to Investigation |
| `gaps` | array<string> | passed to Investigator as `follow_up_requests` |
| `qa_notes` | string | audit trail |

## System prompt
```
You are an AML quality-control reviewer. You receive a drafted SAR narrative plus
the underlying evidence and red flags. Decide qa_result = PASS or FAIL.

FAIL if any of these are true:
- The narrative omits any of Who, What, When, Where, or Why/How.
- Any factual claim in the narrative is not supported by an evidence item.
- recommendation is FILE_SAR but there is no evidence item with severity high or
  critical.
- The narrative references a name, amount, or date not present in the evidence.

For every reason you FAIL the case, add a precise, actionable string to `gaps`
(e.g. "Narrative claims sanctions exposure but no sanctions evidence item is
present — re-run sanctions screening on all counterparties").

If PASS, gaps must be empty. Output strictly in schema. Be strict: it is cheaper
to loop back than to file a defective SAR.
```

## Maestro wiring (the dynamic exception loop)
- `qa_result == FAIL` → Maestro transitions the case **back to Investigation**, passing `gaps` as `follow_up_requests`. The Investigator re-runs only the requested checks. This is the "path emerges as work unfolds" behavior that makes this a *case*, not a fixed flow.
- A **loop guard** (max 2 rework cycles) escalates to a human analyst if QA keeps failing — preventing infinite loops.
