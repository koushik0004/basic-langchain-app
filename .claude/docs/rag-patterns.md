# RAG Patterns

## Retrieval
- Default chunking: 512 tokens, 10% overlap
- Prefer `RecursiveCharacterTextSplitter` for unstructured text
- Use metadata filtering before vector search when possible (reduces retrieved k)
- Always set `k` explicitly; never rely on defaults

## Embeddings
- Local dev: `text-embedding-3-small`
- Prod: `text-embedding-3-large` or provider-specific
- Cache embeddings; never re-embed unchanged docs

## Vector Stores
- Dev: Chroma (in-memory or persist_directory)
- Prod: Qdrant or Pinecone
- Always namespace/collection-isolate per env

## Agentic RAG
- Retrieval as a Tool: wrap retriever in `@tool` with clear docstring
- Use `RunnableWithMessageHistory` for stateful chains
- Grade retrieved docs before generation (relevance check node)
- Fallback: web search tool if retrieval score < threshold

## Prompts
- System prompt in `ChatPromptTemplate.from_messages`
- Keep system prompts < 300 tokens
- Separate retrieval prompt from generation prompt
- Never embed full retrieved docs in system; use human turn

## Evaluation
- Use `ragas` for answer relevancy, faithfulness, context recall
- Log: query, retrieved_docs, answer, latency per request
