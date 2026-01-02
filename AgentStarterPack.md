# Getting Started with the Google Agent Starter Pack

This is a guide to help you get started with the Agent Starter Pack.

Docs at : https://github.com/GoogleCloudPlatform/agent-starter-pack

[Google ADK Cheatsheet](1-basic-agent/GEMINI.md)

## Pre-requisites
- uv and uvx [Install](https://docs.astral.sh/uv/getting-started/installation/)
- Google Cloud SDK [Install](https://docs.cloud.google.com/sdk/docs/install-sdk#deb)
- make [Install](https://www.gnu.org/software/make/)


## Auth with Google Cloud 
Once you have the Google Cloud SDK installed, you need to authenticate with Google Cloud so that once you test agent locally you can eventually deploy it to Cloud.

```bash
gcloud auth login
```

```bash
gcloud config set project <your-project-id>
```

```bash
gcloud config set region <your-region>
```

```bash
gcloud auth login --update-adc --project <your-project-id>
```

## Creating Agent

```bash
uvx agent-starter-pack create <agent-folder-name>
```

If you already have ADK agent created without Agent Starter Pack
```bash
uvx agent-starter-pack enhance <agent folder>
```

Now, Lets make our agents.

Command Run: ```uvx agent-starter-pack create 1-basic-agent```

```
Interactive Prompts & Selections:

Template: 1. adk_base (A base ReAct agent built with Google's Agent Development Kit).

Deployment Target: 2. Cloud Run (GCP Serverless container execution).

Session Type: 1. In-memory session (Ideal for stateless applications).

CI/CD Runner: 1. Simple (Minimal, no CI/CD or Terraform).

GCP Region: us-central1.
```


> **Note:** <br>It will create "app" folder which would be your agent code.
<br>You can rename it to anything you want.
<br>
Ensure you use the same name in your agent.py file when you run

## Quick Start (Local Testing)

Install required packages and launch the local development environment:

Checkout 
** No need for venv here

```bash
make install && make playground
```

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
1. **Develop:** Edit your agent logic in `basic-agent/agent.py`.
2. **Test:** Explore your agent functionality using the local playground with `make playground`. The playground automatically reloads your agent on code changes.
3. **Enhance:** When ready for production, run `uvx agent-starter-pack enhance` to add CI/CD pipelines, Terraform infrastructure, and evaluation notebooks.

The project includes a `GEMINI.md` file that provides context for AI tools like Gemini CLI when asking questions about your template. Very usefule when doing vibe coding.


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
