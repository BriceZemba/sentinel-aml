# Build plan from today to submission

**Key dates (EDT):** Submission closes **June 29, 2026, 11:45pm**. Feedback window
to **July 2**. Public voting **July 3–30**. Finalists present ~**July 23**.
Today is well inside the window — this plan assumes ~4 weeks and is front-loaded so
you have a working demo early and polish later.

Legend: 🧑‍💻 you (code) · ☁️ UiPath platform · 🎬 deliverables

## Week 1 — Foundations & a runnable core (done / in progress)
- [x] 🧑‍💻 Repo scaffolded; Investigator + Narrator coded agents passing tests offline.
- [ ] ☁️ Confirm UiPath Labs access works; log into Automation Cloud; note tenant URL.
- [ ] ☁️ Install CLI: `npm i -g @uipath/cli`; `uip skills install --agent claude`.
- [ ] 🧑‍💻 `uipath auth` in both agent folders; confirm `.env` populated.
- [ ] 🎬 Register/confirm Devpost; create a **draft** project; pick Track 1.

## Week 2 — Deploy agents & stand up the case
- [ ] ☁️ Deploy **Investigator** to Orchestrator (`init → pack → publish`), run the high-risk test input, confirm output.
- [ ] ☁️ Deploy **Narrator**; verify the interrupt creates an **Action Center** task and resumes on submit.
- [ ] ☁️ Build **Triage** + **QA** agents in Agent Builder; test against `data/alerts.json`.
- [ ] ☁️ Build robots/API Workflows: **DataFetcher**, **Filer**, **Notifier**; (optional) **DocIntake** with Document Understanding.
- [ ] ☁️ Create the **Maestro Case** with 5 stages; wire Triage routing first.

## Week 3 — Orchestrate end-to-end + exceptions
- [ ] ☁️ Wire all five stages; map case data in/out of each task.
- [ ] ☁️ Implement the exception paths: dedup auto-close, sanctions escalation, **QA→Investigation loop** with loop guard, SLA escalation.
- [ ] ☁️ Run all four sample alerts through as full cases; confirm distinct outcomes (Duplicate / Filed / Dismissed / Escalated).
- [ ] 🧑‍💻 Capture **Claude Code + `uip`** build/deploy evidence (screenshots + session log) into `CODING_AGENTS.md` / `docs/images/`.
- [ ] 🎬 First full screen-recording rehearsal (find the rough edges early).

## Week 4 — Polish, record, submit
- [ ] 🎬 Record the **≤5-min demo** per `docs/demo-script.md`; upload to YouTube/Vimeo (public).
- [ ] 🎬 Finish the **deck** (`docs/deck-outline.md`) on UiPath's template; set link sharing to public.
- [ ] 🎬 Finalize **README**; add real screenshots to `docs/images/`; confirm MIT license shows in repo About.
- [ ] 🎬 Make the GitHub repo **public**.
- [ ] 🎬 Fill the **Best Product Feedback** survey (use `docs/feedback-notes.md`).
- [ ] 🎬 Complete the Devpost submission (see `docs/devpost-submission.md`) **before** the deadline submit a day early.
- [ ] 🎬 During voting (Jul 3–30): share your public Devpost link to gather **People's Choice** votes.

## Risk buffers
- If Maestro Case setup runs long, demo the agents + Action Center HITL + Orchestrator
  audit logs first; the case wiring can be shown even if one exception path is rough.
- Keep the offline `run_local.py` paths working as a fallback for the video.
- Don't let perfect block submission a complete, working, well-documented core beats
  an ambitious half-wired one.
