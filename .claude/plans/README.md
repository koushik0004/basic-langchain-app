# Plans

Active build plans for this project, split by domain for easier loading.

## Index

- [00 — Context](00-context.md) — current state + goal
- [01 — Root changes](01-root-changes.md) — `requirements.txt`, `.gitignore`
- [02 — Backend](02-backend.md) — FastAPI service under `backend/`
- [03 — Frontend](03-frontend.md) — Next.js app under `frontend/`
- [04 — Run & verify](04-run-and-verify.md) — local commands + checks
- [05 — Critical files](05-critical-files.md) — pointers to source-of-truth files

## Scope rules

- Plans here are **guidance**, not a hard cap. Features beyond what's listed are allowed when they serve the same goal.
- Do not refactor files outside the plan's scope without approval (see `CLAUDE.md` → Agentic Work Rules).
- When a plan is delivered, move its file to `done/` (create the dir on first use) or delete it. Do not leave stale plans.
- Update the relevant plan file when scope shifts — don't let the plan and code diverge silently.
