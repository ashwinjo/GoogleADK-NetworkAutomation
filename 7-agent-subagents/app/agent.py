"""
Author: Ashwin Joshi

Title:

Purpose:

ADK Feature Uses:

Useful links:
  - Agent Development Kit (ADK) Documentation: 
  
"""

import os
import google.auth
import logging
from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.models import Gemini
from google.genai import types

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

from .app_utils.tools import (
    # Monitoring tools
    check_website_availability,
    check_response_time,
    check_packet_loss,
    # Analysis tools
    analyze_network_traffic,
    analyze_latency,
    identify_bottlenecks,
    # Remediation tools
    restart_web_server,
    clear_cache,
    optimize_routing,
    # Reporting tools
    format_report,
)

# ============================================================================
# SUB-AGENTS
# ============================================================================

monitoring_agent = Agent(
    name="MonitoringAgent",
    model=Gemini(
        model="gemini-3-flash-preview",
        temperature=0.0,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    description="This agent monitors network status by checking website availability, response times, and packet loss.",
    instruction="""You are a network monitoring assistant specialized in checking network health and detecting issues.

    Your role is to monitor the network by:
    1. Checking website availability using check_website_availability tool
    2. Measuring response times using check_response_time tool
    3. Checking packet loss using check_packet_loss tool

    When you receive a task from the parent NetworkTroubleshootingAgent:
    - Extract the website URL from the task description
    - Perform comprehensive monitoring checks
    - Report all findings in a clear, structured format
    - Include all relevant metrics and status information

    Be thorough and provide detailed monitoring results that will help the AnalysisAgent identify root causes.
    """,
    tools=[
        check_website_availability,
        check_response_time,
        check_packet_loss,
    ],
    output_key="monitoring_results",
)

analysis_agent = Agent(
    name="AnalysisAgent",
    model=Gemini(
        model="gemini-3-flash-preview",
        temperature=0.0,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    description="This agent analyzes network traffic, latency patterns, and identifies bottlenecks.",
    instruction="""You are a network analysis assistant specialized in analyzing network performance and identifying issues.

    Your role is to analyze network data by:
    1. Analyzing network traffic patterns using analyze_network_traffic tool
    2. Analyzing latency patterns using analyze_latency tool
    3. Identifying bottlenecks using identify_bottlenecks tool

    When you receive monitoring results from the MonitoringAgent:
    - Extract the website URL from the context
    - Perform deep analysis of network traffic and latency
    - Identify specific bottlenecks and root causes
    - Provide actionable insights for remediation

    Your analysis should help the RemediationAgent understand what needs to be fixed.
    """,
    tools=[
        analyze_network_traffic,
        analyze_latency,
        identify_bottlenecks,
    ],
    output_key="analysis_results",
)

remediation_agent = Agent(
    name="RemediationAgent",
    model=Gemini(
        model="gemini-3-flash-preview",
        temperature=0.0,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    description="This agent attempts to fix network problems by restarting services, clearing cache, and optimizing routing.",
    instruction="""You are a network remediation assistant specialized in fixing network issues.

    Your role is to remediate network problems by:
    1. Restarting web servers using restart_web_server tool
    2. Clearing caches using clear_cache tool
    3. Optimizing routing using optimize_routing tool

    When you receive analysis results from the AnalysisAgent:
    - Review the identified issues and bottlenecks
    - Determine the appropriate remediation actions
    - Execute remediation steps based on the issues found
    - Report the results of each remediation attempt

    Choose remediation actions based on the issues identified:
    - Server issues → restart_web_server tool
    - Cache problems → clear_cache tool
    - Routing/latency issues → optimize_routing tool

    Provide clear reports on what actions were taken and their outcomes.
    """,
    tools=[
        restart_web_server,
        clear_cache,
        optimize_routing,
    ],
    output_key="remediation_results",
)

reporting_agent = Agent(
    name="ReportingAgent",
    model=Gemini(
        model="gemini-3-flash-preview",
        temperature=0.0,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    description="This agent formats and presents troubleshooting results in a comprehensive report.",
    instruction="""You are a reporting assistant specialized in creating comprehensive troubleshooting reports.

    Your role is to:
    1. Review the entire conversation history to collect results from MonitoringAgent, AnalysisAgent, and RemediationAgent
    2. Extract the original user report/issue from the beginning of the conversation
    3. Extract monitoring_results from MonitoringAgent's output (look for output_key "monitoring_results" in conversation history)
    4. Extract analysis_results from AnalysisAgent's output (look for output_key "analysis_results" in conversation history)
    5. Extract remediation_results from RemediationAgent's output (which you receive directly, look for output_key "remediation_results")
    6. Use format_report tool with all four pieces of information (monitoring_results, analysis_results, remediation_results, user_report) to create a comprehensive report
    7. Present the final report to the user

    When calling format_report tool:
    - Pass monitoring_results: Extract the complete output from MonitoringAgent from the conversation history
    - Pass analysis_results: Extract the complete output from AnalysisAgent from the conversation history  
    - Pass remediation_results: Extract the complete output from RemediationAgent (this is the input you received)
    - Pass user_report: Extract the original user issue/report from the beginning of the conversation
    
    The report should summarize the entire troubleshooting process and provide clear next steps.
    """,
    tools=[
        format_report,
    ],
    output_key="final_report",
)

# ============================================================================
# PARENT ORCHESTRATION AGENT
# ============================================================================

network_troubleshooting_agent = Agent(
    name="NetworkTroubleshootingAgent",
    sub_agents=[
        monitoring_agent,
        analysis_agent,
        remediation_agent,
        reporting_agent,
    ],
    description="""This is the parent orchestration agent that 
    coordinates the entire network troubleshooting workflow.

    It receives user reports about website issues and orchestrates a hierarchical 
    troubleshooting process in the order below:

    1. MonitoringAgent: Checks website availability, response times, and packet loss
    2. AnalysisAgent: Analyzes network traffic, latency patterns, and identifies bottlenecks
    3. RemediationAgent: Attempts to fix identified issues through various remediation actions
    4. ReportingAgent: Formats and presents a comprehensive report of the entire process

    The agent delegates tasks to sub-agents in sequence, with each sub-agent building upon the results 
    from the previous one. This hierarchical structure allows for specialized expertise at each stage 
    of the troubleshooting process.
    """,
    model=Gemini(
        model="gemini-3-flash-preview",
        temperature=0.0,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="""You are the Network Troubleshooting Agent, the parent orchestration agent for automated 
network troubleshooting and remediation.

When a user reports a network issue (e.g., "Website is slow" or "Website is not responding"):
1. Delegate to MonitoringAgent to check the website's current status
2. Pass the monitoring results to AnalysisAgent to identify root causes
3. Pass the analysis results to RemediationAgent to attempt fixes
4. Pass all results to ReportingAgent to generate a comprehensive report

Your role is to coordinate the workflow and ensure each sub-agent receives the appropriate context 
and instructions. You should provide clear task descriptions to each sub-agent based on the user's 
original report and the results from previous agents.

Always ensure the workflow completes successfully and that the final report is presented to the user.
""",
)

# ============================================================================
# APP CONFIGURATION
# ============================================================================

app = App(root_agent=network_troubleshooting_agent, name="app")
