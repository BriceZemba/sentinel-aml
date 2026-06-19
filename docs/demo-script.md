# 🎬 Sentinel Demo Video Full Production Guide

> Target: **4:30** (hard cap 5:00 judges stop at 5:00). Must show the solution
> **running on UiPath**, not slides. Spoken script is in **English** (recommended for
> judging; add captions). Directions are in French.

---

## 🥇 Les 3 règles d'or
1. **Raconte une histoire, pas une architecture.** Le jury 2025 a été gagné par l'émotion + une démo qui tourne. Ton fil rouge = le cas **Halcyon** (un vrai blanchisseur qu'on attrape).
2. **~70% du temps = le produit qui TOURNE.** ~30% = voix off + 1 diagramme.
3. **Pré-enregistre tout, puis narre par-dessus.** Aucune hésitation à l'écran.

---

## ✅ Pré-production (à préparer AVANT de filmer)
Enregistre/capture ces séquences à l'avance pour les monter ensuite :
- [ ] Le **diagramme du cas** (ton image d'architecture) propre.
- [ ] Un **run complet « approve »** : Start → tout vert → **SAR Filed**.
- [ ] La **pause Action Center** + l'**approbation** (la boîte « approve »).
- [ ] Un **run « reject »** → **Dismissed** (le pouvoir de l'humain).
- [ ] La **sortie de l'Investigator** (score 100, sanctions, layering, evidence).
- [ ] Les **jobs Successful** dans Orchestrator.
- [ ] **Claude Code lançant `uipath pack`** (`✓ Project successfully packaged`) + `pytest` vert pour le bonus.
- [ ] (option) L'**audit trail** du cas terminé.

**Réglages capture :** 1080p, grandes polices dans le terminal/navigateur, **notifications coupées**, secrets masqués (tokens/.env), curseur visible.

---

## 🎤 LE SCRIPT (minuté texte exact à dire)

> Format : **[ÉCRAN]** ce qu'on voit · **« … »** ce que tu dis (anglais) · *(note de jeu)*

### 0:00 – 0:25 HOOK *(ton grave, posé, captivant)*
**[ÉCRAN]** Titre « Sentinel » sur fond sobre, OU une alerte AML qui apparaît.
> « Every year, banks generate millions of money-laundering alerts. About **ninety-five percent are false alarms**. So a real one a shell company moving stolen money through a sanctioned middleman sits in the same pile as the noise, waiting for an exhausted analyst to find it. By the time anyone does, the money is gone. »

*(Ralentis sur « ninety-five percent ». Laisse un micro-silence avant la phrase suivante.)*

> « Meet **Sentinel**: an agentic financial-crime investigator that finds the real one in minutes and **never files a report without a human signing off**. »

### 0:25 – 0:55 CE QUE C'EST *(ton clair, assuré, plus rythmé)*
**[ÉCRAN]** Le diagramme d'architecture (les 5 étapes + agents/robots/humain).
> « Sentinel runs on **UiPath Maestro Case**. Every alert becomes a *case* that moves through five stages. A **low-code agent** triages it. A **coded LangGraph agent** investigates resolving the customer, screening sanctions, detecting laundering patterns. A second coded agent **drafts the regulatory report**. A quality agent checks it. And a **human compliance officer** makes the final call. Agents reason, robots act, people decide all orchestrated by Maestro. »

### 0:55 – 3:10 LA DÉMO EN DIRECT *(le cœur ton vivant, tu commentes l'action)*
**[ÉCRAN]** Orchestrator → tu lances le cas avec les inputs Halcyon.
> « Let's watch a real case. This alert flags **Halcyon Capital** rapid movement of funds, high risk. »

**[ÉCRAN]** Le cas démarre, **Triage** passe au vert.
> « Triage classifies it and routes it to investigation no duplicate, high priority. »

**[ÉCRAN]** **Investigation** tourne, puis sa sortie (score 100, evidence).
> « The Investigator agent goes to work. In seconds it finds what would take an analyst hours: the beneficial owner is **on a sanctions list**. **Two hundred forty thousand dollars** moved in and out the same day classic **layering**. And adverse media confirms an active investigation. Risk score: **one hundred out of a hundred**. And every finding **cites its source** this is not a black box. »

*(C'est ton moment « wow ». Ralentis, montre l'evidence à l'écran avec le curseur.)*

**[ÉCRAN]** **Quality Review** vert.
> « Quality Review confirms the evidence holds up. »

**[ÉCRAN]** **Narrative and Human Review** → le cas se met en **pause** (Suspended).
> « Now the Narrator drafts a regulator-ready report and **stops**. The case is suspended. It will **not** move until a human decides. »

### 3:10 – 3:55 HUMAN-IN-THE-LOOP *(LE beat clé ton solennel puis satisfait)*
**[ÉCRAN]** Action Center → la tâche avec le narratif + l'evidence.
> « This is the heart of it. In **Action Center**, the compliance officer sees the drafted report and the evidence. I approve… »

**[ÉCRAN]** Tu tapes `approve` → le cas reprend → **Filer** → **SAR Filed** (tout vert).
> « …and a robot **files** the Suspicious Activity Report. The case closes: **SAR Filed**, fully audited. »

**[ÉCRAN]** Un autre run où tu **rejects** → **Dismissed**.
> « But watch what happens if I **reject**. The agent doesn't argue. The human is accountable **by law, and by design**. No filing ever happens without them. »

### 3:55 – 4:25 PLATEFORME + BONUS CODING AGENTS *(ton fier, factuel)*
**[ÉCRAN]** Le diagramme tout vert / l'audit trail, PUIS Claude Code + `uipath pack`.
> « Every step each agent, each robot, the human decision is **recorded** against the case. And I didn't hand-write the coded agents: I **built and deployed them with Claude Code**, through UiPath for Coding Agents Python, tests, and all. Low-code and coded agents, RPA, and a human governed by **one platform**. »

### 4:25 – 4:50 IMPACT + CLÔTURE *(ton qui ralentit, qui conclut avec force)*
**[ÉCRAN]** Retour au diagramme ou un plan large « SAR Filed ».
> « Sentinel turns a two-hour manual investigation into **minutes** of agent work plus **one accountable human decision** with an audit trail a regulator can follow. **Reasoning to agents. Action to robots. Accountability to people.** That's Sentinel, on UiPath Maestro. Thank you. »

---

## 🧍 Posture & présence
- **Si tu te montres à la caméra** (recommandé pour l'intro, 5-10 s) : assieds-toi/tiens-toi **droit**, épaules ouvertes, **regarde l'objectif** (pas l'écran), léger sourire. Tu es l'expert, pas l'étudiant qui s'excuse.
- **Si c'est voix off seule** : tiens-toi **debout ou bien droit** en parlant ça s'entend dans la voix (plus d'énergie, plus de projection).
- Mains calmes, pas de tics. Respire entre les sections.

## 🎙️ Voix & tonalité
- **Calme et assuré**, comme quelqu'un qui raconte une histoire passionnante  **jamais pressé, jamais robotique**.
- **Varie le rythme** : lent et grave sur le HOOK et le moment HUMAIN ; plus vif et énergique pendant la démo (les agents qui bossent).
- **Pose des silences** courts après les phrases-chocs (« …the money is gone. » → 1 s).
- **Articule les chiffres** : « ninety-five percent », « two hundred forty thousand », « one hundred out of a hundred ».
- Enregistre la **voix séparément** si tu peux (micro propre, pièce silencieuse), puis cale-la sur la vidéo au montage = son beaucoup plus pro.

## Montage
- **Coupe tout temps mort** : attentes de chargement, hésitations. La démo doit sembler **fluide et rapide**.
- Ajoute des **titres courts** à l'écran pour chaque étape (« 1. Triage », « 2. Investigation »…) ça structure et aide le jury.
- **Sous-titres / captions** : ajoute-les (le jury peut regarder sans le son). Même en anglais, c'est un gros plus.
- **Musique** : optionnelle, **libre de droits**, volume **très bas** sous la voix. Ou silence. **Jamais** de musique copyrightée.
- **Zoom** sur les éléments clés (la sortie de l'Investigator, la tâche Action Center) pour qu'ils soient lisibles.

## ⏱️ Durée
- **Vise 4:30.** Le jury **s'arrête à 5:00** ne mets jamais l'essentiel après 4:30.
- Si tu débordes : coupe d'abord dans la section « ce que c'est » (0:25-0:55), pas dans la démo ni le moment humain.

## 🚫 Erreurs à éviter
- ❌ Lire des slides au lieu de montrer le produit qui tourne.
- ❌ Parler d'architecture pendant 2 minutes avant la démo.
- ❌ Hésiter / chercher des boutons en direct (→ pré-enregistre).
- ❌ Oublier le **moment humain** (c'est ton meilleur atout Track 1).
- ❌ Oublier de montrer **Claude Code** (c'est +2 points gratuits).
- ❌ Musique copyrightée → disqualification possible.

## 📤 Avant d'uploader
- [ ] Durée ≤ 5:00 (idéal 4:30).
- [ ] Montre la solution **qui tourne sur UiPath**.
- [ ] On voit : les agents,  le human-in-t  he-loop, Claude Code, l'audit.
- [ ] Sous-titres ajoutés.
- [ ] Pas de secrets à l'écran (tokens, .env).
           U               le lien dans Devpost.

---

## 🎯 Pourquoi ce script gagne
- **Business Impact** : le coût (95% faux positifs) + le gain (heures → minutes) sont dits explicitement.
- **Creativity** : l'histoire Halcyon + la boucle agent/robot/humain.
- **Platform Usage** : Maestro Case, Agent Builder, coded agents, Action Center, RPA, + **Claude Code** nommés.
- **Technical** : evidence citée, score transparent, le cas suspendu pour l'humain.
- **Presentation** : arc clair Problème → Solution → Démo → Impact, avec un beat émotionnel.
