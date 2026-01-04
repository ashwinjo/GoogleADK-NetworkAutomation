# 2-basic-agent-with-tools

Please ensure you have your Goggle Gemini API key set in your environment variables.
```bash
export GOOGLE_API_KEY=<your-Google-Gemini-API-key>
```

---

## Network Use Case

**Network Troubleshooting & Diagnostics Toolkit** - A collection of agents demonstrating different tool integration patterns for network operations:

- **BGP Troubleshooting** (`agent_custom_tools/`) - Diagnose BGP session issues with custom diagnostic functions
- **Parallel Network Diagnostics** (`parallel_functions_calls/`) - Run device health, latency, and utilization checks simultaneously
- **Subnet Calculations** (`agent_mcp_tools_calls/`) - Calculate subnets via external MCP tool servers
- **Knowledge-Based Assistance** (`agent_builtin_tools/`) - Use Google Search for RFC and documentation lookups

The implementations showcase how agents reason through network problems using observable data, parallel execution for performance, and external tool integrations via MCP.

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

**Network Diagnostics Agent** - Demonstrates parallel execution of network observability tools for faster troubleshooting.

- **Async Tool Execution**: Multiple network tools run simultaneously
- **ToolContext State Management**: Shared state tracking across parallel executions
- **Simulated Network Operations**: Realistic async delays mimicking I/O-bound operations

**Tools Included:**
| Tool | Purpose | Simulated Delay |
|------|---------|-----------------|
| `get_device_health` | CPU, memory, status for routers/firewalls | 2s |
| `get_link_utilization` | Bandwidth usage between sites | 1.5s |
| `measure_latency` | RTT between datacenter/branch locations | 1s |

**Example Query:**
> "Check the health of router1 and router2, measure latency between dc1 and dc2, and check link utilization"

The agent runs all tools in parallel, reducing total wait time from ~4.5s (sequential) to ~2s (parallel).

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

### 6. MCP Tools (`agent_mcp_tools_calls/`)

**MCP (Model Context Protocol) Integration** - Demonstrates connecting to external MCP tool servers using different transport methods.

**Two MCP Toolsets Included:**

| Toolset | Transport | Description |
|---------|-----------|-------------|
| **Subnet Calculator** | `StdioConnectionParams` | Uses `npx supergateway` to connect to SSE-based MCP server |
| **Hugging Face** | `StreamableHTTPServerParams` | Direct HTTP connection with Bearer token auth |

**Connection Methods:**

```python
# Method 1: Stdio via supergateway (for SSE servers)
mcp_subnet_calculator_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=["-y", "supergateway", "--sse", "https://mcp-subnet-calculator.mteke.com/sse"]
        ),
        timeout=30,
    ),
)

# Method 2: Direct HTTP with auth headers
hugging_face_toolset = McpToolset(
    connection_params=StreamableHTTPServerParams(
        url="https://huggingface.co/mcp",
        headers={"Authorization": f"Bearer {HUGGING_FACE_TOKEN}"},
    ),
)
```

**Environment Variables Required:**
- `HUGGING_FACE_TOKEN` - For Hugging Face MCP access (get from huggingface.co/settings/tokens)

**Switching Agents:**
Uncomment the desired `app = App(...)` line at the bottom of `agent.py` to switch between subnet calculator and Hugging Face agents.

---