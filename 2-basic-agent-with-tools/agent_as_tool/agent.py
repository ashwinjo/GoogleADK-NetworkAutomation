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

import datetime

from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.models import Gemini
from google.genai import types

from app.app_utils.tools import get_bgp_summary
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool

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



"""
Agent as a Tool, Why ?

Use of specific tools within an agent excludes the use of any other tools in that agent. 
The following ADK Tools can only be used by themselves, without any other tools, in a single agent object:

> Code Execution with Gemini API
> Google Search with Gemini API
> Vertex AI Search

"""

get_bgp_summary_agent = Agent(
    name="get_bgp_summary_agent",
    model=Gemini(
        model="gemini-3-flash-preview",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    description="Agent to get the BGP summary for a given router.",
    instruction="You are a helpful Network Operations AI assistant expert in BGP summarization.",
    tools=[get_bgp_summary],
)


google_search_agent = Agent(
    name="google_search_agent",
    model=Gemini(
        model="gemini-3-flash-preview",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    description="Agent to search the web for a given query.",
    instruction="You are a helpful Network Operations AI assistant expert in web search.",
    tools=[google_search],
)


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-3-flash-preview",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    description="Root agent to perform network troubleshooting.",
    tools=[AgentTool(get_bgp_summary_agent), 
           AgentTool(google_search_agent)],
)

app = App(root_agent=root_agent, name="agent_as_tool")
