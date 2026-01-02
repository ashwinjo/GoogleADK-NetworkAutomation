
import requests
import json


class ADKClient:
    """Simple client for ADK API interactions."""
    
    def __init__(self, base_url="http://localhost:9000"):
        self.base_url = base_url
    
    def list_agents(self):
        """List all available agents."""
        response = requests.get(f"{self.base_url}/list-apps")
        return response.json()
    
    def create_session(self, app_name, user_id, session_id, initial_state=None):
        """Create a new session."""
        url = f"{self.base_url}/apps/{app_name}/users/{user_id}/sessions/{session_id}"
        response = requests.post(url, json=initial_state or {})
        return response.json()
    
    def send_message(self, app_name, user_id, session_id, message_text):
        """Send a message and get the complete response."""
        payload = {
            "appName": app_name,
            "userId": user_id,
            "sessionId": session_id,
            "newMessage": {
                "role": "user",
                "parts": [{"text": message_text}]
            }
        }
        
        response = requests.post(f"{self.base_url}/run", json=payload)
        return response.json()
    
    def get_session(self, app_name, user_id, session_id):
        """Get session details and history."""
        url = f"{self.base_url}/apps/{app_name}/users/{user_id}/sessions/{session_id}"
        response = requests.get(url)
        return response.json()
    
    def extract_agent_response(self, response_json):
        """Extract agent text from response."""
        texts = []
        for event in response_json:
            if event.get("author") != "user":
                content = event.get("content", {})
                for part in content.get("parts", []):
                    if "text" in part:
                        texts.append(part["text"])
        return "\n".join(texts)

class ADKStreamingClient:
    """Streaming client for real-time responses."""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def send_message_streaming(self, app_name, user_id, session_id, message_text, on_chunk=None):
        """Send a message and stream the response."""
        payload = {
            "appName": app_name,
            "userId": user_id,
            "sessionId": session_id,
            "streaming": True,
            "newMessage": {
                "role": "user",
                "parts": [{"text": message_text}]
            }
        }
        
        response = requests.post(
            f"{self.base_url}/run_sse",
            json=payload,
            stream=True,
            headers={"Accept": "text/event-stream"}
        )
        
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data_str = line[6:]
                    try:
                        data = json.loads(data_str)
                        event_obj = data.get("event", {})
                        
                        if event_obj.get("author") != "user":
                            content = event_obj.get("content", {})
                            for part in content.get("parts", []):
                                if "text" in part and on_chunk:
                                    on_chunk(part["text"])
                    except json.JSONDecodeError:
                        pass


# Usage Example
if __name__ == "__main__":
    client = ADKClient()
    
    # 1. List agents
    agents = client.list_agents()
    print(f"Available agents: {agents}")
    
    # 2. Create session
    session = client.create_session(
        app_name="basic_agent",
        user_id="demo_user",
        session_id="demo_session_001"
    )
    print(f"Session created: {session['id']}")
    
    
    
    
    # 3. Send message
    response = client.send_message(
        app_name="basic_agent",
        user_id="demo_user",
        session_id="demo_session_001",
        message_text="What is BGP in networking? Ashwer in 10 words"
    )
    
    # 4. Extract response
    agent_text = client.extract_agent_response(response)
    print(f"Agent: {agent_text}")
    
    client = ADKStreamingClient()
    
    def print_chunk(text):
        print(text, end="", flush=True)
    
    print("Agent: ", end="", flush=True)
    client.send_message_streaming(
        app_name="basic_agent",
        user_id="demo_user",
        session_id="demo_session_001",
        message_text="Tell me about Python",
        on_chunk=print_chunk
    )
    print()  # New line