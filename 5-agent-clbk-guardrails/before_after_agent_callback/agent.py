"""
Author: Ashwin Joshi

Title:

Purpose:

ADK Feature Uses:

Useful links:
  - Agent Development Kit (ADK) Documentation: 
  
"""

"""
Before Agent Callback:
- The Before and After Agent Callback is a feature that allows you to run code before and after an agent is executed.
- This is useful for adding additional functionality to an agent without having to modify the agent itself.

After Agent Callback:
- The After Agent Callback is a feature that allows you to run code after an agent is executed.
- This is useful for adding additional functionality to an agent without having to modify the agent itself.

Guardrails: (Using Before and After Agent Callback)
- The Guardrails is a feature that allows you to add additional functionality to an agent without having to modify the agent itself.
- This is useful for adding additional functionality to an agent without having to modify the agent itself.
- Guardrails are used to add additional functionality to an agent without having to modify the agent itself.
- Guardrails are used to add additional functionality to an agent without having to modify the agent itself.


Example Use Cases:
- Context Manipulation / Initiation
- Agent Request/ Response Validation
- Agent Request/Response Processing
- Agent Request/Response Logging
- Agent Request/Response Notification
- Agent Request/Response Error Handling
- Agent Request/Response Success Handling
"""
# ADK Imports
import os
import logging
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.runners import InMemoryRunner # Use InMemoryRunner
from google.genai import types # For types.Content
from google.adk.models import LlmRequest, LlmResponse
from google.adk.models import Gemini
from typing import Optional 
from google.adk.apps.app import App
from .app_utils.tools import read_router_config

from dotenv import load_dotenv

load_dotenv()

import google.auth
_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)

# Define the model - Use the specific model name requested
GEMINI_2_FLASH="gemini-2.0-flash"


import re

def extract_router_name(text: str) -> Optional[str]:
    """
    Extracts the router name from a string using a regular expression.

    Args:
        text: The input string containing the router name.

    Returns:
        The router name as a string, or None if no match is found.
    """
    pattern = r"(r\d+-[a-zA-Z]+\d+)"
    match = re.search(pattern, text)

    if match:
        router_name = match.group(1)
        return router_name
    
def check_router_status(router_name: str) -> bool:
    """
    Checks if the router is up and running.
    """
    print(f"[Callback] Checking router status: {router_name}")
    import random
    status = ['up', 'down']
    return random.choice(status)

    
# --- 1. Define the Callback Function ---
def check_if_router_is_up_and_agent_should_run(callback_context: CallbackContext) -> Optional[types.Content]:
    """This function will check if the router is up and if the agent should run.
    """

    current_state = callback_context.state.to_dict()

    print(f"[Callback] before_agent_callback_Last Current State: {current_state}")
    
    session = callback_context._invocation_context.session
    
    # Use Case 1: PreValidation 
    # Get the last user message which is the lst event
 
    if session.events:
        for event in reversed(session.events):
            if event.content:
                # Extract text from content
                print(f"[Callback] event.content: {event.content}")
                if hasattr(event.content, "parts") and event.content.parts:
                    for part in event.content.parts:
                        if hasattr(part, "text") and part.text:
                            last_user_message = part.text
                            break  # break out of innermost for part in event.content.parts
                break  # break out of for event in reversed(session.events) after finding the last_user_message
                            

    print(f"[Callback] before_agent_callback_Last User Message: {last_user_message}")
    callback_context.state['before_agent_callback_latest_user_message'] = last_user_message
    # Use Case 1: PreValidation 
    router_name = extract_router_name(last_user_message)
    
    # Use Case 2:Context Manipulation / Initiation
    callback_context.state['before_agent_callback_latest_router_name'] = router_name
    print(f"[Callback] before_agent_callback_Router Name: {router_name}")

    router_status = check_router_status(router_name)
    print(f"[Callback] Router Status: {router_status}")
    callback_context.state['before_agent_callback_latest_router_status'] = router_status
    # Return a message back to the user as agent output content
    if router_status == 'up':
        return None
    else:
        return types.Content(
            parts=[types.Part(text=f"Agent execution skipped because router {router_name} is down.")],
            role="model" # Assign model role to the overriding response
        )
        
# --- 1. Define the Callback Function ---
def check_if_router_is_up_and_agent_should_process_the_repsonse(callback_context: CallbackContext) -> Optional[types.Content]:
    """This function will check if the router is up and if the agent should run.
    """
    current_state = callback_context.state.to_dict()
    
    print(f"[Callback] Current State: {current_state}")
    
    session = callback_context._invocation_context.session
    
    # Get the last user message which is the lst event
    last_message = ""
    if session.events:
        for event in reversed(session.events):
            if event.content:
                # Extract text from content
                print(f"[Callback] event.content: {event.content}")
                if hasattr(event.content, "parts") and event.content.parts:
                    for part in event.content.parts:
                        if hasattr(part, "text") and part.text:
                            last_message = part.text
                            break  # break out of innermost for part in event.content.parts
                break  # break out of for event in reversed(session.events) after finding the last_user_message
                            
                            
    print(f"[Callback] Agent Response Message: {last_message}")
    print(f"[Callback] Router Name: {callback_context.state['before_agent_callback_latest_router_name']}")
    print(f"[Callback] Router Status: {callback_context.state['before_agent_callback_latest_router_status']}")
    print(f"[Callback] state: {callback_context.state.to_dict()}")
    
    # Check if last message and if it was the validation error
    if "Agent execution skipped because" in last_message:
        callback_context.state['after_agent_callback_latest_user_message'] = "Agent Validation Error"
        return None # None here is to do nothing. In the else we will process the response
    else:
        callback_context.state['after_agent_callback_latest_user_message'] = last_message
        return types.Content(
            parts=[types.Part(text=f"It is now safe to push the response to the router {callback_context.state['before_agent_callback_latest_router_name']}.")],
            role="model" # Assign model role to the overriding response
        )
    
    
root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-3-flash-preview",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="You are a helpful Network AI assistant designed to provide accurate and useful router configurations.",
    tools=[read_router_config],
    before_agent_callback=check_if_router_is_up_and_agent_should_run,
    after_agent_callback=check_if_router_is_up_and_agent_should_process_the_repsonse,
)

app = App(root_agent=root_agent, name="before_after_agent_callback")
