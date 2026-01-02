# routerSecurityMonitorAgent/app/app_utils/tools.py

import subprocess
import json
from typing import Dict, Any


def check_router_firewall_status(router_name: str) -> Dict[str, Any]:
    """
    Check if the router has proper firewall rules configured and enabled.
    
    Args:
        router_name: Name or IP address of the router to check
        
    Returns:
        Dictionary with security_status (boolean) and reasons (string)
    """
    try:
        # Simulate firewall status check (in real implementation, this would connect to router)
        # For demo purposes, we'll use a simulated check
        import random
        firewall_enabled = random.choice([True, True, False])  # 66% success rate
        
        if firewall_enabled:
            return {
                "security_status": True,
                "reasons": f"Firewall is properly configured and enabled on {router_name}. All critical ports are protected with appropriate rules."
            }
        else:
            return {
                "security_status": False,
                "reasons": f"Firewall is disabled or misconfigured on {router_name}. Router is vulnerable to unauthorized access and attacks."
            }
            
    except Exception as e:
        return {
            "security_status": False,
            "reasons": f"Unable to check firewall status for {router_name}: {str(e)}"
        }


def scan_router_open_ports(router_name: str) -> Dict[str, Any]:
    """
    Scan for potentially vulnerable open ports on the router.
    
    Args:
        router_name: Name or IP address of the router to scan
        
    Returns:
        Dictionary with security_status (boolean) and reasons (string)
    """
    try:
        # Use nmap for port scanning (requires nmap to be installed)
        result = subprocess.run(
            ["nmap", "-F", "--host-timeout", "30s", router_name],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            output_lines = result.stdout.split('\n')
            open_ports = []
            
            for line in output_lines:
                if '/tcp' in line and 'open' in line:
                    parts = line.split('/')
                    if len(parts) > 0:
                        port = parts[0].strip()
                        try:
                            port_num = int(port)
                            # Check for commonly vulnerable ports
                            if port_num in [21, 23, 80, 443, 3389, 5900]:  # FTP, Telnet, HTTP, HTTPS, RDP, VNC
                                open_ports.append(f"{port_num} ({line.split()[2]})")
                        except ValueError:
                            continue
            
            if not open_ports:
                return {
                    "security_status": True,
                    "reasons": f"No vulnerable ports detected on {router_name}. Router appears to have secure port configuration."
                }
            else:
                return {
                    "security_status": False,
                    "reasons": f"Vulnerable ports detected on {router_name}: {', '.join(open_ports)}. These ports should be secured or closed."
                }
        else:
            return {
                "security_status": False,
                "reasons": f"Port scan failed for {router_name}: {result.stderr}"
            }
            
    except subprocess.TimeoutExpired:
        return {
            "security_status": False,
            "reasons": f"Port scan timed out for {router_name}. Router may be unresponsive or blocking scans."
        }
    except FileNotFoundError:
        return {
            "security_status": False,
            "reasons": f"nmap not found. Please install nmap for port scanning capabilities on {router_name}."
        }
    except Exception as e:
        return {
            "security_status": False,
            "reasons": f"Unable to scan ports for {router_name}: {str(e)}"
        }


def check_router_firmware_security(router_name: str) -> Dict[str, Any]:
    """
    Check router firmware version and known security vulnerabilities.
    
    Args:
        router_name: Name or IP address of the router to check
        
    Returns:
        Dictionary with security_status (boolean) and reasons (string)
    """
    try:
        # In a real implementation, this would connect to the router's management interface
        # For demo purposes, we'll simulate firmware checking
        import random
        
        # Simulate different firmware states
        firmware_states = [
            {"status": True, "reason": "Firmware is up-to-date with latest security patches."},
            {"status": True, "reason": "Firmware version is current and secure."},
            {"status": False, "reason": "Firmware is outdated and contains known security vulnerabilities (CVE-2023-XXXX)."},
            {"status": False, "reason": "Firmware version is end-of-life and no longer receives security updates."}
        ]
        
        selected_state = random.choice(firmware_states)
        
        return {
            "security_status": selected_state["status"],
            "reasons": f"{router_name}: {selected_state['reason']}"
        }
        
    except Exception as e:
        return {
            "security_status": False,
            "reasons": f"Unable to check firmware security for {router_name}: {str(e)}"
        }