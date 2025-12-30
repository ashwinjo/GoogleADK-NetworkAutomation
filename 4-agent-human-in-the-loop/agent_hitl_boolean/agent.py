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

from google.adk import Agent
from google.adk.apps import App
from google.adk.apps import ResumabilityConfig
from google.adk.tools.function_tool import FunctionTool
from google.genai import types
from dotenv import load_dotenv
import logging

load_dotenv()

from .app_utils.tools import read_router_config, write_router_config


# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)


def confirmation_if_not_spof_router(router_name: str) -> bool:
    """
    Returns True if the router is NOT a Single Point of Failure (SPOF).
    Non-SPOF routers can be modified automatically.
    """
    # Example policy:
    # - r1-sea3 → SPOF router → human approval required
    # - anything else → auto-approved
    return router_name == "r1-sea3"


# Explicit True/False confirmation
root_agent = Agent(
    name="hitl_network_agent",
    model="gemini-2.5-flash",
    instruction="""
    You are a Network Operations Assistant.

    Rules:
    - Use read_router_config for read-only operations.
    - Use write_router_config for configuration changes.
    - Configuration writes may require human approval.
    - Always return tool results to the user.
    - Act like a cautious Tier-2 NOC engineer.
    """,
    tools=[
        # We use function tool for the boolean confirmation functions
        FunctionTool(
            write_router_config,
            require_confirmation=confirmation_if_not_spof_router
        ),
        read_router_config
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.1
    ),
)

app = App(
    name='agent_hitl_boolean',
    root_agent=root_agent,
    # Set the resumability config to enable resumability.
    resumability_config=ResumabilityConfig(
        is_resumable=True,
    ),
)