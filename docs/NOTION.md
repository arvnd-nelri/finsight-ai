<!-- NOTION.md — instructions for Claude on how to write and maintain the FinSight AI Notion documentation -->

# Notion Documentation Instructions

## Purpose

Notion is the informal, readable story of FinSight AI.

Test for every page: if someone had the full codebase and only this
Notion documentation, they should be able to understand how the project
works and answer interview questions about it with confidence.

Notion is written for a human reader who wants to learn and revise.
It does not copy the repository's files.

## What Notion Is Not

- It is not a copy of `docs/*.md`, code files, or the folder structure.
- It does not mirror local files one to one.

The local `docs/` files are short working notes:
`PROJECT.md`, `PROGRESS.md`, `ARCHITECTURE.md`, `DECISIONS.md`.
Notion explains the same project in depth, in its own structure and words.

## What "Synchronized" Means

Update Notion **while the project is being built**, at the same time
as the work is done, so that no part of the project goes undocumented.

- When a feature, decision, experiment, problem, or fix happens,
  document it in Notion in the same session.
- Synchronized means up to date and complete.
  It does not mean identical to the local files.

## Structure

Organize the documentation by milestone.

- **Main page (finsight-ai):** a short overview of the project and
  the goal, the high-level architecture, the tech stack once it is chosen,
  and links to each milestone page with its status.
- **One page per milestone**, created when work on that milestone starts:
  1. Project Setup
  2. Financial Data Collection & Database
  3. Text-to-SQL AI
  4. RAG — Financial Document Understanding
  5. AI Agent & Evidence Verification
  6. Evaluation & Improvement
  7. LLM Fine-Tuning & Model Comparison (optional)
  8. Deployment & Final Presentation
- Add sub-pages under a milestone only when a topic is too large
  for one page.
- Cross-cutting pages (for example a glossary) are fine
  if they become useful. Do not create them in advance.

## What a Milestone Page Should Cover

Include these as they become relevant. Skip anything that has not happened yet.

- **Goal:** what this milestone achieves and why it matters for FinSight AI.
- **Concepts:** the AI Engineering and finance ideas involved, explained in
  simple English with FinSight AI examples (e.g. what Text-to-SQL is, what an
  embedding is, what a 10-K is).
- **What was built:** the components, what each does, how it works,
  and how it connects to the rest of the system. Reference real file
  and module names so the reader can find them in the code.
- **Data flow:** how data moves through this part, with a diagram when it helps.
- **Technologies and decisions:** what was chosen, why,
  which alternatives were considered, and the trade-offs.
- **Journey:** challenges, experiments, mistakes, and how they were solved.
- **Results:** real outputs, metrics, or examples from the actual implementation.
- **Interview prep:** likely interview questions with clear answers,
  key terms, and how to explain this part in 30 seconds and in 3 minutes.
- **Status and open items.**

## Writing Style

- Simple English. Define each term the first time it is used.
- Explain the *why*, not only the *what*.
- Use concrete examples from FinSight AI (real tickers, real queries,
  real outputs) instead of generic examples.
- Use tables, diagrams, code snippets, callouts, and toggles
  where they make something easier to understand.
- Short paragraphs that are easy to skim.

## Design and Formatting

Write like a professional Notion writer and designer.
Every page should look polished, be easy to navigate, and be designed
for clarity. Do not just paste text into a page.

**Use Notion's features with purpose:**

- **Headings** to give the page a clear outline that can be skimmed.
- **Callouts** for key takeaways, definitions, warnings, and
  "why this matters" notes.
- **Tables** to compare technologies, options, and trade-offs.
- **Toggles** for deeper detail, long explanations, and interview Q&A,
  so the main page stays clean.
- **Dividers** between major sections.
- **Code blocks** (with the correct language set) for real code, SQL, and commands.
- **Diagrams** for architecture and data flow.
- **Bold and highlights** only for the points that matter most.
- Columns, quotes, and other blocks when they make the page easier to read.

**Gotcha:** Notion turns plain-text file names like `PROJECT.md` into broken
web links (`http://PROJECT.md`). Always write file names as inline code,
including inside headings and toggle titles, and check the returned page.

**Avoid:**

- Plain pages that are just walls of text or long checkbox lists.
- Unnecessary or decorative emojis, in page icons or in the text.
- Generic, template-looking layouts.
- Formatting for its own sake. Every element should make the page easier to read.

## Accuracy Rules

- Document only what was actually built, decided, or observed.
  Never invent implementations, results, or metrics.
- Label plans clearly as plans ("Planned", "Proposed").
- When something changes, update the old explanation so it stays
  correct, and record the change in the milestone's journey section.

## Scope and Safety

- Write only inside the designated FinSight AI Notion page
  (`finsight-ai`) and its child pages.
- Never put credentials, API keys, or secrets in Notion.
- Do not delete pages the user created without asking first.
