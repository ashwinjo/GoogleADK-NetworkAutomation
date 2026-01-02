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