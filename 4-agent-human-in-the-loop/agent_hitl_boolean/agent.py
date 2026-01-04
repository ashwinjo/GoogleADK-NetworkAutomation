"""
Author: Ashwin Joshi

Title: Human-in-the-Loop Configuration Approval (Boolean)
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


## When you will explicitly need to use True/False confirmation every time

# root_agent = Agent(
#     name="hitl_network_agent",
#     model="gemini-2.5-flash",
#     instruction="""
#     You are a Network Operations Assistant.

#     Rules:
#     - Use read_router_config for read-only operations.
#     - Use write_router_config for configuration changes.
#     - Configuration writes may require human approval.
#     - Always return tool results to the user.
#     - Act like a cautious Tier-2 NOC engineer.
#     """,
#     tools=[
#         # We use function tool for the boolean confirmation functions
#         FunctionTool(
#             write_router_config,
#             require_confirmation=True # Explicit True/False confirmation
#         ),
#         read_router_config
#     ],
#     generate_content_config=types.GenerateContentConfig(
#         temperature=0.1
#     ),
# )


## When a third function is needed to be used for you to confirm action

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