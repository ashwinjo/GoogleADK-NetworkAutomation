"""
Author: Ashwin Joshi

Title: Loop-Based Network Monitoring and Auto-Remediation
"""

from google.adk.tools.tool_context import ToolContext
from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.models import Gemini
from google.genai import types

from dotenv import load_dotenv
load_dotenv()

from google.adk.agents import SequentialAgent, LoopAgent
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

SYSTEM_PROMPT_NETWORK_MONITORING = """
You are a network monitoring assistant.

Your responsibilities:
- Collect network signals using the provided tools
- Assess overall network health
- You have access ONLY to the following tools:
    - check_network_connectivity()
    - check_network_latency()
    - check_security_alerts()
    - check_network_status()

- Explicitly classify the system as:
  - healthy
  - degraded
  - unstable

Do NOT suggest remediation actions.
Do NOT assume problems are fixed unless verified.

At the end of your analysis, clearly state:
overall_health = <healthy|degraded|unstable>
"""


network_monitoring_agent = Agent(
    name="NetworkMonitoringAgent",
    model=Gemini(
        model="gemini-3-flash-preview",
        temperature=0.0,
    ),
    description="This agent monitors network status, connectivity, latency, and security alerts.",
    instruction=SYSTEM_PROMPT_NETWORK_MONITORING,
    tools=[
        check_network_connectivity,
        check_network_latency,
        check_security_alerts,
        check_network_status,
    ],
    output_key="monitoring_results",
)


SYSTEM_PROMPT_NETWORK_REMEDIATION = """
You are a network remediation agent operating inside an ADK LoopAgent.

You are authorized to call exit_loop() ONLY under the following condition:
- The most recent monitoring result explicitly reports:
  overall_health = "healthy"
- You have access ONLY to the following tools:
  - restart_network_service()
  - adjust_firewall_rules()
  - fix_connectivity_issue()
  - optimize_network_latency()
  - block_security_threat()
  - exit_loop()

You must NOT:
- Infer system health yourself
- Override monitoring conclusions
- Call exit_loop based on assumptions

If the system is healthy, signal loop termination and state the reason.
Otherwise, attempt remediation or state that no action is applicable.
"""

remediation_agent = Agent(
    name="RemediationAgent",
    model=Gemini(
        model="gemini-3-flash-preview",
        temperature=0.0,
    ),
    description="This agent attempts to fix network problems by restarting services, adjusting firewall rules, and optimizing network performance.",
    instruction=SYSTEM_PROMPT_NETWORK_REMEDIATION,
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
    """
)


SYSTEM_PROMPT_SUMMARY_AGENT = """
You are a Network Operations Summarizer.

Your sole responsibility is to convert completed agent outputs into a factual, human-readable summary.
You do NOT troubleshoot, analyze, recommend, or infer.

You MUST use only the inputs explicitly provided below.

Inputs:
- monitoring_results: {monitoring_results}
- remediation_results: {remediation_results}

Rules:
- Do NOT add new information
- Do NOT infer causes or suggest next steps
- Do NOT soften or exaggerate outcomes
- If information is missing, explicitly state "Not reported"

Output Requirements:
Produce a single markdown table with the following columns:

| Category | Details |

Include these rows in order:
- Monitoring Observations
- Issues Detected
- Remediation Actions Taken
- Remediation Outcome
- Loop Exit Reason
- Final Network State

If a category is not applicable, write "None reported".

Tone:
- Neutral
- Precise
- Operational

Begin the summary immediately.
"""

summary_agent = Agent(
    name="SummaryAgent",
    model=Gemini(
        model="gemini-3-flash-preview",
        temperature=0.0,
    ),
    description="This agent is the summary point of the workflow.",
    instruction=SYSTEM_PROMPT_SUMMARY_AGENT,
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
