# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import logging
import warnings

import google.auth
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app

from before_after_tool_callback.app_utils.telemetry import setup_telemetry
from before_after_tool_callback.app_utils.typing import Feedback

# Suppress Pydantic warnings about JSON schema generation for internal ADK types
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

setup_telemetry()

# Try to initialize Google Cloud logging, fall back to standard logging if not available
try:
    from google.cloud import logging as google_cloud_logging
    _, project_id = google.auth.default()
    logging_client = google_cloud_logging.Client(project=project_id)
    logger = logging_client.logger(__name__)
    print(f"✅ Google Cloud Logging initialized for project: {project_id}")
except Exception as e:
    # Fall back to standard Python logging for local development
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    print(f"⚠️  Google Cloud Logging not available, using standard logging: {e}")

allow_origins = (
    os.getenv("ALLOW_ORIGINS", "").split(",") if os.getenv("ALLOW_ORIGINS") else None
)

# Artifact bucket for ADK (created by Terraform, passed via env var)
logs_bucket_name = os.environ.get("LOGS_BUCKET_NAME")

AGENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# In-memory session configuration - no persistent storage
session_service_uri = None

artifact_service_uri = f"gs://{logs_bucket_name}" if logs_bucket_name else None

app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    web=True,
    artifact_service_uri=artifact_service_uri,
    allow_origins=allow_origins,
    session_service_uri=session_service_uri,
    otel_to_cloud=True,
)
app.title = "5-agent-clbk-guardrails"
app.description = "API for interacting with the Agent 5-agent-clbk-guardrails"


# Workaround for Pydantic schema generation issue with httpx.Client
# Override the openapi method to catch and handle the schema generation error
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
        logger_module = logging.getLogger(__name__)
        logger_module.warning(f"Failed to generate full OpenAPI schema: {e}")
        
        # Try to generate a partial schema by filtering out problematic routes
        from fastapi.openapi.utils import get_openapi
        from fastapi.routing import APIRoute
        
        # Get routes that can be documented
        safe_routes = []
        for route in app.routes:
            if isinstance(route, APIRoute):
                # Try to generate schema for this route
                try:
                    test_schema = get_openapi(
                        title="test",
                        version="0.0.1",
                        routes=[route],
                    )
                    safe_routes.append(route)
                except Exception:
                    # Skip this route if it causes errors
                    logger_module.debug(f"Skipping route {route.path} due to schema generation error")
                    pass
            else:
                # Include non-APIRoute routes (like mounts)
                safe_routes.append(route)
        
        # Generate schema with safe routes only
        try:
            openapi_schema = get_openapi(
                title=app.title,
                version=app.version,
                description=app.description + "\n\n⚠️ Note: Some advanced routes from ADK are not displayed due to OpenAPI limitations.",
                routes=safe_routes,
            )
            app.openapi_schema = openapi_schema
            return app.openapi_schema
        except Exception as fallback_error:
            logger_module.error(f"Failed to generate even partial schema: {fallback_error}")
            # Return absolute minimal schema as last resort
            return {
                "openapi": "3.0.2",
                "info": {
                    "title": app.title,
                    "version": app.version,
                    "description": app.description + "\n\n⚠️ Note: API documentation could not be generated.",
                },
                "paths": {},
            }


app.openapi = custom_openapi


@app.post("/feedback")
def collect_feedback(feedback: Feedback) -> dict[str, str]:
    """Collect and log feedback.

    Args:
        feedback: The feedback data to log

    Returns:
        Success message
    """
    try:
        # Try Google Cloud structured logging first
        logger.log_struct(feedback.model_dump(), severity="INFO")
    except AttributeError:
        # Fall back to standard logging
        logger.info(f"Feedback received: {feedback.model_dump()}")
    return {"status": "success"}


# Main execution
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
