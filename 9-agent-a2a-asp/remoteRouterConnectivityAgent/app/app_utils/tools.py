"""
Network diagnostic tools for router connectivity testing.
All functions return string results for agent consumption.
"""

import subprocess


def ping_router(router_address: str, count: int = 4) -> str:
    """
    Ping a router to check connectivity and measure latency.
    
    Args:
        router_address: IP address or hostname of the router to ping
        count: Number of ping packets to send (default: 4)
        
    Returns:
        A string containing ping test results including packet loss and latency statistics.
    """
    try:
        # Run ping command
        result = subprocess.run(
            ["ping", "-c", str(count), router_address],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            output = f"""
Ping Test Results:
==================
Target: {router_address}
Status: SUCCESS

{result.stdout}

Connectivity: REACHABLE
"""
        else:
            output = f"""
Ping Test Results:
==================
Target: {router_address}
Status: FAILED

{result.stderr if result.stderr else result.stdout}

Connectivity: UNREACHABLE
"""
    except subprocess.TimeoutExpired:
        output = f"""
Ping Test Results:
==================
Target: {router_address}
Status: TIMEOUT

The ping command timed out after 30 seconds.
Connectivity: UNREACHABLE (Timeout)
"""
    except Exception as e:
        output = f"""
Ping Test Results:
==================
Target: {router_address}
Status: ERROR

Error: {str(e)}
Connectivity: UNKNOWN
"""
    
    return output.strip()


def traceroute_router(router_address: str, max_hops: int = 30) -> str:
    """
    Run a traceroute to a router to identify the network path and measure hop-by-hop latency.
    
    Args:
        router_address: IP address or hostname of the router to traceroute
        max_hops: Maximum number of hops to trace (default: 30)
        
    Returns:
        A string containing traceroute results showing the network path and latency at each hop.
    """
    try:
        # Run traceroute command
        result = subprocess.run(
            ["traceroute", "-m", str(max_hops), router_address],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            output = f"""
Traceroute Results:
===================
Target: {router_address}
Status: SUCCESS

{result.stdout}

Path Analysis: Complete
"""
        else:
            output = f"""
Traceroute Results:
===================
Target: {router_address}
Status: FAILED

{result.stderr if result.stderr else result.stdout}

Path Analysis: Incomplete
"""
    except subprocess.TimeoutExpired:
        output = f"""
Traceroute Results:
===================
Target: {router_address}
Status: TIMEOUT

The traceroute command timed out after 60 seconds.
Path Analysis: Incomplete (Timeout)
"""
    except FileNotFoundError:
        # Fallback to tracepath if traceroute is not available
        try:
            result = subprocess.run(
                ["tracepath", router_address],
                capture_output=True,
                text=True,
                timeout=60
            )
            output = f"""
Traceroute Results (using tracepath):
=====================================
Target: {router_address}
Status: SUCCESS

{result.stdout}

Path Analysis: Complete
"""
        except Exception as e:
            output = f"""
Traceroute Results:
===================
Target: {router_address}
Status: ERROR

Error: {str(e)}
Note: Neither 'traceroute' nor 'tracepath' command is available.
Path Analysis: Failed
"""
    except Exception as e:
        output = f"""
Traceroute Results:
===================
Target: {router_address}
Status: ERROR

Error: {str(e)}
Path Analysis: Failed
"""
    
    return output.strip()

