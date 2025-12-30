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
from google.adk.agents import SequentialAgent
import os
import google.auth
import logging

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

from .app_utils.tools import gather_device_information, check_device_status, ping_test, traceroute, check_firewall_rules


gather_device_information_agent = Agent(
    name="gather_device_information_agent",
    model=Gemini(
        model="gemini-3-flash-preview",
        temperature=0.0,
    ),
    description="This agent gathers information about network issues from the user.",
    instruction="""You are a network troubleshooting assistant specialized in gathering device information.
    Your role is to collect and summarize information about network issues, including affected devices,
    error messages, and problem descriptions. Use the gather_device_information tool to retrieve this information.
    """,
    tools=[gather_device_information],
    output_key="device_information",
)

check_device_status_agent = Agent(
    name="check_device_status_agent",
    model=Gemini(
        model="gemini-3-flash-preview",
        temperature=0.0,
    ),
    description="This agent queries the Network Management System (NMS) for device status information.",
    instruction="""You are a network monitoring assistant specialized in checking device status.
    Your role is to query the NMS for device status, including system metrics, interface status,
    routing protocol status, and overall device health. Use the check_device_status tool to retrieve this information.
    """,
    tools=[check_device_status],
    output_key="device_status",
)

ping_test_agent = Agent(
    name="ping_test_agent",
    model=Gemini(
        model="gemini-3-flash-preview",
        temperature=0.0,
    ),
    description="This agent performs ping tests to verify device connectivity.",
    instruction="""You are a network connectivity assistant specialized in performing ping tests.
    Your role is to execute ping tests to verify device reachability and measure network latency.
    Use the ping_test tool to perform connectivity tests and analyze the results.
    """,
    tools=[ping_test],
    output_key="ping_test_results",
)

traceroute_agent = Agent(
    name="traceroute_agent",
    model=Gemini(
        model="gemini-3-flash-preview",
        temperature=0.0,
    ),
    description="This agent runs traceroute to identify network path and potential bottlenecks.",
    instruction="""You are a network path analysis assistant specialized in traceroute operations.
    Your role is to execute traceroute tests to identify the network path to a device,
    measure hop-by-hop latency, and detect potential bottlenecks. Use the traceroute tool to perform path analysis.
    """,
    tools=[traceroute],
    output_key="traceroute_results",
)

check_firewall_rules_agent = Agent(
    name="check_firewall_rules_agent",
    model=Gemini(
        model="gemini-3-flash-preview",
        temperature=0.0,
    ),
    description="This agent verifies firewall rules to ensure traffic is not being blocked.",
    instruction="""You are a network security assistant specialized in firewall rule verification.
    Your role is to check firewall configurations and rules to ensure legitimate traffic is not being blocked.
    Use the check_firewall_rules tool to verify firewall policies and access control lists.
    """,
    tools=[check_firewall_rules],
    output_key="firewall_rules_results",
)


summarize_network_findings_agent = Agent(
    name="summarize_network_findings_agent",
    model=Gemini(
        model="gemini-3-flash-preview",
        temperature=0.0,
    ),
    description="This agent summarizes the network findings and provides a recommendation for the next steps.",
    instruction="""You are a network troubleshooting assistant specialized in summarizing network findings.
    
    You will get the following information from the previous agents:
    device status whose output is {device_information}
    ping testing is {ping_test_results}, 
    tracerouting is {traceroute_results}, 
    checking firewall rules whose output is {firewall_rules_results}.
    
    **Output:**
    Once you have gathered all the information show me output in tabular format""")


# Create the sequential agent with minimal callback
sequential_network_tshoot_workflow_agent = SequentialAgent(
                                            name="NetworkDeviceTroubleshootingAgent",
                                            sub_agents=[gather_device_information_agent, 
                                                        check_device_status_agent, 
                                                        ping_test_agent, 
                                                        traceroute_agent, 
                                                        check_firewall_rules_agent,
                                                        summarize_network_findings_agent],
                                            description="""This agent will troubleshoot a 
                                            network device by gathering information,
                                            by executing the subagents 
                                            and summarizing the findings."""
                                            
)
# We cannot use instruction here inside the workflow Agent
root_agent=sequential_network_tshoot_workflow_agent

app = App(root_agent=root_agent, name="sequential")
