# Project Architecture

## Overview
**basic-langchain-app** — multi-interface LangChain chat application.
- **CLI** (`app.py`): Interactive console chat using LangChain LCEL
- **Backend** (planned `backend/`): FastAPI REST API exposing chat service
- **Frontend** (planned `frontend/`): Next.js browser UI consuming the REST API

Stack: Python (LangChain, FastAPI) + Node.js (Next.js, React)

---

## Project Structure

```
basic-langchain-app/
├── app.py                    # Root: CLI interactive chat (preserved unchanged)
├── requirements.txt          # Python dependencies
├── .env                      # API keys: ANTHROPIC_API_KEY
├── backend/                  # FastAPI service (planned)
│   └── app/
│       ├── main.py          # FastAPI app factory + router includes
│       ├── core/
│       │   └── config.py    # Pydantic BaseSettings reading .env
│       ├── schemas/
│       │   └── chat.py      # ChatRequest, ChatResponse (Pydantic v2)
│       ├── services/
│       │   └── chat_service.py  # ChatService with async get_reply()
│       └── routers/
│           └── chat.py      # POST /api/v1/chat/ endpoint
├── frontend/                 # Next.js app (planned)
│   └── app/
│       ├── page.tsx         # Main chat UI
│       └── layout.tsx       # Root layout
└── .claude/                  # Claude Code config
    ├── docs/                # Reference docs (RAG, LangGraph, FastAPI, Frontend patterns)
    ├── plans/               # Project build plans
    └── skills/              # Custom slash commands
```

---

## Core Components

### 1. Chat Chain (Root)
**File:** `app.py:9-26`

```python
llm = ChatAnthropic(model="claude-haiku-4-5-20251001", temperature=0.3)
chain = ChatPromptTemplate.from_messages([...]) | llm | StrOutputParser()
```

**Pattern:** LangChain LCEL composition
- `ChatPromptTemplate`: system + user message templates
- `ChatAnthropic`: Claude LLM (Haiku 4.5 for cost)
- `StrOutputParser`: extract text output

### 2. Chat Service (Backend)
**Planned in:** `backend/app/services/chat_service.py`

```python
class ChatService:
    def __init__(self):
        self.chain = build_chain()  # Same logic as app.py
    
    async def get_reply(self, message: str) -> str:
        return await self.chain.ainvoke({"user_input": message})
```

**Key:** Uses `ainvoke()` (async) for non-blocking API.

### 3. FastAPI Endpoints
**Planned in:** `backend/app/routers/chat.py`

```python
@router.post("/chat/", response_model=ChatResponse)
async def chat(req: ChatRequest, service: ChatService = Depends(...)):
    reply = await service.get_reply(req.message)
    return ChatResponse(reply=reply)
```

**Prefix:** `/api/v1/chat/`

### 4. Frontend Chat UI
**Planned in:** `frontend/app/page.tsx`

- Fetch wrapper to `/api/v1/chat/` (POST with `{message: string}`)
- React state for messages history
- Form input + message list display

---

## Data Flow

```
CLI (app.py)
  ↓
  └─→ ChatPromptTemplate
       ↓
       └─→ ChatAnthropic (claude-haiku-4-5)
            ↓
            └─→ StrOutputParser
                 ↓
                 └─→ Console output

Browser (frontend/)
  ↓
  └─→ POST /api/v1/chat/ {message}
       ↓
       └─→ FastAPI Router (chat.py)
            ↓
            └─→ ChatService.get_reply()
                 ↓
                 └─→ (same chain logic)
                      ↓
                      └─→ ChatResponse {reply}
```

---

## Key Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `langchain` | >=0.1.0 | Chain orchestration |
| `langchain-anthropic` | >=0.1.0 | Claude integration |
| `langchain-core` | >=0.1.0 | Prompt, LLM, parser base classes |
| `python-dotenv` | >=1.0.0 | Load `.env` variables |
| `fastapi` | (planned) | REST API framework |
| `pydantic` | (planned) | v2 for schemas + config |
| `next.js` | (planned) | Frontend framework |

---

## Environment & Entry Points

**Root `.env`:**
```
ANTHROPIC_API_KEY=sk-ant-...
```

**CLI entry:**
```bash
python app.py
```

**Backend entry (planned):**
```bash
uvicorn backend.app.main:app --reload
```

**Frontend dev (planned):**
```bash
cd frontend && npm run dev
```

---

## Critical Design Constraints

1. **Preserve CLI**: `app.py` must remain unchanged. Backend extracts chain logic into service layer.
2. **Cost optimization**: Using Haiku 4.5 (cheapest) for all LLM calls.
3. **Async-first backend**: All endpoints use `async def` and `ainvoke()` to avoid blocking.
4. **No LangChain in routers**: Chain logic stays in services; routers only orchestrate and validate.
5. **Single `.env` at root**: Both CLI and backend read from same file.
