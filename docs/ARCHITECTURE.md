<!-- ARCHITECTURE.md — how components connect -->

# FinSight AI — System Architecture

## Current Status

Project setup phase.

No application components have been
implemented yet.

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

### Current (end of Milestone 1)

```text
finsight-ai/
├── src/finsight/        Python package (the application); empty for now
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
| `src/finsight/config.py` | 1–2 | Settings loaded from env vars (no secrets in code) |
| `src/finsight/ingestion/` | 2 | Download and parse SEC EDGAR data |
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

None yet.

## Architecture Changes

Future architectural changes will be
recorded here.
