#!/usr/bin/env python3
"""
Simple ADK API Client - Demonstrates basic synchronous interaction.
Run with: uv run python simple_client.py
"""

import requests
import json


class ADKClient:
    """A simple client for interacting with ADK agents via REST API."""
    
    def __init__(self, base_url="http://localhost:8000", app_name="basic_agent"):
        self.base_url = base_url
        self.app_name = app_name
        
    def list_agents(self):
        """List all available agents."""
        response = requests.get(f"{self.base_url}/list-apps")
        return response.json()
    
    def create_session(self, user_id, session_id=None):
        """Create a new session."""
        payload = {
            "app_name": self.app_name,
            "user_id": user_id
        }
        if session_id:
            payload["session_id"] = session_id
            
        response = requests.post(
            f"{self.base_url}/create_session",
            json=payload
        )
        return response.json()
    
    def send_message(self, user_id, session_id, message_text):
        """Send a message and get the complete response."""
        payload = {
            "app_name": self.app_name,
            "user_id": user_id,
            "session_id": session_id,
            "new_message": {
                "role": "user",
                "parts": [{"text": message_text}]
            }
        }
        
        response = requests.post(
            f"{self.base_url}/run",
            json=payload
        )
        return response.json()
    
    def get_session_history(self, session_id):
        """Get the full session history."""
        response = requests.get(f"{self.base_url}/get_session/{session_id}")
        return response.json()
    
    def extract_agent_response(self, response_json):
        """Extract the agent's text response from the API response."""
        agent_responses = []
        
        for event in response_json.get("events", []):
            # Skip user events
            if event.get("author") == "user":
                continue
                
            content = event.get("content", {})
            parts = content.get("parts", [])
            
            for part in parts:
                if "text" in part:
                    agent_responses.append(part["text"])
        
        return "\n".join(agent_responses)


def main():
    """Example usage of the ADK client."""
    
    # Initialize client
    client = ADKClient()
    
    print("=" * 60)
    print("Simple ADK Client Demo")
    print("=" * 60)
    
    # 1. List available agents
    print("\n1. Available agents:")
    agents = client.list_agents()
    for app in agents.get("apps", []):
        print(f"   • {app.get('name')}: {app.get('description', 'No description')}")
    
    # 2. Create a session
    print("\n2. Creating session...")
    session = client.create_session(user_id="demo_user")
    session_id = session["session_id"]
    print(f"   Session ID: {session_id}")
    
    # 3. Send a series of messages
    print("\n3. Conversation:")
    
    messages = [
        "Hello! What can you help me with?",
        "What's 25 * 4?",
        "Thank you!"
    ]
    
    for msg in messages:
        print(f"\n   You: {msg}")
        
        response = client.send_message(
            user_id="demo_user",
            session_id=session_id,
            message_text=msg
        )
        
        agent_text = client.extract_agent_response(response)
        print(f"   Agent: {agent_text}")
    
    # 4. Retrieve full conversation history
    print("\n4. Full conversation history:")
    history = client.get_session_history(session_id)
    
    for i, event in enumerate(history.get("events", []), 1):
        author = event.get("author", "unknown")
        content = event.get("content", {})
        parts = content.get("parts", [])
        
        for part in parts:
            if "text" in part:
                text = part["text"][:60]  # Truncate for display
                print(f"   [{i}] {author}: {text}...")
    
    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to API server")
        print("   Make sure the server is running:")
        print("   adk api_server .")
    except Exception as e:
        print(f"\n❌ Error: {e}")


