# 4-agent-human-in-the-loop

A base ReAct agent built with Google's Agent Development Kit (ADK)
Agent generated with [`googleCloudPlatform/agent-starter-pack`](https://github.com/GoogleCloudPlatform/agent-starter-pack) version `0.29.3`

Please ensure you have your Goggle Gemini API key set in your environment variables.
export GOOGLE_API_KEY=<your-Google-Gemini-API-key>

---

## Network Use Case

**Configuration Change Approval System** - A safety-first network configuration management system that enforces human approval for risky operations. This implementation demonstrates real-world change control workflows where:

- **Safe Operations Execute Freely**: Read operations (show commands, status checks) proceed without interruption
- **Risky Operations Require Approval**: Configuration writes pause execution and request human authorization
- **Policy-Based Gating**: Different routers have different approval requirements based on criticality
- **Audit Trail**: All approval requests and responses are logged for compliance

**Real-World Scenarios**:

1. **SPOF Protection**: Critical routers (single points of failure) always require approval
2. **Business Hours Policy**: Configuration changes during peak hours trigger human review
3. **Change Freeze Windows**: Agent respects maintenance windows and blocks changes automatically
4. **Multi-Stage Approval**: Different configuration types require different approval levels

This pattern is essential for production network operations where autonomous changes must be balanced with operational safety and compliance requirements.

## ADK Features Demonstrated

This project showcases two distinct Human-in-the-Loop (HITL) implementation patterns:

### 1. Boolean Confirmation Pattern (`agent_hitl_boolean/`)

**Simple, Policy-Based Approval**

- **`require_confirmation` Parameter**: Attach a boolean function to FunctionTool
- **Policy Functions**: `confirmation_if_not_spof_router(router_name) -> bool`
  - Returns `True` when human approval is needed
  - Returns `False` for auto-approved operations
- **Declarative Gating**: Agent automatically pauses when function returns True
- **Example Policy**: Router "r1-sea3" is a SPOF → requires approval for writes
- **Use Case**: Simple yes/no approval gates based on router identity, time, or other context

**Key Code Pattern**:
```python
FunctionTool(
    write_router_config,
    require_confirmation=confirmation_if_not_spof_router
)
```

### 2. Tool-Based Confirmation Wizard (`agent_hitl_tool_use/`)

**Advanced, Custom Approval Workflows**

- **`ToolContext.request_confirmation()`**: Explicitly request human input with custom payloads
- **`ToolContext.tool_confirmation`**: Access human's approval decision and additional data
- **Custom Payloads**: Include structured data in approval requests (`ok_to_write`, etc.)
- **Hint System**: Provide guidance to human reviewers about what they're approving
- **Conditional Logic**: Different approval paths based on payload content
- **State Management**: Track approval status (pending, approved, rejected)

**Key Code Pattern**:
```python
if not tool_confirmation:
    tool_context.request_confirmation(
        hint="This will modify router config",
        payload={"ok_to_write": False}
    )
    return {"status": "pending_approval"}

ok_to_write = tool_confirmation.payload.get("ok_to_write")
if ok_to_write:
    return write_router_config(router_name)
```

### 3. Resumability (Both Implementations)

- **ResumabilityConfig**: `is_resumable=True` enables pause/resume capability
- **Session Persistence**: Agent state preserved while awaiting human response
- **Event Loop Management**: Execution suspends at confirmation point
- **Continuation**: Agent resumes from exact point after approval/rejection

### 4. Safe vs Risky Tool Separation

- **Read Operations**: `read_router_config` never requires approval
- **Write Operations**: `write_router_config` protected by HITL
- **Tool Categorization**: Clear separation between observational and mutating operations
- **Risk-Based Access Control**: Tools annotated with safety requirements

### 5. Low-Temperature Generation

- **Deterministic Behavior**: `temperature=0.1` for consistent, predictable agent actions
- **Production Safety**: Reduced creativity ensures agent follows exact procedures
- **Compliance-Friendly**: Reproducible behavior for audit and regulatory requirements

---

## Comparison: When to Use Each Pattern

| Pattern | Best For | Complexity | Flexibility |
|---------|----------|------------|-------------|
| **Boolean** | Simple approval gates, policy-based decisions | Low | Low |
| **Tool-Based** | Custom workflows, multi-field approvals, conditional logic | Medium | High |

**Choose Boolean Pattern** when:
- Simple yes/no approval is sufficient
- Decision is based on input parameters only
- No additional data needed from human reviewer

**Choose Tool-Based Pattern** when:
- Need custom approval payloads
- Require reviewer to provide additional information
- Implementing multi-stage or conditional workflows
- Building approval wizards with multiple steps

---

## Project Structure

This project is organized as follows:

```
4-agent-human-in-the-loop/
├── app/                 # Core application code
│   ├── agent.py         # Main agent logic
│   ├── fast_api_app.py  # FastAPI Backend server
│   └── app_utils/       # App utilities and helpers
├── tests/               # Unit, integration, and load tests
├── Makefile             # Makefile for common commands
├── GEMINI.md            # AI-assisted development guide
└── pyproject.toml       # Project dependencies and configuration
```

> 💡 **Tip:** Use [Gemini CLI](https://github.com/google-gemini/gemini-cli) for AI-assisted development - project context is pre-configured in `GEMINI.md`.

## Requirements

Before you begin, ensure you have:
- **uv**: Python package manager (used for all dependency management in this project) - [Install](https://docs.astral.sh/uv/getting-started/installation/) ([add packages](https://docs.astral.sh/uv/concepts/dependencies/) with `uv add <package>`)
- **Google Cloud SDK**: For GCP services - [Install](https://cloud.google.com/sdk/docs/install)
- **make**: Build automation tool - [Install](https://www.gnu.org/software/make/) (pre-installed on most Unix-based systems)


## Quick Start (Local Testing)

Install required packages and launch the local development environment:

```bash
make install && make playground
```
> **📊 Observability Note:** Agent telemetry (Cloud Trace) is always enabled. Prompt-response logging (GCS, BigQuery, Cloud Logging) is **disabled** locally, **enabled by default** in deployed environments (metadata only - no prompts/responses). See [Monitoring and Observability](#monitoring-and-observability) for details.

## Commands

| Command              | Description                                                                                 |
| -------------------- | ------------------------------------------------------------------------------------------- |
| `make install`       | Install all required dependencies using uv                                                  |
| `make playground`    | Launch local development environment with backend and frontend - leveraging `adk web` command.|
| `make deploy`        | Deploy agent to Cloud Run (use `IAP=true` to enable Identity-Aware Proxy, `PORT=8080` to specify container port) |
| `make local-backend` | Launch local development server with hot-reload |
| `make test`          | Run unit and integration tests                                                              |
| `make lint`          | Run code quality checks (codespell, ruff, mypy)                                             |

For full command options and usage, refer to the [Makefile](Makefile).


## Usage

This template follows a "bring your own agent" approach - you focus on your business logic, and the template handles everything else (UI, infrastructure, deployment, monitoring).
1. **Develop:** Edit your agent logic in `app/agent.py`.
2. **Test:** Explore your agent functionality using the local playground with `make playground`. The playground automatically reloads your agent on code changes.
3. **Enhance:** When ready for production, run `uvx agent-starter-pack enhance` to add CI/CD pipelines, Terraform infrastructure, and evaluation notebooks.

The project includes a `GEMINI.md` file that provides context for AI tools like Gemini CLI when asking questions about your template.


## Deployment

You can deploy your agent to a Dev Environment using the following command:

```bash
gcloud config set project <your-dev-project-id>
make deploy
```


When ready for production deployment with CI/CD pipelines and Terraform infrastructure, run `uvx agent-starter-pack enhance` to add these capabilities.

## Monitoring and Observability

The application provides two levels of observability:

**1. Agent Telemetry Events (Always Enabled)**
- OpenTelemetry traces and spans exported to **Cloud Trace**
- Tracks agent execution, latency, and system metrics

**2. Prompt-Response Logging (Configurable)**
- GenAI instrumentation captures LLM interactions (tokens, model, timing)
- Exported to **Google Cloud Storage** (JSONL), **BigQuery** (external tables), and **Cloud Logging** (dedicated bucket)

| Environment | Prompt-Response Logging |
|-------------|-------------------------|
| **Local Development** (`make playground`) | ❌ Disabled by default |

**To enable locally:** Set `LOGS_BUCKET_NAME` and `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=NO_CONTENT`.

See the [observability guide](https://googlecloudplatform.github.io/agent-starter-pack/guide/observability.html) for detailed instructions, example queries, and visualization options.
