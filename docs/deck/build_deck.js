/* Sentinel — UiPath AgentHack Track 1 deck.
   Matches the official UiPath AgentHack submission template:
   teal title + thank-you, white content slides, orange foot bar, page numbers,
   UiPath wordmark top-right, pixel-square motif. No icons (clean corporate style). */
const pptxgen = require("pptxgenjs");

// ---- brand palette (sampled from the official template) ----
const TEAL = "0BA2B3";
const TEAL_LIGHT = "4FBECB";
const TEAL_DK = "0A7B88";
const ORANGE = "FB4516";
const INK = "16181D";
const SLATE = "566372";
const GRAY = "F4F5F6";
const LINE = "D9DEE3";
const WHITE = "FFFFFF";
const NAVY = "0A5A66";

const HEAVY = "Arial Black";   // big display (title, THANK YOU)
const HEAD = "Arial";          // section titles (bold)
const BODY = "Arial";

const W = 13.333, H = 7.5;
const MX = 0.7;                 // left margin

const shadow = () => ({ type: "outer", color: "9AA5B1", blur: 6, offset: 2, angle: 90, opacity: 0.18 });

let pres;

// ---------- shared chrome ----------
function wordmark(slide, dark) {
  slide.addText(
    [{ text: "Ui", options: { bold: true } }, { text: "Path", options: { bold: true } }],
    { x: W - 2.1, y: 0.3, w: 1.8, h: 0.5, align: "right", fontFace: HEAD, fontSize: 22, color: dark ? INK : WHITE, margin: 0 }
  );
}
function footBar(slide, n) {
  slide.addShape("rect", { x: 0, y: H - 0.1, w: W, h: 0.1, fill: { color: ORANGE }, line: { type: "none" } });
  if (n) slide.addText(String(n), { x: W - 0.7, y: H - 0.5, w: 0.4, h: 0.3, align: "right", fontFace: BODY, fontSize: 10, color: SLATE, margin: 0 });
}
function sectionTitle(slide, text) {
  slide.addText(text, { x: MX, y: 0.42, w: W - 2.6, h: 0.7, fontFace: HEAD, fontSize: 28, bold: true, color: INK, margin: 0 });
}
function frame(slide, color) {
  slide.addShape("rect", { x: 0.16, y: 0.16, w: W - 0.32, h: H - 0.32, fill: { type: "none" }, line: { color, width: 1 } });
}

// ============================================================
function titleSlide() {
  const s = pres.addSlide();
  s.background = { color: TEAL };
  frame(s, "3AB3C1");
  wordmark(s, false);
  s.addText([
    { text: "Sentinel — Agentic AML", options: { breakLine: true } },
    { text: "Investigation Case Manager", options: {} },
  ], { x: MX, y: 3.05, w: 11.5, h: 1.7, fontFace: HEAVY, fontSize: 44, color: WHITE, lineSpacingMultiple: 0.98, margin: 0 });
  s.addText("UiPath AgentHack — Track 1: Maestro Case.  Build the AI agents of tomorrow.",
    { x: MX, y: 4.78, w: 11, h: 0.4, fontFace: BODY, fontSize: 15, color: INK, margin: 0 });

  // pixel-square motif, bottom-right
  const sq = 0.34;
  const cells = [
    [11.95, 5.40, NAVY], [11.95, 5.78, TEAL_DK], [12.33, 5.78, NAVY],
    [11.57, 6.16, TEAL_DK], [11.95, 6.16, NAVY], [12.33, 6.16, "1C8C9B"],
  ];
  for (const [x, y, c] of cells) s.addShape("rect", { x, y, w: sq, h: sq, fill: { color: c }, line: { type: "none" } });
}

// ============================================================
function teamSlide() {
  const s = pres.addSlide();
  s.background = { color: WHITE };
  wordmark(s, true);
  s.addText([
    { text: "Team", options: { breakLine: true, bold: true } },
    { text: "Sentinel", options: { bold: true } },
  ], { x: MX, y: 0.42, w: 9, h: 1.0, fontFace: HEAD, fontSize: 24, color: INK, lineSpacingMultiple: 1.0, margin: 0 });

  // --- left: the single builder ---
  const px = 1.45, pd = 2.2, py = 2.45;
  s.addShape("ellipse", { x: px, y: py, w: pd, h: pd, fill: { color: GRAY }, line: { color: LINE, width: 1 } });
  s.addText("Photo", { x: px, y: py + pd / 2 - 0.15, w: pd, h: 0.3, align: "center", fontFace: BODY, fontSize: 11, color: SLATE, margin: 0 });
  s.addText("[Your Name]", { x: px - 0.5, y: py + pd + 0.2, w: pd + 1.0, h: 0.4, align: "center", fontFace: HEAD, fontSize: 18, bold: true, color: INK, margin: 0 });
  s.addText([
    { text: "Solo Builder & Team Representative", options: { breakLine: true } },
    { text: "[Independent / Company / School]", options: { breakLine: true } },
    { text: "[name@email.com]", options: {} },
  ], { x: px - 0.5, y: py + pd + 0.62, w: pd + 1.0, h: 1.0, align: "center", fontFace: BODY, fontSize: 12, color: SLATE, paraSpaceAfter: 3, margin: 0 });

  // --- right: about-this-submission panel ---
  const bx = 6.5, bw = W - MX - bx;
  s.addShape("rect", { x: bx, y: 2.0, w: bw, h: 4.2, fill: { color: GRAY }, line: { type: "none" } });
  s.addShape("rect", { x: bx, y: 2.0, w: 0.1, h: 4.2, fill: { color: TEAL }, line: { type: "none" } });
  s.addText("About this submission", { x: bx + 0.35, y: 2.3, w: bw - 0.6, h: 0.4, fontFace: HEAD, fontSize: 16, bold: true, color: INK, margin: 0 });
  s.addText([
    { text: "Solo build — designed, coded, and orchestrated end to end by one person.", options: { bullet: true, breakLine: true } },
    { text: "First-time UiPath builder.", options: { bullet: true, breakLine: true } },
    { text: "Track 1 — UiPath Maestro Case.", options: { bullet: true, breakLine: true } },
    { text: "Hybrid agents (low-code + coded) + RPA, governed by Maestro.", options: { bullet: true, breakLine: true } },
    { text: "Built with Claude Code via UiPath for Coding Agents.", options: { bullet: true } },
  ], { x: bx + 0.35, y: 2.9, w: bw - 0.7, h: 3.1, fontFace: BODY, fontSize: 13.5, color: INK, paraSpaceAfter: 12, margin: 0 });
  footBar(s, 2);
}

// ============================================================
function problemSolutionSlide() {
  const s = pres.addSlide();
  s.background = { color: WHITE };
  wordmark(s, true);
  sectionTitle(s, "Problem statement and proposed solution");
  // subtle asymmetric gray panels (template motif)
  s.addShape("rect", { x: 6.55, y: 1.35, w: 6.78, h: 1.25, fill: { color: GRAY }, line: { type: "none" } });
  s.addShape("rect", { x: 0, y: 4.6, w: 4.1, h: 2.3, fill: { color: GRAY }, line: { type: "none" } });

  s.addText("Problem", { x: MX, y: 1.45, w: 5.6, h: 0.4, fontFace: HEAD, fontSize: 19, bold: true, color: INK, margin: 0 });
  s.addText([
    { text: "~95% of AML transaction-monitoring alerts are false positives.", options: { bullet: true, breakLine: true } },
    { text: "Each one is still investigated by hand — pull data, screen sanctions, write the SAR.", options: { bullet: true, breakLine: true } },
    { text: "A compliance officer must sign off every filing — it's legally mandated.", options: { bullet: true, breakLine: true } },
    { text: "Result: slow, inconsistent, costly, and the risk of late or defective filings.", options: { bullet: true } },
  ], { x: MX, y: 1.95, w: 5.7, h: 3.0, fontFace: BODY, fontSize: 14.5, color: INK, paraSpaceAfter: 10, margin: 0 });

  s.addText("Solution", { x: 6.95, y: 1.45, w: 5.6, h: 0.4, fontFace: HEAD, fontSize: 19, bold: true, color: TEAL, margin: 0 });
  s.addText([
    { text: "Sentinel makes every alert a governed case in UiPath Maestro.", options: { bullet: true, breakLine: true } },
    { text: "Agents investigate, robots act on systems of record, an MLRO signs off.", options: { bullet: true, breakLine: true } },
    { text: "The path is dynamic: duplicates auto-close, sanctions fast-track, weak cases loop back.", options: { bullet: true, breakLine: true } },
    { text: "Every decision is auditable end to end — the differentiator for regulators.", options: { bullet: true } },
  ], { x: 6.95, y: 1.95, w: 5.85, h: 3.0, fontFace: BODY, fontSize: 14.5, color: INK, paraSpaceAfter: 10, margin: 0 });
  footBar(s, 3);
}

// ============================================================
function howItWorksSlide() {
  const s = pres.addSlide();
  s.background = { color: WHITE };
  wordmark(s, true);
  sectionTitle(s, "How it works — one case, five stages");

  const stages = [
    ["1", "Triage", "Low-code agent", "Dedup, classify, prioritize, route"],
    ["2", "Investigation", "Coded agent + robot", "Resolve, analyze, screen, score"],
    ["3", "Narrative", "Coded agent", "Draft the FinCEN 5-Ws SAR"],
    ["4", "Quality Review", "Low-code agent", "Verify evidence; loop back if thin"],
    ["5", "Disposition", "Human MLRO", "Approve → file · reject → dismiss"],
  ];
  const cw = 2.34, gap = 0.16, sx = MX, sy = 1.9, ch = 3.0;
  for (let i = 0; i < 5; i++) {
    const [n, t, who, d] = stages[i];
    const cx = sx + i * (cw + gap);
    const human = i === 4;
    s.addShape("rect", { x: cx, y: sy, w: cw, h: ch, fill: { color: human ? "FEF0EB" : GRAY }, line: { color: human ? ORANGE : LINE, width: human ? 1.5 : 1 } });
    s.addShape("rect", { x: cx, y: sy, w: cw, h: 0.12, fill: { color: human ? ORANGE : TEAL }, line: { type: "none" } });
    s.addText(n, { x: cx + 0.2, y: sy + 0.28, w: 1, h: 0.7, fontFace: HEAVY, fontSize: 30, color: human ? ORANGE : TEAL, margin: 0 });
    s.addText(t, { x: cx + 0.2, y: sy + 1.1, w: cw - 0.4, h: 0.5, fontFace: HEAD, fontSize: 15, bold: true, color: INK, margin: 0 });
    s.addText(who, { x: cx + 0.2, y: sy + 1.58, w: cw - 0.4, h: 0.3, fontFace: BODY, fontSize: 11, bold: true, color: human ? ORANGE : TEAL, margin: 0 });
    s.addText(d, { x: cx + 0.2, y: sy + 1.95, w: cw - 0.35, h: 0.9, fontFace: BODY, fontSize: 12, color: SLATE, margin: 0 });
  }
  s.addShape("rect", { x: MX, y: 5.35, w: W - 2 * MX, h: 0.78, fill: { color: TEAL }, line: { type: "none" } });
  s.addText([
    { text: "Dynamic by design:  ", options: { bold: true } },
    { text: "duplicates auto-close · sanctions fast-track to a senior MLRO · Quality Review loops back to Investigation · SLA breaches escalate.", options: {} },
  ], { x: MX + 0.25, y: 5.35, w: W - 2 * MX - 0.5, h: 0.78, fontFace: BODY, fontSize: 13, color: WHITE, valign: "middle", margin: 0 });
  footBar(s, 4);
}

// ============================================================
function architectureSlide() {
  const s = pres.addSlide();
  s.background = { color: WHITE };
  wordmark(s, true);
  sectionTitle(s, "Solution architecture");

  // Maestro control band
  s.addShape("rect", { x: MX, y: 1.55, w: W - 2 * MX, h: 0.8, fill: { color: TEAL }, line: { type: "none" } });
  s.addText("UiPath Maestro — Case orchestration · SLAs · escalation · full audit trail",
    { x: MX, y: 1.55, w: W - 2 * MX, h: 0.8, align: "center", valign: "middle", fontFace: HEAD, fontSize: 16, bold: true, color: WHITE, margin: 0 });

  const cols = [
    ["AGENTS", TEAL, ["Triage  (low-code, Agent Builder)", "Investigator  (coded · LangGraph)", "Narrator  (coded · LangGraph)", "Quality Review  (low-code)"]],
    ["ROBOTS", NAVY, ["DataFetcher  (API Workflow)", "Filer  (RPA — files the SAR)", "Notifier  (escalations)", "DocIntake  (Document Understanding)"]],
    ["PEOPLE", ORANGE, ["MLRO / Compliance Officer", "Reviews in Action Center", "Owns the filing decision", "Accountable · audited · in control"]],
  ];
  const colw = (W - 2 * MX - 2 * 0.3) / 3;
  for (let i = 0; i < 3; i++) {
    const [t, c, items] = cols[i];
    const cx = MX + i * (colw + 0.3);
    s.addShape("rect", { x: cx, y: 3.05, w: colw, h: 2.9, fill: { color: GRAY }, line: { color: LINE, width: 1 } });
    s.addShape("rect", { x: cx, y: 3.05, w: colw, h: 0.5, fill: { color: c }, line: { type: "none" } });
    s.addText(t, { x: cx, y: 3.05, w: colw, h: 0.5, align: "center", valign: "middle", fontFace: HEAD, fontSize: 14, bold: true, color: WHITE, charSpacing: 2, margin: 0 });
    s.addText(items.map((it, k) => ({ text: it, options: { bullet: true, breakLine: true, bold: k === 0, color: k === 0 ? INK : SLATE } })),
      { x: cx + 0.22, y: 3.7, w: colw - 0.4, h: 2.1, fontFace: BODY, fontSize: 12, paraSpaceAfter: 8, margin: 0 });
  }
  s.addText("Agents never touch source systems — robots do, behind the UiPath credential vault. A CrewAI build of the Investigator drops in behind the same Maestro stage.",
    { x: MX, y: 6.15, w: W - 2 * MX, h: 0.5, align: "center", fontFace: BODY, fontSize: 12, italic: true, color: SLATE, margin: 0 });
  footBar(s, 5);
}

// ============================================================
function benefitsSlide() {
  const s = pres.addSlide();
  s.background = { color: WHITE };
  wordmark(s, true);
  sectionTitle(s, "Benefits and technologies used");

  s.addText("Details", { x: MX, y: 1.3, w: 5, h: 0.35, fontFace: HEAD, fontSize: 16, bold: true, color: INK, margin: 0 });
  const rows = [
    ["End-user", "AML analysts and the MLRO / compliance officer"],
    ["User department", "Financial Crime / BSA-AML Compliance"],
    ["Industries", "Banking, fintech, payments, crypto, gaming"],
    ["UiPath products used", "Maestro Case, Agent Builder, Coded Agents (Python SDK), Action Center, API Workflows + RPA, Document Understanding, Orchestrator"],
    ["Other — APIs / tech", "LangGraph, CrewAI, Claude (Anthropic); built via Claude Code + uip CLI"],
  ];
  const table = rows.map(([k, v]) => [
    { text: k, options: { fill: { color: TEAL }, color: WHITE, bold: true, fontSize: 12, valign: "middle", margin: 4 } },
    { text: v, options: { fill: { color: TEAL_LIGHT }, color: INK, fontSize: 11.5, valign: "middle", margin: 5 } },
  ]);
  s.addTable(table, { x: MX, y: 1.75, w: 6.5, colW: [2.0, 4.5], rowH: [0.55, 0.55, 0.55, 1.05, 0.85], border: { type: "solid", color: WHITE, pt: 2 }, fontFace: BODY });

  s.addText("Benefits, impact and outcomes", { x: 7.65, y: 1.3, w: 5.2, h: 0.4, fontFace: HEAD, fontSize: 16, bold: true, color: INK, margin: 0 });
  s.addText([
    { text: "Multi-hour manual investigations → minutes of agent work + one human decision.", options: { bullet: true, breakLine: true } },
    { text: "Consistent rigor on every alert — no analyst-to-analyst drift.", options: { bullet: true, breakLine: true } },
    { text: "Reconstructable risk score + complete audit trail → fewer late / defective filings.", options: { bullet: true, breakLine: true } },
    { text: "A human is accountable for every SAR filing and dismissal.", options: { bullet: true, breakLine: true } },
    { text: "Production path: swap mocks for core-banking, sanctions, and FinCEN E-Filing.", options: { bullet: true } },
  ], { x: 7.65, y: 1.85, w: 5.2, h: 4.3, fontFace: BODY, fontSize: 13.5, color: INK, paraSpaceAfter: 12, margin: 0 });
  footBar(s, 6);
}

// ============================================================
function platformSlide() {
  const s = pres.addSlide();
  s.background = { color: WHITE };
  wordmark(s, true);
  sectionTitle(s, "Platform depth and coding-agent bonus");

  const cards = [
    ["Hybrid agents, one control plane", "Low-code Agent Builder (Triage, QA) + coded LangGraph agents (Investigator, Narrator) + RPA robots + Document Understanding — all governed by Maestro Case."],
    ["External frameworks, governed", "The Investigator ships in two builds — LangGraph and CrewAI — behind the same UiPath contract, swappable at the Maestro stage. UiPath stays the orchestration layer."],
    ["Built with coding agents (+bonus)", "The coded agents, risk logic, tests, and deploy scripts were built with Claude Code via the UiPath uip CLI. Documented and verifiable in CODING_AGENTS.md."],
    ["Engineered to run, not just demo", "Both coded agents pass automated tests (8 total) and run offline with a deterministic fallback — a case is never left without a result."],
  ];
  const cw = (W - 2 * MX - 0.4) / 2, ch = 1.95, gx = MX, gy = 1.7;
  for (let i = 0; i < 4; i++) {
    const [t, d] = cards[i];
    const cx = gx + (i % 2) * (cw + 0.4);
    const cy = gy + Math.floor(i / 2) * (ch + 0.3);
    s.addShape("rect", { x: cx, y: cy, w: cw, h: ch, fill: { color: GRAY }, line: { color: LINE, width: 1 } });
    s.addShape("rect", { x: cx, y: cy, w: 0.1, h: ch, fill: { color: i === 2 ? ORANGE : TEAL }, line: { type: "none" } });
    s.addText(t, { x: cx + 0.3, y: cy + 0.22, w: cw - 0.5, h: 0.5, fontFace: HEAD, fontSize: 15, bold: true, color: INK, margin: 0 });
    s.addText(d, { x: cx + 0.3, y: cy + 0.74, w: cw - 0.55, h: 1.1, fontFace: BODY, fontSize: 12, color: SLATE, margin: 0 });
  }
  footBar(s, 7);
}

// ============================================================
function thankYouSlide() {
  const s = pres.addSlide();
  s.background = { color: WHITE };
  frame(s, "FBD3C7");
  wordmark(s, true);
  s.addText([
    { text: "THANK", options: { breakLine: true } },
    { text: "YOU.", options: {} },
  ], { x: MX - 0.05, y: 0.8, w: 9, h: 3.6, fontFace: HEAVY, fontSize: 96, color: ORANGE, lineSpacingMultiple: 0.92, margin: 0 });
  s.addText([
    { text: "Sentinel — agents investigate, robots act, a compliance officer signs off.", options: { breakLine: true, bold: true } },
    { text: "GitHub: github.com/<you>/sentinel-aml   ·   Demo video & deck in the submission.", options: {} },
  ], { x: MX, y: 5.0, w: 11.5, h: 0.9, fontFace: BODY, fontSize: 14, color: INK, lineSpacingMultiple: 1.2, margin: 0 });
}

(async () => {
  pres = new pptxgen();
  pres.defineLayout({ name: "W", width: W, height: H });
  pres.layout = "W";
  pres.author = "Sentinel Team";
  pres.title = "Sentinel — Agentic AML Investigation Case Manager";

  titleSlide();
  teamSlide();
  problemSolutionSlide();
  howItWorksSlide();
  architectureSlide();
  benefitsSlide();
  platformSlide();
  thankYouSlide();

  await pres.writeFile({ fileName: "Sentinel-Deck.pptx" });
  console.log("wrote Sentinel-Deck.pptx (8 slides, UiPath template style)");
})();
