# 🚀 Google Agent Development Kit (ADK) for Network Engineers

[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Google ADK](https://img.shields.io/badge/Google_ADK-Latest-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)](https://cloud.google.com/agent-development-kit)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![UV](https://img.shields.io/badge/UV-Package_Manager-blueviolet?style=for-the-badge)](https://docs.astral.sh/uv/)
[![MCP](https://img.shields.io/badge/MCP-Enabled-00C853?style=for-the-badge)](https://modelcontextprotocol.io/)

> **Build trustworthy, production-ready AI agents for network automation and operations.**

---

## 📖 Overview

Network engineers need AI systems that are **understandable**, **trustworthy**, and **operationally relevant**. Traditional script-based automation is brittle and lacks contextual reasoning, while black-box AI chatbots lack the control, observability, and accountability required for production network operations.

This project bridges that gap by demonstrating how Google's Agent Development Kit (ADK)—one of the leading agentic frameworks—enables network engineers to build **agent-based systems** that combine the flexibility of AI with the rigor of production operations.

### 🎯 Why This Project?

Learn how GenAI agents work while tackling real-world use cases faced by:
- **🔧 Network Engineers** - Design reviews, configuration validation, architectural analysis
- **⚙️ Network Automators** - BGP troubleshooting, device diagnostics, workflow orchestration
- **🛠️ SRE Teams** - Multi-turn troubleshooting, observability integration, production deployments
- **📡 NOC Teams** - Context-aware assistance, incident response, state-aware diagnostics

### 📦 What's Included?

This repository provides a collection of **complete, production-ready agents** (not just prompts) built using Google's Agent Development Kit. Each example demonstrates how ADK features map directly to real-world network operations, with:

- ✅ **Complete Working Code** - Ready-to-run implementations with all dependencies
- 🌐 **Network-Specific Use Cases** - Real scenarios from production environments
- 🎓 **ADK Feature Demonstrations** - Practical examples of advanced agent capabilities
- 🧪 **Safe Testing Environment** - Mock backends for safe experimentation (swap with real APIs when ready)

### 💡 Design Philosophy

Every example is designed to be:
- 📚 **Self-Explanatory** - Clear documentation, well-structured code, and inline comments
- 🛡️ **Safe by Design** - Mock backend interactions prevent accidental production changes
- 🌍 **Grounded in Reality** - Based on actual network workflows and operational patterns
- 🚀 **Production-Ready Foundation** - Suitable starting points for real-world systems

> **🚀 Value Proposition:**  
> **Solve real network problems while mastering Google's Agent Development Kit—an industry-leading agentic framework.**

---

## 🚀 Getting Started

### ✅ Prerequisites

Before you begin, ensure you have:
- 🐍 **[uv](https://docs.astral.sh/uv/getting-started/installation/)** - Python package manager (handles all dependency management)
- ☁️ **[Google Cloud SDK](https://cloud.google.com/sdk/docs/install)** - For GCP services integration
- 🔨 **[make](https://www.gnu.org/software/make/)** - Build automation (pre-installed on most Unix systems)
- 🔑 **Google Gemini API Key** - Set as environment variable: `export GOOGLE_API_KEY=<your-key>`

### ⚡ Quick Start

0. **📚 Find sample queries** for every agent in the [SAMPLE_QUERIES.md](./SAMPLE_QUERIES.md) file.

1. **📥 Clone the repository**
   ```bash
   git clone https://github.com/yourusername/GoogleADK-NetworkAutomation.git
   cd GoogleADK-NetworkAutomation
   ```

2. **▶️ Choose an example and run it**
   ```bash
   cd 1-basic-agent
   make install && make playground
   ```


   The playground will launch a web interface where you can interact with the agent.

3. **🔍 Explore the code**
   - 📖 Review `README.md` in each example for use case details
   - 💻 Examine `agent.py` files to understand agent implementation

### 🎨 Agent Starter Pack (Optional)

For scaffolding new agents, use Google Cloud's **[agent-starter-pack](https://github.com/GoogleCloudPlatform/agent-starter-pack)**—an open-source CLI that handles infrastructure setup, CI/CD, and observability.

**✨ Benefits:**
- ⚡ Generate production-ready agent projects in seconds
- 📋 Built-in best practices for deployment and monitoring
- 🎯 Focus on agent logic (prompts, tools, RAG) instead of boilerplate
- 🔗 Seamless integration with Google Cloud services

**📚 Learn more:** See [AgentStarterPack.md](AgentStarterPack.md) for detailed instructions.

---

## 📁 Project Structure

Each example follows a consistent structure for easy navigation:

```
1-basic-agent/                    # Parent folder (example name)
├── README.md                     # 📄 Use case documentation and setup
├── basic_agent/                  # 🤖 Agent implementation folder
│   ├── __init__.py
│   ├── agent.py                  # 🧠 Core agent logic
│   ├── fast_api_app.py          # 🌐 Web interface (optional)
│   └── app_utils/               # 🔧 Utilities and helpers
├── tests/                        # 🧪 Unit and integration tests
│   ├── unit/
│   └── integration/
├── pyproject.toml               # 📦 Project dependencies (uv)
├── uv.lock                      # 🔒 Locked dependencies
├── Makefile                     # ⚙️ Common tasks (install, test, deploy)
└── Dockerfile                   # 🐳 Container configuration
```

### 🎮 Running Examples Locally

Navigate to any example folder and execute:

```bash
make install && make playground
```

**💡 Note:** No virtual environment management needed—`uv` handles dependency isolation automatically.



## 🎯 Learning Path & Use Cases

Follow this structured learning path to master Google ADK for network automation:

---

### 📘 Phase 1: The Foundations

Start here to understand the core concepts of AI agents.

| Path | ADK Feature | Networking Use Case | Link |
|------|-------------|---------------------|------|
| `1-basic-agent/` | Agent Setup, Model Config, Output Schema, Planners, Session Management | **Network Design Review Agent** - AI-powered architectural review for network designs | [View Details](./1-basic-agent/) |
| `2-basic-agent-with-tools/` | Custom Tools, Built-in Tools, Parallel Execution, Agent-as-Tool, MCP Integration | **BGP Troubleshooting Assistant** - Systematic diagnosis of BGP session issues using multiple tool patterns | [View Details](./2-basic-agent-with-tools/) |
| `3-agent-session-context/` | Session State, ToolContext, ReadonlyContext, FunctionTool, Multi-Turn Conversations | **Multi-Turn NOC Assistant** - Context-aware troubleshooting with state persistence across conversation turns | [View Details](./3-agent-session-context/) |

---

### 🛡️ Phase 2: Professional Engineering & Governance

Critical for production-ready network AI operations.

| Path | ADK Feature | Networking Use Case | Link |
|------|-------------|---------------------|------|
| `5-agent-callbacks-guardrails/` | Agent/Model/Tool Callbacks, CallbackContext, Content Filtering, Access Control | **Production Security & Control** - Callback-based guardrails for policy enforcement (e.g., prevent invalid BGP commands) | [View Details](./5-agent-callbacks-guardrails/) |
| `4-agent-human-in-the-loop/` | HITL Confirmation, ResumabilityConfig, Boolean & Tool-Based Approval Patterns | **Configuration Change Approval** - Safety-first network config with human approval gates for high-stakes changes | [View Details](./4-agent-human-in-the-loop/) |
| `10-agent-observability/` | Python Logging, Opik Integration, Trace Visualization, LLM Metrics Tracking | **Production Observability** - Comprehensive logging and tracing—the "audit trail" for network changes | [View Details](./10-agent-observability/) |

---

### 🏗️ Phase 3: Advanced Architectures

Move from single tasks to complex, modular agent systems.

| Path | ADK Feature | Networking Use Case | Link |
|------|-------------|---------------------|------|
| `6-agent-workflows/` | SequentialAgent, ParallelAgent, LoopAgent, Nested Workflows, Exit Control | **Automated Network Troubleshooting Workflows** - Complex sequences (Verify BGP → Run CyPerf Test → Analyze Results) | [View Details](./6-agent-workflows/) |
| `7-agent-subagents/` | Hierarchical Multi-Agent, Sub-Agent Delegation, Parent Orchestration, Dynamic Task Routing | **Hierarchical Network Operations** - Modular approach: one agent for security, another for performance benchmarking | [View Details](./7-agent-subagents/) |
| `8-agent-rag-WIP/` | RAG Integration, Document Retrieval, Knowledge Base | **Documentation-Aware Agent** - Connect to technical documentation and network topologies *(Work in Progress)* | [View Details](./8-agent-rag-WIP/) |

---

### 🚀 Phase 4: Deployment & The "Automation Story"

Deploy agents to production and enable integration with other systems.

| Path | ADK Feature | Networking Use Case | Link |
|------|-------------|---------------------|------|
| `12-agent-deployment-vtxai/` | Vertex AI Agent Engine, Managed Runtime, State Management, Secure Code Execution, Enterprise Observability | **Vertex AI Agent Engine Deployment** - Managed enterprise-grade runtime with built-in playground UI | [View Details](./12-agent-deployment-vtxai/) |
| `11-agent-deployment-cloudrun/` | Cloud Run Deployment, Cloud Build, IAM Policy Binding, Dockerfile Configuration, Serverless Containers | **Cloud Run Deployment** - Serverless containerized agent with automatic scaling and IAM access control | [View Details](./11-agent-deployment-cloudrun/) |
| `13-agent-api-frontend/` | REST API, FastAPI, React Frontend | **REST API Integration** - Expose agents via REST API for consumption by other systems | [View Details](./13-agent-api-frontend/) |
| `13-agent-streamlit-ui/` | Streamlit, Web UI, Interactive Chat | **Streamlit GUI** - Browser-based interface for engineers to interact without CLI | [View Details](./13-agent-streamlit-ui/) |

---

### 🔬 Phase 5: Specialized Use Cases

Advanced patterns for specific operational requirements.

| Path | ADK Feature | Networking Use Case | Link |
|------|-------------|---------------------|------|
| `9-agent-a2a-asp/` | RemoteA2aAgent, Agent Cards, HTTP Communication, Microservices Architecture | **Agent-to-Agent Communication** - Distributed NOC with agents communicating via HTTP | [View Details](./9-agent-a2a-asp/) |
| `14-agent-ollama/` | LiteLLM, Ollama, Local LLM Execution | **Local LLM Execution** - Run agents with local models for sensitive network environments where data cannot leave premises | [View Details](./14-agent-ollama/) |

---

## ✨ Key Features

- 🔧 **Production-Ready Examples** - Complete implementations, not code snippets
- 🛡️ **Safety First** - Mock backends prevent accidental production changes
- 📚 **Comprehensive Documentation** - Every example includes detailed README with ADK feature mapping
- 🧪 **Full Test Coverage** - Unit and integration tests included
- ☁️ **Cloud Deployment Ready** - Examples include Cloud Run and Vertex AI deployments
- 🔍 **Built-in Observability** - Logging, tracing, and monitoring patterns
- 🤝 **Human-in-the-Loop** - Approval workflows and safety guardrails
- 🔄 **Workflow Orchestration** - Sequential, parallel, and loop patterns

---

## 🤝 Contributing

Contributions are welcome! This project aims to be a comprehensive resource for network engineers learning AI agent development.

**🎯 Areas of Interest:**
- 🌐 Additional network automation use cases
- 🔌 Integration examples with network device APIs
- 🚀 Production deployment patterns
- 📊 Observability and monitoring enhancements

Please ensure contributions maintain the project's focus on clarity, safety, and operational relevance.

---

## 📄 License

This project is provided as-is for educational and operational purposes. Please review individual dependencies and ensure compliance with your organization's policies.

---

## 🔮 Long-Term Vision

This project aims to help network engineers:

- 🔄 **Transition from Script-Based to Agent-Based Operations** - Move beyond brittle automation
- 💪 **Build Confidence in AI Systems** - Through enforced observability, control, and accountability
- 🎯 **Design Agents as Disciplined Operators** - AI systems that behave predictably and safely
- 🌉 **Bridge the Skills Gap** - Make advanced AI capabilities accessible to network operators

> **💎 Guiding Principle:**  
> *If a concept cannot be explained clearly to a network engineer, it does not belong here.*

---

**Built with ❤️ for Network Engineers by Network Engineer**

