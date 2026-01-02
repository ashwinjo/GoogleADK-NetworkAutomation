def get_bgp_summary(router_name: str) -> dict:
    """
    Generate a dummy BGP summary suitable for troubleshooting workflows.

    Args:
        router_name: The name of the router to get the BGP summary for.

    Returns:
        A dictionary containing BGP session health and statistics.
    """
    # You can add a real aggregated BGP summary function here, but for now we're using a dummy function
    return {
        "status": "success",
        "router": router_name,
        "router_reachable": True,
        "local_as": 65001,
        "bgp_version": 4,
        "last_checked": "2025-12-30T19:10:00Z",
        "neighbors": [
            {
                "neighbor_ip": "192.168.1.2",
                "neighbor_as": 65002,
                "state": "Established",
                "uptime": "5d03h",
                "session_flaps": 0,
                "prefixes_received": 34,
                "prefixes_expected": 34
            },
            {
                "neighbor_ip": "192.168.1.3",
                "neighbor_as": 65003,
                "state": "Idle",
                "uptime": "00:00:05",
                "session_flaps": 7,
                "prefixes_received": 0,
                "prefixes_expected": 40
            }
        ]
    }


def get_interface_status(router_name: str, interface_name: str) -> dict:
    """
    Generate a dummy interface status for troubleshooting.

    Args:
        router_name: Router name
        interface_name: Interface connected to the BGP neighbor

    Returns:
        Interface operational status and counters
    """
    if interface_name == "GigabitEthernet0/1":
        # Problematic interface (maps to Idle BGP neighbor)
        return {
            "status": "success",
            "router": router_name,
            "interface": interface_name,
            "admin_status": "up",
            "oper_status": "down",
            "input_errors": 124,
            "output_errors": 7,
            "last_flap": "00:02:10",
            "description": "Uplink to ISP-B"
        }

    # Healthy interface
    return {
        "status": "success",
        "router": router_name,
        "interface": interface_name,
        "admin_status": "up",
        "oper_status": "up",
        "input_errors": 0,
        "output_errors": 0,
        "last_flap": "5d03h",
        "description": "Uplink to ISP-A"
    }

def get_bgp_routes(router_name: str, neighbor_ip: str) -> dict:
    """
    Generate dummy BGP route information for a neighbor.

    Args:
        router_name: Router name
        neighbor_ip: BGP neighbor IP

    Returns:
        Routes received from the neighbor
    """
    if neighbor_ip == "192.168.1.3":
        # Idle neighbor → no routes
        return {
            "status": "success",
            "router": router_name,
            "neighbor": neighbor_ip,
            "routes_received": 0,
            "routes": [],
            "note": "No routes received due to non-established BGP session"
        }

    # Healthy neighbor
    return {
        "status": "success",
        "router": router_name,
        "neighbor": neighbor_ip,
        "routes_received": 34,
        "routes": [
            {
                "prefix": "10.10.0.0/16",
                "next_hop": neighbor_ip,
                "as_path": "65002 65100",
                "local_pref": 100,
                "med": 0
            },
            {
                "prefix": "172.16.0.0/12",
                "next_hop": neighbor_ip,
                "as_path": "65002 65200",
                "local_pref": 100,
                "med": 0
            }
        ]
    }
