---
title: Volunteer Operations Automation Platform — Project Specification
last_updated: 2026-08-30
status: living document — update as design decisions are made
companion_file: 00_AI-Context.md
---

# 0. Ethical Boundary (read first)

Clearly separate:
- **Actual ISLA experience**: SOP review, Better Impact access/permissions documentation, Google Forms attachment-permission bug, observed manual cross-system coordination.
- **Self-built prototype**: everything designed and implemented independently below.

Never imply ISLA officially deployed or endorsed the prototype. Use "proposed solution," "prototype," "portfolio extension based on real operational observations."

---

# 1. Business Problem

Volunteer operations at ISLA currently require manual coordination across multiple independent systems — Better Impact, Slack, Google Sheets, Google Forms, and email. A single business event, such as accepting a volunteer application, may require several manual follow-up actions across different platforms.

This creates risks including:
- duplicated manual work
- inconsistent status across systems
- missed onboarding actions
- limited visibility into whether required actions were completed
- dependency on individuals remembering the correct process
- difficult handover when responsibilities change

The prototype does not attempt to replace all existing ISLA systems — Better Impact already owns applications, profiles, activities, hours, reports, communication, and permissions, so rebuilding it would be unrealistic and unnecessary. Instead, the architectural focus is orchestration/integration across selected workflows rather than system replacement.

## Operational Dependency / Human Integration Layer

A significant part of the current process depends on a small number of experienced coordinators who understand how information and actions must move between Better Impact, Slack, forms, spreadsheets, email, and training activities. In practice, these coordinators act as a human integration layer:
- remembering which downstream actions follow a business event
- checking whether status is consistent across systems
- deciding which tasks can safely be delegated to others
- resolving exceptions when systems or permissions don't align
- transferring operational knowledge to future team members (knowledge that itself degrades over time without documentation — coordinators who step back from a process for 6–12 months report needing to relearn parts of it)
- absorbing the loss of institutional knowledge when a team member leaves

This creates both an integration problem and a knowledge/handover problem. The prototype therefore focuses not only on automating system-to-system updates, but also on making workflow state, ownership, failures, and required follow-up actions explicitly visible — rather than living only in one or two people's heads.

## Cross-System State Inconsistency

The same participant's status may be represented in multiple places, for example:
- application/volunteer status (Better Impact)
- Slack membership
- training/attendance records
- email/onboarding communication sent or pending
- spreadsheet-based tracking

Because these updates are coordinated manually, one system can reflect a completed transition (e.g. "accepted") while another still shows the prior state. The prototype treats PostgreSQL as the authoritative operational state and tracks downstream integration completion (Slack/Sheets/Email) separately and explicitly, rather than assuming all systems stay in sync automatically (see Section 8 Source of Truth and Section 12 Integration Consistency Model).

## Observed Operational Workflow (as it actually runs today)

```
Recruitment → Application → Assessment → Decision (successful/unsuccessful)
→ Onboarding → Slack membership → Training → Program Activities
→ Attendance → Volunteer Hours → Communication → Access Permissions
→ Documentation → Handover
```

Example event chain observed in practice: an applicant is assessed → marked successful → records are updated → Slack onboarding happens → an email is sent → training information is shared → attendance/volunteer records begin. Many of these transitions involve manual coordination between people and/or systems, and several do not appear to be automatically synchronised — this is an observation about the general pattern, not a claim that every single step has been individually verified as manual.

## Specific Real ISLA Experience (evidence base — actual work performed/observed; keep separate from the prototype per Section 0)

**SOP Review**: Reviewed an ISLA operational SOP from a new-user perspective, to assess whether a future team member could follow the process unaided. Gaps identified:
- unclear terminology
- unclear distinction between assessment-related forms/processes
- missing transition between assessment Slack channels and successful-member onboarding Slack channels
- SOP lacked links to current forms/templates
- handover/delegation was not addressed

**Better Impact Access Documentation**: Documented administrator roles, permissions, access purposes, sensitive access categories, current access holders, and areas requiring confirmation. Purpose: support access consistency, privacy awareness, handover, future onboarding, and delegation — framed as capacity-building/delegation work, not only a security exercise (e.g. certain recurring tasks, such as updating response templates, were identified as delegable to a trusted IT-capable team member rather than requiring a specific staff member). This observation is the real-world root of the RBAC design, and one input into the broader access/data-governance thinking in Sections 8–10 — it is not the sole origin of the Source of Truth decision, which is a broader architecture judgment made in response to the cross-system inconsistency pattern above.

**Google Forms Attachment Permission Issue**: Applicants upload assessment attachments via Google Forms. One administrator can view the attachments; some assessors can access the form/responses but cannot see the attachments themselves. This forces assessors to work jointly rather than independently. This is evidence of recurring access/integration/application-support friction in the current tool landscape — it is not itself a functional requirement the prototype sets out to fix, and the flagship is not designed to solve this specific bug.

**Reusable Communication Templates (observation)**: Reusable Better Impact email templates were observed to meaningfully reduce repetitive administrative work. This observation is the real-world justification for the prototype's `MessageTemplate` entity and automated-communication design (Section 7).

## Scoping Judgment: Not Every Observed Problem Is an Automation Problem

Slack usage at ISLA involves onboarding, assessment channels, project/team channels, threads, search, notifications, and general user adoption. Some of the friction observed there is a user-adoption or process-governance problem rather than an integration/technical one, and is deliberately left **outside** the prototype's technical automation scope. Not every operational issue observed in the field is treated as something to automate — some are process or training problems, and are named as such rather than forced into a technical solution.

---

# 2. Business Objectives

The prototype aims to demonstrate how volunteer operations could:
1. Reduce repetitive manual cross-system updates.
2. Improve consistency between operational systems.
3. Make workflow completion visible and auditable.
4. Reduce dependence on individual staff remembering manual steps.
5. Provide controlled role-based access to operational functions.
6. Allow selected workflows to be automated while preserving human approval for sensitive actions.
7. Enable selected operational responsibilities to be delegated safely, by making permissions, ownership, and workflow responsibilities explicit rather than implicit knowledge held by one or two people.

Every integration/technology choice below should trace back to one of these objectives (not "used Slack because it's a resume keyword").

---

# 3. Core Stakeholders / Actors

**Volunteer** — submits volunteer hours, views own information, receives operational communication.

**Team Leader** — reviews selected volunteer information, records attendance, approves/rejects volunteer hours.

**Administrator / Program Operations** — reviews applications, changes application status, manages onboarding, monitors workflow completion, approves sensitive outbound actions.

**IT / System Administrator** — manages access and permissions, investigates integration failures, maintains configuration.

**External systems** (not human actors, but system participants) — Slack, Google Sheets, Email provider.

RBAC and API design should be derivable from this actor list.

---

# 4. Project Scope

### In Scope
- volunteer application lifecycle prototype
- volunteer records, program membership
- events and attendance
- volunteer-hour submission and approval
- authentication and RBAC
- selected business workflow automation
- Slack integration, Google Sheets integration, email integration
- integration status / audit logging
- AI Operations Copilot (V3 extension)

### Out of Scope
- replacing Better Impact
- production deployment inside ISLA
- use of real ISLA personal data
- payment processing, payroll, accounting
- full CRM functionality
- custom AI model training
- microservices, high-scale distributed infrastructure

---

# 5. Functional Requirements

| ID | Requirement |
|---|---|
| FR-01 | Administrators shall be able to review applications and change their status. |
| FR-02 | The system shall only create/activate a volunteer record from an accepted application. |
| FR-03 | Users shall authenticate before accessing protected application functions. |
| FR-04 | The system shall restrict business actions according to assigned roles/permissions. |
| FR-05 | Volunteers shall be able to submit volunteer hours. |
| FR-06 | Authorised users shall be able to approve or reject submitted volunteer hours. |
| FR-07 | Authorised users shall be able to record attendance for events. |
| FR-08 | Relevant state changes shall generate internal business events. |
| FR-09 | Selected business events shall trigger configured Slack, Google Sheets, and Email integrations. |
| FR-10 | The system shall record the outcome of each external integration attempt independently. |
| FR-11 | Failed operations shall support controlled retry; previously processed events shall not cause duplicate external actions. |
| FR-12 | Important administrative and automated actions shall be recorded in an audit log. |

---

# 6. Non-Functional Requirements

**Security**
- Protected endpoints require authentication.
- Authorization is enforced server-side.
- Secrets are never stored in source control.
- AI cannot bypass RBAC or business logic.

**Privacy**
- Portfolio environments use synthetic data only.
- Real ISLA volunteer personal data is never used without explicit authorisation.

**Reliability**
- External integration failures must be recorded.
- Duplicate processing must not produce duplicate business actions.
- Failure of one external integration must be independently traceable.

**Maintainability**
- Business logic stays separate from API/controller code.
- Integrations use a consistent adapter/service pattern.
- Key architecture decisions are documented.

**Observability**
- Important application and integration events are logged.
- Failures include enough context to troubleshoot.

**Portability**
- Application runs via Docker in dev/deployment environments.

---

# 7. Domain Model

Core entities: User, Volunteer, Role, Permission, Program, Application, Assessment, Event, Attendance, VolunteerHour, Notification, AuditLog.
Optional if justified: SupportRequest, TrainingRecord, MessageTemplate.

Attendance and volunteer-hour records are operationally significant, not arbitrary schema choices — they contribute to program participation tracking and volunteer recognition/records at ISLA. (Note: certification-tier logic such as Bronze/Gold milestones belongs to the separate ISLA Attendance System case in `00_AI-Context.md` Section 2B and is deliberately not merged into this flagship's domain model — keep the two projects' entities distinct.)

Core workflow:
```
Applicant → Application → Assessment → Accepted/Rejected → Volunteer
→ Onboarding → Training → Attendance / Volunteer Hours
```

Business rules (examples):
- Approved volunteer hours cannot be edited directly by a Volunteer.
- Only accepted applications can be converted into active volunteer records.
- Sensitive outbound actions require human approval.

Schema derivation: entities and relationships must be justified from FR-01–FR-12 above, not added for complexity.

---

# 8. Data Ownership / Source of Truth

- **PostgreSQL** is the source of truth for application and volunteer operational state.
- **Slack** is a communication/collaboration target, not a master data store.
- **Google Sheets** is an external reporting/operational view, not the authoritative database.
- **Email** is an outbound communication channel only.
- External system state must never silently overwrite authoritative application state.

---

# 9. Architecture Overview

```
Real Business Problem
    ↓
Requirements → System Design → Database → Backend → REST API
    ↓
Authentication / RBAC
    ↓
Business Events
    ↓
Integration (Slack / Sheets / Email)
    ↓
Workflow Automation
    ↓
Testing → CI/CD → Docker / Cloud
    ↓
Applied AI (Operations Copilot)
```

**Backend:** Python + FastAPI. **Database:** PostgreSQL.

---

# 10. RBAC (example)

| Role | Can |
|---|---|
| Volunteer | view own profile, submit own volunteer hours |
| Team Leader | view team members, approve/reject hours, record attendance |
| Administrator | manage applications/status, manage users, manage roles/permissions |

Example: `Volunteer → GET /admin/users → 403 Forbidden`; `Administrator → GET /admin/users → 200 OK`.

---

# 11. Example REST API

```
POST   /applications
GET    /applications
GET    /applications/{id}
PATCH  /applications/{id}/status

GET    /volunteers
GET    /volunteers/{id}

POST   /events
POST   /events/{id}/attendance

POST   /volunteer-hours
PATCH  /volunteer-hours/{id}/approve

GET    /reports/volunteer-hours
```

API should represent real business actions, not just CRUD.

---

# 12. Integration Consistency Model

The system does **not** use an all-or-nothing distributed transaction across Slack, Google Sheets, and Email.

```
Business Event
    ↓
Integration Attempts
    ├─ Slack  → SUCCESS / FAILED
    ├─ Email  → SUCCESS / FAILED
    └─ Sheets → SUCCESS / FAILED
```

- Each external integration is tracked independently (e.g. an `IntegrationAttempt` table keyed by `event_id × channel × status`).
- A failure in one SaaS integration does not roll back the authoritative PostgreSQL business transaction.
- Failed integrations can be retried safely.
- Each event has a unique `event_id`; processing must be idempotent (duplicate processing of the same event_id must not produce duplicate external actions — this covers internal retry/re-delivery, not just literal duplicate inbound webhooks).

**Build order decision:** implement one integration (Slack) through the full test matrix (success / failure / duplicate / authorization) before replicating the pattern to Sheets and Email.

---

# 13. Integration Failure Handling

- **Slack API fails** → record failed integration, retry, log error, notify admin if retry exhausted. Do not mark the business action successful.
- **Duplicate event** → prevent duplicate action (event ID / idempotency key / processed-event record).
- **Auth failure (401/403 from external API)** → stop integration, log failure, never expose secrets.

---

# 14. Testing Standard

Beyond "N tests passed," the following scenarios must have real test coverage:

1. **Happy path**: Application accepted → DB updated → Slack called → Email called → Sheets called.
2. **External failure**: Slack API returns 500 → retry → still fails → failure recorded → other business data remains valid.
3. **Duplicate event**: same `application_accepted` event arrives twice → welcome email/Slack/Sheets row each happen only once.
4. **Authorization**: Volunteer tries to approve application → 403 → no external workflow triggered.
5. **(V3) AI invalid output**: LLM returns invalid structured output → validation fails → no external action executed.

---

# 15. CI/CD (required for V2 completion)

```
git push → GitHub Actions → Lint → Unit Tests → Integration Tests → Docker Build → Deploy
```

Priority note: failure/idempotency/authorization test coverage comes before pipeline polish — interviews probe failure modes more than pipeline existence.

---

# 16. Test Environment / Privacy

- Synthetic volunteer data only.
- Separate Slack test workspace, test Google Sheet, test email account, dev API credentials.
- Never connect the prototype to real ISLA production data without explicit permission. This choice is itself a legitimate privacy/security design decision to discuss in interviews.

---

# 17. AI Architecture (V3 — Operations Copilot)

Example request: *"Show me Silver volunteers who missed two training sessions and still have incomplete volunteer hours, then draft follow-up messages."*

```
Natural Language → LLM → Structured Output → Tool/Function Calling
→ Authorised FastAPI Business APIs → PostgreSQL → Retrieve Data
→ RAG (SOPs/policy, if needed) → LLM drafts proposed action
→ Human Approval → Slack/Email → Audit Log
```

Principle: AI never directly accesses or manipulates the database. It goes through authorised application tools → FastAPI business logic → database, preserving authorization, validation, logging, and auditability.

**Tools (examples):** `get_volunteers()`, `get_attendance()`, `get_volunteer_hours()`, `get_program_requirements()`, `draft_follow_up_message()`.

**Structured output example:**
```json
{
  "program": "Silver",
  "missed_training_count": 2,
  "volunteer_hours_status": "incomplete",
  "requested_action": "draft_follow_up"
}
```
Backend validates this before execution.

**RAG** used only for unstructured organisational knowledge (SOPs, FAQs, program commitment documents) — not added just to demonstrate RAG.

**Human-in-the-loop:** AI drafts sensitive actions (emails, status changes); admin approves before real Slack/Email send.

---

# 18. AI Evaluation Criteria

The Operations Copilot is evaluated separately from deterministic backend functionality:
- intent correctly interpreted
- structured output matches required schema
- correct authorised tool selected
- unsupported actions are rejected
- retrieved SOP/policy information is grounded in available documents
- no business action occurs without required human approval
- invalid LLM output cannot bypass application validation
- failure of the LLM does not corrupt operational data

AI quality is not measured only by whether the generated response "looks good."

---

# 19. Development Phases & Completion Criteria

**Version 1 — Backend Foundation**
Requirements, ERD, PostgreSQL, FastAPI, REST API, Auth, RBAC, Business Logic, Validation, Tests, Swagger, Docker, Deployment. → *Good Junior Backend portfolio.*

**Version 2 — Real Integration & Automation**

| Area | Completion condition |
|---|---|
| Integration | Real Slack + Google Sheets + Email connections (test env, synthetic data) |
| Automation | Business event → workflow across multiple SaaS targets |
| Reliability | Retry / idempotency / failure handling |
| Testing | Unit + integration + failure-path (external API failure, duplicate event, authorization) |
| CI/CD | **Required** — lint → unit → integration → Docker build → deploy |
| Deployment | Docker, real cloud deployment |
| Observability | Logging incl. integration failures |
| Docs | README, architecture diagram, API docs |

→ *Strong Integration/Automation flagship — standalone-sufficient for Integration/Application/Automation/Junior Backend Engineer roles.*

**Version 3 — Applied AI**
LLM API, Structured Output, Tool/Function Calling, RAG (where justified), Human-in-the-loop, AI validation, AI failure handling, Operations Copilot. → *Strong AI-enabled Business Application / Junior AI Application portfolio.*

---

# 20. Portfolio Success Criteria

The flagship is successful when:
1. A user can complete the core business workflow through the deployed application.
2. Authentication and RBAC correctly restrict actions.
3. A real business event triggers real test integrations with Slack, Google Sheets, and Email.
4. Integration failures are independently recorded and safely retryable.
5. Duplicate event processing does not produce duplicate external actions.
6. Automated tests cover core business logic, authorization, integrations, and failure paths.
7. CI/CD automatically validates and deploys the application.
8. Architecture, API behaviour, and major design decisions are documented.
9. V3 AI functionality interacts only through controlled application APIs and respects human approval boundaries.
10. The developer can explain the reasoning behind the architecture and implementation without relying on generated documentation.

---

# 21. Interview Story (for reference)

*"I observed that a real volunteer organisation was coordinating operational information manually across several SaaS systems. I analysed the existing process and identified integration and workflow gaps. I designed a PostgreSQL domain model and FastAPI backend with authentication, RBAC and business rules. I then connected the prototype to real SaaS services — Slack, Google Sheets, email — using event-driven workflows and proper failure handling. Finally, I added an AI Operations Copilot that translates natural-language operational requests into controlled business API calls, retrieves relevant organisational knowledge, and proposes actions for human approval."*

## Questions to be ready for
Why PostgreSQL? Why this ERD? Why separate Application from Volunteer? How does JWT auth work? How is RBAC implemented? Why webhooks? What if a webhook/event arrives twice? What if Slack is unavailable? How do you keep Sheets and PostgreSQL consistent? Why AI for this problem specifically? Why not AI for status transitions? How does tool calling work? Why does AI use FastAPI tools instead of querying the DB directly? What happens on invalid LLM output? What requires human approval? How are API credentials protected? What data is synthetic vs. real? What was actual ISLA work vs. your independent prototype?

---

# 22. Build-Order Task Breakdown

Granular, numbered task list from first setup step to V3 completion. Each task has a difficulty rating and a note on whether it's new/hard or repetitive — this is how "how big is this project" gets resolved concretely rather than abstractly.

## Pre-project setup (do before Task 1)

| # | Task | Difficulty |
|---|---|---|
| S1 | Confirm Python install (`python --version`) | Low |
| S2 | Decide PostgreSQL setup: local install vs. Docker (recommend Docker from the start — avoids redoing this at V1 Task 13) | Low |
| S3 | Code editor set up (VS Code recommended — pairs with Claude Code's extension) | Low |
| S4 | Confirm Node.js install (needed for Claude Code itself, which installs via npm) | Low |
| S5 | GitHub account confirmed | Low |
| S6 | Create the repo (decide public/private — portfolio use implies public; keep the "actual ISLA experience vs. prototype" separation in mind for README/commit wording from the very first commit) | Low |
| S7 | Install and authenticate Claude Code with the chosen plan | Low |
| S8 | Create one project folder; place `CLAUDE.md`, `00_AI-Context.md`, `01_Volunteer-Ops-Platform-Spec.md` together at its root | Low |
| S9 | Write `.gitignore` before any secrets can be created (Python: `venv/`, `__pycache__/`, `.env`, etc.) — do this before Task 1, since secrets committed to git history are hard to fully remove later | Low |
| S10 | Establish the `.env.example` habit (real `.env` never committed) | Low |
| S11 | Decide Python virtual environment approach — standard `venv` is enough for this project's scale (poetry/uv would be overkill) | Low |

## Version 1 — Backend Foundation

| # | Task | Difficulty | New vs. repetitive |
|---|---|---|---|
| 1 | Project scaffold: install FastAPI/PostgreSQL deps, create project structure | Low | New (one-time) |
| 2 | ERD by hand (paper or draw.io): Volunteer, Application, Event, etc. and their relationships | Medium | New — mapping "1-to-many"/"many-to-many" onto this specific domain |
| 3 | Define SQLAlchemy models → create tables via Alembic migration | Medium | New — ORM syntax, migration concept |
| 4 | First FastAPI endpoint working (`GET /volunteers`) | Low | New — first "it works" moment |
| 5 | Pydantic request/response validation | Low–Medium | New until the pattern clicks |
| 6 | Repeat the CRUD pattern for Application, Event, etc. | Low | Repetitive — no new concepts |
| 7 | Business logic (e.g. approved hours can't be edited) | Medium | New — "where does this rule live" design judgment |
| 8 | JWT auth (register/login/password hashing) | Medium–High | New — biggest new concept for most people at this stage |
| 9 | RBAC (role field + per-endpoint permission checks) | Medium | New, but straightforward once Task 8 is done |
| 10 | Unit tests (pytest) for business logic | Medium | New if unfamiliar with testing |
| 11 | Integration tests (TestClient hitting the API) | Low–Medium | Extension of Task 10 |
| 12 | Logging & error handling | Low | Pattern-based once the shape is decided |
| 13 | Dockerfile + docker-compose (FastAPI + PostgreSQL together) | Medium | New if unfamiliar with Docker |
| 14 | Deploy to cloud (free tier — e.g. Railway/Render) | Low–Medium | New — first deploy is usually where things get stuck |
| 15 | README + confirm Swagger auto-docs | Low | FastAPI generates this automatically |

## Version 2 — Real Integration & Automation

| # | Task | Difficulty | New vs. repetitive |
|---|---|---|---|
| 16 | Create Slack test workspace, get bot token | Low | New — Slack admin UI |
| 17 | Send a Slack message from FastAPI (one function) | Low–Medium | New — shape of external HTTP calls |
| 18 | Wire Slack notification into "Application accepted" | Low | Wiring only once 16–17 exist |
| 19 | Google Cloud Console: Sheets API credentials (OAuth/service account) | Medium–High | New — OAuth is where most people get stuck |
| 20 | FastAPI function to append a row to Google Sheets | Medium | New — Google API library conventions |
| 21 | Email sending (test account, e.g. SendGrid) | Low–Medium | New — API key handling, templates |
| 22 | Wire all three integrations to fire from one "Application accepted" event | Medium | Design decision — how the event fans out |
| 23 | `IntegrationAttempt`-style table (event_id × channel × status) | Medium–High | New design concept — partial-failure tracking |
| 24 | Retry logic (limited retries with backoff) | Medium | New — backoff/wait design |
| 25 | Idempotency key implementation (don't reprocess the same event_id twice) | High | New — the most conceptually new piece in V2 |
| 26 | Confirm authorization failures never trigger external workflows | Medium | Verification of 9 + 21–25 working together |
| 27 | Failure-path test: mock Slack API returning 500 | High | New — mocking/stubbing as a testing technique |
| 28 | Duplicate-event test: same event sent twice → only one external action each | High | Extension of 27, async behaviour under test |
| 29 | Authorization test: Volunteer role hits approval endpoint → 403 + no external call | Medium | Extension of Task 9's tests |
| 30 | GitHub Actions config (lint → test → build) | Medium | New — YAML, CI concepts |
| 31 | PostgreSQL as a CI service container | High | New — CI-specific environment quirks |
| 32 | Docker build inside CI | Medium | Extension of Task 13 |
| 33 | Deploy from CI (or a documented manual deploy runbook) | Medium | Extension of Task 14 |
| 34 | Log integration failures (observability) | Low–Medium | Extension of Task 12 |

## Version 3 — Applied AI

| # | Task | Difficulty | New vs. repetitive |
|---|---|---|---|
| 35 | Basic LLM API call working (one request/response) | Low | New — API key, response shape |
| 36 | Endpoint that accepts a natural-language request | Low | Extension of Task 4 |
| 37 | Structured Output — fixed JSON schema for the LLM's reply | Medium–High | New — prompt design + schema validation together |
| 38 | Validate the returned JSON with Pydantic; reject if invalid | Medium | Extension of Task 5, but "don't trust the AI's output" is a new mindset |
| 39 | Tool/function-calling definitions (e.g. `get_volunteers()`) exposed to the LLM | High | New — the tool-calling mechanism itself |
| 40 | Map the LLM's chosen tool to the actual FastAPI function and execute it | High | New — the trickiest wiring point in V3 |
| 41 | Confirm the AI only touches the DB via FastAPI (never directly) | Medium | Verification that existing RBAC/validation still holds |
| 42 | Chunk SOP/FAQ docs and embed them (RAG prep) | High | New — embeddings, vector concepts, entirely new territory |
| 43 | Basic vector search (pgvector or Chroma) | High | New — new library/DB extension |
| 44 | Wire retrieved chunks into the LLM prompt for grounded answers | Medium–High | New — RAG pipeline wiring |
| 45 | Endpoint to preview an AI-drafted message before sending | Low–Medium | Extension of Task 4 for the approval UI |
| 46 | Only send via Slack/Email after human approval | Medium | Extension of Task 22, human-in-the-loop logic |
| 47 | Test: deliberately broken LLM JSON → execution blocked | High | New — testing AI failure modes specifically |
| 48 | LLM API failure → retry/controlled error | Medium | Extension of Task 24 |

**Summary**: V1 has 11 setup + 15 build tasks (1 genuinely hard: #8). V2 has 19 tasks (4–5 hard: #19, #23, #25, #27, #28, #31). V3 has 14 tasks (3 genuinely new domains: #37/#39/#40 structured-output+tool-calling, #42/#43 RAG). Most items in each phase are low-difficulty once the hard ones are done — the size of the project is not "one big unknown," it's a short list of specific new concepts plus a long tail of repetition.

## Rough time/duration estimate (for reference, not a commitment)
- Analysis (this spec's Sections 1–9 groundwork): ~20–25h
- V1: ~55–80h · V2: ~58–87h · V3: ~43–67h
- V2-complete (portfolio-sufficient for target roles): ~133–192h total
- Actual calendar time depends entirely on weekly hours available — not yet fixed (open item, see Section 23).

## Open design decisions to resolve early in V2
1. Idempotency key design — where "has event_id X been processed" is checked and stored.
2. Confirm `IntegrationAttempt`-style table shape (event_id × channel × status) before writing integration code.
3. Build Slack integration completely (through the full test matrix) before starting Sheets/Email.

---

# 23. Open Items (deliberately deferred, not forgotten)

These were raised and explicitly parked for later — listed here so they aren't lost, and so another AI/session doesn't assume they were decided:

- **Weekly time budget**: how many hours/week Kent can realistically commit is not yet fixed. All duration estimates above are calendar-time-unknown until this is set.
- **Frontend/UI**: current design is API-only (Swagger UI / Postman for demoing). Whether to add a minimal UI (e.g. a simple React admin screen) for interview demos has not been decided.
- **Second portfolio project** ("AI Helpdesk Automation" or similar, smaller/optional): not committed to; flagship remains primary regardless.
- **Hosting specifics**: "Cloud deployment" is agreed; the actual provider (Railway/Render/Fly.io/etc.) is not chosen.
- **LLM provider for the in-app Operations Copilot** (V3): not chosen yet — deliberately deferred until V3 is actually being built, so the choice reflects whatever's current then.
- **Vector DB for RAG** (pgvector vs. Chroma vs. other): options identified, not chosen.
- **Email provider**: SendGrid mentioned once as an example, not committed.
- **Whether to keep the deployed app running continuously** or spin it up only for interviews (cost management consideration).
- **Progress tracking method, git conventions, timebox handling — decided 2026-08-30**: GitHub Issues + Projects (Kanban, one Milestone per version), simple branch-per-task convention, 1.5x-time timebox rule for "High" difficulty tasks. See `CLAUDE.md` "Progress tracking" section for full detail — no longer open.
- **Resume/LinkedIn/GitHub README presentation** of this project — not yet drafted.

---

# 24. Real Operations → Engineering Design Mapping (for interview reference)

| Observed at ISLA | Engineering response in the prototype |
|---|---|
| Multiple SaaS tools coordinated manually by people | Integration architecture |
| Process knowledge concentrated in a few coordinators | Workflow visibility / auditability |
| Difficulty handing over responsibilities | Explicit process/state/ownership modeling |
| Ad hoc access/permission management | Authentication + RBAC |
| Reusable Better Impact email templates | `MessageTemplate` / automated communication |
| Manual Slack onboarding after acceptance | Business event → Slack API |
| Manual spreadsheet-based tracking | Google Sheets integration |
| Repetitive manual email communication | Email API |
| Status drift between systems for the same participant | PostgreSQL as Source of Truth |
| One integration succeeding while another fails | `IntegrationAttempt` tracking |
| Manual redo of a failed step | Retry logic |
| Risk of doing a step twice | Idempotency |
| Permission/access friction (e.g. Google Forms bug) | Authorization + failure handling design |
| SOP / organisational knowledge scattered or informal | V3 RAG |
| Staff needing to ask questions or issue instructions in plain language | Operations Copilot |
| Sensitive actions needing a human decision | Human-in-the-loop approval |

This table is the throughline for the "why did you build it this way" interview questions in Section 21 — every row traces a specific real observation to a specific engineering decision, rather than the design being technology chosen first and justified after.
