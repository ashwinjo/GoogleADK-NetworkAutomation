# 1-basic-agent

A base ReAct agent built with Google's Agent Development Kit (ADK)
Agent generated with [`googleCloudPlatform/agent-starter-pack`](https://github.com/GoogleCloudPlatform/agent-starter-pack) version `0.29.3`

Please ensure you have your Goggle Gemini API key set in your environment variables.
export GOOGLE_API_KEY=<your-Google-Gemini-API-key>

---

## Network Use Case

**Network Design Review Agent** - An AI-powered Senior Network Architect that performs comprehensive design reviews of network architectures. The agent analyzes textual descriptions of network designs given by user to identify architectural risks, anti-patterns, and missing considerations. It provides structured feedback covering:

- Failure domains and blast radius analysis
- Redundancy and high availability assessment  
- Routing and convergence behavior evaluation
- Security boundaries and traffic isolation review
- Operational complexity and day-2 operations considerations
- Scalability and future growth planning

The agent operates in a **review-only mode** (no direct network access or configuration changes), making it safe for learning and consultation purposes.

## ADK Features Demonstrated

This project showcases multiple ADK capabilities through three different implementations:

### 1. Basic Agent (`basic_agent/`)

- **Agent & App Setup**: Core ADK classes for agent definition
- **Model Configuration**: Gemini Flash 3.0 with retry options
- **System Prompts**: Detailed instruction templates for specialized agent behavior
- **Vertex AI Integration**: Cloud-based LLM execution

### 2. Advanced Configuration 
(`basic_agent_advanced_config_and_cotrol/`)
- **Output Schema**: Pydantic model-based structured outputs (`CommandReadout`)
- **Generation Controls**: 
  - Temperature control for deterministic responses
  - Token limits (`max_output_tokens`)
  - Safety settings for content filtering
- **Planning Strategies**:
  - `PlanReActPlanner`: Multi-step reasoning with planning
  - `BuiltInPlanner` with thinking config (commented example)

### 3. Programmatic Execution (`no_web_agent_run/`)

- **Runner API**: Direct agent invocation without web interface
- **Session Management**: `InMemorySessionService` for stateless operations
- **Event Streaming**: Real-time access to agent execution events
- **Headless Operation**: CLI-based agent interaction

---

Edit the Makefile to change the project name here based on the agent we will be calling

```bash 
# Launch local development server with hot-reload
local-backend-basic-agent:
	uv run uvicorn basic_agent.fast_api_app:app --host localhost --port 8000 --reload

AND in fast_api_app.py file, change the import path to the correct one

from basic_agent.app_utils.telemetry import setup_telemetry
from basic_agent.app_utils.typing import Feedback
```

---

## Troubleshooting / Known Issues

### 1. Google Cloud Logging Initialization

**Issue**: When initializing Google Cloud Logging, you need to explicitly pass the project ID to the `Client()` constructor, otherwise it may fail to initialize properly.

**Solution**: 
```python
from google.cloud import logging as google_cloud_logging
import google.auth

_, project_id = google.auth.default()
logging_client = google_cloud_logging.Client(project=project_id)  # Explicitly pass project
logger = logging_client.logger(__name__)
```

### 2. OpenAPI/Swagger Documentation Error (500 Internal Server Error on `/openapi.json`)

**Issue**: FastAPI's Swagger UI (`/docs`) may fail with "Internal Server Error" when trying to load `/openapi.json`. This is caused by ADK's internal Pydantic models containing `httpx.Client` fields that cannot be serialized to JSON schema by Pydantic 2.x.

**Error**:
```
pydantic.errors.PydanticInvalidForJsonSchema: Cannot generate a JsonSchema 
for core_schema.IsInstanceSchema (<class 'httpx.Client'>)
```

**Solution**: Override the default OpenAPI schema generation with error handling that filters out problematic routes:

```python
def custom_openapi():
    """Generate OpenAPI schema with error handling for unsupported types."""
    if app.openapi_schema:
        return app.openapi_schema
    
    try:
        from fastapi.openapi.utils import get_openapi
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
        app.openapi_schema = openapi_schema
        return app.openapi_schema
    except Exception as e:
        # Filter routes that can be documented and skip problematic ones
        # See fast_api_app.py for full implementation
        ...

app.openapi = custom_openapi
```

This allows the Swagger UI to load successfully, showing your custom endpoints while gracefully handling ADK's internal routes that cannot be documented.