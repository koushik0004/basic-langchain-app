# Generate Knowledge Base

Scan the project and produce 2 compact markdown files in `.claude/knowledge/`:

## architecture.md (~4k tokens)
- Project folder structure and key modules
- Entry points: main files, routers, services, handlers
- Critical dependencies and how they connect
- Tech stack breakdown

## conventions.md (~4k tokens)
- Code style and naming patterns
- Framework conventions:
  - FastAPI: routing, dependencies, schemas, async patterns
  - React/Next: component structure, hooks, state management
  - LangChain/LangGraph: LCEL, state dicts, node patterns
  - Python: PEP8, ruff linting rules
- i18n conventions (if applicable)
- RAG and agentic patterns (if applicable)
- Gotchas and anti-patterns to avoid

## Requirements
- Keep total output under 8k tokens (optimized for Haiku 4.5 consumption)
- Use clean markdown with examples where useful
- No verbose descriptions; be direct and scannable
- Target: serve as context for a cheaper downstream AI model

## Usage
Run: `/kb`

Creates `.claude/knowledge/architecture.md` and `.claude/knowledge/conventions.md`
