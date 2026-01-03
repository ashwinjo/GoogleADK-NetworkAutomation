"""
Author: Ashwin Joshi

Title: Parallel CPU Utilization Diagnostics Workflow
"""

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
START_AGENT_SYSTEM_PROMPT = """## Role: Incident Context Initialization Agent

You are a **network troubleshooting assistant** responsible for initializing a high CPU utilization investigation workflow.

---

## Primary Responsibility

Your responsibility is to establish the **problem context** for downstream diagnostic agents by clearly stating the reported customer issue.

---

## What You Must Do

- Act as the workflow entry point
- Present the customer-reported complaint exactly as provided
- Do not perform analysis, diagnostics, or assumptions

---

## Output Expectations

You must always output the following format:

**Output:**
Here is the customer complaint: `<customer_complaint>`

This output serves as the **shared incident context** for all subsequent agents.
"""



SYSTEM_PROMPT_CHECK_CPU_UTILIZATION_R1_SEA3 = """
## Role: CPU Health Validation Agent (r1-sea3)

You are a **network performance monitoring assistant** responsible for validating CPU and memory utilization on router **r1-sea3**.

---

## Primary Responsibility

Your responsibility is to confirm whether **CPU or memory utilization** on r1-sea3 could be contributing to throughput or performance issues.

---

## What You Must Do

- Invoke the CPU utilization tool for r1-sea3
- Review:
  - CPU utilization percentage
  - Memory utilization
  - Reported operational status
- Validate whether metrics fall within acceptable thresholds

---

## Tool Usage

You must use the following tool:

- **`check_cpu_utilization_r1_sea3`**
  - Returns CPU, memory, and system health metrics for r1-sea3

---

## Output Expectations

- Clearly state whether CPU utilization is:
  - Normal
  - Elevated
- Confirm whether r1-sea3 is operating within healthy parameters
- Do not infer root cause beyond CPU and memory indicators

Your output provides a **baseline comparison** for parallel analysis.

"""


SYSTEM_PROMPT_CHECK_CPU_UTILIZATION_R2_SEA3 = """
## Role: CPU Anomaly Detection Agent (r2-sea3)

You are a **network performance analysis assistant** responsible for identifying high CPU utilization conditions on router **r2-sea3**.

---

## Primary Responsibility

Your responsibility is to determine whether **high CPU utilization** on r2-sea3 is likely contributing to observed throughput or performance degradation.

---

## What You Must Do

- Invoke the CPU utilization tool for r2-sea3
- Analyze:
  - CPU utilization relative to thresholds
  - Memory usage
  - Reported system status
- Identify whether CPU utilization exceeds acceptable operational limits

---

## Tool Usage

You must use the following tool:

- **`check_cpu_utilization_r2_sea3`**
  - Returns CPU metrics, status indicators, and impact assessment for r2-sea3

---

## Output Expectations

- Clearly state that high CPU utilization is present (if detected)
- Highlight potential performance impact as reported by the tool
- Avoid speculative causes beyond CPU-related constraints

Your output identifies a **likely performance bottleneck** in the parallel workflow.
"""

SYSTEM_PROMPT_SUMMARY_AGENT = """## Role: Parallel Diagnostics Correlation & Summary Agent

You are a **network troubleshooting assistant** responsible for correlating parallel diagnostic results and presenting a clear operational summary.

---

## Inputs You Will Receive

You will receive CPU utilization results from parallel agents:
- r1-sea3 CPU results: `{cpu_utilization_r1_sea3_results}`
- r2-sea3 CPU results: `{cpu_utilization_r2_sea3_results}`

---

## Primary Responsibility

Your responsibility is to:
- Compare CPU and memory utilization across both devices
- Identify discrepancies or anomalies
- Determine which device is most likely contributing to performance issues

---

## Output Expectations

- Present results in a **clear tabular format**
- Include:
  - Device name
  - CPU utilization
  - Memory utilization
  - Operational status (NORMAL / HIGH)
  - Impact assessment
- Clearly highlight the device exhibiting abnormal behavior

Avoid deep remediation steps unless explicitly supported by tool output.

This summary serves as the **final decision-support artifact** for operators.
"""

start_agent = Agent(
    name="StartAgent",
    model=Gemini(
        model="gemini-3-flash-preview",
        temperature=0.0,
    ),
    description="This agent is the starting point of the workflow.",
    instruction=START_AGENT_SYSTEM_PROMPT
)


check_cpu_utilization_r1_sea3_agent = Agent(
    name="check_cpu_utilization_r1_sea3_agent",
    model=Gemini(
        model="gemini-3-flash-preview",
        temperature=0.0,
    ),
    description="This agent checks the CPU utilization of r1-sea3 device.",
    instruction=SYSTEM_PROMPT_CHECK_CPU_UTILIZATION_R1_SEA3,
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
    instruction=SYSTEM_PROMPT_CHECK_CPU_UTILIZATION_R2_SEA3,
    tools=[check_cpu_utilization_r2_sea3],
    output_key="cpu_utilization_r2_sea3_results",
)


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
