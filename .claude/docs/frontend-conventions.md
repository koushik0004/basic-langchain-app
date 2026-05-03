# Frontend Conventions (React / Next.js)

## Stack
- Next.js App Router (not Pages)
- TypeScript strict mode
- Tailwind CSS
- React Query (TanStack) for server state
- Zustand for client state (if needed)

## File Structure
```
app/
  (routes)/
  layout.tsx
  page.tsx
components/
  ui/          # primitives (shadcn or custom)
  features/    # domain components
lib/
  api.ts       # typed fetch wrappers
  types.ts     # shared types
```

## Component Rules
- Functional components only
- Props interface above component, not inline
- Server Components by default; add `"use client"` only when needed
- No prop drilling >2 levels; use context or state manager

## API Integration
- All API calls via `lib/api.ts` typed wrappers
- Use React Query `useQuery` / `useMutation`
- SSE streaming: `EventSource` or `fetch` with `ReadableStream`

## Streaming LLM UI
```tsx
// Streaming chat pattern
const [text, setText] = useState("")
const reader = res.body?.getReader()
while (true) {
  const { done, value } = await reader.read()
  if (done) break
  setText(prev => prev + decoder.decode(value))
}
```

## Styling
- Tailwind only; no CSS modules unless component is highly isolated
- Mobile-first breakpoints
- Dark mode via `class` strategy

## Avoid
- `any` type
- `useEffect` for data fetching (use React Query)
- Default exports for components (use named exports)
