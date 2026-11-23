<!-- DECISIONS.md — why we chose each technology -->

# FinSight AI — Technical Decisions

This document records important
project decisions and their reasons.

## Decision Log

### D001 — Incremental Development

Date: November 21, 2026

Decision:
Build FinSight AI incrementally,
following the eight project milestones.

Reason:
Focus on small working features,
understand each component, and avoid
unnecessary complexity.

Alternatives:
Implement the complete system upfront.

Status: Accepted

### D002 — Short CLAUDE.md, Other Docs Read on Demand

Date: November 22, 2026

Decision:
Keep `CLAUDE.md` to a short summary and rules. Read `docs/PROGRESS.md`
each session; read `PROJECT.md`, `ARCHITECTURE.md`, `DECISIONS.md`, and
`NOTION.md` only when the task needs them.

Reason:
`CLAUDE.md` loads into every session, so long content costs tokens
even on small tasks. Detail stays available when it matters.

Alternatives:
Import `PROJECT.md` into `CLAUDE.md` (~7–8k tokens every session).

Trade-offs:
The assistant must judge when a long doc is needed.

Status: Accepted

### D003 — Notion Organized by Milestone, Synced Automatically

Date: November 22, 2026

Decision:
Notion holds an overview page plus one page per milestone, written for a
human reader, not mirroring local files. It is updated in the same turn as
meaningful work, enforced by a `CLAUDE.md` rule plus a Stop hook.

Reason:
Notion should let someone understand the project well enough for
interviews without reading the code, and nothing should go undocumented.

Alternatives:
Mirror local Markdown files in Notion (tried first, dropped).
Instruction-only sync without a hook.

Trade-offs:
Each update costs tokens. The hook can only remind; content quality
still depends on the assistant.

Status: Accepted

## Future Decisions

New decisions should include:

- Date
- Decision
- Reason
- Alternatives considered
- Trade-offs
- Status
