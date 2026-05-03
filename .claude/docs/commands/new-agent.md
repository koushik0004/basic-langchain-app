# New LangGraph Agent

Load @docs/langgraph-patterns.md and scaffold an agent graph.

Required args: $AGENT_TYPE (single|supervisor|subgraph)

Steps:
1. Define State TypedDict
2. Scaffold nodes and edges per pattern
3. Wire entry/exit, conditional edges
4. Show compile() call with checkpointer placeholder
5. Stop — no tests, no runner script unless asked
