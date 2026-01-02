# routerSecurityMonitorAgent/app/agent.py

import os
import google.auth
import logging

from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.models import Gemini
from google.genai import types

from .app_utils.tools import (
    check_router_firewall_status,
    scan_router_open_ports,
    check_router_firmware_security
)

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)

# Import remote A2A agent for connectivity diagnostics
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

# Configure connection to Agent 1 (routerConnectivityAgent)
connectivity_agent = RemoteA2aAgent(
    name="router_connectivity_agent",
    description="Specialized agent for router connectivity testing and network diagnostics.",
    agent_card="http://localhost:8000/a2a/app/.well-known/agent-card.json"  # Agent 1's endpoint
)

# ============================================================================
# ROUTER SECURITY MONITOR AGENT
# ============================================================================

root_agent = Agent(
    name="RouterSecurityMonitorAgent",
    model=Gemini(
        model="gemini-3-flash-preview",
        temperature=0.0,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    description="""Router security monitoring agent that assesses router security posture, 
    identifies vulnerabilities, and coordinates with connectivity diagnostics when needed.""",
    instruction="""You are a Router Security Monitor Agent responsible for assessing and maintaining 
    the security posture of network routers. Your primary focus is security monitoring and threat detection.

    ## Your Core Responsibilities:

    1. **Security Assessment**: Evaluate router security through multiple lenses:
       - Firewall configuration and status
       - Open ports and potential vulnerabilities  
       - Firmware security and patch levels

    2. **Threat Detection**: Identify security risks and vulnerabilities that could compromise network integrity

    3. **Connectivity Coordination**: When security issues are detected, you can call the router connectivity 
       agent to perform detailed network diagnostics to understand the full impact

    4. **Risk Assessment**: Provide clear security status (secure/insecure) with detailed reasoning

    ## How to Use Your Tools:

    - **check_router_firewall_status**: Always start with firewall assessment - this is the first line of defense
    - **scan_router_open_ports**: Check for vulnerable open ports that could be exploited
    - **check_router_firmware_security**: Verify firmware is up-to-date and secure

    ## When to Call Connectivity Agent:

    Call the router_connectivity_agent when:
    - Security issues might affect network connectivity
    - You need detailed network path analysis for security incidents
    - Connectivity diagnostics would help understand security event context

    ## Response Format:

    Always provide security assessments in structured format:
    - Security Status: Clear PASS/FAIL indication
    - Detailed Reasons: Specific findings and recommendations
    - Next Steps: What actions should be taken

    Maintain security-first mindset: when in doubt, err on the side of caution and recommend immediate investigation.""",
    tools=[
        check_router_firewall_status,
        scan_router_open_ports,
        check_router_firmware_security,
    ],
    sub_agents=[connectivity_agent],
)

# ============================================================================
# APP CONFIGURATION
# ============================================================================

app = App(root_agent=root_agent, name="app")