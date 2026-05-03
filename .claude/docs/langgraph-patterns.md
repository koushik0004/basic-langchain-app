# LangGraph Patterns

## State
- Always use `TypedDict` for graph state
- Keep state flat; avoid nested dicts unless necessary
- Add `messages: Annotated[list, add_messages]` for conversation memory

## Graph Structure
- Entry: `START` → planner/router node
- Always define `END` transitions explicitly
- Use conditional edges (`add_conditional_edges`) for branching
- Keep nodes single-responsibility (one action per node)

## Nodes
- Node = pure function: `(state: State) -> dict`
- Return only keys being updated, not full state
- Log node entry/exit in debug mode only

## Tools
- Wrap all external calls as `@tool` with typed args
- Tool errors must be caught and returned as `ToolMessage` with `is_error=True`
- Parallel tool calls: use `Send` API for fan-out

## Checkpointing (persistence)
- Dev: `MemorySaver`
- Prod: `PostgresSaver` or `RedisSaver`
- Thread ID = session/user ID for isolation

## Common Patterns
```python
# Supervisor multi-agent
builder = StateGraph(State)
builder.add_node("supervisor", supervisor_node)
builder.add_node("researcher", researcher_node)
builder.add_node("coder", coder_node)
builder.add_conditional_edges("supervisor", route_fn)

# Subgraph
subgraph = subgraph_builder.compile()
main_graph.add_node("subgraph", subgraph)
```

## Avoid
- Don't mutate state in-place; always return new dict
- Don't call LLM directly in edge functions; only in nodes
- Don't store large artifacts in state; use external store + reference
