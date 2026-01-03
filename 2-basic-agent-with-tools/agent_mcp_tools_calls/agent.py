"""
Author: Ashwin Joshi

Title: MCP Tools Integration Agent

Purpose: Demonstrates how to use MCP (Model Context Protocol) tools with ADK

ADK Feature Uses:
  - McpToolset: Integration with external MCP tool servers
  - StdioConnectionParams: Configure MCP server connections

Useful links:
  - Agent Development Kit (ADK) Documentation: https://google.github.io/adk-docs/
  
"""

import os
import google.auth

from dotenv import load_dotenv
load_dotenv()

from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams, StreamableHTTPServerParams
from mcp import StdioServerParameters

# Configure Vertex AI
_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"



mcp_subnet_calculator_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=[
                "-y",
                "supergateway",
                "--sse",
                "https://mcp-subnet-calculator.mteke.com/sse"
            ]
        ),
        timeout=30,
    ),
)

HUGGING_FACE_TOKEN = os.getenv("HUGGING_FACE_TOKEN")

hugging_face_toolset = McpToolset(
            connection_params=StreamableHTTPServerParams(
                url="https://huggingface.co/mcp",
                headers={
                    "Authorization": f"Bearer {HUGGING_FACE_TOKEN}",
                },
            ),
        )

subnet_calculator_agent = Agent(
    model="gemini-2.5-pro",
    name="mcp_subnet_calculator_agent",
    instruction="Help users calculate subnets using the MCP Subnet Calculator",
    tools=[mcp_subnet_calculator_toolset],
)

hugging_face_agent = Agent(
    model="gemini-2.5-pro",
    name="hugging_face_agent",
    instruction="Help users get information from Hugging Face",
    tools=[hugging_face_toolset],
)


### Un Comment out the agent you want to use

#app = App(root_agent=subnet_calculator_agent, name="agent_mcp_tools_calls")

app = App(root_agent=hugging_face_agent, name="agent_mcp_tools_calls")
