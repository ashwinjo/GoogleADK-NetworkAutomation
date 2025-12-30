import subprocess
from typing import Literal

CommandType = Literal["read", "write"]

def run_frr_command(
    router: str,
    command: str,
    command_type: CommandType = "read",
    timeout: int = 10
) -> str:
    """
    Execute an FRR vtysh command inside a containerlab router.

    Args:
        router (str): Container name (e.g. clab-two-router-bgp-r1)
        command (str): vtysh command (e.g. 'show bgp summary')
        command_type (str): 'read' or 'write'
        timeout (int): seconds

    Returns:
        str: command output

    Raises:
        RuntimeError: on execution failure
    """

    # --- Guardrail (MCP-style) ---
    if command_type == "read":
        if not command.strip().startswith(("show", "exit")):
            raise ValueError(f"Blocked non-read command: {command}")

    # --- Build docker exec command ---
    docker_cmd = [
        "docker",
        "exec",
        router,
        "vtysh",
        "-c",
        command
    ]

    try:
        result = subprocess.run(
            docker_cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=True
        )
        return result.stdout.strip()

    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Command failed on {router}: {e.stderr.strip()}"
        ) from e

    except subprocess.TimeoutExpired:
        raise RuntimeError(f"Command timed out on {router}")
