# Demo video script (≤ 5:00) — shot list

The video is judged directly and is your shot at the **Best Demo / Presentation**
special award ($3,000). Rules: ≤5 min, must show the solution *running* (not
slides), walk the architecture, name the agents and how they're orchestrated, and
show where humans fit. Show coding agents on screen for the bonus.

**Golden rule:** spend ~70% on the product running, ~30% on architecture/voiceover.
Record a clean run first, then narrate.

---

### 0:00–0:30 · Hook + problem
- On camera or voiceover over a single title card.
- "Banks investigate millions of AML alerts a year, and ~95% are false positives.
  Each one is hand-investigated and must be signed off by a compliance officer.
  Meet **Sentinel** — an agentic investigation desk on UiPath Maestro Case."

### 0:30–1:10 · Architecture (one diagram, narrated)
- Show `docs/architecture.md` mermaid diagram.
- "Each alert becomes a *case*. Five stages. A low-code Triage agent, a coded
  LangGraph Investigator, a coded Narrator, a low-code QA agent, robots for the
  system-of-record work, and a human MLRO who owns the filing decision. Maestro
  orchestrates all of it and keeps the audit trail."

### 1:10–1:40 · A case is born + Triage
- In Maestro, show an alert creating a case. Open it.
- Show the Triage agent output: typology, priority, and a **duplicate alert
  auto-closing** (great, fast "dynamic behavior" beat).

### 1:40–2:40 · Investigation (the wow) — the high-risk case
- Trigger the **Halcyon / ALT-2026-0512-002** case.
- Show the Investigator running (Orchestrator job) and the evidence it produced:
  sanctions hit, same-day layering, adverse media — risk score **100 → ESCALATE**.
- Quick cut to the terminal: `python run_local.py ALT-2026-0512-002` so viewers
  see the actual reasoning/evidence JSON. Emphasize **every finding cites a source**
  and **the score is transparent, not a black box**.

### 2:40–3:20 · Narrative + QA loop
- Show the Narrator's drafted SAR narrative.
- Show the **QA agent failing a thin case and looping it back to Investigation**
  with specific gaps — "the path emerges as the work unfolds; this is why it's a
  *case*, not a fixed flow."

### 3:20–4:10 · Human-in-the-loop (the accountability beat)
- Open the **Action Center** task for the MLRO. Show the narrative + evidence.
- Click **Approve** → the Filer robot files the SAR → case closes **SAR Filed**.
- Then show a **Reject** on another case → **Dismissed** with rationale.
- "No SAR is ever filed without a human. The graph literally suspends until the
  officer decides."

### 4:10–4:40 · Coding agents (bonus) + audit trail
- 15–20s of **Claude Code + `uip`** building/deploying an agent
  (`uipath publish` succeeding). "We built and deployed the coded agents with
  Claude Code through UiPath for Coding Agents."
- Show the Maestro **audit view** of a completed case: every stage, agent, robot,
  and the human decision, timestamped.

### 4:40–5:00 · Impact + close
- "Sentinel turns a 2-hour manual investigation into minutes of agent work plus a
  focused human decision — with full auditability. Reasoning to agents, exact
  actions to robots, accountability to people. Orchestrated by UiPath Maestro."

---

## Recording tips
- 1080p, large fonts in terminal/IDE, hide secrets.
- Pre-run everything once; keep takes short and cut.
- Put the YouTube/Vimeo link **unlisted-public** (publicly viewable) in Devpost.
- No copyrighted music — use silence or a royalty-free track.
- Add captions; judges may watch muted.
