<!-- ARCHITECTURE.md — how components connect -->

# FinSight AI — System Architecture

## Current Status

Milestone 2 in progress. The first ingestion component (raw SEC
download) is implemented; nothing downstream of it exists yet.

## Planned High-Level System

```
User
  |
  v
AI Financial Agent
  |
  +-- SQL Tool --> Financial Database
  |
  +-- RAG Tool --> SEC Financial Reports
  |
  v
Evidence Verification
  |
  v
Final Answer
```

This is a proposed architecture.
It may change during implementation.

## Technologies

Technology selections will be documented
as they are introduced and confirmed.

## Repository Layout

The project uses the **src layout**: application code lives in a Python
package under `src/`, separate from tests, data, and docs.

### Current

```text
finsight-ai/
├── src/finsight/        Python package (the application)
│   ├── config.py        settings from env vars / ~/.config/finsight-ai/
│   ├── catalog/         metric catalog: metrics.toml, loader, coverage checks
│   └── ingestion/sec.py SEC EDGAR client and raw company-facts download
├── tests/               pytest tests, mirroring src/finsight/
├── data/                local data; raw/ and processed/ are git-ignored
├── scripts/             helper scripts (e.g. start-notion-mcp.sh)
├── docs/                project documentation
├── .claude/             Claude Code hooks and settings
├── CLAUDE.md            instructions for the coding assistant
├── README.md            project overview and setup steps
└── pyproject.toml       package metadata, dependencies, pytest settings
```

### Planned growth (proposal; created only when each milestone starts)

| Path | Milestone | Purpose |
| --- | --- | --- |
| `src/finsight/ingestion/` (more modules) | 2 | Parse and normalize SEC data |
| `src/finsight/db/` | 2 | Database schema, loading, read-only queries |
| `src/finsight/sql/` | 3 | Text-to-SQL: schema context, generation, validation |
| `src/finsight/rag/` | 4 | Filing text chunking, indexing, retrieval |
| `src/finsight/agent/` | 5 | Tool orchestration and evidence checks |
| `src/finsight/app/` | 3+ | User interface (e.g. Streamlit) |
| `evals/` | 6 | Evaluation questions, gold answers, results |
| `notebooks/` | as needed | Exploration only; real logic moves into `src/` |

Names and boundaries may change once real code shows what fits.

### Placement rules

- Reusable logic goes in `src/finsight/`, never only in a notebook or script.
- `scripts/` holds thin entry points that call code in `src/finsight/`.
- Each module in `src/finsight/` gets matching tests in `tests/`.
- Downloaded or generated data goes in `data/`, never committed.

## Implemented Components

### Raw SEC download (Milestone 2, task 2.1)

```text
scripts/download_sec_data.py  (thin CLI: CIKs in, file paths out)
        |
        |-- finsight.config.get_sec_user_agent()
        |       env var SEC_USER_AGENT, else ~/.config/finsight-ai/sec.env
        |
        v
finsight.ingestion.sec
  SecClient            httpx client: User-Agent header, 30 s timeout,
                       min 0.2 s between requests (SEC limit: 10/s)
  download_company_facts(cik)
        GET https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json
        check: valid JSON, response CIK == requested CIK
        save:  data/raw/sec/companyfacts/CIK##########.json (unchanged)
               + .meta.json (source URL, UTC time, status, size, SHA-256)
        skip if already downloaded (unless --force)
```

Tests use `httpx.MockTransport`, so they never call the real SEC.

### Metric catalog (Milestone 2, task 2.3b)

```text
src/finsight/catalog/metrics.toml   40 metrics: our name -> label, statement,
                                    period type, unit, subtractable,
                                    may_be_absent, us-gaap tags (priority
                                    order), fallback formulas (ordered),
                                    coverage_pct
finsight.catalog.load_catalog()     reads the file, validates every entry
                                    and formula (CatalogError on a bad
                                    one), returns {name: Metric}
finsight.catalog.formula_terms()    "a - B + c" -> [(+1,a), (-1,B), (+1,c)]
```

```text
scripts/check_catalog_coverage.py  [--companies CIK ...] [--year] [--refresh]
        |
        |-- finsight.ingestion.sec.download_frame(tag, unit, period)
        |       GET https://data.sec.gov/api/xbrl/frames/us-gaap/{tag}/{unit}/{period}.json
        |       save: data/raw/sec/frames/us-gaap_{tag}_{unit}_{period}.json + .meta.json
        |       404 (no data): recorded in .meta.json only, returns None
        |
        v
finsight.catalog.coverage
  comparison_group()   non-financial companies (tag heuristics), assets >= $1B
  metric_coverage()    per metric: companies found by a tag / by tag or formula
  company_status()     one company's latest 10-K: tag / formula / missing
```

The catalog is the single list of what the pipeline collects. The cleaning
step (2.4) will read it to map raw tags to our metric names; nothing
reads it yet besides the tests and the coverage survey.

## Architecture Changes

Future architectural changes will be
recorded here.
