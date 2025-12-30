def get_bgp_summary(router_name: str) -> dict:
    """Generate a dummy BGP summary.
    
    Args:
        router_name: The name of the router to get the BGP summary for.

    Returns:
        A dictionary containing the BGP summary for the given router.
    """
    return {
        "status": "success",
        "router": router_name,
        "neighbors": [
            {
                "neighbor_ip": "192.168.1.2",
                "state": "Established",
                "uptime": "5d03h",
                "prefixes_received": 34,
            },
            {
                "neighbor_ip": "192.168.1.3",
                "state": "Idle",
                "uptime": "00:00:05",
                "prefixes_received": 0,
            }
        ],
        "local_as": 65001,
        "bgp_version": 4
    }
