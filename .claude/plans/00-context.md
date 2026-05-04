# 00 — Context

The project currently has a single `app.py` CLI chat loop using LangChain LCEL (`ChatAnthropic` → `ChatPromptTemplate` → `StrOutputParser`).

**Goal:** expose the same chat feature via a REST API (FastAPI) and build a browser UI (Next.js) on top of it.

**Constraint:** the CLI `app.py` is preserved unchanged — backend extracts the chain logic into a service layer; CLI keeps working.
