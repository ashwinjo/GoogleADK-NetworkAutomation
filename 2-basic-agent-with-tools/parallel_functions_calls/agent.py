"""
Author: Ashwin Joshi

Title: Parallel Network Diagnostics Agent

Purpose:
Demonstrate parallel execution of network observability and diagnostics
functions using Google ADK, simulating real-world network troubleshooting.

ADK Feature Uses:
- Parallel tool calling
- Shared ToolContext state
- Async I/O-bound network operations
- Agent-driven orchestration

Useful links:
  - Agent Development Kit (ADK) Documentation
"""

import asyncio
import time
from typing import List
import logging

from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.tools.tool_context import ToolContext

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

# -------------------------
# Network Tools
# -------------------------

async def get_device_health(device: str, tool_context: ToolContext) -> dict:
    """Simulate retrieving device health status."""
    await asyncio.sleep(2)

    health_db = {
        "router1": {"status": "up", "cpu": 42, "memory": 61},
        "router2": {"status": "degraded", "cpu": 88, "memory": 79},
        "fw1": {"status": "up", "cpu": 35, "memory": 55},
    }

    result = health_db.get(device, {"status": "unknown", "cpu": 0, "memory": 0})

    tool_context.state.setdefault("device_health_checks", []).append({
        "device": device,
        "result": result,
        "timestamp": time.time(),
    })

    return {
        "device": device,
        "health_status": result["status"],
        "cpu_percent": result["cpu"],
        "memory_percent": result["memory"],
    }


async def get_link_utilization(
    src: str, dst: str, tool_context: ToolContext
) -> dict:
    """Simulate retrieving link utilization."""
    await asyncio.sleep(1.5)

    utilization = {
        ("dc1", "dc2"): 72,
        ("dc1", "branch1"): 35,
        ("dc2", "branch1"): 81,
    }

    usage = utilization.get((src, dst), 50)

    tool_context.state.setdefault("link_utilization_checks", []).append({
        "src": src,
        "dst": dst,
        "utilization": usage,
        "timestamp": time.time(),
    })

    return {
        "source": src,
        "destination": dst,
        "utilization_percent": usage,
    }


async def measure_latency(
    src: str, dst: str, tool_context: ToolContext
) -> dict:
    """Simulate measuring network latency."""
    await asyncio.sleep(1)

    latency_db = {
        ("dc1", "dc2"): 42,
        ("dc1", "branch1"): 18,
        ("dc2", "branch1"): 65,
    }

    latency = latency_db.get((src, dst), 100)

    tool_context.state.setdefault("latency_measurements", []).append({
        "src": src,
        "dst": dst,
        "latency_ms": latency,
        "timestamp": time.time(),
    })

    return {
        "source": src,
        "destination": dst,
        "latency_ms": latency,
    }

# -------------------------
# Agent Definition
# -------------------------

network_agent = Agent(
    model="gemini-2.0-flash",
    name="parallel_network_diagnostics_agent",
    description=(
        "Agent that performs parallel network health, latency, "
        "utilization, and endpoint analysis."
    ),
    instruction="""
    You are a network diagnostics assistant.

    When users ask about network issues, performance problems,
    or site-to-site connectivity, you should:

    - Run device health checks
    - Measure latency
    - Check link utilization
    - Count active endpoints

    Use multiple tools in parallel whenever possible to
    reduce troubleshooting time.

    Correlate results clearly and provide structured,
    actionable insights.
    """,
    tools=[
        get_device_health,
        get_link_utilization,
        measure_latency
    ],
)

app = App(root_agent=network_agent, name="parallel_functions_calls")