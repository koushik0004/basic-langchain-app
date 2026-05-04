# Project Rules

## Stack
- Python (RAG, agentic RAG, LangChain, LangGraph)
- FastAPI (REST APIs)
- React / Next.js (frontend)

## Response Rules (TOKEN BUDGET - ALWAYS FOLLOW)
- No preamble. No summaries. No "here's what I did."
- Code only unless explanation explicitly requested.
- No docstrings unless asked. No inline comments unless logic is non-obvious.
- Omit type hints on trivial/obvious functions.
- Never repeat code already shown in context.
- Use `# ...` to indicate unchanged sections when editing.
- One-line answers for yes/no or simple factual questions.
- If uncertain, ask ONE clarifying question — not multiple.

## Agentic Work Rules
- Before multi-file changes: output a bullet plan and STOP. Wait for approval.
- Never refactor files not explicitly in scope.
- Never add dependencies without asking first.
- Run only: `pytest`, `ruff`, `mypy` — no other shell commands unless asked.
- After task: list only files changed. No explanation unless asked.

## Code Style
- Python: follow PEP8, use ruff for linting
- FastAPI: use `Annotated` dependencies, Pydantic v2
- LangChain/LangGraph: prefer LCEL where possible; typed state dicts for graphs
- React/Next: functional components, TypeScript, no class components

## Detailed Docs (load only when relevant)
- RAG patterns → @docs/rag-patterns.md
- LangGraph agents → @docs/langgraph-patterns.md
- FastAPI conventions → @docs/fastapi-conventions.md
- Frontend conventions → @docs/frontend-conventions.md

## API & SDK Defaults
- Use `claude-haiku-4-5` as default for LangChain/SDK experiments (cheapest confirmed option).
- Always verify model names against current API before running — outdated names cause 400 errors.
- Before SDK work: check `anthropic` and `langchain` packages, confirm `ANTHROPIC_API_KEY` set.

## i18n Conventions
- Translation keys are maintained across 62 locale files; insert new keys at same relative position in ALL locales.
- Do NOT introduce blank lines between properties when inserting new keys.
- Always grep/check if key already exists in locales before adding (it may already be present).
- Use `/i18n-add` skill for bulk insertions: preserves formatting, validates JSON, reports summary.

## Knowledge Base Generation
When asked to generate compact markdown docs for cheaper models (Haiku context):
- Output to `.claude/knowledge/` directory (create if needed).
- Produce two files: `architecture.md` (~4k tokens) and `conventions.md` (~4k tokens).
- **architecture.md**: project structure, key modules, entry points, critical dependencies.
- **conventions.md**: code style rules, framework patterns (FastAPI/React/LangChain), i18n/RAG/LangGraph rules, gotchas.
- Keep total under 8k tokens; optimize for cheap model consumption.
- Use `/kb` skill: `/ kb` generates both files automatically.

## Plans
- Active build plans → @plans/README.md
- Plans are guidance, not a hard scope cap — features beyond the listed plan are allowed when they serve the same goal. Still follow Agentic Work Rules (ask before multi-file changes / new deps).
