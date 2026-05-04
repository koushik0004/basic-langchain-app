# 01 — Root-level changes

Two files at repo root.

## `requirements.txt`

Add:

- `fastapi>=0.111.0`
- `uvicorn[standard]>=0.29.0`
- `pydantic>=2.0.0`
- `pydantic-settings>=2.0.0`

## `.gitignore`

Add:

- `__pycache__/`
- `*.pyc`
- `node_modules/`
- `.next/`
- `out/`
- `dist/`
