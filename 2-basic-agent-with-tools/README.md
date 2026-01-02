# 2-basic-agent-with-tools

A base ReAct agent built with Google's Agent Development Kit (ADK)
Agent generated with [`googleCloudPlatform/agent-starter-pack`](https://github.com/GoogleCloudPlatform/agent-starter-pack) version `0.29.3`

Please ensure you have your Goggle Gemini API key set in your environment variables.
export GOOGLE_API_KEY=<your-Google-Gemini-API-key>

---

## Network Use Case

**BGP Troubleshooting Assistant** - An intelligent agent system that diagnoses BGP session issues using structured troubleshooting workflows. The agent follows a systematic React pattern to:

- Assess BGP neighbor health by analyzing session states
- Identify misbehaving or unhealthy peers through multiple diagnostic checks
- Investigate interface status for connectivity issues
- Analyze routing information and prefix mismatches
- Provide actionable, evidence-based recommendations

The implementation demonstrates various tool integration patterns - from custom network diagnostic functions to built-in Google Search for knowledge-based assistance, showcasing how agents reason through network problems using observable data rather than assumptions.

## ADK Features Demonstrated

This project showcases comprehensive tool integration capabilities through six different implementations:

### 1. Custom Tools (`agent_custom_tools/`)

- **Custom Python Functions as Tools**: Direct integration of network diagnostic functions
- **React Pattern**: Structured observation → analysis → action workflow
- **Tool Declarations**: `get_bgp_summary`, `get_interface_status`, `get_bgp_routes`
- **Structured Troubleshooting**: Multi-step reasoning with explicit tool usage rules
- **Mock Network Data**: Safe simulation of BGP neighbor states, interface status, and routing tables

### 2. Built-in Tools (`agent_builtin_tools/`)

- **Google Search Integration**: Using ADK's built-in `google_search` tool
- **Knowledge-Based Assistance**: Public documentation and RFC-based troubleshooting
- **Citation Requirements**: Evidence-based recommendations with source attribution
- **No Network Access**: Pure knowledge retrieval mode for training/reference scenarios

### 3. Parallel Function Calls (`parallel_functions_calls/`)

- **Async Tool Execution**: Multiple tools executing simultaneously for performance
- **Thread Safety**: Safe concurrent execution with `ToolContext` state management
- **Performance Optimization**: Reduced latency through parallel data gathering
- **Multiple Data Sources**: Weather, currency, distance, and population tools demonstrating scalability
- **Context State Management**: Tracking concurrent requests safely across parallel executions

### 4. Agent as Tool (`agent_as_tool/`)

- **Multi-Agent Architecture**: Composing agents as tools using `AgentTool`
- **Tool Isolation Pattern**: Required when using exclusive tools (Google Search, Code Execution)
- **Hierarchical Agent Systems**: Root agent orchestrating specialized sub-agents
- **Tool Constraint Handling**: Working around single-tool-per-agent limitations
- **Delegation Pattern**: Root agent delegates to `get_bgp_summary_agent` and `google_search_agent`

### 5. Google Cloud Tools (`agent_google_cloud_tools/`)

- **MCP Integration**: Model Context Protocol server connectivity
- **API Registry**: Dynamic tool discovery via `ApiRegistry`
- **Google Maps Tools**: Real Google Cloud service integration
- **External Service Integration**: Production-ready cloud tool usage
- **Project-Based Configuration**: Cloud project ID management for service calls

### 6. MCP Tools (Work in Progress) (`agent_mcp_tools_calls/`)

- **Placeholder Implementation**: Framework for custom MCP server integration
- **Network Tool Expansion**: Future integration point for network device APIs

---