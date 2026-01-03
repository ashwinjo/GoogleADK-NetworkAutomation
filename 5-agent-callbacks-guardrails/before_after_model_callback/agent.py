"""
Author: Ashwin Joshi

Title: Model Callback Guardrails for Sensitive Content Detection
"""

from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.models import Gemini
from google.genai import types
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest, LlmResponse
from typing import Optional
import random

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


def is_there_password_in_user_request(message: str) -> bool:
    """Checks if the user request contains a password in plaintext.

    Args:
        message (str): The user request message to check for a password.

    Returns:
        bool: True if the user request contains a password in plaintext, False otherwise.
    """
    # You can redirect this to any system. You can also use LLM calbacks to make a decision is something is sensitive.
    if "password" in message.lower():
        return True
    return False

def is_there_password_in_user_response(message: str) -> bool:
    """Checks if the user response contains a password in plaintext.

    Args:
        message (str): The user response message to check for a password.

    Returns:
        bool: True if the user response contains a password in plaintext, False otherwise.
    """
    if "PassWord" in message:
        return True
    return False

def check_sensitive_content_model_request(callback_context: CallbackContext,
                                          llm_request: LlmRequest) -> Optional[types.Content]:
    """ This function will check if the user request contains a password in plaintext.
    If it does, it will return a response to skip the model call.
    """
    state = callback_context.state
    
    # Extract the last user message
    last_user_message = ""
    for content in reversed(llm_request.contents):
        if content.role == "user" and content.parts and len(content.parts) > 0:
            if hasattr(content.parts[0], "text") and content.parts[0].text:
                last_user_message = content.parts[0].text
                break
    
    if is_there_password_in_user_request(last_user_message):
        # Return a response to skip the model call
        state["password_found_in_request"] = True
        
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[
                    types.Part(
                        text="""You have entered password in plaintext.
                        Please remove the password from the request. This is against AshTech Policies.
                        """
                    )
                ],
            )
        )
    else:
         # Return None to use the original response
        state["password_found_in_request"] = False
        return None

def check_sensitive_content_model_response(callback_context: CallbackContext, 
                                           llm_response: LlmResponse) -> Optional[types.Content]:
    """This function will check if the user response contains a password in plaintext.
    If it does, it will return a response to skip the model call.
    """
    state = callback_context.state
  
    # Extract text from the response
    response_text = ""
    for part in llm_response.content.parts:
        if hasattr(part, "text") and part.text:
            response_text += part.text
    
    if is_there_password_in_user_response(response_text):
        # Return a response to skip the model call
        state["password_found_in_response"] = True
        
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[
                    types.Part(
                        text="""This config violates the AshTech Policies.
                        Please ensure you set encryption on the password.
                        """
                    )
                ],
            )
        )
    else:
         # Return None to use the original response
        state["password_found_in_response"] = True
        return None


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-3-flash-preview",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="You are a helpful Network AI assistant designed to provide accurate and useful router configurations.",
    tools=[read_router_config],
    before_model_callback=check_sensitive_content_model_request,
    after_model_callback=check_sensitive_content_model_response,
)

app = App(root_agent=root_agent, name="before_after_model_callback")
