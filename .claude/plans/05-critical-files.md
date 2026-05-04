# 05 — Critical files

Source-of-truth files that drive this plan.

- `app.py` — source of chain logic to migrate into the service layer.
- `requirements.txt` — must be updated before `pip install`.
- `.env` (repo root) — provides `ANTHROPIC_API_KEY` consumed by `backend/app/core/config.py`.
- `.claude/docs/fastapi-conventions.md` — canonical backend conventions.
- `.claude/docs/frontend-conventions.md` — canonical frontend conventions.
