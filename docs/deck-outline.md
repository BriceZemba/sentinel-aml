# Presentation deck outline

> ✅ **The deck is already built** at [`deck/Sentinel-Deck.pptx`](deck/Sentinel-Deck.pptx),
> styled to match the **official UiPath AgentHack template** (teal title + thank-you,
> orange foot bars, teal data table, clean corporate look, no icons). Regenerate it
> any time with `node deck/build_deck.js`. It has 8 slides:
> **1** Title · **2** Team (fill placeholders) · **3** Problem & Solution ·
> **4** How it works (5 stages) · **5** Solution architecture · **6** Benefits &
> technologies (table) · **7** Platform depth & coding-agent bonus · **8** Thank you.
>
> Before submitting: fill the **Team** slide and paste your **GitHub link** on the
> closing slide. The outline below documents the content rationale.

A completed deck is a required submission item *and* feeds the finalist
Presentation score. The official AgentHack template is linked from the
[resources page](https://uipath-agenthack.devpost.com/resources).

1. **Title**: Sentinel: Agentic AML Investigation Case Manager · Track 1 · team + roles.
2. **Problem**: 95% false positives, manual investigations, mandatory human sign-off, cost/risk. One stat-heavy slide.
3. **Why a Case (not BPMN)** "goal fixed, path not"; dynamic, exception-heavy. Quote the Maestro Case framing.
4. **Solution overview**: the 5 stages, one line each.
5. **Architecture**: the actor map + case-flow diagram (from `docs/architecture.md`). The money slide.
6. **The agents**: Triage (low-code), Investigator (coded/LangGraph), Narrator (coded + HITL), QA (low-code); what each does and why that actor.
7. **Human-in-the-loop & governance**: Action Center sign-off, escalation, audit trail; "humans accountable for high-impact decisions."
8. **Dynamic/exception handling**: dedup, QA loop-back, sanctions fast-track, SLA escalation, loop guard.
9. **UiPath platform usage**: Maestro Case, Agent Builder, Coded Agents (Python SDK), Action Center, API Workflows/RPA, Document Understanding, Orchestrator; + LangGraph under UiPath governance.
10. **Coding agents (bonus)**: built/deployed with Claude Code via `uip`; show one screenshot.
11. **Impact & adoption**: time per alert ↓, consistency ↑, auditability; realistic path to production; who buys it.
12. **Demo + links**: GitHub, video, "what's next" (CrewAI variant, more typologies).
