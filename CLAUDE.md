# Project Context

## Current Status (update this each session — 1–2 lines, detail lives in GitHub Issues)
S1–S11, V1 Task 1, and Task 2 (ERD) complete; **Task 3 in progress** (2026-09-03): SQLAlchemy models + Alembic migrations underway, translating the Section 7 ERD into real PostgreSQL tables (temporary dev Postgres container `volunteer-ops-postgres-dev`, formal docker-compose deferred to Task 13). `Application` modeled as the example by Claude Code; `Assessment` and `User` written by Kent, reviewed, and migrated successfully — all 3 tables confirmed in the DB with correct constraints (e.g. `Assessment.application_id` unique for 1:1, `User.email` unique for login lookup). Next up: Kent writes the remaining 9 models himself — `Volunteer`, `MembershipTier`, `Event`, `Attendance`, `Role`, `Permission`, `UserRole`, `RolePermission`, `VolunteerHour` — each reviewed by Claude Code before migrating. See GitHub Issues/Projects board (not yet set up) for detailed task status going forward (Section 22 of `01_Volunteer-Ops-Platform-Spec.md` lists all tasks S1–S11, 1–15, 16–34, 35–48).

This project (Volunteer Operations Automation Platform) has its context split across two files in the project root. Read both before starting work.

See @00_AI-Context.md for Kent's background, career direction, target roles, work style, and the agreed coding/learning workflow (including the "write hard/new concepts yourself first, review-only from Claude Code" rule).

See @01_Volunteer-Ops-Platform-Spec.md for the full project specification: business problem, objectives, stakeholders, scope, functional/non-functional requirements, domain model, source of truth, architecture, integration consistency model, testing standard, CI/CD requirement, AI (Operations Copilot) architecture and evaluation criteria, and success criteria.

## Progress tracking (decided 2026-08-30)
- **GitHub Issues + Projects** is the source of truth for task status — no separate tool (Notion/Trello). One Issue per task from `01_Volunteer-Ops-Platform-Spec.md` Section 22 (S1–S11, 1–15, 16–34, 35–48). A Kanban board (To Do / In Progress / Done) with a Milestone per version (V1/V2/V3).
- Branch/commit convention: one branch per task (e.g. `feature/08-jwt-auth`), commit messages reference the task number, `closes #N` to auto-close Issues on merge. Keep this lightweight — no heavier commit convention is needed at this project's scale.
- **Timebox rule**: if a task marked "High" difficulty in Section 22 runs 1.5x over its estimated time, stop and reassess (return to this chat or use Claude Code's Plan Mode) rather than continuing to push through — treat this as a signal to question the design, not personal ability.
- Review cadence: a weekly glance at the GitHub Projects board (closed Issues this week) is enough — deliberately not more elaborate than this, given the standing risk of over-investing in process/planning at the expense of actually building (see `00_AI-Context.md` Section 3 on Deliberative/Analytical tendencies).
- AI-side memory (this file, Claude.ai memory, Claude Code sessions) is not the record of what's done — it can drift or age out. Git history and GitHub Issues are the authoritative record; the "Current Status" line above is just a quick-orientation pointer, not a source of truth.

## Working rules for this session

- Treat the completion-criteria tables in `01_Volunteer-Ops-Platform-Spec.md` (Section 19) as the current target for whichever version (V1/V2/V3) is in progress. Don't add scope beyond what's listed there without flagging it first.
- Follow the coding/learning workflow in `00_AI-Context.md`: for new/hard-concept tasks (auth, RBAC, idempotency, tool calling, etc.), wait for Kent to attempt the code himself first, then review and point out issues rather than rewriting it outright. For repetitive/pattern-established tasks (e.g. additional CRUD endpoints once a pattern exists), implementing directly is fine.
- Do not use full auto-accept / skip-permissions behavior on this project — Kent reviews each diff manually.
- Keep the "actual ISLA experience vs. self-built prototype" distinction in mind for any comments, docstrings, or README content — never phrase things as if ISLA deployed this.
- If a design decision meaningfully changes something documented in the spec file (e.g. the integration consistency model, the domain model, scope), flag it explicitly so Kent can decide whether to update `01_Volunteer-Ops-Platform-Spec.md`.

## Session management (how Kent works across sessions)

- **Continuing same-day work**: `claude --continue` resumes the most recent conversation in this project with full history and file awareness — no need to re-explain or re-feed the md files.
- **Switching topics/versions** (e.g. moving from V1 to V2, or the conversation is getting long/unfocused): use `/clear` to reset. This drops the conversation history, but `CLAUDE.md` (and its imports) is read fresh automatically on the next message, so project context is not lost — only the specific back-and-forth is.
- **Long single session**: if context is getting large, use `/compact` to condense before it forces a reset.
- **Multiple past sessions / switching projects**: `claude --resume` opens a picker of past sessions to choose from.
- **The 5-hour usage window** (Pro/Max plan limit) is a separate thing from conversation/session continuity — hitting it doesn't erase the conversation; resume normally once it resets.
- **Important**: Claude Code conversation history is not a permanent record (it can age out over time). Any design decision worth remembering long-term should be written into `CLAUDE.md` or `01_Volunteer-Ops-Platform-Spec.md` directly, not left to live only in past session history.

## Model selection (decided 2026-08-30)

Default to **`/model opusplan`**: Opus is used automatically during Plan Mode, and it switches to Sonnet for execution. This maps directly onto the agreed coding/learning workflow:
- **Design discussion / code review step** (Plan Mode, Opus): the "write it yourself first, then have Claude Code review only" step for new/hard concepts — Opus's stronger reasoning is worth it here since this is where catching subtle mistakes matters most.
- **Implementation step** (Sonnet): repetitive/pattern-established tasks, and writing out code once a design is agreed.
- If Opus access isn't available on the current plan (Pro plan may restrict it — check with `/status`), fall back to plain `sonnet` for both steps rather than skipping the review step.
- `haiku` is fine as a manual override for trivial, low-stakes tasks (e.g. boilerplate that doesn't need review) but is not the default.
