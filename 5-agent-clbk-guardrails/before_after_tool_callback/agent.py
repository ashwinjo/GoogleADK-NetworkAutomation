"""
Author: Ashwin Joshi

Title:

Purpose:

ADK Feature Uses:

Useful links:
  - Agent Development Kit (ADK) Documentation: 
  
"""

from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.models import Gemini
from google.genai import types
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import ToolContext
from typing import Optional, Dict, Any
from google.adk.tools.base_tool import BaseTool
import copy

from dotenv import load_dotenv

load_dotenv()

import os
import google.auth
import logging
from .app_utils.tools import read_router_config

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)



# --- Define Before Tool Callback ---
def before_tool_callback(tool: BaseTool,
                         args: Dict[str, Any], 
                         tool_context: ToolContext
    ) -> Optional[Dict]:
    """Simple callback that modifies tool arguments or skips the tool call.
    Main use would be argument validation to the funtion"""
    tool_name = tool.name
    print(f"[Callback] Before tool call for '{tool_name}'")
    print(f"[Callback] Original args: {args}")   
    # Skip the call completely for restricted countries
    if (
        tool_name == "read_router_config"
        and args.get("router_name", "").lower() == "r1-gov51"
    ):
        print("[Callback] Blocking restricted router")
        return {"result": "Access to this router has been restricted. as it is in gov cloud"}
    
    
    print("[Callback] Proceeding with normal tool call")
    return None

# --- Define After Tool Callback ---
def after_tool_callback(tool: BaseTool, 
                        args: Dict[str, Any], 
                        tool_context: ToolContext, 
                        tool_response: Dict) -> Optional[Dict]:
    """
    Simple callback that modifies the tool response after execution.
    """
    tool_name = tool.name
    print(f"[Callback] After tool call for '{tool_name}'")
    print(f"[Callback] Args used: {args}")
    print(f"[Callback] Original response: {tool_response}")

    import ast
    # Handle both cases: when result is a dict or when it's a string representation
    original_result = tool_response.get("result", tool_response)
    
    # If it's a string, try to parse it as a literal
    if isinstance(original_result, str):
        try:
            original_result = ast.literal_eval(original_result)
        except (ValueError, SyntaxError):
            # If parsing fails, use the original response as-is
            original_result = tool_response
    
    # Ensure original_result is a dict
    if not isinstance(original_result, dict):
        print(f"[Callback] Warning: result is not a dict, using tool_response directly")
        original_result = tool_response
    
    print(f"[Callback] Extracted result: '{original_result}'")

    # Mask PassWord in the response
    if tool_name == "read_router_config" and isinstance(original_result, dict):
        modified = False
        
        # Replace PassWord in config field
        if "config" in original_result and "PassWord" in original_result.get('config', ''):
            original_result['config'] = original_result['config'].replace("PassWord", "******")
            modified = True
        
        if modified:
            print(f"[Callback] Modified response: {original_result}")
            return original_result
        
    print("[Callback] No modifications needed, returning original response")
    return None

root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-3-flash-preview",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="You are a helpful Network AI assistant designed to provide accurate and useful router configurations.",
    tools=[read_router_config],
    before_tool_callback=before_tool_callback,
    after_tool_callback=after_tool_callback,
)

app = App(root_agent=root_agent, name="before_after_tool_callback")

