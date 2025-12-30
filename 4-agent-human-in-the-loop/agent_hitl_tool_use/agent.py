# agent/write_with_confirmation.py

from google.adk.tools.tool_context import ToolContext
from .app_utils.tools import write_router_config

from google.adk import Agent
from google.adk.apps import App, ResumabilityConfig
from google.genai import types
from dotenv import load_dotenv
import logging

from .app_utils.tools import read_router_config


load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
def write_router_config_confirmation_wizard(
    router_name: str,
    tool_context: ToolContext
):
    """
    Human-in-the-loop wrapper for write_router_config
    """

    tool_confirmation = tool_context.tool_confirmation

    # Step 1: Ask for approval
    if not tool_confirmation:
        tool_context.request_confirmation(
            hint=(
                """This action will MODIFY router configuration.
                "Approve or reject the write operation.
                "Sample Answer: {"confirmed": true, "payload":{"ok_to_write": false}} """
            ),
            payload={
                "ok_to_write": False
            },
        )
        return {
            "status": "pending_approval",
            "message": "Awaiting human approval before applying configuration."
        }

    # Step 2: Process approval
    ok_to_write = tool_confirmation.payload.get("ok_to_write", False)
    
    print("XXXXXXXX", ok_to_write)
    if ok_to_write:
        return write_router_config(router_name)

    return {
        "status": "rejected",
        "message": "Human reviewer rejected the configuration change."
    }


root_agent = Agent(
    name="network_engineer_agent",
    model="gemini-2.5-flash",
    instruction="""
    You are a Network Engineer AI assisting a NOC team.

    Capabilities:
    - Read router configurations
    - Propose configuration changes
    - Require HUMAN approval before making any write changes

    Rules:
    - Always use tools for network operations
    - Never write configuration without explicit confirmation
    - Clearly explain what action is being taken
    - Return tool outputs verbatim to the user
    """,
    tools=[
        read_router_config,
        write_router_config_confirmation_wizard,
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.1
    ),
)

app = App(
    name="agent_hitl_tool_use",
    root_agent=root_agent,
    resumability_config=ResumabilityConfig(
        is_resumable=True
    ),
)