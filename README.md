# FinSight AI

An evidence-grounded financial research agent for public companies.
Ask a plain-English question about a company's financial performance and get
an answer backed by SEC data: the figures, their reporting periods and units,
and citations to the filings they came from.

Master's-level AI Engineering capstone.

> **Status:** Milestone 1 (Project Setup) is complete; Milestone 2 (data
> collection) is next. No application features are implemented yet.
> See [`docs/PROGRESS.md`](docs/PROGRESS.md).

## Planned Capabilities

- SEC EDGAR data ingestion into a financial database
- Text-to-SQL for numerical questions
- RAG over 10-K / 10-Q filings for explanations
- A tool-using agent with evidence checks
- Evaluation of accuracy, grounding, latency, and cost

## Repository Layout

```text
finsight-ai/
├── src/finsight/   application code (Python package)
├── tests/          automated tests
├── data/           local data, mostly not committed (see data/README.md)
├── scripts/        helper scripts
├── docs/           project documentation
└── pyproject.toml  package metadata, dependencies, test settings
```

## Documentation

| File | Contents |
| --- | --- |
| [`docs/PROJECT.md`](docs/PROJECT.md) | Vision, design, and 8-milestone roadmap |
| [`docs/PROGRESS.md`](docs/PROGRESS.md) | Current milestone and next steps |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Components and repository layout |
| [`docs/DECISIONS.md`](docs/DECISIONS.md) | Technical decisions and trade-offs |

## Setup

Requires Python 3.12 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"   # installs finsight in editable mode, plus pytest
pytest                    # runs the test suite
```
