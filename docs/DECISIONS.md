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

### D004 — Git With a GitHub Remote Over SSH

Date: November 22, 2026

Decision:
Use Git on a single `main` branch, with a GitHub repository as the remote
(`origin`), connected over SSH. `.gitignore` is written before the first
commit and the staged files are scanned for secrets before pushing.

Reason:
Gives a full history and an off-machine backup. SSH reuses the existing
key and needs no token typed on each push.

Alternatives:
HTTPS with a personal access token. Feature branches and pull requests
(heavier than needed for a solo project at this stage).

Trade-offs:
Committing straight to `main` is simple but has no review step.
Revisit if the project gains collaborators or CI.

Status: Accepted

### D005 — src Layout, Folders Created Only When Needed

Date: November 22, 2026

Decision:
Put application code in a package at `src/finsight/`, with `tests/`,
`data/`, `scripts/`, and `docs/` alongside. Create sub-packages only when
the milestone that needs them starts; list the planned ones in
`ARCHITECTURE.md`.

Reason:
The src layout forces tests to import the installed package, which
catches packaging mistakes early. Creating folders on demand avoids empty
placeholders that guess at an architecture not yet designed.

Alternatives:
Flat layout (`finsight/` at the repo root): simpler, but tests can
silently import local files instead of the installed package.
Creating every planned folder now.

Trade-offs:
The src layout needs the package installed (`pip install -e .`) before
tests can import it.

Status: Accepted

### D006 — pyproject.toml With setuptools, pytest for Tests

Date: November 23, 2026

Decision:
Describe the project in a single `pyproject.toml`: setuptools as the build
backend, Python >= 3.12, runtime dependencies added only when a milestone
needs them, and development tools (pytest) in a `dev` optional-dependency
group. Install with `pip install -e ".[dev]"`. Use pytest for all tests.

Reason:
`pyproject.toml` is the current Python standard: one file holds metadata,
dependencies, and tool settings. setuptools is the most widely used and
documented backend. Editable install lets code changes take effect without
reinstalling. pytest is the de facto Python test tool.

Alternatives:
`requirements.txt` only (no package metadata; does not make `finsight`
importable). uv or Poetry (faster or richer, but extra tools to learn now).
hatchling backend (fine, but less familiar). unittest (built in, more verbose).

Trade-offs:
No lock file yet, so exact library versions are not pinned. Revisit
(e.g. `pip freeze` or uv) once real dependencies arrive in Milestone 2.

Status: Accepted

### D007 — Fetch SEC Data Directly With httpx

Date: November 23, 2026

Decision:
Download SEC EDGAR data by calling the `data.sec.gov` JSON API directly,
using the httpx library. Save each response unchanged in `data/raw/` with a
metadata file (source URL, UTC time, size, SHA-256). Read the required
User-Agent (name and email) from the `SEC_USER_AGENT` environment variable
or `~/.config/finsight-ai/sec.env`, never from the repository. Wait at least
0.2 s between requests (SEC limit: 10 per second).

Reason:
Direct calls keep every step visible and explainable, which is the point of
this milestone, with one small dependency. httpx has timeouts on by default
and a mock transport for network-free tests; its API mirrors `requests`.

Alternatives:
An SEC library such as `edgartools` (faster start, but hides the data
handling). Bulk `companyfacts.zip` (suits thousands of companies, overkill
for a few). `requests` instead of httpx (equally simple; no built-in mock
transport, no default timeout).

Trade-offs:
We write and maintain the parsing and cleaning logic ourselves.
Revisit the bulk download if the company list grows large.

Status: Accepted

## Future Decisions

New decisions should include:

- Date
- Decision
- Reason
- Alternatives considered
- Trade-offs
- Status
