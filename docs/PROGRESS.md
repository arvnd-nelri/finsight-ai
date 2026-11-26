<!-- PROGRESS.md — current milestone and next tasks -->

# FinSight AI — Progress Tracker

## At a Glance

| | |
| --- | --- |
| **Current milestone** | 2 of 8 — Financial Data Collection & Database |
| **Status** | In progress |
| **Next step** | Task 2.3/2.4: agree the metric-to-tag mapping and the restatement policy, then build the cleaning step |
| **Blockers** | None |
| **Last updated** | November 24, 2026 |

## Milestone Overview

| # | Milestone | Status |
| --- | --- | --- |
| 1 | Project Setup | Done |
| 2 | Financial Data Collection & Database | In progress |
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

---

## Milestone 2 — Financial Data Collection & Database

**Goal:** Build a trustworthy, reproducible ETL pipeline that turns SEC
EDGAR data into a database of verified financial facts, each linked to its
source filing.

**Definition of done:** a reproducible pipeline and a DuckDB database (candidate)
with verified, provenance-linked data for the initial companies; basic
analytical SQL works.

### Tasks (proposed plan; adjust as work shows what fits)

| # | Task | Status | Notes |
| --- | --- | --- | --- |
| 2.1 | Download Microsoft's raw company-facts JSON | Done | `finsight.config`, `finsight.ingestion.sec`, `scripts/download_sec_data.py`; 29 tests pass. Live run Nov 24: HTTP 200, 4,938,072 bytes, checksum re-verified, `data/raw/` git-ignored |
| 2.2 | Explore the raw JSON structure | Done | Findings below. Exploration was ad hoc (not project code); the rules it found become tested code in 2.4 |
| 2.3 | Choose the 3 metrics and their XBRL tags | Not started | Revenue, net income, operating income; tags can change over years |
| 2.4 | Clean, de-duplicate, label periods | Not started | Each 10-K repeats prior years; derive periods from `start`/`end` |
| 2.5 | Load into DuckDB | Not started | DuckDB is still a candidate; confirm and record in `DECISIONS.md` |
| 2.6 | Validate values against the real 10-K | Not started | Manual check against the filing |
| 2.7 | Basic SQL queries | Not started | e.g. revenue by fiscal year |
| 2.8 | Add Apple | Not started | Tests that the pipeline is not Microsoft-specific (different fiscal year-end) |
| 2.9 | Decide the final company list | Not started | Based on real effort per company after 2.8; current lean: about 10 companies across industries |

### Agreed So Far

- **Fetch approach:** call the SEC API directly with httpx (D007).
- **SEC access rules:** a User-Agent with name and email on every request
  (stored outside the repo, never committed), at most 10 requests per
  second, download once and reuse the raw copy.
- **Company scope:** decide at the end of Milestone 2 (task 2.9), once
  Microsoft and Apple show the real cost per company.

### Task 2.2 Findings (Microsoft, file retrieved Nov 24, 2026)

Raw SEC values below are not yet validated against the filings (task 2.6).

- **Size:** 4 taxonomies (`us-gaap` 562 concepts, `dei`, `ecd`, `ffd`),
  33,058 fact entries. Entry fields: `start`, `end`, `val`, `accn`, `fy`,
  `fp`, `form`, `filed`, `frame` (`start` absent for point-in-time facts).
- **`fy`/`fp` describe the filing, confirmed.** Of 65 annual
  `NetIncomeLoss` entries, 47 have `fy` different from the period's year.
  The first entry is a 3-month figure (Jul–Sep 2007) labelled `fy 2010, fp FY`.
- **Annual reports contain quarterly data.** 10-K entries include quarters
  and 6/9-month spans, so duration must be computed from `start`/`end`.
- **Duplicates:** up to 5 copies of the same annual period across filings.
- **Non-financial-statement forms:** values also come from `8-K`,
  `DEF 14A` (proxy) and `10-Q/A`; the latest annual `NetIncomeLoss` entry
  is from a `DEF 14A`. Filter by form.
- **Revenue tag changed twice:** `Revenues` (FY2008–FY2010),
  `SalesRevenueNet` (FY2009–FY2017),
  `RevenueFromContractWithCustomerExcludingAssessedTax` (FY2016–FY2026).
  Overlap years agree for FY2009–2010 but not FY2016–2017.
- **Restatements:** FY2016 and FY2017 net income and operating income
  differ between filings (e.g. FY2016 net income 16,798,000,000 in the FY2016
  and FY2017 10-Ks, 20,539,000,000 in the FY2018 10-K). Likely cause: the new
  revenue accounting standard (ASC 606) adopted in FY2018; confirm in 2.6.
- **`frame`:** one entry per period carries a `frame` tag (the SEC's own
  de-duplication); for restated years it marks the latest value. Its label
  is calendar-based (`CY2016`), not the fiscal year.
- **Coverage:** annual net and operating income FY2008–FY2026; latest 10-K
  filed 2026-07-29.

---

## Progress History

### November 23, 2026
- Added `pyproject.toml` (setuptools build, Python >= 3.12, pytest as a
  `dev` extra, pytest settings). No runtime dependencies yet.
- Installed the project into `.venv` in editable mode (`pip install -e ".[dev]"`).
- Added `tests/test_setup.py` with 3 setup checks; `pytest` result: 3 passed.
- Added setup instructions to `README.md`.
- Milestone 1 complete. Committed and pushed as `3f0980a`.
- Started planning Milestone 2: walked through ETL, EDGAR, XBRL, CIK, fiscal
  years, and provenance; drafted tasks 2.1–2.9; agreed to decide the
  company list after Microsoft and Apple are working.
- Chose option A with httpx (D007). Created `~/.config/finsight-ai/sec.env`
  (placeholder, outside the repo). Added `httpx` dependency, `finsight.config`,
  `finsight.ingestion.sec`, `scripts/download_sec_data.py`, and 26 tests
  (29 total, all passing, no network). Confirmed the script stops with a
  clear error while the placeholder is still in place.

### November 24, 2026
- First live SEC download (Microsoft): HTTP 200, 4.9 MB, checksum verified.
  Task 2.1 done.
- Explored the raw JSON (task 2.2): confirmed the `fy` trap, found three
  revenue tags over time, duplicate copies, non-10-K forms, and restated
  FY2016–2017 values. Findings recorded above.

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
