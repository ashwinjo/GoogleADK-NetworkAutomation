# Google Agent Development Kit (ADK) for Network Engineers

## Overview

### Why?

Network engineers need AI systems that are **understandable**, **trustworthy**, and **operationally relevant**. Traditional script-based automation is brittle and lacks the ability to reason through complex scenarios. However, black-box AI chatbots lack the control, observability, and accountability required for production network operations.

This project bridges that gap by demonstrating how Google's Agent Development Kit (ADK) which is one of the leading Agentic Frameworks enables network engineers to build **agent-based systems**.

Goal is to be able to learn how GenAI Agents work while tacking some common use cases faced by
- Network Engineers
- Network Automators
- SRE
- NOC 


### What?

This repository is a collection of **ready to use complete agents** (not just prompts) built using Google's Agent Development Kit. 
Each example demonstrates how ADK features map directly to real-world network operations.
### How?

Every example is designed to be:
- **Self-explanatory** - Clear documentation and code structure
- **Safe by design** - We are not making real calls. Mocking the backend device interactions. ( You can replace it with real calls once you decide to implement it)
- **Grounded in reality** - Based on actual network workflows that I have seen.
- **Production-ready foundation** - Suitable as a starting point for real systems.

> **🚀 Value Proposition:**  
> **Solve real network problems while mastering an industry-leading Google Agent Development Kit agent framework.**

## Getting Started

To help you get started quickly, we'll use the **agent-starter-pack**—an open-source CLI and template collection from Google Cloud. The agent-starter-pack bridges the gap between local prototypes and production-ready AI agents.

It works as a scaffolding engine, taking care of infrastructure setup, CI/CD, and observability so you can focus entirely on agent logic—such as prompts, tools, and RAG pipelines.

Refer [AgentStarterPack](AgentStarterPack.md)

**Getting Started:**

1. Install the agent-starter-pack CLI by following the instructions at [agent-starter-pack GitHub](https://github.com/GoogleCloudPlatform/agent-starter-pack).
2. Use the CLI to scaffold a new agent project in seconds.
3. Plug in your own ADK-powered agent logic—no boilerplate required.
4. Benefit from built-in best practices for production-readiness.

*Full step-by-step instructions and example workflows coming soon!*

---
## Nomenclature and Folder Structure:
```
```
    1-basic-agent/ <<<<<<< ADK Agent Parent Folder Name >>>>>>>
    ├── README.md
    ├── agent1/ <<<<<<< ADK Agent folder >>>>>>>
    │   ├── __init__.py
    │   ├── agent.py <<< Agent Logic File >>>
    |---other_folders
    ├── tests/
    │   └── test_agent.py
    ├── requirements.txt
    └── pyproject.toml
```
** To run the agent locally:

cd <ADK Agent Parent Folder Name>

```bash
make install && make playground
```
** No need of venv when using uv. uv will take care of the dependencies and versioning.

> Start with this scaffold for any new agent!



## Use Cases

| Path | ADK Feature | Networking Use Case | Link |
|------|-------------|---------------------|------|
| `1-basic-agent/` | Agent Setup, Model Config, Output Schema, Planners, Session Management | Network Design Review Agent - AI-powered architectural review for network designs | [View Details](./1-basic-agent/) |
| `2-basic-agent-with-tools/` | Custom Tools, Built-in Tools, Parallel Execution, Agent-as-Tool, MCP Integration | BGP Troubleshooting Assistant - Systematic diagnosis of BGP session issues using multiple tool patterns | [View Details](./2-basic-agent-with-tools/) |
| `3-agent-session-context/` | Session State, ToolContext, ReadonlyContext, FunctionTool, Multi-Turn Conversations | Multi-Turn NOC Assistant - Context-aware troubleshooting with state persistence across conversation turns | [View Details](./3-agent-session-context/) |
| `4-agent-human-in-the-loop/` | HITL Confirmation, ResumabilityConfig, Boolean & Tool-Based Approval Patterns | Configuration Change Approval System - Safety-first network config management with human approval gates | [View Details](./4-agent-human-in-the-loop/) |
| `5-agent-callbacks-guardrails/` | Agent/Model/Tool Callbacks, CallbackContext, Content Filtering, Access Control | Production Security & Control System - Callback-based guardrails for policy enforcement and data protection | [View Details](./5-agent-callbacks-guardrails/) |
| `6-agent-workflows/` | SequentialAgent, ParallelAgent, LoopAgent, Nested Workflows, Exit Control | Automated Network Troubleshooting Workflows - Three orchestration patterns (parallel, sequential, loop) for network ops | [View Details](./6-agent-workflows/) |
| `7-agent-subagents/` | Hierarchical Multi-Agent, Sub-Agent Delegation, Parent Orchestration, Dynamic Task Routing | Hierarchical Website Troubleshooting - Parent agent orchestrating specialized sub-agents for complex workflows | [View Details](./7-agent-subagents/) |
| `9-agent-a2a-asp/` | RemoteA2aAgent, Agent Cards, HTTP Communication, Microservices Architecture | Distributed Network Operations Center - Agent-to-agent communication via HTTP for microservices-style architecture | [View Details](./9-agent-a2a-asp/) |
| `10-agent-observability/` | Python Logging, Opik Integration, Trace Visualization, LLM Metrics Tracking | Production Observability & Monitoring - Comprehensive logging and observability patterns for production deployments | [View Details](./10-agent-observability/) |
| `11-agent-deployment-cloudrun/` | Cloud Run Deployment, Cloud Build, IAM Policy Binding, Dockerfile Configuration, Serverless Containers | Cloud Run Deployment - Serverless containerized agent deployment with automatic scaling and IAM-based access control | [View Details](./11-agent-deployment-cloudrun/) |
| `12-agent-deployment-vtxai/` | Vertex AI Agent Engine, Managed Runtime, State Management, Secure Code Execution, Enterprise Observability | Vertex AI Agent Engine Deployment - Managed enterprise-grade agent runtime with built-in state persistence and playground UI | [View Details](./12-agent-deployment-vtxai/) |

---

## Requirements

Before you begin, ensure you have:
- **uv**: Python package manager (used for all dependency management in this project) - [Install](https://docs.astral.sh/uv/getting-started/installation/) ([add packages](https://docs.astral.sh/uv/concepts/dependencies/) with `uv add <package>`)
- **Google Cloud SDK**: For GCP services - [Install](https://cloud.google.com/sdk/docs/install)
- **make**: Build automation tool - [Install](https://www.gnu.org/software/make/) (pre-installed on most Unix-based systems)


## Long-Term Vision

This project aims to help network engineers:

- Transition from script-based automation to agent-based operations
- Build confidence in AI systems through enforced observability, control, and accountability
- Design AI agents that behave like disciplined operators

> **Guiding Principle:**  
> If a concept cannot be explained clearly to a network engineer, it does not belong here.

