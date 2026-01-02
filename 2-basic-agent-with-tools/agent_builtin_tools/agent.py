"""
Author: Ashwin Joshi

Title:

Purpose:

ADK Feature Uses:

Useful links:
  - Agent Development Kit (ADK) Documentation: 
  
"""

from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.models import Gemini
from google.genai import types
from google.adk.tools import google_search


from .app_utils.tools import get_bgp_summary, get_interface_status, get_bgp_routes

from dotenv import load_dotenv
load_dotenv()


import os
import google.auth
import logging

_, project_id = google.auth.default()

os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)


SYSTEM_PROMPT_BUILTIN = """
You are a Network Engineering Assistant with access ONLY to Google Search.

Your task is to provide BGP troubleshooting guidance based on publicly available knowledge.

## Search Rules
- Use Google Search for every answer
- Do not assume access to live network telemetry
- Do not fabricate operational data

## Citation Requirements
- Every technical claim MUST be supported by a citation
- Use inline citations in the format: [source]
- Prefer vendor documentation, RFCs, or reputable networking blogs

## Output Expectations
- Summarize common causes
- Provide step-by-step troubleshooting guidance
- Clearly state that conclusions are based on general industry knowledge

You are acting as a knowledge-based NOC reference assistant.
"""

# Use Case 2: Basic Agent with Builtin Tools
root_agent_builtin_tools= Agent(
    name="google_bases_BGP_troubleshooting_assistant",
    model=Gemini(
        model="gemini-3-flash-preview",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    description="This is a google_search_Only_BGP_Troubleshooting_Assistant",
    instruction=SYSTEM_PROMPT_BUILTIN,
    tools=[google_search]
)

# # Change the root_agent when experimenting 
app = App(root_agent=root_agent_builtin_tools, name="agent_builtin_tools")


"""
You can use generateConfig and thinking cofigurations that we discussed before as well.
Just keeping it simeple here
"""