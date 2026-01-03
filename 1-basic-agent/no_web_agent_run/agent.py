

"""
Author: Ashwin Joshi

Title: Network Troubleshooting Agent (No Web Interface)
"""

import datetime

from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.models import Gemini
from google.genai import types
from dotenv import load_dotenv
import asyncio
import os
import logging


load_dotenv()


import os
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


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-3-flash-preview",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    description="Supervior Agent to perform Network Troubleshooting",
    instruction="You are a helpful Network Operations AI assistant that analyzes network state, consult topology & docs, and safely remediate network issues.",
)

# Setting up now web agent access


from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

# --- 5. Set up Session Management and Runners ---

session_service = InMemorySessionService()

# Create an async setup function
async def init_system():
    # AUS
	await session_service.create_session(app_name="NO_WEB_AGENT_CALL", 
                                         user_id="some_random_generate_user_id", 
                                         session_id="some_random_generated_session_id") # It will be auto if not given



# Create a runner for EACH agen
network_runner = Runner(
    # A2S2
    agent=root_agent,
    app_name="NO_WEB_AGENT_CALL",
    session_service=session_service
)

asyncio.run(init_system())

# Agent Interaction
def call_agent(query):
    content = types.Content(role='user', parts=[types.Part(text=query)])
    #US
    events = network_runner.run(user_id="some_random_generate_user_id", 
                                session_id="some_random_generated_session_id", 
                                new_message=content)

    for event in events:
        print(f"\nDEBUG EVENT: {event}\n")
        if event.is_final_response() and event.content:
            final_answer = event.content.parts[0].text.strip()
            print("\n🟢 FINAL ANSWER\n", final_answer, "\n")

call_agent("How can I can configure OSPF on Cisco Router")

#app = App(root_agent=root_agent, name="no_web_agent_run")
