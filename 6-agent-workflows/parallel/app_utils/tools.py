"""
Network troubleshooting tools for Cisco routers.
All functions accept router_name as argument and return JSON with tool_call_status, output, and reachability.
"""

import json
from typing import Dict, Any


def check_cpu_utilization_r1_sea3(device_name: str = "r1-sea3") -> Dict[str, Any]:
    """
    Check CPU utilization on r1-sea3 device.
    
    Args:
        device_name: Name of the device (default: r1-sea3)
        
    Returns:
        Dictionary with tool_call_status, output, and reachability fields
    """
    # Simulated CPU utilization values for r1-sea3: Normal CPU utilization
    cpu_utilization = 38.5
    memory_utilization = 52.0
    
    # Determine status
    status = "NORMAL" if cpu_utilization < 70 else "HIGH"
    
    output = f"""
CPU Utilization Report for {device_name}:
==========================================

Device: {device_name}
----------------------
CPU Utilization: {cpu_utilization}%
Memory Utilization: {memory_utilization}%
Status: {status}
Threshold: < 70% (Normal), >= 70% (High)

Analysis:
=========
✓ CPU utilization is within normal range ({cpu_utilization}%)
✓ Device is operating normally
✓ No performance degradation expected

System Metrics:
===============
- CPU Usage: {cpu_utilization}% (Normal)
- Memory Usage: {memory_utilization}%
- Temperature: 42°C (Normal)
- Uptime: 45 days, 12 hours, 23 minutes

Conclusion:
===========
{device_name} is operating within normal parameters. CPU utilization 
is healthy and should not impact throughput performance.
"""
    
    return {
        "tool_call_status": "success",
        "output": output.strip(),
        "reachability": "yes",
        "cpu_utilization": cpu_utilization,
        "memory_utilization": memory_utilization,
        "status": status
    }


def check_cpu_utilization_r2_sea3(device_name: str = "r2-sea3") -> Dict[str, Any]:
    """
    Check CPU utilization on r2-sea3 device and identify high CPU utilization issues.
    
    Args:
        device_name: Name of the device (default: r2-sea3)
        
    Returns:
        Dictionary with tool_call_status, output, and reachability fields
    """
    # Simulated CPU utilization values for r2-sea3: High CPU utilization (causing throughput issues)
    cpu_utilization = 87.3
    memory_utilization = 68.0
    
    # Determine status
    status = "HIGH" if cpu_utilization >= 70 else "NORMAL"
    
    output = f"""
CPU Utilization Report for {device_name}:
==========================================

Device: {device_name}
----------------------
CPU Utilization: {cpu_utilization}% [HIGH CPU DETECTED]
Memory Utilization: {memory_utilization}%
Status: {status}
Threshold: < 70% (Normal), >= 70% (High)

Analysis:
=========
✗ CPU utilization is HIGH ({cpu_utilization}%) - EXCEEDS THRESHOLD
✗ Device performance may be degraded
✗ Throughput issues likely due to high CPU utilization

System Metrics:
===============
- CPU Usage: {cpu_utilization}% (HIGH - Exceeds 70% threshold)
- Memory Usage: {memory_utilization}%
- Temperature: 48°C (Elevated)
- Uptime: 45 days, 12 hours, 23 minutes

Root Cause Identification:
==========================
The high CPU utilization on {device_name} ({cpu_utilization}%) is likely 
the primary cause of reduced throughput compared to r1-sea3.

Impact Assessment:
==================
Performance degradation expected due to high CPU ({cpu_utilization}%):
  - Packet processing delays
  - Reduced forwarding capacity
  - Potential packet drops under load
  - Increased latency
  - Lower throughput compared to r1-sea3

Recommendations:
================
1. Investigate processes consuming CPU on {device_name}
2. Check for routing protocol convergence issues
3. Review interface statistics for high packet rates
4. Consider load balancing or traffic redistribution
5. Monitor CPU trends over time to identify patterns
6. Check for background processes or scheduled tasks
7. Review routing table size and complexity
"""
    
    return {
        "tool_call_status": "success",
        "output": output.strip(),
        "reachability": "yes",
        "cpu_utilization": cpu_utilization,
        "memory_utilization": memory_utilization,
        "status": status,
        "high_cpu_alert": True
    }

