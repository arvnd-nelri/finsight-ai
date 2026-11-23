<!-- PROGRESS.md — current milestone and next tasks -->

# FinSight AI — Progress Tracker

## At a Glance

| | |
| --- | --- |
| **Current milestone** | 1 of 8 — Project Setup |
| **Status** | In progress |
| **Next step** | Initialize Git and `.gitignore` |
| **Blockers** | None |
| **Last updated** | November 22, 2026 |

## Milestone Overview

| # | Milestone | Status |
| --- | --- | --- |
| 1 | Project Setup | In progress |
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
| 1.4 | Python virtual environment | Partly done | `.venv` exists (Python 3.14.0). No packages installed yet and no dependency file (e.g. `requirements.txt`) |
| 1.5 | Git and `.gitignore` | Not started | Folder is not a Git repository yet |
| 1.6 | Basic project structure | Not started | Only `docs/` and `scripts/` exist; no source or test folders yet |
| 1.7 | Basic test setup | Not started | e.g. pytest with one passing test |
| 1.8 | Notion knowledge base | Done | Overview on the `finsight-ai` page + "Milestone 1 — Project Setup" page, per `docs/NOTION.md`. Kept current as work continues |
| 1.9 | Automatic Notion sync | Done | Rule in `CLAUDE.md` + hooks in `.claude/settings.json` (`.claude/hooks/notion-sync.sh`). Notion read/write tools pre-approved; delete/move still ask |

### Recommended Order for Remaining Work

1. **Git + `.gitignore`.** Protects the work done so far. Ignore `.venv/`,
   `.DS_Store`, secret/env files, and `.claude/.notion-pending`.
2. **Project structure.** Create source and test folders.
3. **Dependencies + test setup.** Add a dependency file and one passing test
   to prove the environment works.

---

## Progress History

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

### November 21, 2026
- Created the four documentation files and moved them into `docs/`.
- Verified the Notion MCP connection by creating four child pages under
  `finsight-ai`. These pages are copies of local files and will be replaced.

### Before November 21, 2026
- Created the `finsight-ai` project folder and the first `CLAUDE.md`.
- Created `.venv` and `scripts/start-notion-mcp.sh` (November 20).
