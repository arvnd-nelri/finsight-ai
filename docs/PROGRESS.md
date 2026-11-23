<!-- PROGRESS.md — current milestone and next tasks -->

# FinSight AI — Progress Tracker

## At a Glance

| | |
| --- | --- |
| **Current milestone** | 2 of 8 — Financial Data Collection & Database (not started) |
| **Status** | Milestone 1 complete |
| **Next step** | Commit and push the Milestone 1 work, then plan Milestone 2's first step (fetch Microsoft's SEC data) |
| **Blockers** | None |
| **Last updated** | November 23, 2026 |

## Milestone Overview

| # | Milestone | Status |
| --- | --- | --- |
| 1 | Project Setup | Done |
| 2 | Financial Data Collection & Database | Not started |
| 3 | Text-to-SQL | Not started |
| 4 | RAG over SEC Filings | Not started |
| 5 | AI Agent & Evidence Verification | Not started |
| 6 | Evaluation & Improvement | Not started |
| 7 | Fine-Tuning & Model Comparison (optional) | Not started |
| 8 | Deployment & Presentation | Not started |

---

## Milestone 1 — Project Setup

**Goal:** Get a working development environment, an organized repository, and a
documentation system in place, so that every later milestone starts on a solid
foundation.

**Definition of done:** the environment runs, the project files are organized,
documentation can be updated locally and in Notion, and setup checks have
passed. No financial features are needed to finish this milestone.

### Tasks

| # | Task | Status | Notes |
| --- | --- | --- | --- |
| 1.1 | Claude Code working in VS Code | Done | Used through the VS Code extension to read and edit project files |
| 1.2 | Local documentation set up | Done | `docs/` holds PROJECT, PROGRESS, ARCHITECTURE, DECISIONS, NOTION; `CLAUDE.md` defines when to read and update each |
| 1.3 | Notion MCP connection | Done | Claude Code read the `finsight-ai` page and created/edited child pages. Launched by `scripts/start-notion-mcp.sh`; the token is loaded from `~/.config/finsight-ai/notion.env`, outside the repo |
| 1.4 | Python virtual environment | Done | `.venv` (Python 3.14.0). Dependencies declared in `pyproject.toml`; project installed with `pip install -e ".[dev]"` |
| 1.5 | Git and `.gitignore` | Done | Repository on branch `main`, remote `origin` = `git@github.com:arvnd-nelri/finsight-ai.git` (SSH). First commit pushed. `.gitignore` excludes `.venv/`, secrets, `.DS_Store`, `.claude/.notion-pending` |
| 1.6 | Basic project structure | Done | src layout: `src/finsight/`, `tests/`, `data/` (raw/processed git-ignored), root `README.md`. Planned growth listed in `docs/ARCHITECTURE.md` |
| 1.7 | Basic test setup | Done | pytest 9.2.0, configured in `pyproject.toml`. `tests/test_setup.py`: 3 setup checks (import, installed, loads from `src/`), all passing |
| 1.8 | Notion knowledge base | Done | Overview on the `finsight-ai` page + "Milestone 1 — Project Setup" page, per `docs/NOTION.md`. Kept current as work continues |
| 1.9 | Automatic Notion sync | Done | Rule in `CLAUDE.md` + hooks in `.claude/settings.json` (`.claude/hooks/notion-sync.sh`). Notion read/write tools pre-approved; delete/move still ask |

**Milestone 1 is complete:** the definition of done is met (environment
runs, files organized, docs updated locally and in Notion, setup checks pass).

### Recommended Next Steps

1. **Commit and push** the Milestone 1 work (structure, `pyproject.toml`,
   tests, doc updates) as one commit.
2. **Start Milestone 2** (plan, not yet started): read the Milestone 2
   section of `docs/PROJECT.md`, then take the first small step: fetch
   Microsoft's SEC company-facts data and save the raw response in
   `data/raw/`.

---

## Progress History

### November 23, 2026
- Added `pyproject.toml` (setuptools build, Python >= 3.12, pytest as a
  `dev` extra, pytest settings). No runtime dependencies yet.
- Installed the project into `.venv` in editable mode (`pip install -e ".[dev]"`).
- Added `tests/test_setup.py` with 3 setup checks; `pytest` result: 3 passed.
- Added setup instructions to `README.md`.
- Milestone 1 complete.

### November 22, 2026
- Expanded `docs/PROJECT.md` into the full project vision (15 sections).
- Added `docs/NOTION.md`: how Notion is structured (by milestone),
  what "synchronized" means, and design and formatting rules.
- Rewrote `CLAUDE.md` to be short: a project summary, what to read when,
  and when to update each doc. Detailed content now lives only in `docs/`.
- Reviewed actual setup state: found an existing `.venv` and
  `scripts/start-notion-mcp.sh`; confirmed Git is not initialized.
- Cleared the `finsight-ai` Notion page: moved all five child pages
  (Documentation Setup Test, Project Plan, Progress, Architecture,
  Decisions) to Notion trash, to start fresh with the milestone layout.
- Set up automatic Notion sync: `CLAUDE.md` rule, PostToolUse + Stop hooks,
  Notion tool permissions. Hook script pipe-tested (6 cases) and confirmed
  firing live on a real edit.
- Built the Notion knowledge base: project overview on the main page and
  the "Milestone 1 — Project Setup" page.
- Set up Git: wrote `.gitignore`, ran `git init -b main`, scanned the staged
  files for secrets (none), made the first commit (10 files), linked the
  GitHub remote over SSH, and pushed `main`.
- Created the base project structure (src layout): `src/finsight/`,
  `tests/`, `data/` with a README, and a root `README.md`. Documented the
  current layout, planned growth, and placement rules in `ARCHITECTURE.md`.

### November 21, 2026
- Created the four documentation files and moved them into `docs/`.
- Verified the Notion MCP connection by creating four child pages under
  `finsight-ai`. These pages are copies of local files and will be replaced.

### Before November 21, 2026
- Created the `finsight-ai` project folder and the first `CLAUDE.md`.
- Created `.venv` and `scripts/start-notion-mcp.sh` (November 20).
