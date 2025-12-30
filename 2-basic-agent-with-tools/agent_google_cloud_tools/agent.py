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

"""
Author: Ashwin Joshi

Title:

Purpose:

ADK Feature Uses:

Useful links:
  - Agent Development Kit (ADK) Documentation: 
  
"""

import os
import logging

from google.adk.apps.app import App
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.api_registry import ApiRegistry
from google.adk.models import Gemini
from google.genai import types

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)

# TODO: Fill in with your GCloud project id and MCP server name
PROJECT_ID = "adkstuff"
MCP_SERVER_NAME = "projects/adkstuff/locations/global/mcpServers/google-mapstools.googleapis.com-mcp"

api_registry = ApiRegistry(PROJECT_ID)
registry_tools = api_registry.get_toolset(
    mcp_server_name=MCP_SERVER_NAME,
)
root_agent = LlmAgent(
    model=Gemini(
        model="gemini-3-flash-preview",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    name="google_maps_agent",
    instruction=f"""
                    You are a helpful data analyst agent with access to Google Maps. The project ID is: {PROJECT_ID}

                    When users ask about data:
                    - Use the project ID {PROJECT_ID} when calling Google Maps tools.

                    Mandatory Requirements:
                    - Always use the Google Maps tools to fetch real data rather than making assumptions.
                    - For all Google Maps operations, use project_id: {PROJECT_ID}.
    """,
    tools=[registry_tools],
)

app = App(root_agent=root_agent, name="agent_google_cloud_tools")