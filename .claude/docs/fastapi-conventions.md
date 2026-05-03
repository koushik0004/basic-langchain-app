# FastAPI Conventions

## Structure
```
app/
  main.py          # app factory, lifespan, router includes
  routers/         # one file per domain
  services/        # business logic (no FastAPI imports)
  schemas/         # Pydantic v2 models (request/response)
  dependencies/    # Annotated deps
  core/            # config, logging, exceptions
```

## Routing
- Prefix: `/api/v1/`
- Router per domain: `router = APIRouter(prefix="/rag", tags=["rag"])`
- Use `Annotated` for all dependencies

## Request/Response
- Always use Pydantic v2 (`model_config = ConfigDict(...)`)
- Separate request schema from response schema
- Use `response_model` on all endpoints

## Async
- All endpoints `async def`
- Use `asyncio.gather` for parallel I/O in services
- DB sessions: use `async with` context manager

## Streaming (LLM responses)
```python
from fastapi.responses import StreamingResponse

@router.post("/chat")
async def chat(req: ChatRequest):
    return StreamingResponse(stream_llm(req), media_type="text/event-stream")
```

## Error Handling
- Custom `HTTPException` subclasses in `core/exceptions.py`
- Global exception handler via `@app.exception_handler`
- Return `{"detail": "...", "code": "ERROR_CODE"}` format

## Middleware
- CORS, request ID, timing — add in `main.py` lifespan
- Never add middleware in routers

## LangChain Integration
- Wrap chains/agents in service layer
- Never import LangChain directly in routers
- Use background tasks for long-running agent calls: `BackgroundTasks`
