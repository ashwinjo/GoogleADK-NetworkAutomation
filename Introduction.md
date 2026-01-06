## What is an AI Agent ?

An AI Agent is an autonomous software system that uses reasoning m tools and memory to achieve specific goals with minimal human intervention. Unlike traditional automation that follows rigid "if-then" rules, agents can perceive their environment, create multi-step plans, and adapt to unexpected changes. They act as an "intelligent brain" (typically powered by a Large Language Model) that can independently decide which tools to use—such as APIs, web searches, or databases—to complete a task.


##  What is Agent Framework ?

An Agent Framework is the underlying software infrastructure, that provides the necessary APIs, memory management, and orchestration layers to build these agents.
The framework serves as the "backbone" that allows developers to define agent roles, connect them to external data pipelines, and manage how multiple agents collaborate within a single system.

## What is Google Agent Development Kit (ADK) ?

Google Agent Development Kit (ADK) is a modular, open-source Python framework designed specifically to build, evaluate, and deploy production-ready AI agents and multi-agent systems.  
It is "multi-agent by design," allowing you to create complex hierarchies where a primary agent can delegate specialized sub-tasks to other agents seamlessly.
While it is model-agnostic and supports various LLMs, it is highly optimized for the Google Cloud ecosystem, integrating natively with Gemini models and the Vertex AI Agent Engine.
The framework provides unique capabilities like bidirectional audio and video streaming, enabling users to interact with agents through natural, multimodal dialogue rather than just text.
ADK also features a robust Evaluation Framework and a Developer UI, allowing you to trace execution steps, inspect state changes, and systematically test agent performance before deployment.

[Google ADK Cheatsheet](1-basic-agent/GEMINI.md)

## What is Agent Starter Pack ?

Agent Starter Pack is a CLI tool that helps you create a new agent project with a lot of boilerplate code and configuration.
[Agent Starter Pack Documentation](https://googlecloudplatform.github.io/agent-starter-pack/)


Quick Start with Agent Starter Pack:
```bash
uvx agent-starter-pack create <agent-parent-folder-name>
```

The follow the interactive menu to create the agent.