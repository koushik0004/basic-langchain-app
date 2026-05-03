# Plan: FastAPI Backend + Next.js Frontend

## Context
The project currently has a single `app.py` CLI chat loop using LangChain LCEL (ChatAnthropic → ChatPromptTemplate → StrOutputParser). The goal is to expose the same chat feature via a REST API (FastAPI) and build a browser UI (Next.js) on top of it. The CLI `app.py` is preserved unchanged.

---

## File Changes

### Root-level updates (2 files)
- **`requirements.txt`** — add `fastapi>=0.111.0`, `uvicorn[standard]>=0.29.0`, `pydantic>=2.0.0`, `pydantic-settings>=2.0.0`
- **`.gitignore`** — add `__pycache__/`, `*.pyc`, `node_modules/`, `.next/`, `out/`, `dist/`

---

## Backend: `backend/` directory

### File creation order (dependency-safe)

1. `backend/app/__init__.py` — empty
2. `backend/app/core/__init__.py` — empty
3. `backend/app/core/config.py` — Pydantic `BaseSettings` reading `ANTHROPIC_API_KEY` from root `.env`
4. `backend/app/schemas/__init__.py` — empty
5. `backend/app/schemas/chat.py` — `ChatRequest` (message: str) + `ChatResponse` (reply: str), Pydantic v2 `ConfigDict`
6. `backend/app/services/__init__.py` — empty
7. `backend/app/services/chat_service.py` — `ChatService` class with `async get_reply(message)` using `chain.ainvoke()`; chain built once in `__init__`
8. `backend/app/routers/__init__.py` — empty
9. `backend/app/routers/chat.py` — `POST /chat/` endpoint, `Annotated` dependency on `ChatService`, `response_model=ChatResponse`
10. `backend/app/main.py` — FastAPI app factory with `lifespan`, CORS for `http://localhost:3000`, includes router at `/api/v1`

### Key decisions
- Chain logic extracted from `app.py` into `ChatService` — routers never import LangChain directly
- `ainvoke` used (not `invoke`) to keep the async event loop non-blocking
- `.env` stays at repo root; `config.py` uses `SettingsConfigDict(env_file=".env")`

---

## Frontend: `frontend/` directory

### Scaffold command (run from repo root)
```bash
npx create-next-app@latest frontend --typescript --tailwind --app --no-src-dir --import-alias "@/*" --no-eslint
cd frontend && npm install @tanstack/react-query
```

### Files to write/replace after scaffold

1. **`frontend/types.ts`** — `ChatRequest`, `ChatResponse`, `Message` interfaces (no `any`)
2. **`frontend/lib/api.ts`** — typed `sendMessage(req: ChatRequest): Promise<ChatResponse>` fetch wrapper; base URL from `NEXT_PUBLIC_API_URL ?? "http://localhost:8000"`
3. **`frontend/components/features/ChatBox.tsx`** — `"use client"` component; `useMutation` from TanStack Query; message list state; user/assistant bubble layout with Tailwind
4. **`frontend/app/layout.tsx`** — replace scaffold; add `QueryClientProvider` wrapper (`"use client"`)
5. **`frontend/app/page.tsx`** — Server Component; renders `<ChatBox />`

---

## Running Locally

**Backend** (from `backend/` with venv active):
```bash
source ../.venv/bin/activate
pip install -r ../requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend** (from `frontend/`):
```bash
npm run dev   # http://localhost:3000
```

---

## Verification

| Check | Command |
|---|---|
| Swagger UI loads | `curl http://localhost:8000/docs` |
| Chat endpoint works | `curl -X POST http://localhost:8000/api/v1/chat/ -H "Content-Type: application/json" -d '{"message":"Hello"}'` |
| CORS preflight | `curl -X OPTIONS http://localhost:8000/api/v1/chat/ -H "Origin: http://localhost:3000" -v` |
| Frontend smoke test | Open `http://localhost:3000`, send a message, see assistant reply |
| TypeScript clean | `cd frontend && npx tsc --noEmit` |

---

## Critical Files
- `app.py` — source of chain logic to migrate into service layer
- `requirements.txt` — must be updated before `pip install`
- `.env` (repo root) — provides `ANTHROPIC_API_KEY` consumed by `backend/app/core/config.py`
- `.claude/docs/fastapi-conventions.md` — canonical backend conventions
- `.claude/docs/frontend-conventions.md` — canonical frontend conventions
