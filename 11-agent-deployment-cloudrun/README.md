# 11-agent-deployment-cloudrun

Please ensure you have your Google Gemini API key set in your environment variables.
export GOOGLE_API_KEY=<your-Google-Gemini-API-key>

---

### Prerequisites

Ensure you have:
1. Google Cloud SDK installed and authenticated
2. Google Gemini API key set in environment variables
3. GCP project with billing enabled

### Authentication Setup

```bash
gcloud auth login
gcloud auth login --update-adc --project <your-project-id>
gcloud config set project <your-project-id>
gcloud config set region <your-region>
```

Verify your configuration:

```bash
gcloud config list
[core]
account = ashwinjosh@gmail.com
disable_usage_reporting = True
project = adkstuff

Your active configuration is: [default]
```

```deploy:
	PROJECT_ID=$$(gcloud config get-value project) && \
	gcloud beta run deploy google-adk-network-automation \
		--source . \
		--memory "4Gi" \
		--project $$PROJECT_ID \
		--region "us-central1" \
		--no-allow-unauthenticated \
		--no-cpu-throttling \
		--labels "created-by=adk" \
		--update-build-env-vars "AGENT_VERSION=$(shell awk -F'"' '/^version = / {print $$2}' pyproject.toml || echo '0.0.0')" \
		--update-env-vars \
		"COMMIT_SHA=$(shell git rev-parse HEAD)" \
		$(if $(IAP),--iap) \
		$(if $(PORT),--port=$(PORT))

The deploy command in the Makefile builds and deploys your agent:

```bash
make deploy
```

This command:
1. Builds a Docker image using Cloud Build
2. Deploys the container to Cloud Run
3. Returns a service URL for accessing your agent

### Configure IAM Permissions

**⚠️ Note: For testing only. Use least privilege in production.**

Grant public access (development/testing):

```bash
gcloud run services add-iam-policy-binding google-adk-network-automation \
  --member="allUsers" \
  --role="roles/run.invoker" \
  --region us-central1
```

For production, use specific service accounts or authenticated users instead of `allUsers`.

### Example Deployment Output

```bash
Building using Dockerfile and deploying container to Cloud Run service [google-adk-network-automation]
✓ Building and deploying new service... Done.
  ✓ Building Container... Logs are available at [Cloud Build URL]
  ✓ Creating Revision...
  ✓ Routing traffic...
Done.
Service URL: https://google-adk-network-automation-216136305446.us-central1.run.app
```

### Customization

- **Service Name**: Change `google-adk-network-automation` in Makefile
- **Agent Folder**: Update folder name in Dockerfile
- **Memory/CPU**: Adjust `--memory` flag in Makefile deploy command
- **Region**: Modify `--region` parameter as needed

---

### Customization

If you chnage your agent folder name from `app` to lets's say `basic_agent`, you will need to update.

Dockerfile:
```bash
COPY ./basic_agent ./basic_agent
CMD ["uv", "run", "uvicorn", "basic_agent.fast_api_app:app", "--host", "0.0.0.0", "--port", "8080"]
```

Makefile:
```bash
local-backend:
	uv run uvicorn basic_agent.fast_api_app:app --host localhost --port 8000 --reload

```