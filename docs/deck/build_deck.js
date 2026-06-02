/* Sentinel — UiPath AgentHack Track 1 deck generator (pptxgenjs). */
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const FA = require("react-icons/fa");

// ---------- palette ----------
const INK = "0E1633";      // deep navy (dark slides)
const NAVY = "1E2761";     // primary navy
const ICE = "CADCFC";      // ice blue
const WHITE = "FFFFFF";
const AMBER = "F2A33C";    // accent / human / alerts
const TEAL = "1FB6A6";     // agents
const GREEN = "33B27B";    // robots
const SLATE = "5B6B8C";    // muted text
const CARD = "F4F6FB";     // light card bg
const CARDLINE = "E2E7F3";
const HEAD = "Trebuchet MS";
const BODY = "Calibri";

const W = 13.333, H = 7.5;

// ---------- icon rasterizer ----------
async function icon(name, color, size = 256) {
  const Comp = FA[name];
  if (!Comp) throw new Error("missing icon " + name);
  const svg = ReactDOMServer.renderToStaticMarkup(
    React.createElement(Comp, { color, size: String(size) })
  );
  const png = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + png.toString("base64");
}
const ICONS = {};
async function preload() {
  const need = {
    shield: "FaShieldAlt", warn: "FaExclamationTriangle", route: "FaRoute",
    map: "FaSitemap", robot: "FaRobot", userCheck: "FaUserCheck",
    search: "FaSearch", pen: "FaPenFancy", check2: "FaCheckDouble",
    gavel: "FaGavel", bolt: "FaBolt", sync: "FaSyncAlt", code: "FaCode",
    chart: "FaChartLine", server: "FaServer", puzzle: "FaPuzzlePiece",
    link: "FaLink", db: "FaDatabase", bank: "FaUniversity", lock: "FaLock",
    clipboard: "FaClipboardCheck", users: "FaUsersCog", file: "FaFileSignature",
    arrow: "FaArrowRight", brain: "FaBrain", balance: "FaBalanceScale",
  };
  for (const [k, v] of Object.entries(need)) {
    ICONS[k] = { [WHITE]: await icon(v, "#" + WHITE) };
  }
}
async function iconColored(slide, key, color, x, y, d) {
  const data = await icon(faName(key), "#" + color);
  slide.addImage({ data, x, y, w: d, h: d });
}
const FAMAP = {
  shield: "FaShieldAlt", warn: "FaExclamationTriangle", route: "FaRoute",
  map: "FaSitemap", robot: "FaRobot", userCheck: "FaUserCheck", search: "FaSearch",
  pen: "FaPenFancy", check2: "FaCheckDouble", gavel: "FaGavel", bolt: "FaBolt",
  sync: "FaSyncAlt", code: "FaCode", chart: "FaChartLine", server: "FaServer",
  puzzle: "FaPuzzlePiece", link: "FaLink", db: "FaDatabase", bank: "FaUniversity",
  lock: "FaLock", clipboard: "FaClipboardCheck", users: "FaUsersCog",
  file: "FaFileSignature", arrow: "FaArrowRight", brain: "FaBrain", balance: "FaBalanceScale",
};
function faName(k) { return FAMAP[k]; }

const shadow = () => ({ type: "outer", color: "1E2761", blur: 7, offset: 3, angle: 90, opacity: 0.13 });

// circle with white icon
async function iconBadge(slide, key, cx, cy, d, circleColor) {
  slide.addShape("ellipse", { x: cx, y: cy, w: d, h: d, fill: { color: circleColor }, line: { type: "none" } });
  const id = d * 0.5;
  const data = await icon(faName(key), "#" + WHITE, 256);
  slide.addImage({ data, x: cx + (d - id) / 2, y: cy + (d - id) / 2, w: id, h: id });
}

// kicker + title block for light slides
function header(slide, kicker, title, accent = TEAL) {
  slide.addText(kicker.toUpperCase(), { x: 0.7, y: 0.42, w: 11, h: 0.3, fontFace: HEAD, fontSize: 12, bold: true, color: accent, charSpacing: 3, margin: 0 });
  slide.addText(title, { x: 0.7, y: 0.72, w: 12, h: 0.7, fontFace: HEAD, fontSize: 30, bold: true, color: NAVY, margin: 0 });
}

function pageFoot(slide, n, dark = false) {
  slide.addText("Sentinel · UiPath AgentHack · Track 1: Maestro Case", { x: 0.7, y: H - 0.42, w: 9, h: 0.3, fontFace: BODY, fontSize: 9, color: dark ? "7E8AB0" : SLATE, margin: 0 });
  slide.addText(String(n), { x: W - 0.9, y: H - 0.42, w: 0.3, h: 0.3, fontFace: BODY, fontSize: 9, color: dark ? "7E8AB0" : SLATE, align: "right", margin: 0 });
}

(async () => {
  await preload();
  const p = new pptxgen();
  p.defineLayout({ name: "W", width: W, height: H });
  p.layout = "W";
  p.author = "Sentinel Team";
  p.title = "Sentinel — Agentic AML Investigation Case Manager";

  // ============ SLIDE 1 — TITLE (dark) ============
  let s = p.addSlide();
  s.background = { color: INK };
  // subtle corner accents
  s.addShape("rect", { x: 0, y: 0, w: W, h: 0.12, fill: { color: TEAL }, line: { type: "none" } });
  await iconBadge(s, "shield", 0.7, 1.5, 1.0, TEAL);
  s.addText("SENTINEL", { x: 0.7, y: 2.7, w: 11, h: 1.0, fontFace: HEAD, fontSize: 60, bold: true, color: WHITE, charSpacing: 2, margin: 0 });
  s.addText("Agentic AML Investigation Case Manager", { x: 0.72, y: 3.75, w: 11.5, h: 0.6, fontFace: HEAD, fontSize: 24, color: ICE, margin: 0 });
  s.addText([
    { text: "Agents investigate.  Robots act.  A compliance officer signs off.", options: { color: "AEBBDD", breakLine: true } },
    { text: "Every alert a governed, fully-audited case on UiPath Maestro.", options: { color: "AEBBDD" } },
  ], { x: 0.72, y: 4.5, w: 11.5, h: 0.8, fontFace: BODY, fontSize: 15, lineSpacingMultiple: 1.15, margin: 0 });
  s.addShape("rect", { x: 0.72, y: 5.75, w: 4.6, h: 0.5, fill: { color: NAVY }, line: { color: TEAL, width: 1 } });
  s.addText("Track 1 · UiPath Maestro Case", { x: 0.72, y: 5.75, w: 4.6, h: 0.5, fontFace: HEAD, fontSize: 13, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
  s.addText("Built with Claude Code + UiPath for Coding Agents", { x: 5.6, y: 5.83, w: 7, h: 0.35, fontFace: BODY, fontSize: 12, italic: true, color: AMBER, valign: "middle", margin: 0 });

  // ============ SLIDE 2 — PROBLEM (light, stats) ============
  s = p.addSlide(); s.background = { color: WHITE };
  header(s, "The problem", "Compliance teams are drowning in false alarms", AMBER);
  const stats = [
    { big: "~95%", lab: "of AML transaction-monitoring alerts are false positives", c: AMBER, ic: "warn" },
    { big: "Hours", lab: "of manual work per alert: pull data, screen, write the SAR", c: TEAL, ic: "search" },
    { big: "Human", lab: "sign-off on every filing is legally mandated", c: GREEN, ic: "gavel" },
  ];
  let x = 0.7;
  for (const st of stats) {
    s.addShape("rect", { x, y: 1.75, w: 3.85, h: 2.55, fill: { color: CARD }, line: { color: CARDLINE, width: 1 }, shadow: shadow() });
    s.addShape("rect", { x, y: 1.75, w: 0.1, h: 2.55, fill: { color: st.c }, line: { type: "none" } });
    await iconBadge(s, st.ic, x + 0.35, 2.05, 0.7, st.c);
    s.addText(st.big, { x: x + 0.3, y: 2.85, w: 3.4, h: 0.8, fontFace: HEAD, fontSize: 40, bold: true, color: NAVY, margin: 0 });
    s.addText(st.lab, { x: x + 0.32, y: 3.65, w: 3.35, h: 0.55, fontFace: BODY, fontSize: 13, color: SLATE, margin: 0 });
    x += 4.05;
  }
  s.addText([
    { text: "The result:  ", options: { bold: true, color: NAVY } },
    { text: "slow, inconsistent investigations, analyst burnout, and the risk of late or defective regulatory filings — at enormous cost.", options: { color: NAVY } },
  ], { x: 0.7, y: 4.7, w: 11.9, h: 0.9, fontFace: BODY, fontSize: 16, align: "center", valign: "middle", margin: 0 });
  pageFoot(s, 2);

  // ============ SLIDE 3 — WHY A CASE (light, two-col) ============
  s = p.addSlide(); s.background = { color: WHITE };
  header(s, "Why agentic case management", "The goal is fixed. The path is not.", TEAL);
  // left: BPMN, right: Case
  const colY = 1.85, colH = 3.5;
  s.addShape("rect", { x: 0.7, y: colY, w: 5.75, h: colH, fill: { color: CARD }, line: { color: CARDLINE, width: 1 } });
  s.addText("A FIXED FLOW (BPMN)", { x: 1.0, y: colY + 0.25, w: 5.2, h: 0.4, fontFace: HEAD, fontSize: 15, bold: true, color: SLATE, margin: 0 });
  s.addText([
    { text: "Predictable, repeatable sequence", options: { bullet: true, breakLine: true } },
    { text: "Same steps every time", options: { bullet: true, breakLine: true } },
    { text: "Great for flow complexity", options: { bullet: true, breakLine: true } },
    { text: "Wrong fit when work branches on evidence", options: { bullet: true } },
  ], { x: 1.0, y: colY + 0.8, w: 5.1, h: 2.4, fontFace: BODY, fontSize: 14.5, color: NAVY, paraSpaceAfter: 8, margin: 0 });

  s.addShape("rect", { x: 6.85, y: colY, w: 5.75, h: colH, fill: { color: NAVY }, line: { type: "none" }, shadow: shadow() });
  s.addShape("rect", { x: 6.85, y: colY, w: 0.1, h: colH, fill: { color: TEAL }, line: { type: "none" } });
  s.addText("AN AGENTIC CASE (SENTINEL)", { x: 7.15, y: colY + 0.25, w: 5.2, h: 0.4, fontFace: HEAD, fontSize: 15, bold: true, color: TEAL, margin: 0 });
  s.addText([
    { text: "Goal fixed: decide + document every alert", options: { bullet: true, breakLine: true } },
    { text: "Path emerges as evidence unfolds", options: { bullet: true, breakLine: true } },
    { text: "Branches, loops back, escalates dynamically", options: { bullet: true, breakLine: true } },
    { text: "Humans stay accountable at decision points", options: { bullet: true } },
  ], { x: 7.15, y: colY + 0.8, w: 5.1, h: 2.4, fontFace: BODY, fontSize: 14.5, color: WHITE, paraSpaceAfter: 8, margin: 0 });
  s.addText("AML investigations are exception-heavy and dynamic — the textbook case for UiPath Maestro Case.", { x: 0.7, y: 5.65, w: 11.9, h: 0.5, fontFace: BODY, fontSize: 14, italic: true, color: SLATE, align: "center", margin: 0 });
  pageFoot(s, 3);

  // ============ SLIDE 4 — SOLUTION: 5 STAGES (light flow) ============
  s = p.addSlide(); s.background = { color: WHITE };
  header(s, "What Sentinel does", "Every alert flows through five governed stages", TEAL);
  const stages = [
    { n: "1", t: "Triage", who: "Low-code agent", d: "Dedup, classify, set priority & SLA, route", ic: "route", c: TEAL },
    { n: "2", t: "Investigation", who: "Coded agent + robot", d: "Resolve entities, analyze txns, screen, score", ic: "search", c: TEAL },
    { n: "3", t: "Narrative", who: "Coded agent", d: "Draft a FinCEN 5-Ws SAR narrative", ic: "pen", c: TEAL },
    { n: "4", t: "Quality Review", who: "Low-code agent", d: "Verify evidence; loop back if thin", ic: "check2", c: TEAL },
    { n: "5", t: "Disposition", who: "Human MLRO", d: "Approve → file SAR · reject → dismiss", ic: "gavel", c: AMBER },
  ];
  const cw = 2.32, gap = 0.18, sx = 0.62, sy = 2.0, ch = 3.3;
  for (let i = 0; i < stages.length; i++) {
    const st = stages[i]; const cx = sx + i * (cw + gap);
    s.addShape("rect", { x: cx, y: sy, w: cw, h: ch, fill: { color: i === 4 ? "FBF1E2" : CARD }, line: { color: i === 4 ? AMBER : CARDLINE, width: i === 4 ? 1.5 : 1 }, shadow: shadow() });
    await iconBadge(s, st.ic, cx + cw / 2 - 0.42, sy + 0.3, 0.84, st.c);
    s.addText(st.n, { x: cx + 0.1, y: sy + 0.12, w: 0.5, h: 0.4, fontFace: HEAD, fontSize: 17, bold: true, color: st.c, margin: 0 });
    s.addText(st.t, { x: cx + 0.1, y: sy + 1.3, w: cw - 0.2, h: 0.4, fontFace: HEAD, fontSize: 15.5, bold: true, color: NAVY, align: "center", margin: 0 });
    s.addText(st.who, { x: cx + 0.1, y: sy + 1.72, w: cw - 0.2, h: 0.3, fontFace: BODY, fontSize: 10.5, bold: true, color: st.c, align: "center", margin: 0 });
    s.addText(st.d, { x: cx + 0.16, y: sy + 2.1, w: cw - 0.3, h: 1.0, fontFace: BODY, fontSize: 11.5, color: SLATE, align: "center", margin: 0 });
  }
  s.addText("Dynamic by design:  duplicates auto-close · sanctions fast-track · QA loops back to Investigation · SLA breaches escalate", { x: 0.62, y: 5.6, w: 12.1, h: 0.5, fontFace: BODY, fontSize: 13, italic: true, color: NAVY, align: "center", margin: 0 });
  pageFoot(s, 4);

  // ============ SLIDE 5 — ARCHITECTURE / ACTOR MAP ============
  s = p.addSlide(); s.background = { color: WHITE };
  header(s, "Architecture", "The right actor for every task — one control plane", TEAL);
  // Maestro banner
  s.addShape("rect", { x: 0.7, y: 1.7, w: 11.93, h: 0.85, fill: { color: NAVY }, line: { type: "none" }, shadow: shadow() });
  await iconBadge(s, "map", 0.95, 1.83, 0.58, TEAL);
  s.addText("UiPath Maestro — Case orchestration, SLAs, escalation & audit trail", { x: 1.7, y: 1.7, w: 10.8, h: 0.85, fontFace: HEAD, fontSize: 16, bold: true, color: WHITE, valign: "middle", margin: 0 });
  // three columns
  const cols = [
    { t: "AGENTS", c: TEAL, ic: "brain", items: ["Triage  (low-code)", "Investigator  (coded · LangGraph)", "Narrator  (coded · LangGraph)", "Quality Review  (low-code)"] },
    { t: "ROBOTS", c: GREEN, ic: "robot", items: ["DataFetcher  (API Workflow)", "Filer  (RPA — files the SAR)", "Notifier  (escalations)", "DocIntake  (Document Understanding)"] },
    { t: "PEOPLE", c: AMBER, ic: "userCheck", items: ["MLRO / Compliance Officer", "Approves or rejects in Action Center", "Owns the filing decision", "Accountable, audited, in control"] },
  ];
  let cx2 = 0.7; const colw = 3.84, cgap = 0.2;
  for (const col of cols) {
    s.addShape("rect", { x: cx2, y: 2.85, w: colw, h: 3.0, fill: { color: CARD }, line: { color: CARDLINE, width: 1 } });
    s.addShape("rect", { x: cx2, y: 2.85, w: colw, h: 0.55, fill: { color: col.c }, line: { type: "none" } });
    await iconBadge(s, col.ic, cx2 + 0.2, 2.9, 0.45, NAVY);
    s.addText(col.t, { x: cx2 + 0.75, y: 2.85, w: colw - 0.8, h: 0.55, fontFace: HEAD, fontSize: 15, bold: true, color: WHITE, valign: "middle", charSpacing: 2, margin: 0 });
    s.addText(col.items.map((it, i) => ({ text: it, options: { bullet: true, breakLine: true, color: i === 0 ? NAVY : SLATE, bold: i === 0 } })),
      { x: cx2 + 0.25, y: 3.6, w: colw - 0.45, h: 2.1, fontFace: BODY, fontSize: 12.5, paraSpaceAfter: 9, margin: 0 });
    cx2 += colw + cgap;
  }
  s.addText("Agents never touch source systems — robots do, behind the UiPath credential vault. Every step is logged.", { x: 0.7, y: 6.1, w: 11.93, h: 0.4, fontFace: BODY, fontSize: 12.5, italic: true, color: SLATE, align: "center", margin: 0 });
  pageFoot(s, 5);

  // ============ SLIDE 6 — HUMAN IN THE LOOP (dark) ============
  s = p.addSlide(); s.background = { color: INK };
  s.addText("HUMAN-IN-THE-LOOP & GOVERNANCE", { x: 0.7, y: 0.5, w: 11, h: 0.3, fontFace: HEAD, fontSize: 12, bold: true, color: AMBER, charSpacing: 3, margin: 0 });
  s.addText("No SAR is ever filed without a human", { x: 0.7, y: 0.82, w: 12, h: 0.7, fontFace: HEAD, fontSize: 30, bold: true, color: WHITE, margin: 0 });
  const hil = [
    { ic: "userCheck", t: "Binding sign-off", d: "The Narrator graph literally suspends at an interrupt that becomes a UiPath Action Center task. It resumes only when the MLRO submits." },
    { ic: "bolt", t: "Smart escalation", d: "Sanctions exposure fast-tracks to a senior MLRO; SLA breaches auto-escalate to a supervisor with a notification." },
    { ic: "sync", t: "Self-correcting loop", d: "Quality Review bounces thin cases back to Investigation with specific gaps — with a loop guard that hands off to a human after two cycles." },
    { ic: "lock", t: "Audit by construction", d: "Every stage, agent run, robot job, and human decision is recorded against the case — a trail a regulator can follow." },
  ];
  let hy = 1.9;
  for (let i = 0; i < hil.length; i++) {
    const it = hil[i]; const col = i % 2; const row = Math.floor(i / 2);
    const bx = 0.7 + col * 6.1; const by = 1.95 + row * 1.95;
    s.addShape("rect", { x: bx, y: by, w: 5.85, h: 1.7, fill: { color: NAVY }, line: { type: "none" } });
    await iconBadge(s, it.ic, bx + 0.3, by + 0.35, 0.95, i === 0 ? AMBER : TEAL);
    s.addText(it.t, { x: bx + 1.5, y: by + 0.25, w: 4.2, h: 0.4, fontFace: HEAD, fontSize: 16, bold: true, color: WHITE, margin: 0 });
    s.addText(it.d, { x: bx + 1.5, y: by + 0.68, w: 4.25, h: 0.95, fontFace: BODY, fontSize: 12, color: "B9C4E2", margin: 0 });
  }
  pageFoot(s, 6, true);

  // ============ SLIDE 7 — PLATFORM USAGE (light grid) ============
  s = p.addSlide(); s.background = { color: WHITE };
  header(s, "Deep UiPath platform usage", "One governed stack — low-code, coded & external frameworks", TEAL);
  const comps = [
    { ic: "map", t: "Maestro Case", d: "Lifecycle, SLAs, escalation, audit" },
    { ic: "users", t: "Agent Builder", d: "Triage + QA low-code agents" },
    { ic: "code", t: "Coded Agents", d: "Python SDK + LangGraph crews" },
    { ic: "userCheck", t: "Action Center", d: "Human-in-the-loop sign-off" },
    { ic: "server", t: "API Workflows + RPA", d: "DataFetcher · Filer · Notifier" },
    { ic: "db", t: "Document Understanding", d: "KYC document extraction" },
    { ic: "puzzle", t: "Orchestrator", d: "Runs & schedules agents/robots" },
    { ic: "link", t: "UiPath for Coding Agents", d: "Built via Claude Code + uip CLI" },
  ];
  const gx = 0.7, gy = 1.8, gw = 2.95, gh = 1.62, ggap = 0.13;
  for (let i = 0; i < comps.length; i++) {
    const it = comps[i]; const col = i % 4; const row = Math.floor(i / 4);
    const bx = gx + col * (gw + ggap); const by = gy + row * (gh + 0.2);
    s.addShape("rect", { x: bx, y: by, w: gw, h: gh, fill: { color: CARD }, line: { color: CARDLINE, width: 1 }, shadow: shadow() });
    await iconBadge(s, it.ic, bx + 0.22, by + 0.26, 0.58, i === 7 ? AMBER : NAVY);
    s.addText(it.t, { x: bx + 0.9, y: by + 0.2, w: gw - 1.02, h: 0.68, fontFace: HEAD, fontSize: 12, bold: true, color: NAVY, valign: "middle", margin: 0 });
    s.addText(it.d, { x: bx + 0.22, y: by + 0.97, w: gw - 0.4, h: 0.55, fontFace: BODY, fontSize: 11, color: SLATE, margin: 0 });
  }
  s.addText([
    { text: "External frameworks under UiPath governance:  ", options: { bold: true, color: NAVY } },
    { text: "the Investigator & Narrator are LangGraph (LangChain) graphs; a CrewAI variant drops in behind the same Maestro stage.", options: { color: SLATE } },
  ], { x: 0.7, y: 5.75, w: 11.93, h: 0.6, fontFace: BODY, fontSize: 13, align: "center", valign: "middle", margin: 0 });
  pageFoot(s, 7);

  // ============ SLIDE 8 — CODING AGENTS BONUS (dark accent) ============
  s = p.addSlide(); s.background = { color: NAVY };
  s.addShape("rect", { x: 0, y: 0, w: 0.18, h: H, fill: { color: AMBER }, line: { type: "none" } });
  s.addText("BONUS · UIPATH FOR CODING AGENTS", { x: 0.8, y: 0.6, w: 11, h: 0.3, fontFace: HEAD, fontSize: 12, bold: true, color: AMBER, charSpacing: 3, margin: 0 });
  s.addText("This solution was built by Claude Code", { x: 0.8, y: 0.95, w: 12, h: 0.7, fontFace: HEAD, fontSize: 30, bold: true, color: WHITE, margin: 0 });
  await iconBadge(s, "code", 0.8, 2.1, 1.0, AMBER);
  s.addText([
    { text: "Claude Code drove the UiPath uip CLI + skills to build, test, and deploy the coded agents.", options: { breakLine: true, color: ICE } },
  ], { x: 2.1, y: 2.2, w: 10.4, h: 0.8, fontFace: BODY, fontSize: 15, margin: 0 });
  const ev = [
    "LangGraph Investigator & Narrator graphs — written by the coding agent",
    "Transparent risk scoring + the Action Center HITL interrupt pattern",
    "Automated test suites (5 passing) and the uip pack → publish → deploy flow",
  ];
  s.addText(ev.map(e => ({ text: e, options: { bullet: { code: "2713" }, breakLine: true, color: WHITE } })),
    { x: 0.85, y: 3.45, w: 11.6, h: 1.6, fontFace: BODY, fontSize: 14.5, paraSpaceAfter: 10, margin: 0 });
  s.addShape("rect", { x: 0.85, y: 5.35, w: 11.6, h: 1.0, fill: { color: INK }, line: { color: AMBER, width: 1 } });
  s.addText([
    { text: "Documented & verifiable:  ", options: { bold: true, color: AMBER } },
    { text: "CODING_AGENTS.md records the tool, its contribution, and evidence (CLI flow, screenshots, session log) — targeting the full +2 platform-usage bonus.", options: { color: ICE } },
  ], { x: 1.1, y: 5.35, w: 11.1, h: 1.0, fontFace: BODY, fontSize: 13, valign: "middle", margin: 0 });
  pageFoot(s, 8, true);

  // ============ SLIDE 9 — IMPACT (light stats) ============
  s = p.addSlide(); s.background = { color: WHITE };
  header(s, "Business impact & adoption", "From hours of manual work to minutes + one decision", AMBER);
  const imp = [
    { big: "Minutes", lab: "Agent investigation replaces hours of manual review", c: TEAL, ic: "chart" },
    { big: "Consistent", lab: "Same rigor on every alert — no analyst drift", c: NAVY, ic: "balance" },
    { big: "Audit-ready", lab: "Reconstructable score + full decision trail", c: GREEN, ic: "clipboard" },
  ];
  x = 0.7;
  for (const st of imp) {
    s.addShape("rect", { x, y: 1.8, w: 3.85, h: 2.4, fill: { color: CARD }, line: { color: CARDLINE, width: 1 }, shadow: shadow() });
    await iconBadge(s, st.ic, x + 0.32, 2.08, 0.7, st.c);
    s.addText(st.big, { x: x + 0.3, y: 2.85, w: 3.4, h: 0.7, fontFace: HEAD, fontSize: 30, bold: true, color: NAVY, margin: 0 });
    s.addText(st.lab, { x: x + 0.32, y: 3.5, w: 3.35, h: 0.6, fontFace: BODY, fontSize: 12.5, color: SLATE, margin: 0 });
    x += 4.05;
  }
  s.addShape("rect", { x: 0.7, y: 4.5, w: 11.93, h: 1.6, fill: { color: NAVY }, line: { type: "none" }, shadow: shadow() });
  s.addText("Who adopts it", { x: 1.0, y: 4.7, w: 11, h: 0.4, fontFace: HEAD, fontSize: 15, bold: true, color: TEAL, margin: 0 });
  s.addText([
    { text: "Banks, fintechs, payment & crypto firms running BSA/AML programs — fewer late filings, lower cost per alert, and ", options: { color: WHITE } },
    { text: "decisions a regulator can follow end to end.", options: { color: WHITE, bold: true } },
    { text: "  Production path: swap mocked connectors for core-banking, sanctions, and FinCEN E-Filing.", options: { color: "B9C4E2" } },
  ], { x: 1.0, y: 5.15, w: 11.3, h: 0.85, fontFace: BODY, fontSize: 14, margin: 0 });
  pageFoot(s, 9);

  // ============ SLIDE 10 — CLOSE (dark) ============
  s = p.addSlide(); s.background = { color: INK };
  s.addShape("rect", { x: 0, y: 0, w: W, h: 0.12, fill: { color: TEAL }, line: { type: "none" } });
  await iconBadge(s, "shield", 0.8, 0.9, 0.85, TEAL);
  s.addText("Reasoning to agents. Action to robots.\nAccountability to people.", { x: 0.8, y: 1.95, w: 11.5, h: 1.5, fontFace: HEAD, fontSize: 34, bold: true, color: WHITE, lineSpacingMultiple: 1.05, margin: 0 });
  s.addText("All orchestrated and governed by UiPath Maestro Case.", { x: 0.82, y: 3.5, w: 11, h: 0.5, fontFace: HEAD, fontSize: 18, color: ICE, margin: 0 });
  const links = [
    { ic: "code", t: "GitHub", d: "github.com/<you>/sentinel-aml  ·  MIT" },
    { ic: "chart", t: "Demo video", d: "5-min walkthrough of the live solution" },
    { ic: "file", t: "Deck & docs", d: "Architecture · setup · CODING_AGENTS.md" },
  ];
  let lx = 0.8;
  for (const l of links) {
    s.addShape("rect", { x: lx, y: 4.4, w: 3.84, h: 1.5, fill: { color: NAVY }, line: { type: "none" } });
    await iconBadge(s, l.ic, lx + 0.3, 4.7, 0.6, TEAL);
    s.addText(l.t, { x: lx + 1.05, y: 4.68, w: 2.7, h: 0.5, fontFace: HEAD, fontSize: 15, bold: true, color: WHITE, valign: "middle", margin: 0 });
    s.addText(l.d, { x: lx + 0.3, y: 5.3, w: 3.3, h: 0.5, fontFace: BODY, fontSize: 11, color: "B9C4E2", margin: 0 });
    lx += 4.04;
  }
  s.addText("Sentinel · UiPath AgentHack 2026 · Track 1: UiPath Maestro Case", { x: 0.8, y: 6.6, w: 11.7, h: 0.4, fontFace: BODY, fontSize: 12, italic: true, color: "7E8AB0", margin: 0 });

  await p.writeFile({ fileName: "Sentinel-Deck.pptx" });
  console.log("wrote Sentinel-Deck.pptx");
})();
