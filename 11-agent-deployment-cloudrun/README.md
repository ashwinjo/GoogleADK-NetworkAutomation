# 12-agent-deployment

A base ReAct agent built with Google's Agent Development Kit (ADK)
Agent generated with [`googleCloudPlatform/agent-starter-pack`](https://github.com/GoogleCloudPlatform/agent-starter-pack) version `0.29.3`

1) Ensure you have your Goggle Gemini API key set in your environment variables
2) Ensure you have your Google Cloud SDK installed and authenticated


Make sure you have all the GCP variables set in your environment variables.

```bash
gcloud auth login
```

```bash
gcloud auth login --update-adc --project <your-project-id>
```


```bash
gcloud config set project <your-project-id>
```

```bash
gcloud config set region <your-region>
```
```bash
gcloud config list
[core]
account = ashwinjosh@gmail.com
disable_usage_reporting = True
project = adkstuff

Your active configuration is: [default]
```
> Below is our deploy command for Cloud Run.
Change the agent-deployment to whatever you want your deployment name to be

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

```

> You can also change the name of your agent folder to anything you want.
> Need to change the name in Dockerfile.

Let's Deploy: 

```bash
ubuntusand@ubuntusand:~/GoogleADK-NetworkAutomation/11-agent-deployment-cloudrun-WIP$ make deploy 
PROJECT_ID=$(gcloud config get-value project) && \
gcloud beta run deploy google-adk-network-automation \
        --source . \
        --memory "4Gi" \
        --project $PROJECT_ID \
        --region "us-central1" \
        --no-allow-unauthenticated \
        --no-cpu-throttling \
        --labels "created-by=adk" \
        --update-build-env-vars "AGENT_VERSION=0.1.0" \
        --update-env-vars \
        "COMMIT_SHA=2a0e6904c528992dec231216e74f61a29c60c3ec" \
         \

```

2 things are happening here:

1. https://console.cloud.google.com/cloud-build to build the docker image
2. This docker image is then deployed to Cloud Run (Serverless container execution).

```bash
Building using Dockerfile and deploying container to Cloud Run service [google-adk-network-automation] in project [adkstuff] region [us-central1]
✓ Building and deploying new service... Done.                                                                                                                                                                    
  ✓ Validating Service...                                                                                                                                                                                        
  ✓ Uploading sources...                                                                                                                                                                                         
  ✓ Building Container... Logs are available at [https://console.cloud.google.com/cloud-build/builds;region=us-central1/b2580591-5a53-4db0-9534-4d8a7c53c4d5?project=216136305446].                              
  ✓ Creating Revision...                                                                                                                                                                                         
  ✓ Routing traffic...                                                                                                                                                                                           
Done.                                                                                                                                                                                                            
Service [google-adk-network-automation] revision [google-adk-network-automation-00001-96r] has been deployed and is serving 100 percent of traffic.
Service URL: https://google-adk-network-automation-216136305446.us-central1.run.app
```

You will get -"Error Forbidden: The caller does not have permission"
This is because you need to give the Cloud Run service account the necessary permissions to access the Google Gemini API.

** Note: This is for testing purposes only. You should not do this in production. Follow principle of least privilege always

```bash
gcloud run services add-iam-policy-binding google-adk-network-automation \
  --member="allUsers" \
  --role="roles/run.invoker" \
  --region us-central1
```

This will give the Cloud Run service account the necessary permissions to access the Google Gemini API.

```bash
ubuntusand@ubuntusand:~/GoogleADK-NetworkAutomation/11-agent-deployment-cloudrun-WIP$ gcloud run services add-iam-policy-binding google-adk-network-automation \
  --member="allUsers" \
  --role="roles/run.invoker" \
  --region us-central1
Updated IAM policy for service [google-adk-network-automation].
bindings:
- members:
  - allUsers
  role: roles/run.invoker
etag: BwZHbfq9Hbs=
version: 1
```