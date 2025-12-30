"""
Author: Ashwin Joshi

Title:
Google ADK Sessions for Network Engineers – BGP Troubleshooting Example

Purpose:
Demonstrate how ADK Sessions and State enable multi-turn,
context-aware network troubleshooting conversations.

ADK Feature Uses:
- Session
- State
- ToolContext
- ReadonlyContext
- FunctionTool

Useful Links:
- Agent Development Kit (ADK) Documentation:
  https://cloud.google.com/vertex-ai/docs/agent-development-kit
"""

import os
import logging
import google.auth

from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.models import Gemini
from google.adk.tools import ToolContext, FunctionTool
from google.adk.agents.readonly_context import ReadonlyContext
from google.genai import types

# -------------------------------------------------------------------
# Environment setup
# -------------------------------------------------------------------

_, project_id = google.auth.default()

os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

# Logging for demo visibility
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------------------------------------------------------   
# Tool: Simulated BGP Summary
# Demonstrates ToolContext + Session State
# -------------------------------------------------------------------

def get_bgp_summary(router_name: str, tool_context: ToolContext) -> dict:
    """
    Simulates fetching BGP summary data for a router.
    Stores the active router in session state.
    """
    logging.info(f"Running get_bgp_summary for router: {router_name}")

    # Persist context across turns
    tool_context.state["active_router"] = router_name
    tool_context.state["last_tool_used"] = "get_bgp_summary"

    return {
        "status": "success",
        "router": router_name,
        "local_as": 65001,
        "neighbors": [
            {
                "neighbor_ip": "192.168.1.2",
                "state": "Established",
                "uptime": "5d03h",
                "prefixes_received": 34,
            },
            {
                "neighbor_ip": "192.168.1.3",
                "state": "Idle",
                "uptime": "00:00:05",
                "prefixes_received": 0,
            },
        ],
    }

# -------------------------------------------------------------------
# Instruction using ReadonlyContext
# Demonstrates dynamic instruction based on session state
# -------------------------------------------------------------------

def instruction_with_state(context: ReadonlyContext) -> str:
    router = context.state.get("active_router", "no router selected")

    return f"""
            You are a Network Operations Center (NOC) Assistant.

            Current troubleshooting context:
            - Active router: {router}

            Guidelines:
            - Treat this as an ongoing troubleshooting session
            - Use available tools to gather facts
            - Build on prior context instead of re-asking questions
            - Respond like a Tier-2 network engineer
            """

# -------------------------------------------------------------------
# Agent definition
# -------------------------------------------------------------------

root_agent = Agent(
    name="noc_bgp_agent",
    model=Gemini(
        model="gemini-3-flash-preview",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=instruction_with_state,
    tools=[
        FunctionTool(get_bgp_summary) # NOte the use of FunctionTool here
    ],
    # Automatically stores LLM responses in session.state["response"]
    output_key="response",
)

# -------------------------------------------------------------------
# App entry point
# -------------------------------------------------------------------
app = App(root_agent=root_agent, name="app")
