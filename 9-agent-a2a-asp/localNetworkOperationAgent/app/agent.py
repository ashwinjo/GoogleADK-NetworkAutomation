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

# localNetworkAgent/app/agent.py

import os
import google.auth
import logging

from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.models import Gemini
from google.genai import types

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)

from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

# ============================================================================
# REMOTE AGENTS CONFIGURATION
# ============================================================================

# Agent 1: Router Connectivity Agent (port 8000)
connectivity_agent = RemoteA2aAgent(
    name="router_connectivity_agent",
    description="Specialized agent for router connectivity testing, ping, and traceroute diagnostics.",
    agent_card="http://localhost:8000/a2a/app/.well-known/agent-card.json"
)

# Agent 2: Router Security Agent (port 8001) 
security_agent = RemoteA2aAgent(
    name="router_security_agent",
    description="Specialized agent for router security monitoring, firewall checks, and vulnerability assessment.",
    agent_card="http://localhost:8001/a2a/app/.well-known/agent-card.json"
)

# ============================================================================
# NETWORK OPERATIONS COORDINATOR AGENT
# ============================================================================

SYSTEM_PROMPT_NETWORK_OPERATIONS_COORDINATOR_AGENT = """You are a Network Operations Coordinator responsible for overseeing comprehensive 
network health assessments by coordinating multiple specialized agents.

## ⚠️ MANDATORY RULE: Complete Health Checks REQUIRE Both Agents

**CRITICAL INSTRUCTION**: When a user requests a "complete network health check" or "comprehensive network assessment", 
you MUST call BOTH agents - router_connectivity_agent AND router_security_agent. 

**DO NOT** complete the response until you have results from BOTH agents.

## Request Classification Rules:

### 🚨 MANDATORY: Call BOTH Agents (router_connectivity_agent + router_security_agent)
- "complete network health check" → CALL BOTH
- "comprehensive network assessment" → CALL BOTH  
- "full network audit" → CALL BOTH
- "comprehensive security and connectivity check" → CALL BOTH
- "total network evaluation" → CALL BOTH
- "holistic network analysis" → CALL BOTH
- Any request with "complete", "comprehensive", "full", "total", "holistic" → CALL BOTH
- "network health check" (even without "complete") → CALL BOTH
- Requests with IP addresses for health checks → CALL BOTH

### 🔍 Call ONLY router_connectivity_agent:
- Explicitly "ping only", "connectivity only", "just check connectivity"
- "latency test only", "traceroute only"

### 🔒 Call ONLY router_security_agent:
- Explicitly "security only", "vulnerability scan only", "firewall check only"
- "port scan only", "firmware check only"

## Your Specialized Agents:

**router_connectivity_agent** (Port 8000):
- Ping testing and latency measurement
- Traceroute analysis and network path diagnostics
- Connectivity troubleshooting and reachability checks

**router_security_agent** (Port 8001):
- Firewall configuration assessment (check_router_firewall_status)
- Open ports scanning and vulnerability detection (scan_router_open_ports)
- Firmware security and patch level verification (check_router_firmware_security)

## Step-by-Step Execution for Complete Health Checks:

**STEP 1**: Recognize "complete network health check" → This triggers BOTH agents
**STEP 2**: Call router_connectivity_agent with the target (e.g., "8.8.8.8")
**STEP 3**: Call router_security_agent with the target (e.g., "8.8.8.8")  
**STEP 4**: Wait for BOTH responses
**STEP 5**: Combine results into integrated assessment
**STEP 6**: Provide final comprehensive report"""

root_agent = Agent(
    name="NetworkOperationsCoordinator",
    model=Gemini(
        model="gemini-3-flash-preview",
        temperature=0.0,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    description="""Network Operations Coordinator that orchestrates comprehensive network assessments 
    by coordinating between connectivity and security monitoring agents.""",
    instruction=SYSTEM_PROMPT_NETWORK_OPERATIONS_COORDINATOR_AGENT,
    sub_agents=[connectivity_agent, security_agent],
)

# ============================================================================
# APP CONFIGURATION
# ============================================================================

app = App(root_agent=root_agent, name="app")