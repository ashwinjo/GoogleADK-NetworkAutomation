# 12-agent-deployment-vtxai

Please ensure you have your Google Gemini API key set in your environment variables.

```bash
export GOOGLE_API_KEY=<your-Google-Gemini-API-key>
```
---

**Vertex AI Agent Engine Deployment for Network Automation** - 

This example demonstrates deploying ADK-based network automation agents to Vertex AI Agent Engine (formerly "Reasoning Engine"), Google Cloud's enterprise-grade managed runtime for AI agents. This deployment pattern offers:

- **Managed Serverless Platform**: No infrastructure management - automatic scaling for network operations
- **Built-in State Management**: Native session and memory persistence across multi-turn conversations
- **Secure Code Execution**: Sandboxed Python execution for parsing network CLI outputs and metrics
- **Enterprise Observability**: Integrated Cloud Trace and Cloud Logging for full agent workflow visibility
- **IAM-Based Governance**: Least-privilege permissions per agent (e.g., "run tests only, no deletion")
- **Playground Integration**: Browser-based testing interface for agent interaction

Unlike Cloud Run deployments, Vertex AI Agent Engine provides specialized capabilities for stateful, long-running agent conversations with built-in memory management—ideal for complex network troubleshooting workflows that span multiple interactions.

## ADK Features Demonstrated

This project showcases Vertex AI Agent Engine deployment patterns for ADK agents:

### 1. Agent Engine Deployment

- **Agent Starter Pack Enhancement**: `enhance --adk -d agent_engine` for existing non agent workflows
- **Automated Deployment Script**: Custom deployment module with configuration management
- **Entrypoint Configuration**: `agent_engine_app` module and `agent_engine` object
- **Dependency Management**: UV-based requirements export and package handling

### 2. Resource Configuration

- **Compute Resources**: CPU (4 cores) and Memory (8Gi) allocation
- **Auto-Scaling Settings**: Min/Max instance configuration (1-10 instances)
- **Container Concurrency**: Request handling capacity (9 concurrent requests)
- **Region Selection**: Regional deployment for low-latency access

### 3. Observability & Telemetry

- **OpenTelemetry Integration**: `GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY=true`
- **Message Content Capture**: `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true`
- **Deployment Metadata**: JSON-based deployment tracking with Agent Engine IDs
- **Service Account Management**: Automatic service account provisioning

### 4. Programmatic Agent Access

- **Vertex AI Python SDK**: `vertexai` library for agent communication
- **Agent Engine Discovery**: List and retrieve deployed agents programmatically
- **Streaming Query Support**: Async streaming for real-time agent responses
- **Session Management**: User-based session tracking (`user_id` parameter)

### 5. Agent Client Implementation

- **Python Client Example**: [`vertexai_agent_client/vtxai.py`](./vertexai_agent_client/vtxai.py)
- **Authentication Handling**: Application Default Credentials (ADC) integration
- **Rich Output Formatting**: Enhanced terminal output for agent responses
- **Environment Configuration**: `.env`-based configuration management

---

## What is Vertex AI Agent Engine?

**Vertex AI Agent Engine** is Google Cloud's fully managed, enterprise-grade runtime for deploying and scaling AI agents. Key advantages for network automation:

- **No Infrastructure Management**: Serverless platform with automatic scaling
- **Native State Persistence**: Built-in session and memory management
- **Secure Execution Environment**: Sandboxed Python code execution
- **Full Observability**: Cloud Trace and Logging integration
- **IAM Governance**: Fine-grained permission control per agent

---

## Let's Deploy the Agent to Vertex AI Agent Engine

### Prerequisites

Ensure you have:

1. Google Cloud SDK installed and authenticated
2. Google Gemini API key set in environment variables
3. GCP project with Vertex AI API enabled

### Step 1: Enhance Existing Agent

If you have an existing agent, enhance it for Agent Engine deployment:

**Note**: 

If you are enhancing an existing agent that has been set to ```cloud run```, delete everything in the folderexcept the agent folder. 


```bash
uvx agent-starter-pack enhance --adk -d agent_engine
```


>If you don't have an existing agent, you can create a new one with the Agent Starter Pack:
```bash
uvx agent-starter-pack create <agent-folder-name>
```
and then in the interactive UI select "Vertex AI Agent Engine" as the deployment target.

### Step 2: Deploy to Vertex AI Agent Engine

```bash
make deploy
```
** Note** :  Agent Folder Name is `basic_agent` so we using that in place of the default `app` references

```bash
deploy:
	# Export dependencies to requirements file using uv export.
	(uv export --no-hashes --no-header --no-dev --no-emit-project --no-annotate > basic_agent/app_utils/.requirements.txt 2>/dev/null || \
	uv export --no-hashes --no-header --no-dev --no-emit-project > basic_agent/app_utils/.requirements.txt) && \
	uv run -m basic_agent.app_utils.deploy \
		--source-packages=./basic_agent \
		--entrypoint-module=basic_agent.agent_engine_app \
		--entrypoint-object=agent_engine \
		--requirements-file=basic_agent/app_utils/.requirements.txt
```

### Example Deployment Output

```bash
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🤖 DEPLOYING AGENT TO VERTEX AI AGENT ENGINE 🤖         ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

📋 Deployment Parameters:
  Project: adkstuff
  Location: us-central1
  Display Name: 12-agent-deployment-vtxai
  Min Instances: 1
  Max Instances: 10
  CPU: 4
  Memory: 8Gi
  Container Concurrency: 9

🌍 Environment Variables:
  GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY: true
  GOOGLE_CLOUD_REGION: us-central1
  NUM_WORKERS: 1
  OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT: true

✅ Deployment successful!
Service Account: service-216136305446@gcp-sa-aiplatform-re.iam.gserviceaccount.com
📊 Open Console Playground: [URL]
```

**Note**: Vertex AI Agent Engine uses a playground UI instead of ADK Web interface.

---

## Interacting with Deployed Agent

### Install Vertex AI SDK

```bash
uv add vertexai
```

### Python Client Example

```python
from vertexai import agent_engines
import vertexai

# Initialize Vertex AI
PROJECT_ID = 'adkstuff'
REGION = 'us-central1'
vertexai.init(project=PROJECT_ID, location=REGION)

# List deployed agents
agents_list = list(agent_engines.list())
if not agents_list:
    print("❌ No deployed agents found. Please deploy your agent first.")
    exit(1)

remote_agent = agents_list[0]  # Use the most recent agent

# Stream a response from the agent
import asyncio

async def get_agent_response(message):
    async for item in remote_agent.async_stream_query(
        message=message,
        user_id="user_42",  # Optional: session tracking
    ):
        print(item)

if __name__ == "__main__":
    question = "What are the best ways to deploy VPN clients? Answer in 20 words or less."
    asyncio.run(get_agent_response(question))
```

### Authentication

```bash
gcloud auth application-default login
```

### Full Working Example

See [`vertexai_agent_client/vtxai.py`](./vertexai_agent_client/vtxai.py) for a complete implementation with:
- Environment variable configuration
- Rich terminal output formatting
- Error handling and retry logic
- Session management examples

---
