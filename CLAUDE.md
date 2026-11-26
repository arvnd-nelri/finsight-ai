# FinSight AI — Claude Code Instructions

## The Project in Brief

FinSight AI is a master's-level AI Engineering capstone: an evidence-grounded
financial research agent. Users ask plain-English questions about public
companies and get answers backed by SEC data, with figures, periods, units,
and cited sources.

It combines SEC data ingestion, a financial SQL database, Text-to-SQL, RAG over
10-K/10-Q filings, a tool-using agent with evidence checks, evaluation, optional
fine-tuning, and deployment, built in **8 milestones, in order**.

The full vision lives in `docs/PROJECT.md`. Do not duplicate it here.

## Session Start

1. Read `docs/PROGRESS.md`. It is short and tells you the current milestone,
   what is done, and the next step.
2. Read other docs **only when the task needs them**:

| Read this | When |
| --- | --- |
| `docs/PROJECT.md` | Starting a new milestone, making a design or technology choice, or when the project's goals or scope matter. Read only the relevant sections. |
| `docs/ARCHITECTURE.md` | Adding or changing components or how they connect |
| `docs/DECISIONS.md` | Before making a choice that may already have been decided |
| `docs/NOTION.md` | Before writing anything to Notion |

Skip these for small tasks (bug fixes, renames, single edits).
Do not auto-import long docs into this file.

## How to Work With Me

I am learning AI Engineering while building this project.

- Act as my coding assistant and technical mentor.
- Explain important concepts and decisions in simple English,
  using FinSight AI examples.
- Build in small, working, tested steps. Prefer practical,
  maintainable solutions over complexity.
- When there is an important choice, compare 2–3 options with trade-offs
  and give a clear recommendation.
- **At the end of each task, recommend the next concrete step** based on
  `docs/PROGRESS.md` and the current milestone's definition of done.
- Do not assume the final architecture or features in advance.

## Keeping Documentation Current

Update docs as part of finishing a task, not later:

| What happened | Update |
| --- | --- |
| Task completed, started, or blocked | `docs/PROGRESS.md` (task table, next step, history) |
| Technology or approach chosen | `docs/DECISIONS.md` (new D-number entry) |
| Component added or connections changed | `docs/ARCHITECTURE.md` |
| Project vision, scope, or milestones changed | `docs/PROJECT.md` |
| Anything worth learning or explaining | Notion, following `docs/NOTION.md` |

- **Update Notion automatically, in the same turn, without being asked**,
  whenever something meaningful happens (task done, decision made, problem
  solved, new concept used). This includes plans or agreements reached in
  discussion with no file edits; the hook cannot detect those, so update
  `docs/PROGRESS.md` and Notion yourself. Skip trivial changes. A Stop hook
  (`.claude/hooks/notion-sync.sh`) reminds you if project files changed but
  Notion was not updated.
- Keep the top-line purpose comment in each `docs/*.md` file.
- Edit only the sections that changed. Do not rewrite whole files.

## Rules

- Document only real work and real results. Never invent implementations,
  metrics, or financial figures. Label plans as plans.
- Never commit or write credentials or secrets anywhere in the repo or Notion.
  Secrets live outside the repo (e.g. `~/.config/finsight-ai/`).
- Use only the `finsight-ai` Notion page and its children.
