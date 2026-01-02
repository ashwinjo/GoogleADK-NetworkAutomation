# ruff: noqa
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
import google.auth
import logging

from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.models import Gemini
from google.genai import types

from .app_utils.tools import ping_router, traceroute_router

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)

# ============================================================================
# ROOT AGENT
# ============================================================================

root_agent = Agent(
            name="RouterDiagnosticsAgent",
            model=Gemini(
                model="gemini-3-flash-preview",
                temperature=0.0,
                retry_options=types.HttpRetryOptions(attempts=3),
            ),
            description="This agent performs network diagnostics on routers by pinging and running traceroutes.",
            instruction="""You are a network diagnostics assistant specialized in testing router connectivity.

            Your role is to:
            1. Ping a router using the ping_router tool to check connectivity and measure latency
            2. Run a traceroute against the router using the traceroute_router tool to identify the network path

            When you receive a request to test a router:
            - First, ping the router to check if it's reachable and measure basic connectivity
            - Then, run a traceroute to see the network path and identify any routing issues
            - Present both results in a clear, structured format

            Always perform both operations (ping and traceroute) when testing a router.
            """,
            tools=[
                ping_router,
                traceroute_router,
            ],
        )

# ============================================================================
# APP CONFIGURATION
# ============================================================================

app = App(root_agent=root_agent, name="app")
