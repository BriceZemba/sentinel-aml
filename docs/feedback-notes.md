# Best Product Feedback notes to submit ($1,500, individual)

Fill the AgentHack feedback survey during the **Feedback Period (to July 2,
2026)**. This prize goes to individuals and is **separate** from project judging
pure upside. Quality matters: it's scored on completeness, viability, and impact.
Capture real friction as you build (don't write it after). Below are prompts +
starter observations to expand with your own experience.

## What makes feedback win
Be specific, reproducible, and constructive. Each item: **what you did → what you
expected → what happened → suggested fix**. Bug reports, UX gaps, missing docs,
and integration suggestions all count.

## Maestro Case
- Stage-data mapping: was passing `evidence[]`/`red_flags[]` between a coded agent
  and the next stage smooth? Note any type-coercion or schema-binding friction.
- The split between "Narrator owns the Action Center task" vs. "approval as its own
  stage" was the recommended pattern discoverable in docs?
- Loop-back routing (QA → Investigation) with a loop guard: how easy to express?
- Audit view: did it capture agent + robot + human steps clearly enough for a
  compliance use case? What was missing?

## Coded Agents / Python SDK / `uipath-langchain`
- `uipath init` → `pack` → `publish` flow: any step that needed undocumented args?
- Mapping a LangGraph `interrupt()` to an Action Center task: was the contract
  (input form fields, resume payload shape) clearly documented? This is the most
  likely high-impact feedback area.
- Checkpointer behavior on UiPath vs. local `MemorySaver`: any surprises?
- Pydantic input/output models → UiPath trigger form rendering: fidelity?

## Agent Builder
- Tool attachment (Data Service / Maestro query) ergonomics.
- Context Grounding setup over a policy PDF: indexing time, citation quality.
- Output-schema enforcement strictness.

## UiPath for Coding Agents (`uip` + Claude Code)
- `uip skills install --agent claude`: did the skills cover the commands you
  needed, or were there gaps where Claude Code guessed?
- Any command where the skill's instructions were stale vs. actual CLI behavior.

## Document Understanding
- KYC extraction accuracy on the doc types you tried; taxonomy setup effort.

> Tip: keep a running list in this file as you build, then paste the polished
> version into the survey. One submission per entrant.
