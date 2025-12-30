"""
Network monitoring and remediation tools for loop agent.
All functions return JSON with tool_call_status, output, and network_status.
"""

import json
from typing import Dict, Any
import random


# ============================================================================
# NETWORK MONITORING TOOLS
# ============================================================================

def check_network_connectivity(server_address: str) -> Dict[str, Any]:
    """
    Check connectivity to a network server or device.
    
    Args:
        server_address: IP address or hostname of the server to check
        
    Returns:
        Dictionary with tool_call_status, output, and network_status fields
    """
    # Simulate connectivity check with random results
    is_reachable = random.choice([True, True, True, False])  # 75% success rate
    
    if is_reachable:
        output = f"""
        Connectivity Check Results for {server_address}:
        ================================================
        Target: {server_address}
        Status: REACHABLE
        
        Ping Test:
        Sending 5 ICMP packets to {server_address}
        Success rate: 100% (5/5)
        Round-trip time: min/avg/max = 8/12/18 ms
        
        TCP Connection Test:
        Port 80 (HTTP): OPEN
        Port 443 (HTTPS): OPEN
        Port 22 (SSH): OPEN
        
        DNS Resolution: SUCCESS
        Resolved IP: {server_address}
        
        Overall Status: CONNECTED
        """
        network_status = "healthy"
    else:
        output = f"""
        Connectivity Check Results for {server_address}:
        ================================================
        Target: {server_address}
        Status: UNREACHABLE
        
        Ping Test:
        Sending 5 ICMP packets to {server_address}
        Success rate: 0% (0/5)
        Request timeout
        
        TCP Connection Test:
        Port 80 (HTTP): TIMEOUT
        Port 443 (HTTPS): TIMEOUT
        Port 22 (SSH): TIMEOUT
        
        DNS Resolution: SUCCESS
        Resolved IP: {server_address}
        
        Overall Status: DISCONNECTED
        Issue Detected: No response from target server
        """
        network_status = "unreachable"
    
    return {
        "tool_call_status": "success",
        "output": output.strip(),
        "network_status": network_status
    }


def check_network_latency(server_address: str, threshold_ms: int = 100) -> Dict[str, Any]:
    """
    Check network latency to a server and compare against threshold.
    
    Args:
        server_address: IP address or hostname of the server to check
        threshold_ms: Maximum acceptable latency in milliseconds (default: 100ms)
        
    Returns:
        Dictionary with tool_call_status, output, and network_status fields
    """
    # Simulate latency measurement
    avg_latency = random.randint(15, 150)
    is_high_latency = avg_latency > threshold_ms
    
    output = f"""
    Latency Check Results for {server_address}:
    ===========================================
    Target: {server_address}
    Threshold: {threshold_ms} ms
    
    Latency Measurements (10 samples):
    Minimum: {avg_latency - 5} ms
    Average: {avg_latency} ms
    Maximum: {avg_latency + 10} ms
    Jitter: {random.randint(2, 8)} ms
    
    Threshold Comparison:
    Average Latency: {avg_latency} ms
    Threshold: {threshold_ms} ms
    Status: {'EXCEEDED' if is_high_latency else 'WITHIN LIMITS'}
    
    Path Analysis:
    Hop Count: {random.randint(5, 12)}
    Bottleneck Detected: {'YES - High latency detected' if is_high_latency else 'NO'}
    """
    
    network_status = "high_latency" if is_high_latency else "healthy"
    
    return {
        "tool_call_status": "success",
        "output": output.strip(),
        "network_status": network_status
    }


def check_security_alerts() -> Dict[str, Any]:
    """
    Check for security alerts and potential threats in the network.
    
    Returns:
        Dictionary with tool_call_status, output, and network_status fields
    """
    # Simulate security alert detection
    has_alerts = random.choice([True, False, False])  # 33% chance of alerts
    
    if has_alerts:
        alert_types = random.choice([
            ["Suspicious login attempts", "Port scan detected"],
            ["Firewall rule violation", "Unauthorized access attempt"],
            ["DDoS attack detected", "Malware signature detected"]
        ])
        
        output = f"""
        Security Alert Check Results:
        =============================
        Scan Time: 2025-01-15 14:45:30 UTC
        
        Security Status: ALERTS DETECTED
        
        Active Alerts ({len(alert_types)}):
        """
        for i, alert in enumerate(alert_types, 1):
            output += f"""
        Alert #{i}: {alert}
            Severity: {'HIGH' if 'attack' in alert.lower() or 'malware' in alert.lower() else 'MEDIUM'}
            Source IP: 192.168.{random.randint(1, 255)}.{random.randint(1, 255)}
            Timestamp: 2025-01-15 14:{random.randint(40, 50)}:{random.randint(0, 59)} UTC
            Status: ACTIVE"""
        
        output += f"""
        
        Firewall Status:
        Active Connections: {random.randint(500, 2000)}
        Blocked Connections (last hour): {random.randint(50, 500)}
        Intrusion Detection: ACTIVE
        
        Recommendation: Immediate remediation required
        """
        network_status = "security_alert"
    else:
        output = f"""
        Security Alert Check Results:
        =============================
        Scan Time: 2025-01-15 14:45:30 UTC
        
        Security Status: NO ALERTS
        
        Active Alerts: 0
        Firewall Status: NORMAL
        Intrusion Detection: ACTIVE (No threats detected)
        Active Connections: {random.randint(500, 2000)}
        Blocked Connections (last hour): {random.randint(0, 20)}
        
        Overall Status: SECURE
        """
        network_status = "healthy"
    
    return {
        "tool_call_status": "success",
        "output": output.strip(),
        "network_status": network_status
    }


def check_network_status(server_addresses: str) -> Dict[str, Any]:
    """
    Comprehensive network status check for multiple servers.
    
    Args:
        server_addresses: Comma-separated list of server addresses to check
        
    Returns:
        Dictionary with tool_call_status, output, and network_status fields
    """
    addresses = [addr.strip() for addr in server_addresses.split(",")]
    issues_found = []
    
    output = f"""
    Comprehensive Network Status Check:
    ===================================
    Check Time: 2025-01-15 14:50:00 UTC
    Servers Checked: {len(addresses)}
    
    Server Status Summary:
    """
    
    for addr in addresses:
        is_healthy = random.choice([True, True, False])  # 66% healthy
        if not is_healthy:
            issues_found.append(addr)
        
        output += f"""
    {addr}:
        Connectivity: {'UP' if is_healthy else 'DOWN'}
        Latency: {random.randint(10, 200)} ms
        Response Time: {'Normal' if is_healthy else 'Timeout'}
        """
    
    if issues_found:
        output += f"""
    
    Issues Detected:
    - {len(issues_found)} server(s) with connectivity problems: {', '.join(issues_found)}
    - Network stability: DEGRADED
    
    Recommendation: Remediation required
    """
        network_status = "degraded"
    else:
        output += f"""
    
    Overall Network Status: HEALTHY
    All servers responding normally
    No issues detected
    """
        network_status = "healthy"
    
    return {
        "tool_call_status": "success",
        "output": output.strip(),
        "network_status": network_status
    }


# ============================================================================
# REMEDIATION TOOLS
# ============================================================================

def restart_network_service(service_name: str, server_address: str) -> Dict[str, Any]:
    """
    Restart a network service on a server.
    
    Args:
        service_name: Name of the service to restart (e.g., 'nginx', 'apache', 'ssh')
        server_address: IP address or hostname of the server
        
    Returns:
        Dictionary with tool_call_status, output, and network_status fields
    """
    # Simulate service restart
    restart_successful = random.choice([True, True, True, False])  # 75% success rate
    
    if restart_successful:
        output = f"""
        Service Restart Results:
        ========================
        Server: {server_address}
        Service: {service_name}
        
        Action: Restarting {service_name} service...
        Status: SUCCESS
        
        Service Status:
        Before: STOPPED / FAILED
        After: RUNNING
        
        Verification:
        Service PID: {random.randint(1000, 9999)}
        Uptime: 0 seconds (just restarted)
        Port Status: LISTENING
        
        Health Check:
        Service responding: YES
        Response time: {random.randint(5, 20)} ms
        
        Result: Service successfully restarted and operational
        """
        network_status = "remediated"
    else:
        output = f"""
        Service Restart Results:
        ========================
        Server: {server_address}
        Service: {service_name}
        
        Action: Restarting {service_name} service...
        Status: FAILED
        
        Error Details:
        Service restart command failed
        Error: Permission denied or service not found
        Service Status: STILL FAILED
        
        Recommendation: Manual intervention required
        Check service configuration and permissions
        """
        network_status = "remediation_failed"
    
    return {
        "tool_call_status": "success",
        "output": output.strip(),
        "network_status": network_status
    }


def adjust_firewall_rules(rule_action: str, source_ip: str, destination_ip: str, port: int) -> Dict[str, Any]:
    """
    Adjust firewall rules to allow or block specific traffic.
    
    Args:
        rule_action: Action to take ('allow' or 'block')
        source_ip: Source IP address or CIDR block
        destination_ip: Destination IP address
        port: Port number to apply rule to
        
    Returns:
        Dictionary with tool_call_status, output, and network_status fields
    """
    # Simulate firewall rule adjustment
    rule_applied = random.choice([True, True, True, False])  # 75% success rate
    
    if rule_applied:
        output = f"""
        Firewall Rule Adjustment Results:
        =================================
        Action: {rule_action.upper()}
        Source: {source_ip}
        Destination: {destination_ip}
        Port: {port}
        Protocol: TCP
        
        Status: SUCCESS
        
        Rule Applied:
        Rule ID: FW-{random.randint(1000, 9999)}
        Previous Status: {'BLOCKED' if rule_action == 'allow' else 'ALLOWED'}
        New Status: {'ALLOWED' if rule_action == 'allow' else 'BLOCKED'}
        
        Verification:
        Rule Active: YES
        Traffic Flow: {'PERMITTED' if rule_action == 'allow' else 'BLOCKED'}
        Test Connection: {'SUCCESS' if rule_action == 'allow' else 'BLOCKED (Expected)'}
        
        Result: Firewall rule successfully {'added' if rule_action == 'allow' else 'removed'}
        """
        network_status = "remediated"
    else:
        output = f"""
        Firewall Rule Adjustment Results:
        =================================
        Action: {rule_action.upper()}
        Source: {source_ip}
        Destination: {destination_ip}
        Port: {port}
        
        Status: FAILED
        
        Error Details:
        Firewall configuration update failed
        Error: Invalid rule syntax or firewall service unavailable
        Rule Status: UNCHANGED
        
        Recommendation: Check firewall configuration and service status
        """
        network_status = "remediation_failed"
    
    return {
        "tool_call_status": "success",
        "output": output.strip(),
        "network_status": network_status
    }


def fix_connectivity_issue(server_address: str, issue_type: str = "general") -> Dict[str, Any]:
    """
    Attempt to fix connectivity issues with a server.
    
    Args:
        server_address: IP address or hostname of the server
        issue_type: Type of connectivity issue ('general', 'dns', 'routing', 'interface')
        
    Returns:
        Dictionary with tool_call_status, output, and network_status fields
    """
    # Simulate connectivity fix attempt
    fix_successful = random.choice([True, True, False])  # 66% success rate
    
    remediation_steps = {
        "general": ["Flushing ARP cache", "Restarting network interface", "Checking routing table"],
        "dns": ["Flushing DNS cache", "Restarting DNS service", "Verifying DNS configuration"],
        "routing": ["Checking routing table", "Restarting routing daemon", "Verifying BGP/OSPF neighbors"],
        "interface": ["Bringing interface down/up", "Checking interface configuration", "Verifying physical connection"]
    }
    
    steps = remediation_steps.get(issue_type, remediation_steps["general"])
    
    output = f"""
    Connectivity Issue Remediation Results:
    ========================================
    Server: {server_address}
    Issue Type: {issue_type.upper()}
    
    Remediation Steps Executed:
    """
    
    for i, step in enumerate(steps, 1):
        output += f"""
    Step {i}: {step}
        Status: COMPLETED"""
    
    if fix_successful:
        output += f"""
    
    Final Status: SUCCESS
    
    Verification:
    Connectivity Test: PASSED
    Ping Test: SUCCESS (5/5 packets)
    Response Time: {random.randint(8, 25)} ms
    
    Result: Connectivity issue resolved
    Server {server_address} is now reachable
    """
        network_status = "remediated"
    else:
        output += f"""
    
    Final Status: PARTIAL SUCCESS
    
    Verification:
    Connectivity Test: FAILED
    Ping Test: FAILED (0/5 packets)
    
    Result: Automatic remediation unsuccessful
    Issue persists - manual intervention may be required
    Check physical connections and server status
    """
        network_status = "remediation_partial"
    
    return {
        "tool_call_status": "success",
        "output": output.strip(),
        "network_status": network_status
    }


def optimize_network_latency(server_address: str, optimization_method: str = "routing") -> Dict[str, Any]:
    """
    Attempt to optimize network latency to a server.
    
    Args:
        server_address: IP address or hostname of the server
        optimization_method: Method to use ('routing', 'qos', 'cache')
        
    Returns:
        Dictionary with tool_call_status, output, and network_status fields
    """
    # Simulate latency optimization
    optimization_successful = random.choice([True, True, False])  # 66% success rate
    
    methods = {
        "routing": ["Analyzing routing paths", "Updating routing table", "Optimizing BGP paths"],
        "qos": ["Configuring Quality of Service", "Prioritizing traffic", "Adjusting bandwidth allocation"],
        "cache": ["Enabling content caching", "Configuring cache headers", "Optimizing cache TTL"]
    }
    
    steps = methods.get(optimization_method, methods["routing"])
    
    initial_latency = random.randint(100, 200)
    optimized_latency = initial_latency - random.randint(20, 60) if optimization_successful else initial_latency
    
    output = f"""
    Network Latency Optimization Results:
    =====================================
    Server: {server_address}
    Optimization Method: {optimization_method.upper()}
    
    Initial Latency: {initial_latency} ms
    
    Optimization Steps:
    """
    
    for i, step in enumerate(steps, 1):
        output += f"""
    Step {i}: {step}
        Status: COMPLETED"""
    
    if optimization_successful:
        output += f"""
    
    Final Status: SUCCESS
    
    Latency Improvement:
    Before: {initial_latency} ms
    After: {optimized_latency} ms
    Improvement: {initial_latency - optimized_latency} ms ({round((initial_latency - optimized_latency) / initial_latency * 100, 1)}%)
    
    Verification:
    Current Latency: {optimized_latency} ms
    Status: WITHIN ACCEPTABLE LIMITS
    
    Result: Latency successfully optimized
    """
        network_status = "remediated"
    else:
        output += f"""
    
    Final Status: NO SIGNIFICANT IMPROVEMENT
    
    Latency Results:
    Before: {initial_latency} ms
    After: {initial_latency} ms
    Improvement: 0 ms
    
    Analysis:
    Current optimization methods did not yield improvement
    May require physical infrastructure changes or different approach
    
    Result: Latency optimization attempted but no significant improvement
    """
        network_status = "remediation_partial"
    
    return {
        "tool_call_status": "success",
        "output": output.strip(),
        "network_status": network_status
    }


def block_security_threat(source_ip: str, threat_type: str = "suspicious_activity") -> Dict[str, Any]:
    """
    Block a security threat by updating firewall rules.
    
    Args:
        source_ip: IP address of the threat source
        threat_type: Type of threat ('suspicious_activity', 'ddos', 'malware', 'unauthorized_access')
        
    Returns:
        Dictionary with tool_call_status, output, and network_status fields
    """
    # Simulate threat blocking
    block_successful = random.choice([True, True, True, False])  # 75% success rate
    
    if block_successful:
        output = f"""
        Security Threat Blocking Results:
        =================================
        Threat Source: {source_ip}
        Threat Type: {threat_type.replace('_', ' ').upper()}
        
        Action: Blocking threat source...
        Status: SUCCESS
        
        Firewall Rule Applied:
        Rule ID: SEC-{random.randint(1000, 9999)}
        Action: BLOCK
        Source IP: {source_ip}
        Destination: ALL
        Port: ALL
        Protocol: ALL
        
        Verification:
        Rule Active: YES
        Threat Blocked: YES
        Test Connection from {source_ip}: BLOCKED (Expected)
        
        Security Status:
        Threat Status: MITIGATED
        Network Status: SECURED
        
        Result: Security threat successfully blocked
        """
        network_status = "remediated"
    else:
        output = f"""
        Security Threat Blocking Results:
        =================================
        Threat Source: {source_ip}
        Threat Type: {threat_type.replace('_', ' ').upper()}
        
        Action: Blocking threat source...
        Status: FAILED
        
        Error Details:
        Firewall rule update failed
        Error: Firewall service unavailable or rule limit exceeded
        Threat Status: STILL ACTIVE
        
        Recommendation: Manual intervention required
        Check firewall service status and rule capacity
        """
        network_status = "remediation_failed"
    
    return {
        "tool_call_status": "success",
        "output": output.strip(),
        "network_status": network_status
    }

