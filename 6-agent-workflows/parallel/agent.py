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
from zoneinfo import ZoneInfo

from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.models import Gemini
from google.genai import types
from google.adk.agents import ParallelAgent, SequentialAgent

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

from .app_utils.tools import check_cpu_utilization_r1_sea3, check_cpu_utilization_r2_sea3

# Define the subagents

check_cpu_utilization_r1_sea3_agent = Agent(
    name="check_cpu_utilization_r1_sea3_agent",
    model=Gemini(
        model="gemini-3-flash-preview",
        temperature=0.0,
    ),
    description="This agent checks the CPU utilization of r1-sea3 device.",
    instruction="""You are a network troubleshooting assistant specialized in checking the CPU utilization of r1-sea3 device.
    Use the check_cpu_utilization_r1_sea3 tool to check the CPU utilization of r1-sea3 device.""",
    tools=[check_cpu_utilization_r1_sea3],
    output_key="cpu_utilization_r1_sea3_results",
)   

check_cpu_utilization_r2_sea3_agent = Agent(
    name="check_cpu_utilization_r2_sea3_agent",
    model=Gemini(
        model="gemini-3-flash-preview",
        temperature=0.0,
    ),
    description="This agent checks the CPU utilization of r2-sea3 device.",
    instruction="""You are a network troubleshooting assistant specialized in checking the CPU utilization of r2-sea3 device.
    Use the check_cpu_utilization_r2_sea3 tool to check the CPU utilization of r2-sea3 device.""",  
    tools=[check_cpu_utilization_r2_sea3],
    output_key="cpu_utilization_r2_sea3_results",
)

start_agent = Agent(
    name="StartAgent",
    model=Gemini(
        model="gemini-3-flash-preview",
        temperature=0.0,
    ),
    description="This agent is the starting point of the workflow.",
    instruction="""You are a network troubleshooting assistant specialized in starting the workflow.
    You will always output below text
    **Output:**
    Here is the customer complaint: <customer_complaint>
    """
)

summary_agent = Agent(
    name="SummaryAgent",
    model=Gemini(
        model="gemini-3-flash-preview",
        temperature=0.0,
    ),
    description="This agent is the summary point of the workflow.",
    instruction="""You are a network troubleshooting assistant specialized in summarizing the workflow. You will get the output from the previous agents and you will summarize the output in a human readable format.
    Output from the previous agents:
    {cpu_utilization_r1_sea3_results} 
    and 
    {cpu_utilization_r2_sea3_results} 
    
    **Output:**
    Once you have gathered all the information show me output in tabular format
    """
)

# Create the parallel agent with minimal callback   
parallel_network_tshoot_workflow_agent = ParallelAgent(
                                            name="NetworkDeviceTroubleshootingAgent",
                                            sub_agents=[check_cpu_utilization_r1_sea3_agent, 
                                                        check_cpu_utilization_r2_sea3_agent],
                                            description="""This agent will troubleshoot 
                                            low throughput issues on a 
                                            network device by checking the CPU utilization 
                                            on given network devices."""
                                            
)

high_cpu_utilization_sequential_agent = SequentialAgent(
    name="HighCPUUtilizationSequentialAgent",
    sub_agents=[start_agent,parallel_network_tshoot_workflow_agent,summary_agent],
    description="""This agent will troubleshoot high CPU utilization issues on a 
    network device by checking the CPU utilization on given network devices."""
)
# We cannot use instruction here inside the workflow Agent
root_agent=high_cpu_utilization_sequential_agent

app = App(root_agent=root_agent, name="parallel")
