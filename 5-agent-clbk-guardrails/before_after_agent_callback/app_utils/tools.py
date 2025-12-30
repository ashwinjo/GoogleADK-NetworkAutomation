def read_router_config(router_name: str) -> str:
    """Read the configuration of a router.

    Args:
        router_name: The name of the router to read the configuration for.

    Returns:
        A string with the configuration of the router.
    """
    router_config = f"""
                        !
                        hostname {router_name}
                        interface GigabitEthernet0/0
                        ip address 192.168.1.1 255.255.255.0
                        no shutdown
                        !
                        router ospf 1
                        network 192.168.1.0 0.0.0.255 area 0
                        !
                        line vty 0 4
                        login local
                        transport input ssh
                        !
                        end
                        """
    return {
        "status": "success",
        "router_name": router_name,
        "config": router_config,
        "message": f"The configuration of the router {router_name} is: {router_config}"
    }

def write_router_config(router_name: str) -> str:
    
    """
    Generate a small sample configuration that can be sent to a Cisco router.

    Args:
        router_name: The router's hostname to set.
        config: The simple configuration body as a single string or snippet.

    Returns:
        Confirmation message with the configuration to be applied.
    """
    # This is a simple illustrative implementation and does not persist configs.
    # Make a small config script using the given values for a Cisco router.
    router_config = f"""!
                        hostname {router_name}
                        end
                        """
    return {
        "status": "success",
        "router_name": router_name,
        "config": router_config,
        "message": f"Apply the following configuration to {router_name}."
    }