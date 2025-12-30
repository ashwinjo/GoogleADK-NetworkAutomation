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
from google.adk.tools.tool_context import ToolContext
from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.models import Gemini
from google.genai import types

from dotenv import load_dotenv
load_dotenv()

from google.adk.agents import ParallelAgent, SequentialAgent, LoopAgent
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

from .app_utils.tools import (
    check_network_connectivity,
    check_network_latency,
    check_security_alerts,
    check_network_status,
    restart_network_service,
    adjust_firewall_rules,
    fix_connectivity_issue,
    optimize_network_latency,
    block_security_threat,
)

# Define the subagents
# --- Tool Definition ---
def exit_loop(tool_context: ToolContext):
  """Call this function ONLY when the critique indicates no further changes are needed, signaling the iterative process should end."""
  print(f"  [Tool Call] exit_loop triggered by {tool_context.agent_name}")
  tool_context.actions.escalate = True
  # Return empty dict as tools should typically return JSON-serializable output
  return {}

network_monitoring_agent = Agent(
    name="NetworkMonitoringAgent",
    model=Gemini(
        model="gemini-3-flash-preview",
        temperature=0.0,
    ),
    description="This agent monitors network status, connectivity, latency, and security alerts.",
    instruction="""You are a network monitoring assistant specialized in checking network health and detecting issues.
    Your role is to monitor the network by checking connectivity, latency, security alerts, and overall network status.
    Use the available monitoring tools (check_network_connectivity, check_network_latency, check_security_alerts, check_network_status)
    to identify any network problems. Report any issues found, including connectivity problems, high latency, or security threats.
    Be thorough in your monitoring and provide detailed status reports.
    """,
    tools=[
        check_network_connectivity,
        check_network_latency,
        check_security_alerts,
        check_network_status,
    ],
    output_key="monitoring_results",
)

remediation_agent = Agent(
    name="RemediationAgent",
    model=Gemini(
        model="gemini-3-flash-preview",
        temperature=0.0,
    ),
    description="This agent attempts to fix network problems by restarting services, adjusting firewall rules, and optimizing network performance.",
    instruction="""You are a network remediation assistant specialized in fixing network issues.
    Your role is to attempt to resolve network problems detected by the monitoring agent.
    Use the available remediation tools (restart_network_service, adjust_firewall_rules, fix_connectivity_issue,
    optimize_network_latency, block_security_threat) to address issues such as:
    - Connectivity problems: Use fix_connectivity_issue or restart_network_service
    - High latency: Use optimize_network_latency
    - Security threats: Use block_security_threat or adjust_firewall_rules
    - Service failures: Use restart_network_service
    Analyze the issue and apply the appropriate remediation steps.
    Report the results of your remediation attempts.
    If the network is stable, call the exit_loop tool to end the loop.
    """,
    tools=[
        restart_network_service,
        adjust_firewall_rules,
        fix_connectivity_issue,
        optimize_network_latency,
        block_security_threat,
        exit_loop,
    ],
    output_key="remediation_results",
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
    """,
    output_key="start_results",
)
summary_agent = Agent(
    name="SummaryAgent",
    model=Gemini(
        model="gemini-3-flash-preview",
        temperature=0.0,
    ),
    description="This agent is the summary point of the workflow.",
    instruction="""You are a network troubleshooting assistant specialized in summarizing the workflow. 
    You will get the output from the previous agents
    monitoring_results: {monitoring_results}
    remediation_results: {remediation_results}
    and you will summarize the output in tabular format.""",
    output_key="summary_results",
)

loop_agent = LoopAgent(
    name="NetworkLoopAgent",
    sub_agents=[network_monitoring_agent, remediation_agent],
    description="""This agent monitors a network and automatically attempts 
    to fix common network problems. It checks for connectivity issues, 
    latency problems, and security alerts. If problems are detected, 
    it calls the remediation agent to attempt to resolve them. """,
    max_iterations=3,       # Maximum number of iterations to run the loop before exitingx
)

sequential_pipeline_agent = SequentialAgent(
    name="SequentialPipelineAgent",
    sub_agents=[start_agent, loop_agent, summary_agent],
    description="""This agent is the sequential pipeline of the workflow.
    It will start the workflow, monitor the network, attempt to fix the network problems,
    and summarize the output.""",
)

app = App(root_agent=loop_agent, name="loop")
