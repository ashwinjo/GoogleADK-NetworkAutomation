#!/usr/bin/env python3
"""Quick test script to verify API connectivity and basic functionality."""

import requests
import sys

BASE_URL = "http://localhost:8000"


def test_api():
    """Run a series of tests to verify the ADK API is working correctly."""
    print("Testing ADK API...\n")
    
    # 1. Health check
    print("1. Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"   ✓ Status: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        print("\n❌ Server is not running. Start it with:")
        print("   adk api_server .")
        sys.exit(1)
    
    # 2. List apps
    print("\n2. List Available Agents...")
    try:
        response = requests.get(f"{BASE_URL}/list-apps")
        apps = response.json()
        print(f"   ✓ Found {len(apps.get('apps', []))} agent(s):")
        for app in apps.get('apps', []):
            print(f"      - {app.get('name', 'unknown')}")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        sys.exit(1)
    
    # 3. Create session
    print("\n3. Create Session...")
    try:
        session_resp = requests.post(
            f"{BASE_URL}/create_session",
            json={"app_name": "basic_agent", "user_id": "test_user"}
        )
        session_data = session_resp.json()
        session_id = session_data["session_id"]
        print(f"   ✓ Session ID: {session_id}")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        sys.exit(1)
    
    # 4. Send test message (synchronous)
    print("\n4. Send Test Message (synchronous)...")
    try:
        msg_resp = requests.post(
            f"{BASE_URL}/run",
            json={
                "app_name": "basic_agent",
                "user_id": "test_user",
                "session_id": session_id,
                "new_message": {
                    "role": "user",
                    "parts": [{"text": "Hello! Can you introduce yourself briefly?"}]
                }
            },
            timeout=30
        )
        result = msg_resp.json()
        events = result.get("events", [])
        print(f"   ✓ Received {len(events)} events")
        
        # Extract and display the agent's response
        for event in events:
            if event.get("author") != "user":
                content = event.get("content", {})
                parts = content.get("parts", [])
                for part in parts:
                    if "text" in part:
                        response_text = part["text"][:100]  # First 100 chars
                        print(f"   Agent response: {response_text}...")
                        break
                break
        
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        sys.exit(1)
    
    # 5. Test streaming
    print("\n5. Test Streaming (SSE)...")
    try:
        stream_resp = requests.post(
            f"{BASE_URL}/run_sse",
            json={
                "app_name": "basic_agent",
                "user_id": "test_user",
                "session_id": session_id,
                "new_message": {
                    "role": "user",
                    "parts": [{"text": "Count to 3"}]
                }
            },
            stream=True,
            headers={"Accept": "text/event-stream"},
            timeout=30
        )
        
        chunk_count = 0
        for line in stream_resp.iter_lines():
            if line and line.decode('utf-8').startswith('data: '):
                chunk_count += 1
                if chunk_count > 10:  # Stop after a few chunks
                    break
        
        print(f"   ✓ Received {chunk_count} streaming chunks")
        
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        # Don't exit, streaming may not be critical
    
    # 6. Get session history
    print("\n6. Retrieve Session History...")
    try:
        history_resp = requests.get(f"{BASE_URL}/get_session/{session_id}")
        history = history_resp.json()
        event_count = len(history.get("events", []))
        print(f"   ✓ Session contains {event_count} events")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        # Don't exit
    
    print("\n" + "=" * 60)
    print("✅ All critical tests passed!")
    print("=" * 60)
    print("\nNext steps:")
    print("  • Run the interactive chat: uv run python chat_interface.py")
    print("  • View API docs: http://localhost:8000/docs")
    print("  • Read the guide: cat API_INTEGRATION_GUIDE.md")


if __name__ == "__main__":
    test_api()


