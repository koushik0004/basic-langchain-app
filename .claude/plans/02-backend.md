# 02 — Backend (`backend/`)

FastAPI app following `.claude/docs/fastapi-conventions.md`.

## File creation order (dependency-safe)

1. `backend/app/__init__.py` — empty
2. `backend/app/core/__init__.py` — empty
3. `backend/app/core/config.py` — Pydantic `BaseSettings` reading `ANTHROPIC_API_KEY` from root `.env`
4. `backend/app/schemas/__init__.py` — empty
5. `backend/app/schemas/chat.py` — `ChatRequest` (`message: str`) + `ChatResponse` (`reply: str`), Pydantic v2 `ConfigDict`
6. `backend/app/services/__init__.py` — empty
7. `backend/app/services/chat_service.py` — `ChatService` class with `async get_reply(message)` using `chain.ainvoke()`; chain built once in `__init__`
8. `backend/app/routers/__init__.py` — empty
9. `backend/app/routers/chat.py` — `POST /chat/` endpoint, `Annotated` dependency on `ChatService`, `response_model=ChatResponse`
10. `backend/app/main.py` — FastAPI app factory with `lifespan`, CORS for `http://localhost:3000`, includes router at `/api/v1`

## Key decisions

- Chain logic extracted from `app.py` into `ChatService` — routers never import LangChain directly.
- `ainvoke` used (not `invoke`) to keep the async event loop non-blocking.
- `.env` stays at repo root; `config.py` uses `SettingsConfigDict(env_file=".env")`.
