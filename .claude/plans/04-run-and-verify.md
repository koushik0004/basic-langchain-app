# 04 — Run & verify

## Running locally

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

## Verification

| Check | Command |
|---|---|
| Swagger UI loads | `curl http://localhost:8000/docs` |
| Chat endpoint works | `curl -X POST http://localhost:8000/api/v1/chat/ -H "Content-Type: application/json" -d '{"message":"Hello"}'` |
| CORS preflight | `curl -X OPTIONS http://localhost:8000/api/v1/chat/ -H "Origin: http://localhost:3000" -v` |
| Frontend smoke test | Open `http://localhost:3000`, send a message, see assistant reply |
| TypeScript clean | `cd frontend && npx tsc --noEmit` |
