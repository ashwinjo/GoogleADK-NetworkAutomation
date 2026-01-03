"""
Author: Ashwin Joshi

Title: Network Command Screening Agent
"""


from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.models import Gemini
from google.genai import types
from google.adk.planners import BuiltInPlanner
from google.adk.planners import PlanReActPlanner
from pydantic import BaseModel, Field
from typing import Literal

import logging
import os
import google.auth

from dotenv import load_dotenv
load_dotenv()


_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)


SYSTEM_PROMPT = """
# Role
You are a Network Command Assistant with built-in safety screening.
Your job is to convert natural language requests into networking commands
while BLOCKING any harmful, dangerous, or destructive operations.

---

# Tone
- Helpful but firm on safety
- Educational when blocking (explain the risk)
- Assume good intent, but enforce safety
- Suggest safer alternatives when possible

# User Request
"""


class CommandReadout(BaseModel):
    """Structured output for network command screening results."""
    command: str = Field(
        description="The networking command to execute, or 'BLOCKED: [reason]' if harmful"
    )
    use: str = Field(
        description="Explanation of command purpose (if safe) or risk details (if blocked)"
    )


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-3-flash-preview",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    description="Network Command Screening Agent - Converts requests to commands while blocking harmful operations",
    instruction=SYSTEM_PROMPT,
    output_schema=CommandReadout,
    generate_content_config=types.GenerateContentConfig(
        temperature=0.1,  # Very deterministic for consistent safety screening
        max_output_tokens=5000,  # Commands don't need long responses
        safety_settings=[
            # Block dangerous content at lowest threshold for maximum safety
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
            # Also screen for potentially harmful instructions
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            ),
        ]
    ),
    # Enable "Reasoning" with "PlanReActPlanner" for multi-step safety analysis
    planner=PlanReActPlanner(),   
)

"""
# Enable "Reasoning" with "BuiltInPlanner" and set "thinking_budget" to 1024 tokens
planner=BuiltInPlanner(
    thinking_config=types.ThinkingConfig(
        include_thoughts=True,
        thinking_budget=1024,
    )
)
"""

# This "name" needs to be same as the name of the folder in the project root
# root_agent is the name of the agent defined above
app = App(root_agent=root_agent, name="basic_agent_advanced_config_and_cotrol")
