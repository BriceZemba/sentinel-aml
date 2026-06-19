# Sentinel Submission Evidence (for judges)

**Project:** Sentinel Agentic AML Investigation Case Manager
**Track:** UiPath Maestro Case · **Entrant:** ZEMBA Wendemi Brice Roméo (Individual, first-time UiPath builder)
**Repo:** https://github.com/<BriceZemba>/sentinel-aml

This pack supports the submission, with a focus on the **coding-agent bonus** (built with
Claude Code through UiPath for Coding Agents).

## Contents
- `CODING_AGENTS.md` how Claude Code built/deployed the solution (the bonus write-up).
- `Sentinel-Deck.pdf` the presentation deck.
- `logs/tests-passing.txt` automated tests for all three coded agents (8 passing), run by Claude Code.
- `logs/uipath-cli.txt` the UiPath CLI (`uipath`) driven by Claude Code: version + `uipath pack` success.
- `screenshots/`
  - `01-architecture.png` solution architecture (agents / robots / human, governed by Maestro).
  - `02-agents-successful.png` Investigator + Narrator jobs Successful on Orchestrator.
  - `03-publish-agent.png`, `04-deploy-agent.png` publishing/deploying the coded agents.
  - `05-investigator-output.png` Investigator result (risk score, cited evidence).
  - `06-narrator-output.png` Narrator result (SAR narrative + disposition).
  - `07-how-it-works.png` the five-stage case flow.

## Coding-agent bonus verification (the three required points)
- **(a) Tool used:** Claude Code (Anthropic's CLI), with UiPath skills installed via
  `uip skills install --agent claude` (22 UiPath skills).
- **(b) How it contributed:** wrote the LangGraph Investigator and Narrator coded agents, the
  CrewAI variant, the risk-scoring logic, the Action Center human-in-the-loop interrupt, the
  automated tests, and the `uipath` pack/publish/deploy flow.
- **(c) Evidence:** `logs/tests-passing.txt` (8 passing tests), `logs/uipath-cli.txt`
  (`uipath pack` succeeding), `CODING_AGENTS.md`, and the screenshots above. All reproducible
  from the public repo.

## UiPath components used
Maestro Case · Agent Builder (Triage, QA) · Coded Agents / Python SDK + uipath-langchain
(Investigator, Narrator) · Action Center (human sign-off) · API Workflows + RPA (Filer) ·
Orchestrator · plus LangGraph and CrewAI under UiPath governance.

## Agent type
Both coded and low-code agents, plus RPA and a human decision, orchestrated by Maestro.
