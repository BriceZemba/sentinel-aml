# Devpost submission step by step

You already have Devpost access and lab access. This is the exact sequence to
submit Sentinel, plus how to line up the extra prizes.

## Before you open the submission form, have these ready
- ✅ **Public GitHub repo** URL (MIT license visible in the *About* box).
- ✅ **Demo video** URL (YouTube/Vimeo, publicly viewable, ≤5:00).
- ✅ **Deck** link (Google Drive/OneDrive/Dropbox, "anyone with link can view").
- ✅ Project **title**, **track** (UiPath Maestro Case), written **description**.
- ✅ 3–6 **screenshots** (case audit view, Action Center task, Investigator output, architecture diagram).

## Step 1: Make the GitHub repo public & compliant
1. Push this repo to GitHub (see commands at the bottom).
2. Repo must be **public**. Settings → General → Danger Zone if it's private.
3. Confirm `LICENSE` (MIT) is detected GitHub shows "MIT License" in the right
   sidebar / About. Add a short description + topics (`uipath`, `agentic-ai`, `aml`).
4. README must contain (it does): project description, UiPath components, agent
   type (coded + low-code), setup instructions, coding-agent usage.

## Step 2: Upload the demo video
1. Upload to YouTube (Visibility: **Unlisted** is allowed as "publicly visible"
   per most readings, but **Public** is safest) or Vimeo.
2. Title it "Sentinel — UiPath AgentHack Track 1 Demo". Paste the GitHub link in
   the description. No copyrighted music.
3. Copy the watch URL.

## Step 3: Host the deck
1. Export the deck to PDF and upload to Drive/OneDrive/Dropbox.
2. Set sharing to **Anyone with the link can view**. Test in an incognito window.

## Step 4: Fill the Devpost project page
On the hackathon site → **Enter a Submission** (or edit your draft):
1. **Project name:** Sentinel Agentic AML Investigation Case Manager.
2. **Elevator pitch:** one line "An agentic financial-crime investigation desk on
   UiPath Maestro Case: agents investigate, robots act, a compliance officer signs
   off — fully audited."
3. **Track:** select **UiPath Maestro Case**.
4. **Description** (paste/adapt from README): business problem → what it does →
   how it works (5 stages, actors) → UiPath components → coding-agent usage →
   impact. Use headings.
5. **Built with:** add tags `uipath`, `uipath-maestro`, `agent-builder`,
   `langgraph`, `langchain`, `python`, `claude`, `action-center`.
6. **Image/screenshots:** upload the case audit view first (it's the thumbnail).
7. **Links:** GitHub repo, demo video, deck.
8. **"Try it out" links:** GitHub + deck.

## Step 5: Coding-agent bonus
In the description **and** README, explicitly state: (a) tool = **Claude Code**;
(b) how it contributed (built the coded agents, tests, deploy scripts); (c)
evidence — link `CODING_AGENTS.md` and show the clip in the video. This is the
cheapest points in the whole rubric.

## Step 6: Submit
- Click **Submit** (not just save draft). You can keep editing until the deadline,
  but a submitted entry is what counts. **Submit at least a day early.**

## Step 7: Extra prizes (separate actions)
- **Best Product Feedback ($1,500, to you individually):** complete the feedback
  survey during the Feedback Period (to **July 2**). Use `docs/feedback-notes.md`.
  This is separate from the project and doesn't count against the 2-prize cap.
- **People's Choice ($500):** during voting (**Jul 3–30**) share your public
  Devpost project link with your network. One vote per person; no vote manipulation.
- **Special awards** (Most Creative / Best Demo / Best Cross-Platform): no separate
  entry — judges pick from all submissions. We've engineered the build + video to
  target Best Cross-Platform Integration and Best Demo.

## Prize-stacking reality check
A single project can win **max 2**: one Track/Grand prize **+** one Special Award.
Best Product Feedback and People's Choice sit outside that cap. Target:
**Best of Maestro Case ($5k) + a Special Award ($1.5–3k) + Feedback ($1.5k) +
People's Choice ($0.5k)**.

## Finalists
If selected, you'll be asked to post the solution as a **UiPath Community Forum**
use case before the finale (~Jul 23). Keep the README polished — it's most of that
post.

---

### Git push commands
```bash
cd "sentinel-aml"
git init
git add .
git commit -m "Sentinel — agentic AML investigation case manager (UiPath AgentHack Track 1)"
git branch -M main
git remote add origin https://github.com/<you>/sentinel-aml.git
git push -u origin main
```
> Make sure `.env` files are **not** committed (`.gitignore` already excludes them).
