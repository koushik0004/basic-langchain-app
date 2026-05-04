# Code Conventions & Patterns

## Python Style

**Linter:** `ruff` (PEP8 + common fixes)
**Type hints:** Use on public APIs, omit on internal/trivial functions
**Format:** 4 spaces, lines ≤100 chars recommended

```python
# Good: type hints on public functions
async def get_reply(self, message: str) -> str:
    return await self.chain.ainvoke({"user_input": message})

# OK: no hints on internal helpers
def _parse_env():
    return load_dotenv()
```

---

## LangChain / LCEL Patterns

### 1. Chain Composition (LCEL)
Always build chains using pipe (`|`) operator, not method calls.

```python
# Good: LCEL composition
chain = ChatPromptTemplate.from_messages([...]) | llm | StrOutputParser()

# Avoid: chaining method calls
chain = ChatPromptTemplate(...).bind_partial(x=y).invoke(...)
```

### 2. Prompts with Templates
Use `ChatPromptTemplate.from_messages()` for composable prompts.

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{user_input}")
])
```

**Rules:**
- System prompt first, then user placeholders
- Use dict-based variable injection: `{variable_name}`
- Keep system prompts < 300 tokens

### 3. Async Chains
In async contexts (FastAPI, async services), use `ainvoke()` not `invoke()`.

```python
# In FastAPI or async service
result = await chain.ainvoke({"user_input": message})

# In CLI (sync context)
result = chain.invoke({"user_input": message})
```

### 4. LLM Models
Always specify model explicitly. Current default:

```python
llm = ChatAnthropic(
    model="claude-haiku-4-5-20251001",  # Cheapest option confirmed
    temperature=0.3  # Moderate randomness for helpful responses
)
```

**Model selection:**
- `claude-haiku-4-5`: default (cheapest, fast)
- `claude-sonnet-4-6`: balanced cost/quality for complex tasks
- `claude-opus-4-7`: most capable (expensive, use for critical paths)

---

## FastAPI Conventions

### 1. App Structure
```
backend/app/
├── main.py           # App factory + lifespan
├── core/config.py    # Settings (read .env)
├── schemas/          # Pydantic request/response models
├── services/         # Business logic (NO FastAPI imports)
└── routers/          # Endpoints (import from services)
```

### 2. Request/Response Schemas
Use Pydantic v2 with explicit `ConfigDict`:

```python
from pydantic import BaseModel, ConfigDict

class ChatRequest(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {...}})
    message: str

class ChatResponse(BaseModel):
    reply: str
```

### 3. Dependencies with Annotated
Always use `Annotated` for FastAPI dependencies:

```python
from typing import Annotated
from fastapi import Depends

@router.post("/chat/")
async def chat(
    req: ChatRequest,
    service: Annotated[ChatService, Depends(get_chat_service)]
):
    return ChatResponse(reply=await service.get_reply(req.message))
```

### 4. Async Endpoints
All endpoints must be `async def`:

```python
@router.post("/chat/")
async def chat(req: ChatRequest) -> ChatResponse:
    result = await expensive_operation()
    return ChatResponse(reply=result)
```

### 5. Error Handling
Return `HTTPException` with structured error body:

```python
from fastapi import HTTPException

if not message.strip():
    raise HTTPException(
        status_code=400,
        detail={"message": "Empty message not allowed", "code": "EMPTY_INPUT"}
    )
```

---

## Service Layer Pattern

**Goal:** Isolate LangChain logic from FastAPI routers.

```python
# services/chat_service.py
class ChatService:
    def __init__(self):
        self.chain = self._build_chain()
    
    def _build_chain(self):
        llm = ChatAnthropic(model="claude-haiku-4-5-20251001", temperature=0.3)
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant..."),
            ("user", "{user_input}")
        ])
        return prompt | llm | StrOutputParser()
    
    async def get_reply(self, message: str) -> str:
        """Entry point for routers — use ainvoke for async."""
        return await self.chain.ainvoke({"user_input": message})

# routers/chat.py
@router.post("/chat/")
async def chat(req: ChatRequest, service: ChatService = Depends(...)):
    reply = await service.get_reply(req.message)
    return ChatResponse(reply=reply)
```

**Why this works:**
- Services: pure Python, testable without mocking LangChain
- Routers: thin orchestration layer, only handle HTTP concerns
- Changes to chain logic don't touch endpoints

---

## Frontend (React/Next.js) Patterns

### 1. Component Structure
Functional components only, TypeScript strict mode:

```typescript
interface ChatUIProps {
  initialMessage?: string;
}

export function ChatUI({ initialMessage }: ChatUIProps) {
  return <div>{/* JSX */}</div>;
}
```

### 2. Fetching Chat Responses
Use typed fetch wrappers, never raw `fetch()`:

```typescript
// lib/api.ts
export async function postChat(message: string): Promise<string> {
  const res = await fetch("/api/v1/chat/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  });
  if (!res.ok) throw new Error("Chat failed");
  const data = await res.json();
  return data.reply;
}

// In component
const reply = await postChat(userInput);
```

### 3. Server/Client Components
Use Server Components by default. Add `"use client"` only for interactivity:

```typescript
// app/page.tsx (Server Component)
import { ChatUI } from "@/components/ChatUI";
export default function Page() {
  return <ChatUI />;
}

// components/ChatUI.tsx (Client Component)
"use client";
import { useState } from "react";
export function ChatUI() { /* interactive state */ }
```

---

## Response Rules (Token Budget)

Follow `.claude/CLAUDE.md` response rules:
- **No preamble, no summaries** — code only unless explanation requested
- **No docstrings unless asked** — one-line comments only for non-obvious logic
- **Omit type hints on trivial functions**
- **Multi-file changes:** output bullet plan first, wait for approval

---

## Gotchas & Anti-Patterns

### ❌ Don't
- Call LangChain directly in routers (breaks testability)
- Use `invoke()` in FastAPI (blocks event loop; use `ainvoke()`)
- Hard-code `.env` values in code (use `BaseSettings`)
- Mutate chain state across requests (build chain once in `__init__`)
- Omit `response_model` on endpoints (makes schema unclear)
- Use `any` type in TypeScript frontend code

### ✅ Do
- Build chains once in service `__init__`, reuse across calls
- Use `Annotated[Type, Depends(...)]` for all FastAPI deps
- Specify model names explicitly (never rely on defaults)
- Test services independently of routers
- Keep system prompts < 300 tokens
- Use TypeScript strict mode on all components

---

## Common Tasks

### Add a new endpoint
1. Create request/response schema in `schemas/`
2. Add method to `ChatService`
3. Create endpoint in `routers/chat.py` using `Annotated` dependency
4. Test: `pytest services/test_chat_service.py`

### Update the system prompt
**File:** `services/chat_service.py:_build_chain()`
- Edit the `("system", "...")` tuple in `ChatPromptTemplate.from_messages()`
- Keep under 300 tokens
- Test in CLI: `python app.py`

### Add error handling
**File:** `routers/chat.py`
- Wrap service calls in try/except
- Return `HTTPException(status_code=..., detail={...})`
- Document in endpoint docstring
