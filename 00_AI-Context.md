---
title: AI Context Note — Kent
last_updated: 2026-08-30
purpose: Portable context for any AI assistant (Claude / ChatGPT / Gemini) to avoid re-explaining background
---

# 1. Personal Background

- **TAFE Diploma in Programming** (C# / JS foundation) → now studying a **Master of Information Technology (Information Systems focus)**. Has also worked with Python. This progression (technical foundation → business/systems understanding → applied practice) is the backbone of the career narrative in Section 2A below — not a pivot away from a technical background, but a re-convergence of technical skill + business understanding.
- Uses AI across four modes of work: idea generation, research/information organisation, coding/technical work, and writing/editing.
- Building an **Obsidian-based portable context system** (this file) so any AI assistant can pick up context without repeated re-explanation.
- Also volunteers with **ISLA** (City of Sydney international student volunteer/training program, ~100 participants per monthly event) — this is both a real commitment and a source of portfolio material (see Project B below).

---

# 2. Active Projects

## A. Career & Portfolio Strategy (PRIMARY — flagship project)

**Full project specification lives in a separate file: `01_Volunteer-Ops-Platform-Spec.md`.** That file is the living System/Project Specification (business problem, objectives, stakeholders, scope, FR/NFR, data model, architecture, integration consistency model, AI evaluation, success criteria). This file only holds the summary needed to orient a new AI session quickly.

### Career direction (decided, stable)
> Build intelligent business applications by combining backend development, API integration, workflow automation, and applied AI — supported by an Information Systems background.

- Not aiming to be: "a Business Analyst who can code a little" or "a Data Scientist who builds models."
- Aiming to be: an engineer who understands business systems and turns operational problems into working technical solutions.
- Skill balance target: Business/Systems Understanding 30% · Backend/API/Integration 40% · AI Application/Automation 30%.

### Target roles (priority order)
1. Integration Engineer / Integration Developer
2. Application Engineer
3. Automation Engineer / Automation Developer
4. AI Application Engineer
5. (Secondary) Junior Backend Engineer, Implementation Engineer, Solutions Engineer, Business Applications Developer, Application Support Engineer

### Explicitly NOT targeting
Data Scientist, ML Researcher, ML Engineer (model training), Computer Vision Engineer, embedded/low-level C++, pure DevOps/Platform Engineering, algorithm-heavy Big Tech SWE.

**AI stance:** use existing LLMs as components inside applications; do not train models. Rule of thumb — deterministic business rules → normal code; ambiguous/unstructured language or intent → AI.

### Flagship project: "Volunteer Operations Automation Platform"
Based on real ISLA operational observations (see spec file for full Business Problem statement). One-line summary: ISLA coordinates volunteer operations manually across Better Impact, Google Forms/Sheets/Drive, Slack, and Outlook — the prototype demonstrates how a central business application could coordinate selected workflows across these systems.

**Hard ethical boundary (never violate):** clearly separate actual ISLA experience (SOP review, Better Impact access documentation, Google Forms permissions bug) from the self-built prototype. Never imply ISLA deployed or endorsed the prototype — use "proposed solution / prototype / portfolio extension."

### Development phases (see spec file for full completion-criteria tables)
- **V1 — Backend Foundation**: PostgreSQL + FastAPI + Auth/RBAC + Business Logic + tests + Docker + deploy. Standalone-complete: good Junior Backend portfolio.
- **V2 — Real Integration & Automation**: Slack/Sheets/Email real connections + retry/idempotency + failure-path tests + **CI/CD required**. Standalone-complete: strong Integration/Automation flagship. *(CI/CD upgraded from optional to required 2026-08-30; priority is failure/idempotency/authorization test coverage first, pipeline second.)*
- **V3 — Applied AI ("Operations Copilot")**: LLM → Structured Output → Tool calling → FastAPI (AI never touches DB directly) → RAG → human approval → Slack/Email. Extends an already-complete system rather than being load-bearing.

### What NOT to add (unless a genuine requirement emerges)
Stripe, Kafka, Kubernetes, microservices, Redis (unless needed), complex distributed architecture, custom model training.

### Guiding principle
> One complete, understandable, deployable system where every major design decision has a reason — not maximum technology count.

---

## B. ISLA Attendance System (secondary — practice/portfolio-building case)

- Redesigning attendance management for ISLA's monthly volunteer/training events (~100 international students).
- Constraints: near-zero budget, Microsoft 365 environment, government IT policy, diverse user base, low event frequency (reduces automation ROI), certification integrity (Bronze/Gold milestones tied to attendance).
- Recommended stack: QR code → Microsoft Forms → Excel Online → Power BI (Power Automate optional).
- Key insight: existing participant registration list enables list-based reconciliation (VLOOKUP/conditional formatting to flag mismatches).
- Self-assessed as a **practice/skill-building case, not a centerpiece portfolio piece** — lacks quantitative justification, stakeholder analysis, risk matrices, post-implementation KPIs needed for mid/senior BA work. Could be strengthened later with those artifacts if desired, but is not the current priority (Project A is primary).

---

# 3. Work Style & Preferences

- Wants to **understand underlying logic**, not just be told steps (e.g. asks how mechanisms actually work).
- Prefers **large tasks broken into small, concrete, numbered items** with an honest difficulty rating and a note on what's genuinely new vs. repetitive — this is how ambiguity about project "size" gets resolved for him.
- Wants **honest, direct assessment** — explicitly values pushback over agreement; dislikes vague reassurance ("this is great!") without substance.
- Comfortable revising earlier decisions when new reasoning is presented (e.g. moved CI/CD from optional to required, reprioritized failure-testing above pipeline existence) — treat prior "decided" items as revisable, not fixed doctrine, when Kent brings a reasoned counter-argument.
- Iterates through structured analysis and is willing to pivot when constraints surface (e.g. ROI framing dropped for the volunteer-context case).
- Explicitly self-aware about gaps (e.g. flagged that the ISLA case alone isn't senior-BA-portfolio-level) — respond to this kind of self-assessment by confirming/correcting rather than over-reassuring.

---

# 4. Direct AI Instructions

- Treat the Section 2A decision log (career direction, target roles, V1–V3 completion criteria, CI/CD requirement, testing standards) as **the current settled state** unless Kent explicitly revisits it.
- When Kent asks "how do I build X," default to **breaking it into a numbered task list with difficulty level and what's new-to-him vs. repetitive** (the format used for V1–V3 breakdowns), rather than abstract phase descriptions.
- Always maintain the **actual ISLA experience vs. self-built prototype** separation in any wording suggested for the portfolio — never phrase things in a way that implies ISLA deployed or endorsed the prototype.
- When evaluating whether a technology/feature belongs in the portfolio, apply the standing filter: *is this justified by a real requirement, or is it being added to look impressive?* Default to leaving it out if unjustified.
- When giving portfolio/career advice, be willing to say "this isn't enough" or "this is a weaker choice" rather than defaulting to encouragement — this has been explicitly requested and well-received.
- For job description evaluation: judge by responsibilities/technologies in the JD body (verbs like "integrate," "automate," "troubleshoot" = good fit; "train model," "research," competitive-programming screens = poor fit), not by job title alone.

### Coding/learning workflow (decided 2026-08-30)
Kent is rebuilding rusty web-dev knowledge (core programming concepts from TAFE are retained; web/app-building specifics are rusty) while building the flagship project, using a mix of chat (planning/concepts) and Claude Code (hands-on implementation). The agreed rule, to avoid "tutorial hell" (understanding generated code vs. being able to produce it unaided):
- **New/hard-concept tasks** (e.g. JWT auth, RBAC, idempotency, tool calling — the "high difficulty, first-time" items in the task breakdowns): Kent writes a first attempt himself (timeboxed ~15–20 min, imperfect is fine) *before* involving Claude Code. Claude Code is then asked to **review only** ("point out what's wrong or missing — don't rewrite it"), and Kent does the fix himself. Do not default to writing the implementation for him on these tasks even if asked casually — nudge back toward "try it yourself first" framing if he skips straight to "build X."
- **Repetitive/pattern-established tasks** (e.g. the 2nd+ CRUD endpoint once the pattern is clear): fine to delegate straight to Claude Code — low learning value in redoing these by hand.
- Avoid recommending Claude Code's full auto-accept/"skip permissions" mode for this project — Kent should review each diff manually while learning.

### Tool division: this chat vs. Claude Code (decided 2026-08-30)
- **This chat (Claude.ai)**: requirements definition, architecture/scope decisions, spec-file updates, career/portfolio strategy, conceptual "why does this work" explanations — anything decoupled from an actual codebase.
- **Claude Code**: hands-on implementation, plus code-level design discussion via Plan Mode (Shift+Tab) — endpoint design, error-handling approach, and similar decisions are better made in Claude Code once code exists, since it has the actual project context. Not a strict "requirements here, code there" split — the dividing line is "does this need the real codebase in context," not "is code being written right now."
- Recommend Kent copy the essentials of this file and `01_Volunteer-Ops-Platform-Spec.md` into a `CLAUDE.md` at the project root, since Claude Code does not share this chat's cross-session memory — `CLAUDE.md` is its equivalent persistent context, read automatically at the start of each session.
