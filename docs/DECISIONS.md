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

### D008 — Keep Every Reported Version; Default to the Latest Annual Report

Date: November 25, 2026

Decision:
Store one row per company, metric, fiscal period, and source filing, so
every reported version of a number is kept with its accession number and
filing date. The default value is the one from the most recently filed annual
report (`10-K` or `10-K/A`). Revenue is the union of three tags
(`RevenueFromContractWithCustomerExcludingAssessedTax`, `SalesRevenueNet`,
`Revenues`) under the same rule; if one filing reports the same period under
two tags, that order is the tie-break.

Reason:
Microsoft restated FY2016 and FY2017 (e.g. FY2016 net income 16,798,000,000
in the FY2016 10-K, 20,539,000,000 in the FY2018 10-K; raw SEC values, not
yet validated). The latest version uses the same accounting rules across
years, so trends compare like with like, while the kept originals let answers
say a value was restated and cite both filings.

Alternatives:
Latest value only (simpler, but loses the restatement history). Originally
reported value only (mixes accounting standards across years, so trends
mislead).

Trade-offs:
More rows and a slightly more complex schema; queries must pick the default
version explicitly.

Status: Accepted

### D009 — Non-Financial Companies First; Banks and Insurers Later

Date: November 25, 2026

Decision:
The initial company list (about 10, final at task 2.9) contains only
non-financial companies. Banks and insurers are a planned extension.

Reason:
Banks and insurers report differently (loans, deposits, interest income;
no cost of revenue or inventory), so the draft 40-metric catalog does not
fit them. One shared catalog keeps cleaning, validation, and tests simpler
while Milestone 2 is still being built.

Alternatives:
Include one bank now (wider coverage, but about 8 extra bank-specific
metrics plus their own cleaning and checks during the first data milestone).

Trade-offs:
FinSight AI cannot answer questions about banks or insurers until the
extension is built. Adding them later also tests that the catalog is easy
to extend.

Status: Accepted

### D010 — Metric Catalog as a TOML File Inside the Package

Date: November 25, 2026

Decision:
Store the metric catalog in `src/finsight/catalog/metrics.toml`, read with
Python's built-in `tomllib` and validated by `finsight.catalog.load_catalog()`.

Reason:
The catalog is data, not logic: it should be easy to read and edit like a
table, with comments for evidence. TOML is readable, supports comments, and
needs no extra dependency. Validation on load turns typos into clear errors.

Alternatives:
A Python dictionary in a module (works, but harder to read for
non-programmers and mixes data with code). YAML (similar readability, but
needs a third-party library and has surprising type rules).

Trade-offs:
TOML is read-only in the standard library; the file is edited by hand.

Status: Accepted

### D011 — Catalog Tags Must Mean the Same Thing; Gaps Use Formulas or "May Be Absent"

Date: November 25, 2026

Decision:
A tag joins a metric only if it means the same thing. Where companies
report a metric in parts, a fallback formula combines same-meaning parts
(e.g. SG&A = sales and marketing + general and administrative). Where many
companies legitimately do not report a metric (no cost-of-revenue line, no
debt), it is marked `may_be_absent` instead of being forced.

Reason:
A broader tag raises coverage but silently changes the number's meaning
(payables including accrued liabilities; net interest instead of interest
expense). A wrong number with a citation is worse than an honest gap.

Alternatives:
Accept broader tags to maximise coverage (more answers, some subtly wrong).
Accept only the single most common tag (simple, but misses Microsoft's SG&A).

Trade-offs:
Lower measured coverage for some metrics; answers say "not reported" more
often. Formulas need validation and are labelled derived.

Status: Accepted

### D012 — Store Standardized Building-Block Metrics Under Our Own Names

Date: November 25, 2026

Decision:
The database stores a fixed set of 40 building-block metrics for every
company (the metric catalog), under our own names such as `revenue` and
`total_liabilities`, never raw SEC tags. Ratios (margins, EBITDA, current
ratio) are computed from them, not stored. Each value is labelled reported,
derived (from a formula), not applicable, or missing, and keeps its source.

Reason:
Companies tag the same item differently and change tags over time, so raw
tags cannot be compared across companies or years. Forty metrics chosen
from what 10-K/10-Q readers ask cover most numeric questions; explanations
and segment figures come from the filing text (Milestone 4).

Alternatives:
A few metrics only (too narrow for a graduate project). Every tag a company
reports (thousands, inconsistent across companies, hard for Text-to-SQL).

Trade-offs:
The catalog needs maintenance as the taxonomy changes; custom tags are
invisible in company facts; banks and insurers need their own set (D009).

Status: Accepted

## Future Decisions

New decisions should include:

- Date
- Decision
- Reason
- Alternatives considered
- Trade-offs
- Status
