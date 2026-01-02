# 3-agent-session-context

A base ReAct agent built with Google's Agent Development Kit (ADK)
Agent generated with [`googleCloudPlatform/agent-starter-pack`](https://github.com/GoogleCloudPlatform/agent-starter-pack) version `0.29.3`

Please ensure you have your Goggle Gemini API key set in your environment variables.
export GOOGLE_API_KEY=<your-Google-Gemini-API-key>

---

## Network Use Case

**Multi-Turn NOC Assistant** - A context-aware Network Operations Center (NOC) troubleshooting assistant that maintains state across multiple conversation turns. Unlike stateless agents, this implementation demonstrates how to:

- **Persist Troubleshooting Context**: Remember which router is being investigated across multiple questions
- **Build Progressive Diagnostics**: Each interaction builds on previous tool calls and findings
- **Avoid Redundant Queries**: The agent recalls prior context instead of re-asking for information
- **Maintain Session Continuity**: Track the active router, last tool used, and historical interactions

**Real-World Scenario**: A NOC engineer troubleshoots a router over multiple interactions:
1. "Check BGP summary for router R1"
2. "What's wrong with neighbor 192.168.1.3?" ← Agent remembers R1 context
3. "Show me the interface status" ← Agent still knows we're working on R1

This pattern mirrors actual NOC workflows where troubleshooting happens incrementally, not in single-shot queries.

## ADK Features Demonstrated

This project showcases stateful agent capabilities and session management:

### 1. Session Management

- **InMemorySessionService**: Session creation, retrieval, and deletion
- **Session Properties**: Access to `id`, `app_name`, `user_id`, `state`, `events`, and `last_update_time`
- **State Initialization**: Pre-populate session state with initial values
- **Session Lifecycle**: Create, use, and clean up sessions programmatically

### 2. ToolContext - State Persistence

- **Tool State Management**: Store data in `tool_context.state` during tool execution
- **Cross-Turn Data Sharing**: Information persisted across multiple agent turns
- **Context Tracking**: Record active router and last tool used for continuity
- **Structured State Updates**: Dictionary-based state management within tools

### 3. ReadonlyContext - Dynamic Instructions

- **State-Aware Instructions**: Agent instructions that adapt based on current session state
- **Dynamic Prompting**: Instruction changes reflect active troubleshooting context
- **Context Injection**: Current router displayed in agent's system prompt
- **Reactive Guidance**: Agent behavior adapts to what it already knows

### 4. FunctionTool Wrapper

- **Tool Context Integration**: Wrapping Python functions with `FunctionTool` for state access
- **Enhanced Tool Capabilities**: Tools gain access to session state via `tool_context` parameter
- **State Injection**: ADK automatically provides `ToolContext` to wrapped functions

### 5. Output Key Management

- **Response Persistence**: `output_key="response"` stores LLM responses in session state
- **Historical Tracking**: Prior agent responses accessible in `session.state["response"]`
- **Audit Trail**: Built-in conversation history for analysis or debugging

### 6. Multi-Turn Conversations

- **Stateful Interactions**: Each turn builds on previous conversation history
- **Context Retention**: Agent "remembers" prior facts without re-querying tools
- **Incremental Problem Solving**: Progressive diagnosis across multiple interactions
- **Natural Conversation Flow**: Mimics real engineer-to-engineer troubleshooting dialogue

---
