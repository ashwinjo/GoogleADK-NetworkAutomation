"""
Network troubleshooting tools for Cisco routers.
All functions accept router_name as argument and return JSON with tool_call_status, output, and reachability.
"""

import json
from typing import Dict, Any


def gather_device_information(router_name: str) -> Dict[str, Any]:
    """
    Gather information about the issue from the user.
    
    Args:
        router_name: Name of the Cisco router to troubleshoot
        
    Returns:
        Dictionary with tool_call_status, output, and reachability fields
    """
    output = f"""
        Router: {router_name}
        Issue Report Summary:
        =====================
        Affected Devices: {router_name}
        Error Messages: 
        - Interface GigabitEthernet0/0/1 is down
        - BGP neighbor 192.168.1.1 is in Idle state
        - OSPF neighbor 10.0.0.1 is down
        """
            
    return {
        "tool_call_status": "success",
        "output": output.strip(),
        "reachability": "yes"
    }


def check_device_status(router_name: str) -> Dict[str, Any]:
    """
    Query the Network Management System (NMS) for the status of the affected device.
    
    Args:
        router_name: Name of the Cisco router to check
        
    Returns:
        Dictionary with tool_call_status, output, and reachability fields
    """
    output = f"""
    NMS Query Results for {router_name}:
    ====================================
    Device Name: {router_name}
    Device Type: Cisco ASR 1000 Series
    IP Address: 192.168.100.1
    SNMP Status: Reachable
    Last Poll: 2025-01-15 14:35:22 UTC

    System Status:
    CPU Utilization: 45%
    Memory Utilization: 62%
    Temperature: 42°C (Normal)
    
    Interface Status:
    GigabitEthernet0/0/0: UP/UP (Connected)
    GigabitEthernet0/0/1: DOWN/DOWN (Disconnected) [ISSUE DETECTED]
    GigabitEthernet0/0/2: UP/UP (Connected)
    Serial0/1/0: UP/UP (Connected)
    
    Routing Protocol Status:
    BGP: Active, 3 neighbors, 1 in Idle state
    OSPF: Active, 5 neighbors, 1 down
    EIGRP: Active, 2 neighbors, all established
    
    Uptime: 45 days, 12 hours, 23 minutes
    Last Reboot: 2024-12-01 02:15:00 UTC
    """
    
    return {
        "tool_call_status": "success",
        "output": output.strip(),
        "reachability": "yes"
    }


def ping_test(router_name: str) -> Dict[str, Any]:
    """
    Perform a ping test to the device from a known location.
    
    Args:
        router_name: Name of the Cisco router to ping
        
    Returns:
        Dictionary with tool_call_status, output, and reachability fields
    """
    output = f"""
                Ping Test Results for {router_name}:
                ====================================
                Source: Network Operations Center (NOC) - 10.0.0.100
                Destination: {router_name} - 192.168.100.1

                Type escape sequence to abort.
                Sending 5, 100-byte ICMP Echos to 192.168.100.1, timeout is 2 seconds:
                !!!!!
                Success rate is 100 percent (5/5), round-trip min/avg/max = 12/15/22 ms

                Extended Ping Statistics:
                Packets Sent: 5
                Packets Received: 5
                Packets Lost: 0 (0% loss)
                
                Round Trip Time (RTT):
                Minimum: 12 ms
                Average: 15 ms
                Maximum: 22 ms
                
                Path MTU Discovery:
                Path MTU: 1500 bytes
                
                Connectivity Status: REACHABLE
                """
    
    return {
        "tool_call_status": "success",
        "output": output.strip(),
        "reachability": "yes"
    }


def traceroute(router_name: str) -> Dict[str, Any]:
    """
    Run a traceroute to identify potential bottlenecks.
    
    Args:
        router_name: Name of the Cisco router to traceroute
        
    Returns:
        Dictionary with tool_call_status, output, and reachability fields
    """
    output = f"""
            Traceroute to {router_name} (192.168.100.1):
            ============================================
            Source: Network Operations Center (NOC) - 10.0.0.100

            Tracing the route to 192.168.100.1

            1  10.0.0.1 (10.0.0.1)  2 msec  1 msec  1 msec
            2  10.0.1.1 (10.0.1.1)  5 msec  4 msec  5 msec
            3  192.168.50.1 (192.168.50.1)  8 msec  7 msec  8 msec
            4  192.168.100.1 (192.168.100.1)  12 msec  15 msec  14 msec

            Path Analysis:
            Total Hops: 4
            Total Latency: 14 ms (average)
            
            Hop-by-Hop Breakdown:
            Hop 1 (10.0.0.1): 2 ms - Core Switch
            Hop 2 (10.0.1.1): 5 ms - Distribution Router
            Hop 3 (192.168.50.1): 8 ms - Edge Router
            Hop 4 (192.168.100.1): 14 ms - {router_name} [TARGET]
            
            Bottleneck Detection:
            No significant bottlenecks detected
            All hops responding within normal latency thresholds
            Path is optimal
            """
    
    return {
        "tool_call_status": "success",
        "output": output.strip(),
        "reachability": "yes"
    }


def check_firewall_rules(router_name: str) -> Dict[str, Any]:
    """
    Verify that firewall rules are not blocking traffic.
    
    Args:
        router_name: Name of the Cisco router to check firewall rules
        
    Returns:
        Dictionary with tool_call_status, output, and reachability fields
    """
    output = f"""
    Firewall Rules Check for {router_name}:
    =======================================
    Device: {router_name}
    IP Address: 192.168.100.1
    Firewall Type: Cisco Zone-Based Firewall

    Zone Configuration:
    Inside Zone: Trusted
    Outside Zone: Untrusted
    DMZ Zone: Semi-Trusted

    Active Firewall Policies:
    Policy Name: INSIDE_TO_OUTSIDE
        Status: Active
        Action: Inspect
        Service: HTTP, HTTPS, DNS, ICMP
        Status: ALLOWED
        
    Policy Name: OUTSIDE_TO_INSIDE
        Status: Active
        Action: Drop
        Service: All
        Status: BLOCKED (Expected)
        
    Policy Name: INSIDE_TO_DMZ
        Status: Active
        Action: Inspect
        Service: HTTP, HTTPS, SSH
        Status: ALLOWED

    Access Control Lists (ACLs):
    ACL Name: INBOUND_TRAFFIC
        Rule 10: Permit TCP 80,443 from any to 192.168.100.1 - MATCHED
        Rule 20: Permit ICMP from any to 192.168.100.1 - MATCHED
        Rule 30: Deny all - NOT MATCHED
        
    ACL Name: OUTBOUND_TRAFFIC
        Rule 10: Permit all from 192.168.100.1 - MATCHED

    Firewall Statistics:
    Packets Processed: 1,234,567
    Packets Allowed: 1,200,000 (97.2%)
    Packets Blocked: 34,567 (2.8%)
    
    Traffic Flow Status:
    Inbound Traffic: ALLOWED (No blocking detected)
    Outbound Traffic: ALLOWED (No blocking detected)
    Inter-Zone Traffic: ALLOWED (No blocking detected)
    
    Conclusion: No firewall rules are blocking legitimate traffic to/from {router_name}
    """
    
    return {
        "tool_call_status": "success",
        "output": output.strip(),
        "reachability": "yes"
    }

