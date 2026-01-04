# 14-agent-ollama

A base ReAct agent built with Google's Agent Development Kit (ADK) using **local LLM execution via Ollama**.
Agent generated with [`googleCloudPlatform/agent-starter-pack`](https://github.com/GoogleCloudPlatform/agent-starter-pack) version `0.29.3`

Please ensure you have Ollama running locally with your preferred model.

```bash
# Install Ollama (https://ollama.ai)
curl -fsSL https://ollama.com/install.sh | sh

# Pull the default model (gemma3n)
ollama pull gemma3n

# Or use a different model by setting environment variables
export OLLAMA_MODEL=llama3.2
export OLLAMA_API_BASE=http://localhost:11434
```

---

## Network Use Case

**Local LLM Network Design Review Agent** - An AI-powered Senior Network Architect that performs comprehensive design reviews of network architectures, running entirely on **local infrastructure**. This is critical for:

- **🔒 Sensitive Environments** - Network data that cannot leave the premises (air-gapped networks, defense, financial institutions)
- **📡 Offline Operations** - NOC environments without reliable internet access
- **💰 Cost Control** - Avoid per-token API costs for high-volume internal usage
- **⚡ Low Latency** - Local inference eliminates network round-trips to cloud APIs

The agent analyzes textual descriptions of network designs to identify:

- Failure domains and blast radius analysis
- Redundancy and high availability assessment
- Routing and convergence behavior evaluation
- Security boundaries and traffic isolation review
- Operational complexity and day-2 operations considerations
- Scalability and future growth planning

The agent operates in a **review-only mode** (no direct network access or configuration changes), making it safe for learning and consultation purposes.

---

## ADK Features Demonstrated

This project showcases how to run ADK agents with **local LLMs** instead of cloud-hosted models:

### 1. LiteLLM Integration (`app/agent.py`)

- **LiteLlm Model Wrapper**: ADK's adapter for non-Google models
- **Ollama Backend**: Local LLM serving via Ollama
- **Model Flexibility**: Easy switching between local models (Gemma, Llama, Mistral, etc.)
- **Environment Configuration**: Configurable API base and model selection

```python
from google.adk.models.lite_llm import LiteLlm

OLLAMA_API_BASE = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3n")

ollama_llm = LiteLlm(
    model=f"ollama_chat/{OLLAMA_MODEL}",
    api_base=OLLAMA_API_BASE,
)
```

### 2. Hybrid Model Support

- **Cloud Fallback**: Can use Gemini as primary with Ollama as backup (or vice versa)
- **A/B Testing**: Compare local vs cloud model responses
- **Cost Optimization**: Route simple queries to local models, complex ones to cloud

### 3. Standard ADK Features

- **Agent & App Setup**: Core ADK classes for agent definition
- **System Prompts**: Detailed instruction templates for specialized agent behavior
- **Structured Output**: Consistent response format for design reviews

---

## Switching Between Models

### Use Ollama (Local)

Edit `app/agent.py` to use the local LLM:

```python
root_agent = Agent(
    name="root_agent",
    model=ollama_llm,  # Use local Ollama model
    description="Network Design Review Agent",
    instruction=SYSTEM_PROMPT
)
```

### Use Gemini (Cloud)

The default configuration uses Gemini:

```python
root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-3-flash-preview",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    description="Network Design Review Agent",
    instruction=SYSTEM_PROMPT
)
```

---

## Quick Start

```bash
# 1. Start Ollama with your model
ollama serve &
ollama pull gemma3n

# 2. Install dependencies and launch playground
make install && make playground
```

---

## Commands

| Command              | Description                                                                                 |
| -------------------- | ------------------------------------------------------------------------------------------- |
| `make install`       | Install all required dependencies using uv                                                  |
| `make playground`    | Launch local development environment with ADK web interface                                 |
| `make local-backend` | Launch local development server with hot-reload                                             |
| `make test`          | Run unit and integration tests                                                              |
| `make lint`          | Run code quality checks (codespell, ruff, mypy)                                             |

---

## Supported Local Models
Any model supported by Ollama works with this setup:

---

## Troubleshooting / Known Issues

### 1. Ollama Connection Refused

**Issue**: Agent fails to connect to Ollama with "Connection refused" error.

**Solution**: Ensure Ollama is running:
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not, start it
ollama serve
```

### 2. Model Not Found

**Issue**: Error indicating the model doesn't exist.

**Solution**: Pull the model first:
```bash
ollama pull gemma3n  # or your preferred model
```

### 3. Slow Inference on CPU

**Issue**: Local inference is very slow without GPU.

**Solution**: 
- Use a smaller model (e.g., `gemma3n:2b` instead of `gemma3n:9b`)
- Ensure GPU acceleration is enabled if available
- Consider using quantized models (e.g., `llama3.2:3b-q4_0`)

### 4. Memory Issues

**Issue**: Out of memory errors when loading large models.

**Solution**: 
- Use smaller/quantized models
- Close other applications
- Increase swap space
- Set `OLLAMA_MAX_LOADED_MODELS=1` to limit concurrent models