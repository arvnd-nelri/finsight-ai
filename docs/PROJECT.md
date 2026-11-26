<!-- PROJECT.md — full 8-milestone vision for FinSight AI: the main file for understanding what the project is, why it exists, and where it is going -->

# FinSight AI
## Project context, vision, and development direction

| | |
| --- | --- |
| **Project type** | Master's-level AI Engineering capstone |
| **Working description** | An evidence-grounded financial research and analytics agent for public companies |
| **Primary domain** | Company financial performance and SEC filings |
| **Status** | Milestone 1 (Project setup) in progress. See `docs/PROGRESS.md` for the latest verified state |
| **Target** | A demonstrable, rigorously evaluated project by the end of winter break, with advanced extensions as time and resources allow |
| **Last updated** | November 22, 2026 |

> **How to read this document:** This is the project's comprehensive context and current direction, not a fixed specification or a second set of coding rules. It records the problem, motivation, intended capabilities, likely architecture, development sequence, and important uncertainties. Some components, tools, milestones, and priorities may change based on experiments, feasibility, and new information. Treat proposals as proposals, not as completed implementations or irrevocable decisions. `CLAUDE.md` describes how the coding assistant should work; this document explains what the project is and why it exists.

## Contents

1. Executive summary
2. Why build this?
3. Intended users and example questions
4. What the user experience may look like
5. Data sources and the financial domain
6. Proposed technical design
7. Current technology direction and reasons
8. Development roadmap (8 milestones)
9. Evaluation and research contribution
10. Quality, safety, and responsible use
11. Working approach, learning, and resources
12. Documentation and project continuity
13. Known project state
14. Open choices and likely future evolution
15. What success looks like

## 1. Executive summary

FinSight AI aims to let someone ask plain-English questions about the financial performance of public companies and receive understandable, checkable answers grounded in primary financial evidence. It will work with two kinds of information:

1. **Structured financial facts:** Numbers such as revenue, net income, operating income, operating expenses, and reported segment results, including the reporting periods and units attached to those numbers.
2. **Unstructured filing text:** Management discussion, explanations of performance, business descriptions, and risk disclosures from SEC filings such as Form 10-K and Form 10-Q.

The envisioned system will combine reliable financial data ingestion, a database, natural-language-to-SQL analysis, retrieval over filing text (RAG), and an AI agent that selects the right tools for a question. It should be able to cite where the data came from, distinguish evidence from inference, and say when information is insufficient.

The engineering and research contribution goes beyond a financial chatbot: the project will evaluate answer quality, source grounding, robustness, latency, and cost; investigate common failures; and compare approaches. Fine-tuning an open model is a desirable **advanced extension**, not a prerequisite for a strong working capstone.

## 2. Why build this?

Financial questions are often easy to ask but time-consuming to answer correctly. A person may need to find filings, locate the appropriate values, understand financial periods, write queries, compute ratios, compare companies, read management commentary, and verify the source of each statement. Generic LLM responses can sound convincing while using outdated numbers, mixing fiscal periods, or inventing explanations.

FinSight AI explores how a tool-using language-model system can make financial research more accessible **without giving up traceability or evaluation**. The project is also intended to demonstrate skills relevant to AI Engineer, ML Engineer, Applied AI, LLM Engineer, GenAI Engineer, and NLP-related roles: data pipelines, SQL, retrieval, tool calling, agent orchestration, evaluation, model adaptation, APIs, and deployment.

The financial domain provides real constraints and an interesting combination of numerical reasoning and document understanding. The goal is to develop transferable AI engineering skills, not to claim that a finance-specific project guarantees a finance-industry job.

## 3. Intended users and example questions

Potential users include students, researchers, business analysts, and professionals who want to explore publicly reported company performance. The initial application is a research and analysis aid, not an investment advisor or a system for autonomous trading.

The people who actually read 10-K and 10-Q reports, and what they look for (reviewed November 25, 2026):

- **Investors and equity analysts:** growth, profitability, earnings per share, cash generation, shareholder returns, comparisons between companies.
- **Lenders and credit analysts:** liquidity, debt, interest coverage, lease obligations.
- **Acquirers, competitors, and regulators:** the business, risks, R&D, acquisitions, goodwill, accounting.

FinSight AI serves them as a fast research assistant: an answer with its source in seconds, instead of searching a 100+ page filing. It does not replace careful reading for important decisions; the cited sources let users check each answer. This list of readers drives the metric catalog (Milestone 2, task 2.3b).

### Questions about financial numbers (structured analysis)

- How did Microsoft's revenue change from fiscal 2021 through fiscal 2025?
- What is the year-over-year growth in a company's net income?
- Compare Apple's and Microsoft's operating margins for specified fiscal years.
- Did a company's reported operating expenses grow faster than its revenue?
- What were the reported revenues of different business segments, when consistently available?

### Questions about management explanations (document analysis)

- What reasons did management give for revenue growth in a particular annual filing?
- Which risks were emphasized in the company's Form 10-K?
- How did the discussion of a specific risk change between two annual filings?

### Questions needing both kinds of evidence (combined analysis)

- Revenue grew by a given percentage. What explanation did the company provide in its filing?
- Compare two companies' reported profitability trends and summarize each management team's relevant commentary.
- Which reported business segments drove a change in revenue, and where is that described?

Answers should show the figures, periods, units, and source filings used. Claims about *why* a number changed should be attributed to the filing or explicitly presented as a limited interpretation, not asserted as proven causation. Cross-company comparisons should identify differences in fiscal year-ends, definitions, and availability.

## 4. What the user experience may look like

A simple web interface could accept a question in ordinary English and return:

- A direct explanation written for a non-specialist.
- Financial figures or a table/chart when numerical analysis is needed.
- The reporting period, calculation, and assumptions behind each metric.
- Links or references to the underlying SEC facts and filing passages.
- A clear indication when a question is ambiguous, data is missing, or the sources do not support a confident answer.

For learning and debugging, an expandable panel could show the SQL query, retrieved filing passages, selected tools, and evidence checks. The initial user interface can be simple; correctness and provenance matter more than visual polish.

**Important:** Any mockup or sample number is illustrative until retrieved and validated from a real filing. Never present illustrative values as company facts.

## 5. Data sources and the financial domain

### Primary source: SEC EDGAR

The initial plan is to use official U.S. Securities and Exchange Commission (SEC) EDGAR data, including:

- **Form 10-K:** Annual reports with financial statements, management discussion, and risk disclosures.
- **Form 10-Q:** Quarterly reports for more recent periods.
- **XBRL/company facts:** Machine-readable tagged financial concepts made available through SEC data services.
- **Filing metadata:** Company identifiers, form types, accession identifiers, filing dates, report periods, and references needed for provenance.

Initial candidates are **Microsoft**, followed by **Apple**, with additional companies added after the pipeline works reliably. This is a practical starting choice, not a permanent domain restriction.

The planned approach is to begin with a small, well-verified set of financial facts and filings rather than collect everything at once. Official sources and stable local caches make experiments reproducible. Automated downloads should comply with SEC access guidance, use an appropriately identified client, and avoid unnecessary repeat requests.

### Financial concepts to learn as needed

- **Revenue:** Amount earned from goods or services, as reported under the relevant accounting definition.
- **Net income:** Earnings after expenses and other items included in the reporting period.
- **Operating income:** Profit from operations under the company's reported definition.
- **Operating margin:** Operating income divided by revenue, multiplied by 100.
- **Revenue growth:** Change in revenue between comparable periods, divided by the earlier period's revenue.
- **Fiscal year:** A company's accounting year, which may not match a calendar year.
- **Business segment:** A reported part of a company's operations; segment definitions can change over time.

These are working introductions, not substitutes for the definitions in a filing. Financial fields must be selected and compared carefully. The project should document the exact meaning of each implemented metric.

### Data correctness challenges

This domain is challenging mainly because financial *meaning and provenance* matter:

- An annual figure is not interchangeable with a single-quarter or year-to-date figure.
- Two records can share a fiscal-year label but refer to different durations or reporting dates.
- Financial values have units (USD, shares, USD/share, etc.) and sometimes differing scales.
- Some prior-period values can appear again in later filings, including revisions or restatements.
- Similar XBRL tags can represent different accounting concepts; company-specific tags may require separate handling.
- The same metric can have different definitions or reporting practices across companies.
- A company's fiscal year-end may differ from another company's.
- Segments and other disclosures may change or be unavailable.

The data model should preserve source and period metadata, not just `company`, `year`, and `value`. Selection rules and calculations should be validated against actual filing evidence.

## 6. Proposed technical design (subject to change)

There are **two separate flows**: preparing trusted information, and answering a user's question.

### A. Data preparation flow

```text
SEC EDGAR sources
   |
   +--> Structured financial facts
   |       --> validate and normalize
   |       --> financial SQL database + provenance
   |
   +--> 10-K / 10-Q narrative text
           --> extract and clean relevant sections
           --> chunk and index for retrieval
           --> searchable passages + filing references
```

The ingestion pipeline must record what was downloaded, which filing a value came from, and how it was selected or transformed. A first version may be a few straightforward Python scripts; additional scheduling and automation can come later if justified.

### B. Question-answering flow

```text
User question
      |
      v
Question understanding / agent workflow
      |
      +--> SQL tool --> validated financial database --> calculated result
      |
      +--> Retrieval tool --> relevant SEC filing passages
      |
      v
Assemble answer with figures and cited evidence
      |
      v
Validation / evidence checks and uncertainty handling
      |
      v
Response: explanation + sources + optional chart/table
```

For a numerical question, the LLM can help formulate a query, but SQL or Python should perform the arithmetic. For an explanatory question, RAG should provide source passages before the model summarizes. For mixed questions, the system should combine both sets of evidence. The SQL tool should be restricted to appropriate read-only queries; source text must be treated as untrusted content rather than as instructions.

This is a *candidate architecture*. The first working system can be simpler and does not need an agent framework until tool orchestration becomes useful. One agent with clear tools is a better initial choice than introducing many specialized agents without evidence of a benefit.

### What "self-improving" means here

It means a **controlled, evaluation-driven engineering loop**, not an LLM silently changing itself on every conversation:

1. Run a representative set of independently checked questions.
2. Detect errors in numbers, periods, SQL, retrieved evidence, or explanations.
3. Analyze failure patterns.
4. Improve prompts, schema descriptions, retrieval, tools, data quality, or (optionally) model weights.
5. Re-test on held-out examples and record what changed.

Any model training should use reviewed training data, with evaluation examples kept separate.

## 7. Current technology direction and reasons

All choices below are **candidates unless explicitly recorded as selected in `docs/DECISIONS.md` or implemented in code**. Use what the system needs, when it needs it.

| Area | Current candidate | Why it fits | Notes / alternatives |
| --- | --- | --- | --- |
| Main language | Python | Data processing, ML tools, APIs, and orchestration | Initial development choice |
| Financial data | SEC EDGAR APIs and filings | Official public-company source | Start with a limited set and cache locally |
| Structured analytics | DuckDB + SQL | Lightweight, local, good for analytical queries | PostgreSQL may fit later multi-user needs |
| LLM | A suitable hosted API initially | Fast path to building and testing the workflow | Provider/model/cost not selected yet; local model possible |
| User interface | Streamlit | Quick interactive prototype | Can change if requirements expand |
| Agent orchestration | LangGraph, when needed | Explicit multi-step tool workflows | Simple function-based flow is also valid early |
| Document search | RAG with embeddings and/or keyword search | Ground explanations in filings | Start simple; evaluate hybrid search and reranking if needed |
| Vector/index storage | Chroma or another small local index | Convenient initial passage search | Choice should follow retrieval tests |
| Tracing | Langfuse or OpenTelemetry | Inspect tool calls, latency, costs, and failures | Introduce when measurement becomes useful |
| Model adaptation | Hugging Face, PyTorch, PEFT / LoRA | Experiment with smaller specialized models | Advanced, depends on curated data and GPU access |
| Serving / packaging | FastAPI and Docker | APIs and reproducible execution | Add near final delivery if justified |
| Development | VS Code, Claude Code, Git, tests | Incremental coding and traceable changes | Claude Code is a coding assistant, not the runtime LLM |
| Knowledge base | Local Markdown + project-scoped Notion page | Project continuity, plain-English learning, interview prep | Notion MCP read/write verified (see Section 13) |

**MCP** (Model Context Protocol) is used to connect Claude Code to Notion for documentation. Building an MCP server inside the FinSight AI application is optional, not a core requirement. Similarly, DPO, RL training, multi-agent setups, and low-level inference optimization are not mandatory just to make the project sound advanced.

## 8. Development roadmap (8 milestones)

The project has one ordered sequence of **eight milestones**. Each milestone contains smaller implementable tasks, but those tasks are not separate roadmaps. The exact work can be adjusted when real constraints appear. Milestone 7 is an advanced stretch milestone that may be reduced or skipped if it would jeopardize a reliable final product.

| # | Milestone | Core outcome |
| --- | --- | --- |
| 1 | Project setup | Working environment, repo, and documentation |
| 2 | Financial data collection and database | Verified, provenance-linked financial facts in DuckDB |
| 3 | Text-to-SQL | Plain-English numerical questions answered from the database |
| 4 | RAG over filings | Explanations grounded in cited filing passages |
| 5 | Tool-using agent and verification | One system handling numeric, narrative, and mixed questions |
| 6 | Evaluation and improvement | Reproducible benchmark, error analysis, measured improvements |
| 7 | Fine-tuning and model comparison (optional) | Evidence on whether a small adapted model is worth it |
| 8 | Deployment and presentation | Runnable, documented, demonstrable system |

### Milestone 1 - Project setup

**Goal:** Establish the working environment and project context.

Likely work:
- Verify Claude Code in VS Code and the project folder.
- Establish Python virtual environment and reproducible dependencies.
- Initialize Git, `.gitignore`, repository structure, and basic test setup.
- Confirm `CLAUDE.md`, the project-context Markdown files, and the existing Notion page.
- Verify Notion MCP connectivity and its ability to read/write within the project page only.
- Create an initial, simple architecture and progress record, clearly labeled as planned.

**Definition of done:** The environment runs, the project files are organized, documentation can be updated, and setup checks have passed. No financial ingestion feature needs to be invented to call setup complete.

**Interview learning:** Project structure, environments, version control, secrets, documentation and reproducibility.

### Milestone 2 - Financial data collection and database

**Goal:** Build a trustworthy source of structured company financial facts.

Likely work:
- Retrieve initial Microsoft SEC data and preserve raw responses/metadata.
- Identify appropriate annual revenue, net income, and operating income concepts.
- Grow these into a metric catalog of building-block metrics (draft: 40) that covers the common annual and quarterly questions of the readers in section 3.
- Start with non-financial companies; banks and insurers are a later extension.
- Normalize period, units, company identifiers, filings, and source links.
- Validate extracted figures against source filings.
- Store data in DuckDB and query it with SQL.
- Expand to a second company, likely Apple, after the first ingestion is reliable.

**Definition of done:** A reproducible pipeline and database containing verified, provenance-linked financial data for initial companies; basic analytical SQL works.

**Interview learning:** APIs, ETL, XBRL, data modeling, fiscal periods, SQL, data quality and lineage.

### Milestone 3 - Natural-language financial analytics (Text-to-SQL)

**Goal:** Let a user ask numerical financial questions in English.

Likely work:
- Give the LLM an accurate description of the available schema and metrics.
- Generate SQL for supported questions and execute it through a restricted read-only layer.
- Return numerical answers with periods, calculation details and source references.
- Build a minimal interactive interface and a set of known-answer tests.

**Definition of done:** A user can ask a small set of real financial questions in plain English and get verified answers from the database.

**Interview learning:** LLM prompting/tool use, schema understanding, SQL generation, validation, error handling, and limitations of LLM arithmetic.

### Milestone 4 - Retrieval over financial filings (RAG)

**Goal:** Answer questions requiring explanations from written SEC reports.

Likely work:
- Download selected 10-K/10-Q filing text and retain source locations.
- Extract appropriate narrative sections, clean and chunk text.
- Index the content for retrieval and test passage relevance.
- Produce answers grounded in retrieved passages with checkable citations.

**Definition of done:** The system answers representative management-discussion and risk questions with passages that actually support its claims.

**Interview learning:** Document ingestion, embeddings, semantic and keyword search, chunking, retrieval evaluation, grounding and citations.

### Milestone 5 - Unified tool-using financial agent and verification

**Goal:** Bring structured and document analysis together.

Likely work:
- Coordinate SQL and filing-search tools with a manageable orchestration design.
- Handle numeric, narrative, and mixed questions.
- Add checks for period consistency, source support and unsupported conclusions.
- Handle ambiguous requests and missing evidence gracefully.

**Definition of done:** One system can select the needed tools and produce coherent, appropriately sourced financial answers across question types.

**Interview learning:** Agent workflows, tool calling, state, safety boundaries, source verification and trade-offs of agents versus simpler pipelines.

### Milestone 6 - Evaluation and iterative improvement

**Goal:** Demonstrate reliability with actual measurements.

Likely work:
- Build a growing, carefully verified test collection covering easy and difficult questions.
- Include numeric questions, joins/aggregations, cross-period comparisons, filing explanations, mixed questions, and unanswerable cases.
- Track answer correctness, SQL result correctness, evidence/citation support, latency, cost and failure categories.
- Establish simple baselines and compare improvements through controlled experiments.
- Add regression tests for previously observed failures.

**Definition of done:** Reproducible benchmark results, meaningful error analysis and documented improvements or limitations.

**Interview learning:** Benchmark design, gold answers, train/test separation, baselines, metrics, ablation studies and experimental validity.

**Note:** Earlier discussions used labels such as A/B/C for *experimental configurations*. Those are only comparison candidates within this milestone, not alternate project roadmaps. Public datasets such as FinQA or Text-to-SQL benchmarks may help with related experiments, but must be checked for task fit; none automatically replaces a grounded FinSight evaluation set.

### Milestone 7 - Optional fine-tuning and model comparison

**Goal:** Explore whether an adapted small model can achieve useful task accuracy efficiently.

Possible work:
- Curate verified question/schema/SQL examples without evaluation leakage.
- Establish a small open-model baseline.
- Use parameter-efficient fine-tuning such as LoRA/QLoRA if compute permits.
- Compare untuned, tuned, and API-model configurations on held-out questions.
- Measure accuracy, latency, compute requirements, and estimated cost.

**Definition of done if undertaken:** A reproducible experiment with defensible conclusions, including negative results if applicable. If compute, cost, or time is insufficient, document the constraint and continue to final delivery.

**Interview learning:** Supervised fine-tuning, data curation, PEFT, overfitting, generalization, model serving and cost/quality trade-offs.

### Milestone 8 - Deployment and capstone presentation

**Goal:** Deliver a reproducible, presentable engineering artifact.

Likely work:
- Harden tests and improve error handling and observability.
- Package the application and APIs appropriately; use Docker if practical.
- Provide configuration instructions that do not leak credentials.
- Prepare a README, architecture diagram, evaluation report, known limitations and a concise demo.
- Document technical decisions and interview-ready explanations using real implementation evidence.

**Definition of done:** Another technically capable person can understand, run, inspect and evaluate the delivered system, and the project can be demonstrated end-to-end.

**Interview learning:** System design, testing, deployment, monitoring, costs, limitations and defending engineering choices.

## 9. Evaluation and research contribution

The most valuable capstone contribution is **measured reliability**, not the number of frameworks in the repository. A possible guiding research question is:

> How reliably can an AI system combine structured financial facts and narrative evidence from SEC filings to answer financial questions, and what design choices improve correctness, grounding, latency, and cost?

Possible experimental questions:
- How much does schema context or database-tool validation affect Text-to-SQL accuracy?
- Does adding document retrieval improve explanations while preserving numerical correctness?
- Which failure types remain after adding source checks or restricted retries?
- Can a smaller adapted model approach the quality of a stronger API model on a well-defined subset of tasks?
- How does performance change across companies, fiscal years, question difficulty or unfamiliar schemas?

Candidate metrics:

| Dimension | Example measurement |
| --- | --- |
| Numeric accuracy | Exact or tolerance-aware match to independently computed values |
| SQL correctness | Compare executed results against verified expected results, not query string similarity alone |
| Retrieval quality | Whether relevant source passages were found |
| Citation grounding | Whether cited filing passages genuinely support specific claims |
| Coverage / abstention | Correct behavior on ambiguous, missing-data, or unanswerable questions |
| Reliability | Failure rates and regressions after changes |
| Latency | End-to-end time and optionally p95 latency |
| Cost | API/token/compute cost per question or per correct answer |

A high-quality evaluation set needs independently checked expected answers and clean separation from fine-tuning examples. LLM-as-judge scoring may help with narrative responses but should be calibrated against human inspection and not treated as unquestionable ground truth. Actual measurements, including failures, should be preserved. No target accuracy or cost saving is assumed in advance.

## 10. Quality, safety, and responsible use

The system should be useful without creating false confidence about financial information.

- Rely primarily on official SEC facts and filings, preserving source IDs, dates, units, and cited locations.
- Distinguish reported facts, calculated metrics, management explanations, and system-generated interpretations.
- Avoid inventing unavailable numbers, causal explanations, or citations.
- Use read-only query execution and defensible safeguards around LLM-generated SQL.
- Treat retrieved documents as data, not as authoritative instructions to the agent.
- Keep credentials outside source control and documentation.
- Test ambiguous questions, contradictory evidence, missing data, and misleading responses.
- State data freshness and scope; public SEC filing data is not necessarily current market data.
- Frame outputs as research/educational financial analysis, not personalized investment recommendations.

These are project quality objectives; implementation details should be selected pragmatically as the system develops.

## 11. Working approach, learning, and resources

The user is building this project while learning and uses **Claude Code in VS Code** as the coding assistant. The learning style is practical: implement a small working feature, understand its purpose and data flow, test it, and then extend it. There is no requirement to complete a long prerequisite course before coding.

Claude Code can help write code, tests, documentation, and implementation explanations. The user should still understand: what problem each component solves, why it was selected, the inputs/outputs, how it is tested, and what can fail. This is essential for interviews and independent engineering judgment.

Visible progress should happen regularly, ideally each work session: a verified data retrieval, new query, passing test, corrected data selection rule, working interface feature, evaluation measurement, or documented design decision. There is no parallel daily-session roadmap; these are simply small tasks within the current milestone.

### Resource assumptions and uncertainties

- An ordinary development laptop is sufficient for initial ingestion, SQL, RAG experiments, and a simple interface, especially if model inference uses a hosted API.
- A coding assistant subscription does not automatically cover runtime LLM API usage.
- Fine-tuning multi-billion-parameter models may require access to a capable GPU, university resources, or rented compute; this is not needed during setup.
- API pricing, provider choice, compute availability, final winter-break date, and deployment hosting have not been established yet.
- Avoid committing to heavy infrastructure or spending before the baseline system and evaluation plan justify it.

The intent is to finish a reliable, well-evaluated core project by winter break, prioritizing the earlier milestones and final presentation over optional advanced features if time is limited.

## 12. Documentation and project continuity

Documentation supports two audiences:

1. **The coding assistant:** Needs concise, accurate project context to resume from the current state.
2. **The learner / future interviewer:** Needs clear explanations, examples, architecture, decisions, failures, experiments and what was actually implemented.

Current local documentation roles:

| Document | Role |
| --- | --- |
| `CLAUDE.md` | Persistent coding-assistant working instructions |
| `docs/PROJECT.md` | This comprehensive, flexible project vision and development context |
| `docs/PROGRESS.md` | Current milestone, actual completed tasks, blockers, and next task |
| `docs/ARCHITECTURE.md` | Current implemented architecture, plus clearly labeled proposals |
| `docs/DECISIONS.md` | Decisions made, reasons, alternatives, and trade-offs |
| `docs/NOTION.md` | Instructions for how the Notion knowledge base is structured, written, and kept up to date |

The existing **`finsight-ai` Notion page** is the detailed learning and interview-preparation knowledge base. It is organized by milestone (one page per milestone plus an overview), written in its own structure rather than copying local files, and updated in parallel with the work so nothing goes undocumented. `docs/NOTION.md` holds the full rules.

Technical terms should be explained in plain English using examples from this project. Documentation should distinguish planned work from completed work, avoid fabricated metrics, and preserve important changes and their reasons. Additional Markdown files can be created later when their usefulness becomes clear.

## 13. Known project state

This is a snapshot as of November 23, 2026. `docs/PROGRESS.md` is the source of truth for current state.

**Confirmed:**

- The `finsight-ai` folder exists, with a project-level `CLAUDE.md`.
- Local docs live in `docs/`: `PROJECT.md`, `PROGRESS.md`, `ARCHITECTURE.md`, `DECISIONS.md`, and `NOTION.md`.
- Claude Code is in use through the VS Code extension.
- The Notion MCP connection works: Claude Code has read the `finsight-ai` Notion page and created and edited child pages under it (November 21, 2026).
- The Python environment works: `.venv` (Python 3.14.0) with the project installed from `pyproject.toml`; `pytest` passes 3 setup checks.
- Git is set up on `main` with a GitHub remote.
- The Notion knowledge base uses the milestone-based layout described in `docs/NOTION.md`.

**Not yet confirmed:**

- Any SEC ingestion, database schema, SQL agent, RAG pipeline, evaluation or deployed service has been implemented.

Milestone 1 (Project setup) is complete. The next milestone is **Milestone 2: Financial data collection and database**.

## 14. Open choices and likely future evolution

The following are intentionally not finalized:

- Exact initial companies, financial metrics, and historical coverage (direction so far: about 10 non-financial companies, a draft catalog of 40 metrics).
- Which SEC filing sections to index and how to cite them precisely.
- Data schema and treatment of restatements, fiscal periods, company-specific facts, and segment data.
- Runtime LLM provider/model and any external API budget.
- Which retrieval method, embedding model, vector store, and reranking approach actually work best.
- Whether orchestration requires LangGraph or can remain simpler for the initial scope.
- How extensive financial evidence checking should be, and which claims require explicit abstention.
- Which evaluation questions and datasets best reflect intended user tasks.
- Whether to complete fine-tuning, preference optimization, or cross-domain extensions.
- Final hosting, frontend/backend separation, and deployment environment.

Changes should follow evidence from implementation, testing, scope, and resources. Record consequential choices in `docs/DECISIONS.md`; explain current components in `docs/ARCHITECTURE.md`; update the current task in `docs/PROGRESS.md`. Keep this document aligned with the overall project vision without turning it into a daily task tracker.

## 15. What success looks like

At a minimum, the finished core system should let a person ask meaningful financial questions over authentic public-company data, combine numerical analysis and filing evidence where appropriate, return traceable answers, handle uncertainty, and demonstrate its reliability through a reproducible evaluation. It should include a usable interface, maintainable source code, tests, a clear architecture, and a candid account of results and limitations.

A stronger stretch outcome would show rigorous comparisons between agent configurations and/or an adapted smaller model, with measured effects on correctness, grounding, latency, and cost. The value comes from well-reasoned engineering and honest evaluation, not simply accumulating tool names.

**Next practical action:** Milestone 1 is complete. Start Milestone 2 by retrieving a small amount of Microsoft financial information from the SEC, checking its reporting periods and provenance, and building the first trustworthy data pipeline.
