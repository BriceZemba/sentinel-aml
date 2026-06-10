# Build the low-code agents (Agent Builder)

Two agents are built low-code in **Agent Builder** (Studio Web) so the submission
shows both low-code and coded agents working together.

## Triage Agent
1. Studio Web → **Agent Builder → New agent** → name **"Sentinel Triage"**.
2. Paste the system prompt from [../agents/triage/triage-agent.md](../agents/triage/triage-agent.md).
3. Define **input** and **output** schemas to match that spec (use the field tables).
4. Attach tools:
   - A **Data Service / Maestro query** tool: "Get open cases for customer".
   - *(Optional)* a **Context Grounding** index over your AML policy PDF so the
     agent cites thresholds.
5. Choose the model (any available LLM in your tenant). Keep temperature low.
6. **Test** with the alerts in `../data/alerts.json`. Confirm:
   - `ALT-2026-0512-003` is flagged `is_duplicate = true` (dup of `...-001`).
   - `ALT-2026-0512-002` gets `priority = high`.
   - `ALT-2026-0512-004` is routed routine/low.
7. **Publish** so Maestro can call it as a task.

## Quality Review Agent
1. New agent → **"Sentinel QA"**.
2. Paste the system prompt from [../agents/qa/qa-agent.md](../agents/qa/qa-agent.md).
3. Input: `sar_narrative, evidence, red_flags, recommendation`. Output:
   `qa_result, gaps, qa_notes`.
4. Test that a narrative claiming sanctions exposure **without** a sanctions
   evidence item returns `qa_result = FAIL` with a specific gap.
5. Publish.

## Tips for scoring well
- Give each agent a **tight, schema-constrained output** judges reward
  deliberate design over a chatty prompt.
- Use **Context Grounding** for at least one agent: grounding the Triage or QA
  agent in the actual AML policy is a concrete "deep platform usage" point.
- Keep the low-code agents focused; push the heavy multi-step reasoning to the
  coded Investigator. The contrast (low-code vs coded) is itself a talking point
  for the Best Cross-Platform Integration special award.
