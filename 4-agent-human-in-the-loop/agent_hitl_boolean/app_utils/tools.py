def read_router_config(router_name: str) -> dict:
    """"    
    Read the configuration of a router.
    Safe operation: does NOT require HITL.
    """""
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
        "message": f"Configuration successfully read for router {router_name}."
    }


def write_router_config(router_name: str) -> dict:
    """
    Write configuration to a router.
    Risky operation: protected by Human-in-the-Loop.
    
    """
    router_config = f"""
    !
    hostname {router_name}
    end
    """
    return {
        "status": "success",
        "router_name": router_name,
        "config": router_config,
        "message": f"Configuration {router_config} pushed to {router_name}."
    }  