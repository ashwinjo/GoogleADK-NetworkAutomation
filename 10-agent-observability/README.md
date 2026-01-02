# 10-agent-observability

A base ReAct agent built with Google's Agent Development Kit (ADK)
Agent generated with [`googleCloudPlatform/agent-starter-pack`](https://github.com/GoogleCloudPlatform/agent-starter-pack) version `0.29.3`

---

## Network Use Case

**Production Observability & Monitoring** - Demonstrates comprehensive observability patterns for production agent deployments. In network operations, observability is critical for:

- **Incident Response**: Debugging agent behavior during network outages
- **Performance Optimization**: Identifying slow tool calls or model latency
- **Compliance & Auditing**: Tracking all agent actions for regulatory requirements
- **Cost Management**: Understanding LLM token usage and API costs
- **Quality Assurance**: Validating agent decision-making through conversation traces

### Real-World Scenario

**NOC Agent Debugging**:
- Agent fails to diagnose router issue correctly
- Ops team needs to review: What tools were called? What did they return? How did the LLM reason?
- Observability traces show: Agent called `ping_router` but misinterpreted packet loss percentage
- Root cause identified: Tool output parsing issue
- Fix deployed and validated through trace comparison

**Cost Optimization**:
- Finance notices high Gemini API costs
- Observability shows: Agent making redundant tool calls in loops
- Traces reveal: Agent not caching results, re-calling same tool multiple times
- Optimization: Implement tool response caching
- Cost reduction: 40% decrease in API calls

---

## ADK Features Demonstrated

This project showcases two observability approaches:

### 1. Basic Logging (`basic_logging/`)

**Built-in Python Logging**

- **Standard Library**: Uses Python's `logging` module
- **Log Levels**: DEBUG, INFO, WARNING, ERROR for different event types
- **Structured Format**: `'%(asctime)s - %(levelname)s - %(name)s - %(message)s'`
- **Console Output**: Logs printed to terminal for local development

**What Gets Logged**:
- Agent initialization and configuration
- Tool invocations with arguments
- Model requests and responses
- Session state changes
- Error stack traces

**Code Pattern**:
```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)

# ADK automatically logs to this logger
root_agent = Agent(
    name="root_agent",
    model=Gemini(...),
    tools=[get_weather, get_current_time],
)
```

> You need to use -v tag when running your agent <br>

> uv run adk web . -v --port 8501 --reload_agents

**Advantages**:
- Zero external dependencies
- Simple setup for local development
- Works offline
- Lightweight performance overhead

**Limitations**:
- No structured trace visualization
- Difficult to query across multiple sessions
- No LLM-specific metrics (tokens, cost)
- Limited to single process

**Best For**:
- Local development and debugging
- Simple agents with few tools
- Quick prototyping
- Log file analysis

### 2. Third-Party Logging (`third_party_logging/`)

**Opik Integration - Advanced LLM Observability**

- **Opik**: Open-source LLM observability platform (by Comet)
- **ADK Integration**: `OpikTracer` + `track_adk_agent_recursive()`
- **Rich Traces**: Hierarchical view of agent → model → tools
- **LLM Metrics**: Token usage, cost, latency, model parameters
- **Web UI**: Visual trace explorer and dashboard

**What Gets Tracked**:
- **Agent Traces**: Complete conversation flows
- **Model Calls**: Prompt content, responses, token counts
- **Tool Executions**: Tool name, arguments, results, duration
- **Metadata**: Environment, model version, tags
- **Spans**: Nested execution hierarchy

**Code Pattern**:
```python
from opik.integrations.adk import OpikTracer, track_adk_agent_recursive

# Configure Opik tracer
opik_tracer = OpikTracer(
    name="network-monitoring-agent",
    tags=["production", "network", "monitoring"],
    metadata={
        "environment": "production",
        "model": "gemini-3-flash-preview",
        "framework": "google-adk",
        "team": "noc-ops"
    },
    project_name="network-operations"
)

# Instrument agent - single function call
track_adk_agent_recursive(root_agent, opik_tracer)
```

**Opik Dashboard Features**:
- **Trace Explorer**: Visual tree of agent execution
- **Filter & Search**: Query by tag, model, duration, error status
- **Cost Analysis**: Track token usage and estimated API costs
- **Performance Metrics**: Latency distributions, slow tool identification
- **Comparison**: Compare traces side-by-side for debugging
- **Alerts**: Set up alerts for errors or performance degradation

**Advantages**:
- **Visual Debugging**: See execution flow graphically
- **LLM-Specific Metrics**: Token counts, model parameters
- **Cross-Session Analysis**: Query across multiple conversations
- **Team Collaboration**: Share traces via web UI
- **Cost Tracking**: Monitor LLM API costs
- **Production-Ready**: Handles high-volume logging

**Setup Requirements**:
```bash
pip install opik
# Set up Opik account (free tier available)
# Configure OPIK_API_KEY environment variable
```

**Best For**:
- Production deployments
- Multi-agent systems
- LLM cost optimization
- Team collaboration and debugging
- Compliance and audit trails

---

## Feature Comparison

| Feature | Basic Logging | Opik (Third-Party) |
|---------|--------------|-------------------|
| **Setup Complexity** | Minimal | Medium (requires account) |
| **Dependencies** | None | `opik` package |
| **Visualization** | Text logs | Interactive web UI |
| **Token Tracking** | No | Yes (with costs) |
| **Cross-Session Queries** | Manual (grep) | Built-in search |
| **Performance Overhead** | Minimal | Low-Medium |
| **Cost** | Free | Free tier + paid plans |
| **Best For** | Development | Production |

---

## Observability Best Practices

### 1. Development vs Production

**Development (Basic Logging)**:
- Use Python logging for quick iterations
- Log level: DEBUG for maximum visibility
- Console output sufficient

**Production (Third-Party Logging)**:
- Use structured observability platform (Opik, Langfuse, etc.)
- Log level: INFO (DEBUG only for troubleshooting)
- Centralized logging service (GCP Cloud Logging, Datadog, etc.)

### 2. What to Log

**Always Log**:
- Agent initialization (model, tools, config)
- Tool invocations (name, args, result, duration)
- Model calls (prompt summary, token count, latency)
- Errors and exceptions (with full stack trace)
- Session IDs for correlation

**Conditionally Log**:
- Full prompt/response content (privacy/security considerations)
- User PII (mask or exclude)
- Sensitive data (passwords, keys - never log)

### 3. Metadata & Tagging

**Useful Tags**:
- Environment: `development`, `staging`, `production`
- Agent type: `network-monitoring`, `security-analysis`
- Model: `gemini-3-flash-preview`, `gemini-2.0-flash`
- Team: `noc-ops`, `security-team`
- Customer: `customer-id-123`

**Useful Metadata**:
- Model parameters: temperature, max_tokens
- Tool set version: `tools-v2.1.0`
- Deployment: Cloud Run service name/version

### 4. Alerting & Monitoring

**Key Metrics to Monitor**:
- Error rate: % of agent runs that fail
- Latency: p50, p95, p99 response times
- Token usage: Total tokens/day for cost tracking
- Tool failures: Which tools fail most often
- Loop detection: Agent stuck in reasoning loops

**Alert On**:
- Error rate > 5%
- Latency p95 > 30 seconds
- Daily token usage > budget threshold
- Tool failure rate > 10%
- Agent loop detected (>10 iterations)

---

## Integration Examples

### Google Cloud Logging

```python
import google.cloud.logging

client = google.cloud.logging.Client()
client.setup_logging()

# Now Python logs automatically go to Cloud Logging
logging.info("Agent initialized")
```

### Custom Telemetry

```python
from google.adk.agents.callback_context import CallbackContext
from typing import Optional

def log_tool_usage(tool: BaseTool, args: Dict, tool_context: ToolContext, 
                   tool_response: Dict) -> Optional[Dict]:
    """After-tool callback for custom logging"""
    duration = calculate_duration()
    logging.info(f"Tool: {tool.name}, Duration: {duration}ms, Args: {args}")
    
    # Send to custom telemetry system
    send_to_datadog({
        "metric": "agent.tool.duration",
        "value": duration,
        "tags": [f"tool:{tool.name}", "environment:production"]
    })
    return None

root_agent = Agent(
    after_tool_callback=log_tool_usage,
    ...
)
---