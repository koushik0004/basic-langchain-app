# 03 — Frontend (`frontend/`)

Next.js app following `.claude/docs/frontend-conventions.md`.

## Scaffold (run from repo root)

```bash
npx create-next-app@latest frontend --typescript --tailwind --app --no-src-dir --import-alias "@/*" --no-eslint
cd frontend && npm install @tanstack/react-query
```

## Files to write/replace after scaffold

1. **`frontend/types.ts`** — `ChatRequest`, `ChatResponse`, `Message` interfaces (no `any`).
2. **`frontend/lib/api.ts`** — typed `sendMessage(req: ChatRequest): Promise<ChatResponse>` fetch wrapper; base URL from `NEXT_PUBLIC_API_URL ?? "http://localhost:8000"`.
3. **`frontend/components/features/ChatBox.tsx`** — `"use client"` component; `useMutation` from TanStack Query; message list state; user/assistant bubble layout with Tailwind.
4. **`frontend/app/layout.tsx`** — replace scaffold; add `QueryClientProvider` wrapper (`"use client"`).
5. **`frontend/app/page.tsx`** — Server Component; renders `<ChatBox />`.
