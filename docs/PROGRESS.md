<!-- PROGRESS.md — current milestone and next tasks -->

# FinSight AI — Progress Tracker

## At a Glance

| | |
| --- | --- |
| **Current milestone** | 2 of 8 — Financial Data Collection & Database |
| **Status** | In progress |
| **Next step** | Task 2.4: clean annual data for Microsoft, driven by the metric catalog |
| **Blockers** | None |
| **Last updated** | November 25, 2026 |

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
| 2.3 | Choose the 3 metrics and their XBRL tags | Done | Revenue = 3 tags (see D008), `NetIncomeLoss`, `OperatingIncomeLoss`. Restatement policy: keep all versions, default latest annual report (D008) |
| 2.3b | Build the metric catalog | Done | 40 metrics in `src/finsight/catalog/metrics.toml` (D010, D011, D012), measured across 2,057 large non-financial companies and spot-checked on 15 companies' own 10-Ks (results below). Re-runnable with `scripts/check_catalog_coverage.py` (`finsight.catalog.coverage`, frames download in `finsight.ingestion.sec`); 70 tests pass |
| 2.4 | Clean annual data | Not started | Driven by the metric catalog; applies the cleaning rules below; derive periods from `start`/`end` |
| 2.4q | Clean quarterly data | Not started | Quarterly rules below, including derived Q4; database designed for both annual and quarterly from the start |
| 2.5 | Load into DuckDB | Not started | DuckDB is still a candidate; confirm and record in `DECISIONS.md` |
| 2.6 | Validate values against the real 10-K | Not started | Manual check against the filing |
| 2.7 | Basic SQL queries | Not started | e.g. revenue by fiscal year |
| 2.8 | Add Apple | Not started | Tests that the pipeline is not Microsoft-specific (different fiscal year-end) |
| 2.9 | Decide the final company list | Not started | Based on real effort per company after 2.8; current lean: about 10 companies across industries |

### Agreed So Far

- **Fetch approach:** call the SEC API directly with httpx (D007).
- **Restatements:** keep every version, default to the latest annual report (D008).
- **Building blocks, not just a few metrics:** store a complete set of basic
  metrics for every company so any ratio or comparison a user asks for can be
  computed from them. Use our own metric names, never raw tags, in the
  database and in tests. Derived values are labelled and keep their inputs'
  sources. (Agreed Nov 25; recorded as D012.)
- **Annual and quarterly:** the same building blocks serve both; only the
  period differs. Each catalog metric records whether it is a period total
  (duration) or a snapshot (instant) and whether it can be subtracted
  (EPS and share counts cannot). (Agreed Nov 25.)
- **SEC access rules:** a User-Agent with name and email on every request
  (stored outside the repo, never committed), at most 10 requests per
  second, download once and reuse the raw copy.
- **Company scope:** decide at the end of Milestone 2 (task 2.9), once
  Microsoft and Apple show the real cost per company. The user and Claude
  decide the list together then; the user may bring their own picks.
  Starting shortlist: the 15 spot-checked companies (Nov 25). Two groups: the
  coverage check looks at all SEC filers (counts only, nothing stored);
  our database holds about 10 chosen companies.
- **Non-financial companies first** (D009). Banks and insurers are a later
  extension that needs about 8 bank-specific metrics. (Agreed Nov 25.)
- **Draft catalog: 40 metrics** (agreed Nov 25; final list after the
  coverage check). Chosen from what 10-K/10-Q readers ask (PROJECT.md,
  section 3). The 15 → 40 expansion adds the items marked + (25 new).

### Draft Metric Catalog (40, proposed)

| Statement | Metrics |
| --- | --- |
| Income (14) | revenue, cost of revenue, gross profit, R&D, +SG&A, operating income, +interest expense, +pretax income, +income tax, net income, +basic EPS, diluted EPS, +basic shares, diluted shares |
| Balance sheet (16) | cash, +short-term investments, +accounts receivable, +inventory, +current assets, +PP&E (net), +goodwill, +intangible assets, total assets, +accounts payable, +current liabilities, +short-term debt, long-term debt, +lease liabilities, total liabilities, total equity |
| Cash flow (10) | operating cash flow, +investing cash flow, +financing cash flow, capex, +depreciation & amortization, +stock-based compensation, +dividends paid, +dividends per share, +share buybacks, +acquisitions paid |

Why, by reader: investors (growth, margins, EPS, free cash flow, ROE,
shareholder returns); lenders (current/quick ratio, net debt, interest
coverage, lease liabilities); acquirers and competitors (R&D intensity,
goodwill, intangibles, acquisitions paid).

Not covered by the catalog: segment figures (e.g. Azure) and "why"
questions come from the filing text (Milestone 4, RAG); stock price and
valuation (P/E) are not in SEC filings (out of scope). FinSight AI is a
research assistant with cited sources, not a replacement for reading the
filing. FinanceBench (a public 10-K question set) is a candidate for
Milestone 6 evaluation.

### Coverage Survey, First Pass (Nov 25, 2026)

SEC frames API, 81 requests (77 candidate tags + 4 financial flags); raw
frames saved unchanged in `data/raw/sec/frames/`. Annual items: `CY2025`;
balance-sheet items: `CY2025Q4I`. Coverage = share of companies reporting
at least one candidate tag. Universe: 6,241 companies reporting `Assets`;
713 flagged as banks/insurers by a tag heuristic (approximation); measured
on the 2,193 non-financial companies with assets ≥ $1B. Survey script is
exploration code in the session scratchpad; it becomes a project script
when the catalog file is built.

- **Good (≥ 80%), 21 metrics:** revenue 86.1, pretax income 82.0, income
  tax 87.0, net income 89.4, EPS and share counts 83.9–85.5, cash 93.2,
  current assets 80.3, PP&E 82.1, total assets 100, current liabilities
  80.3, lease liabilities 83.5, total liabilities 80.7 (99.3 with the
  formula liabilities-and-equity − equity), total equity 96.5, operating /
  investing / financing cash flow 93.9 / 89.0 / 93.8, D&A 86.3,
  stock-based compensation 82.1.
- **Low because many companies don't have the item (expected), 9:** R&D
  36.3, inventory 53.6, short-term investments 23.8, goodwill 72.4,
  intangibles 71.4, dividends paid 51.4, dividends per share 41.8,
  buybacks 58.7, acquisitions 43.9.
- **Low because of other tag names (needs work), 10:** cost of revenue
  53.1, gross profit 38.5, SG&A 44.2, interest expense 36.8, operating
  income 75.7, receivables 69.9, payables 66.1, short-term debt 59.8,
  long-term debt 61.3, capex 73.0.
- **Our first two companies:** Microsoft has no single SG&A tag (reports
  sales & marketing and G&A separately) and no acquisitions tag in
  CY2025; Apple has no interest-expense, goodwill, intangibles, lease, or
  acquisitions tag in these frames.
- **Limits:** about 4–7% of companies fall outside a single calendar frame
  (fiscal-year timing), so no metric reaches 100% this way; frames cannot
  tell "doesn't have it" from "uses another name"; custom tags are invisible.

### Coverage Survey, Second Pass (Nov 25, 2026)

- **Filter tightened:** funds, lenders, and brokers (BlackRock, Interactive
  Brokers, Annaly, a gold trust, captive-finance arms) leaked through the
  first filter. Added 3 flag tags (one, `PayablesToCustomers`, later
  turned out to have no 2025 data and was dropped); universe 2,193 → 2,057.
- **Alternatives measured** with frames (34 extra tags), then the own files
  of 12 large companies checked (Amazon, Alphabet, Apple, NVIDIA, J&J,
  Exxon, Oracle, Pfizer, IBM, AT&T, Deere, Microsoft).
- **Frames API gap found:** across those 12, 461 of 466 expected frame
  entries matched; all 5 misses were `InterestExpenseNonoperating` CY2025
  (Amazon, Alphabet, NVIDIA, J&J, AT&T). Interest-expense coverage is
  therefore understated. The pipeline reads company files, so it is not
  affected.
- **Added (same meaning only, D011):** cost-of-revenue excl. D&A, interest
  and debt expense, operating interest expense, trade payables, capital
  improvements; formulas gross profit = revenue − cost of revenue, SG&A =
  S&M + G&A, long-term debt = total − current. Rejected broader tags
  (payables incl. accrued liabilities, net interest, receivables incl.
  notes) and costs-and-expenses as an operating-income substitute.
- **Marked may be absent:** cost of revenue and gross profit (single-step
  income statements: Exxon, AT&T, Oracle, Deere), operating income (not
  presented by J&J, Pfizer, IBM, Exxon), SG&A, interest expense (Apple
  does not disclose it separately), short- and long-term debt.
- **Result (2,057 companies, tag or formula):** every metric that should
  always exist is now ≥ 74% (receivables 74.0, payables 79.2, all others
  ≥ 80; total liabilities 97.9 with its formula). Gross profit 40.8 → 64.0
  and SG&A 47.0 → 60.7 thanks to formulas. Numbers per metric are in
  `metrics.toml`.

### Company Spot-Check (Nov 25, 2026)

Checked all 40 metrics in the latest 10-K of 15 companies' own files
(Walmart, Costco, Nike, Microsoft, Apple, Amazon, Alphabet, NVIDIA, Oracle,
IBM, J&J, Pfizer, Exxon, AT&T, Deere). Found per company: 30–39 of 40;
most gaps are genuine (no R&D at retailers, no dividends at Amazon, no
goodwill at Apple, no operating-income line at J&J/Pfizer/IBM).

- **Formula bug fixed:** total liabilities = (liabilities + equity) −
  parent-only equity overstated companies with minority owners (Walmart:
  by $6.3B). `formula` became an ordered `formulas` list; equity including
  minority owners is subtracted first. Temporary equity (Walmart: $0.3B)
  stays inside the result; documented in the catalog.
- **Added:** pretax = domestic + foreign (Oracle), long-term debt = total
  debt − current debt (Oracle), `InventoryFinishedGoodsNetOfReserves`
  (Nike's whole inventory), `AccountsReceivableNet` (Deere's unclassified
  balance sheet).
- **Known limits:** company facts contain only standard taxonomies (`dei`,
  `ecd`, `ffd`, `invest`, `srt`, `us-gaap`), so company-made custom tags are
  invisible (Deere's PP&E). Deere's balance sheet is unclassified (no
  current assets/liabilities). Exxon reports basic shares only and no
  stock-based-compensation line in its cash flow.
- **To check in 2.4:** warn when `InventoryFinishedGoodsNetOfReserves` is
  used while other inventory parts (raw materials, work in process) exist.

### Cleaning Rules for Task 2.4

From task 2.2 findings plus extra checks on Nov 25:

1. Derive each period from `start`/`end`; never from `fy`/`fp`.
2. Annual = duration of 350–380 days (Microsoft has 365 and 366; 52/53-week
   years such as Apple's give 364 or 371).
3. Keep only annual-report forms: `10-K` and `10-K/A`.
4. Keep only `USD` values; report anything else.
5. Map tags to metrics (revenue = 3 tags, D008).
6. One row per company, metric, period, and filing; default = latest filed (D008).
7. Keep negative values (losses are real data).
8. Report, don't silently fix: same-filing conflicts, missing years,
   periods with several start dates, filings dated before the period end.

**Quarterly rules (task 2.4q):**

- Q1–Q3: use the 3-month value; if only year-to-date is reported, subtract
  (Q2 = 6-month − Q1, Q3 = 9-month − 6-month).
- Q4 = annual (10-K) − 9-month year-to-date (10-Q), labelled derived, both
  sources kept.
- Snapshot (balance-sheet) items: use the quarter-end value directly.
- Never subtract per-share values or share counts; Q4 EPS only where
  reported, otherwise "not available".
- Store fiscal quarter and real dates (Microsoft fiscal Q1 = Jul–Sep).
- Check Q1 + Q2 + Q3 + Q4 = annual wherever Q4 was reported.

Evidence (Microsoft, Nov 25): 10-Qs carry 3-, 6-, and 9-month values;
stand-alone Q4 appears in 10-Ks only through FY2020 (likely the 2021 SEC
rule change); Q4 operating cash flow is never reported stand-alone.

Extra checks on Microsoft's 967 relevant entries (of 33,058) found no unit,
conflict, start-date, gap, sign, or scale problems; the only catch was 366-day
leap years, which an exact-365 rule would have dropped.

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

### November 25, 2026
- Committed and pushed task 2.1 as `fa18a85`.
- Chose option C for restatements (D008). Task 2.3 done.
- Checked Microsoft's 967 relevant entries for hidden issues (units,
  conflicts, gaps, signs, scale): none, except 366-day leap years.
  Wrote 8 cleaning rules for task 2.4.
- Scope discussion: 3 metrics are too narrow for a graduate-level project.
  Agreed to build a metric catalog of company-neutral building blocks first
  (task 2.3b), chosen by measured coverage across all SEC filers.
- Agreed to support quarterly questions too. Checked Microsoft: no
  stand-alone Q4 after FY2020 and never for operating cash flow, so Q4 will
  be derived (annual − 9 months). Added quarterly rules and task 2.4q.
- Reviewed who reads 10-K/10-Q reports and what they ask (investors,
  lenders, acquirers/competitors; FinanceBench question types). Grew the
  draft catalog from 15 to 40 metrics to cover their common questions.
- Chose non-financial companies first; banks and insurers later (D009).
- Ran the coverage survey (81 frames requests): 21 metrics ≥ 80%, 9 low
  because the item is often absent, 10 need more tags or formulas.
- Saved the catalog in the project: `src/finsight/catalog/metrics.toml`
  + `finsight.catalog.load_catalog()` (D010), 15 new tests (44 total,
  all passing). Confirmed the file matches the surveyed draft exactly.
- Second coverage pass: tighter financial filter, 12 companies' own files
  checked, same-meaning tags and 3 formulas added (D011), formula
  validation in the loader; 54 tests pass. Found an incomplete SEC frames
  file for `InterestExpenseNonoperating`.
- Company spot-check on 15 companies (added Walmart, Costco, Nike): fixed a
  total-liabilities formula bug (minority owners), added ordered formula
  lists and 4 same-meaning fixes; 56 tests pass. Custom tags confirmed
  invisible in company facts.
- Turned the survey into project code: `download_frame()` / `load_frame()`
  in `finsight.ingestion.sec` (404s recorded in metadata only),
  `finsight.catalog.coverage`, and `scripts/check_catalog_coverage.py`
  (`--companies`, `--year`, `--refresh`). Re-downloaded all 94 frames with
  metadata (38 s); results identical to the exploration. Removed 38
  exploration files without provenance. 70 tests pass. Task 2.3b done.

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
