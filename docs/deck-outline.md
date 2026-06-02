# Presentation deck outline (use UiPath's template)

A completed deck is a required submission item *and* feeds the finalist
Presentation score. Use the **official AgentHack template** linked from the
[resources page](https://uipath-agenthack.devpost.com/resources); map your content
onto these slides. Keep it to ~10–12 slides.

1. **Title** — Sentinel: Agentic AML Investigation Case Manager · Track 1 · team + roles.
2. **Problem** — 95% false positives, manual investigations, mandatory human sign-off, cost/risk. One stat-heavy slide.
3. **Why a Case (not BPMN)** — "goal fixed, path not"; dynamic, exception-heavy. Quote the Maestro Case framing.
4. **Solution overview** — the 5 stages, one line each.
5. **Architecture** — the actor map + case-flow diagram (from `docs/architecture.md`). The money slide.
6. **The agents** — Triage (low-code), Investigator (coded/LangGraph), Narrator (coded + HITL), QA (low-code); what each does and why that actor.
7. **Human-in-the-loop & governance** — Action Center sign-off, escalation, audit trail; "humans accountable for high-impact decisions."
8. **Dynamic/exception handling** — dedup, QA loop-back, sanctions fast-track, SLA escalation, loop guard.
9. **UiPath platform usage** — Maestro Case, Agent Builder, Coded Agents (Python SDK), Action Center, API Workflows/RPA, Document Understanding, Orchestrator; + LangGraph under UiPath governance.
10. **Coding agents (bonus)** — built/deployed with Claude Code via `uip`; show one screenshot.
11. **Impact & adoption** — time per alert ↓, consistency ↑, auditability; realistic path to production; who buys it.
12. **Demo + links** — GitHub, video, "what's next" (CrewAI variant, more typologies).

## Scoring hooks to hit explicitly (say these words)
- *Business Impact*: quantify (alerts/analyst/day, $ of investigator time saved, fewer late filings).
- *Platform Usage*: name every UiPath component; stress coded + low-code + external framework under one governance layer.
- *Technical Execution*: show the passing tests, the transparent scoring, the exception paths.
- *Creativity*: the QA→Investigation emergent loop and the agent/robot/human task-fit mapping.
- *Presentation*: clean problem→solution→impact arc; rehearse the live Q&A.

Share the deck as a link with **"anyone with the link can view"** access.
