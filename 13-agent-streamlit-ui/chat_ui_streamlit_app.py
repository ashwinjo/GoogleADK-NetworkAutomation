import json
import uuid
import requests
import streamlit as st
from sseclient import SSEClient

# -----------------------------
# App Configuration
# -----------------------------
st.set_page_config(
    page_title="ADK Agent Console",
    layout="wide",
)

st.title("🧠 ADK Agent Control Console")
st.caption("A professional Streamlit UI for interacting with ADK servers")

# -----------------------------
# Sidebar – Configuration
# -----------------------------
with st.sidebar:
    st.header("🔧 Configuration")

    base_url = st.text_input(
        "1. ADK Server Endpoint",
        value="",
        placeholder="http://localhost:9000",
        help="Base URL where ADK server is running",
        key="base_url"
    )

    user_id = st.text_input(
        "2. User ID",
        value="",
        placeholder="PeterParker_001",
        help="Enter your user ID",
        key="user_id"
    )

    session_id = st.text_input(
        "3. Session ID (optional)",
        value="",
        help="Leave blank to auto-create a session ID",
        key="session_id"
    )

    st.markdown("---")
    st.markdown(
        """
        **📝 Notes:**
        - Session ID will be auto-generated if left blank
        - Session state persists on the ADK server
        - Create a session first before running agents
        """
    )

# -----------------------------
# Helper Functions
# -----------------------------
def pretty_json(data):
    """Display JSON data in a nicely formatted way."""
    st.json(data, expanded=True)

def generate_session_id():
    """Generate a unique session ID."""
    return f"s_{uuid.uuid4().hex[:8]}"

def validate_config():
    """Validate that required configuration is provided."""
    base_url = st.session_state.get("base_url", "").strip()
    user_id = st.session_state.get("user_id", "").strip()
    
    if not base_url:
        return False, "⚠️ Please enter ADK Server Endpoint in the sidebar"
    if not user_id:
        return False, "⚠️ Please enter User ID in the sidebar"
    
    return True, None

def safe_api_call(func, *args, **kwargs):
    """Wrapper for API calls with comprehensive error handling."""
    try:
        response = func(*args, **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("❌ **Connection Error:** Could not connect to the ADK server. Make sure it's running.")
        return None
    except requests.exceptions.Timeout:
        st.error("❌ **Timeout Error:** The request took too long to complete.")
        return None
    except requests.exceptions.HTTPError as e:
        try:
            error_detail = e.response.json()
            st.error(f"❌ **HTTP Error {e.response.status_code}:** {json.dumps(error_detail, indent=2)}")
        except:
            st.error(f"❌ **HTTP Error:** {str(e)}")
        return None
    except json.JSONDecodeError:
        st.error("❌ **Invalid JSON Response:** The server returned invalid JSON.")
        return None
    except Exception as e:
        st.error(f"❌ **Unexpected Error:** {str(e)}")
        return None

# -----------------------------
# Main Content Area
# -----------------------------

# 1. List Apps
st.header("1️⃣ List Available Apps")
st.markdown("Discover all available apps on the ADK server.")

col1, col2 = st.columns([3, 1])
with col1:
    app_name = st.text_input(
        "Selected App Name",
        value="basic_agent",
        help="Enter the app name you want to use",
        key="app_name"
    )

with col2:
    if st.button("📋 List Apps", use_container_width=True):
        is_valid, error_msg = validate_config()
        if not is_valid:
            st.error(error_msg)
        else:
            with st.spinner("Fetching apps..."):
                base_url_val = st.session_state.get("base_url", "").strip()
                result = safe_api_call(requests.get, f"{base_url_val}/list-apps")
                if result:
                    st.success("✅ Apps retrieved successfully")
                    st.subheader("Response:")
                    pretty_json(result)

st.divider()

# 2. Create Session
st.header("2️⃣ Create Session")
st.markdown("Create a new session with optional initial state.")

create_col1, create_col2 = st.columns([2, 1])
with create_col1:
    create_session_id = st.text_input(
        "Session ID",
        value=st.session_state.get("last_created_session_id", st.session_state.get("session_id", "")),
        help="Leave blank to auto-generate",
        key="create_session_id"
    )

with create_col2:
    if st.button("🔄 Generate New ID", use_container_width=True):
        st.session_state.create_session_id = generate_session_id()
        st.rerun()

create_initial_state = st.text_area(
    "Initial State (JSON)",
    value='{\n  "visit_count": 1\n}',
    height=120,
    help="Optional JSON object for initial session state",
    key="create_initial_state"
)

if st.button("✨ Create Session", type="primary", use_container_width=True):
    is_valid, error_msg = validate_config()
    if not is_valid:
        st.error(error_msg)
    else:
        if not create_session_id.strip():
            create_session_id = generate_session_id()
            st.session_state.create_session_id = create_session_id
        
        try:
            payload = json.loads(create_initial_state) if create_initial_state.strip() else {}
        except json.JSONDecodeError as e:
            st.error(f"❌ **Invalid JSON in Initial State:** {str(e)}")
        else:
            with st.spinner(f"Creating session {create_session_id}..."):
                base_url_val = st.session_state.get("base_url", "").strip()
                user_id_val = st.session_state.get("user_id", "").strip()
                app_name_val = st.session_state.get("app_name", "basic_agent").strip()
                url = f"{base_url_val}/apps/{app_name_val}/users/{user_id_val}/sessions/{create_session_id}"
                result = safe_api_call(requests.post, url, json=payload)
                if result:
                    st.success(f"✅ Session Created: `{create_session_id}`")
                    st.subheader("Response:")
                    pretty_json(result)
                    # Store last created session ID (not bound to widget)
                    st.session_state.last_created_session_id = create_session_id
                    st.info(f"💡 **Tip:** Session ID `{create_session_id}` has been created. You can use it in other operations below.")

st.divider()

# 3. Get Session State
st.header("3️⃣ Get Session State")
st.markdown("Retrieve the current state of an existing session.")

get_session_id = st.text_input(
    "Session ID to Retrieve",
    value=st.session_state.get("last_created_session_id", st.session_state.get("session_id", "")),
    help="Enter the session ID to retrieve",
    key="get_session_id"
)

if st.button("🔍 Get Session", use_container_width=True):
    is_valid, error_msg = validate_config()
    if not is_valid:
        st.error(error_msg)
    elif not get_session_id.strip():
        st.warning("⚠️ Please specify a Session ID to retrieve")
    else:
        with st.spinner(f"Retrieving session {get_session_id}..."):
            base_url_val = st.session_state.get("base_url", "").strip()
            user_id_val = st.session_state.get("user_id", "").strip()
            app_name_val = st.session_state.get("app_name", "basic_agent").strip()
            url = f"{base_url_val}/apps/{app_name_val}/users/{user_id_val}/sessions/{get_session_id}"
            result = safe_api_call(requests.get, url)
            if result:
                st.success("✅ Session retrieved successfully")
                st.subheader("Response:")
                pretty_json(result)

st.divider()

# 4. Update Session State
st.header("4️⃣ Update Session State")
st.markdown("Update the state of an existing session using a state delta.")

update_session_id = st.text_input(
    "Session ID to Update",
    value=st.session_state.get("last_created_session_id", st.session_state.get("session_id", "")),
    help="Enter the session ID to update",
    key="update_session_id"
)

update_state_delta = st.text_area(
    "State Delta (JSON)",
    value='{\n  "key1": "value1",\n  "key2": 42\n}',
    height=120,
    help="JSON object with the state changes to apply",
    key="update_state_delta"
)

if st.button("🔄 Update State", use_container_width=True):
    is_valid, error_msg = validate_config()
    if not is_valid:
        st.error(error_msg)
    elif not update_session_id.strip():
        st.warning("⚠️ Please specify a Session ID to update")
    else:
        try:
            payload = {"stateDelta": json.loads(update_state_delta)}
        except json.JSONDecodeError as e:
            st.error(f"❌ **Invalid JSON in State Delta:** {str(e)}")
        else:
            with st.spinner(f"Updating session {update_session_id}..."):
                base_url_val = st.session_state.get("base_url", "").strip()
                user_id_val = st.session_state.get("user_id", "").strip()
                app_name_val = st.session_state.get("app_name", "basic_agent").strip()
                url = f"{base_url_val}/apps/{app_name_val}/users/{user_id_val}/sessions/{update_session_id}"
                result = safe_api_call(requests.patch, url, json=payload)
                if result:
                    st.success("✅ Session state updated successfully")
                    st.subheader("Response:")
                    pretty_json(result)

st.divider()

# 5. Run Agent (Synchronous - streaming=false)
st.header("5️⃣ Run Agent (Synchronous)")
st.markdown("Run the agent synchronously with `streaming=false` using `/run` endpoint.")

sync_session_id = st.text_input(
    "Session ID",
    value=st.session_state.get("last_created_session_id", st.session_state.get("session_id", "")),
    help="Enter the session ID for this run",
    key="sync_session_id"
)

sync_user_message = st.text_area(
    "User Message",
    value="Hey what is meaning of BGP in networking?",
    height=100,
    help="Enter your message to send to the agent",
    key="sync_user_message"
)

if st.button("🚀 Run /run", type="primary", use_container_width=True):
    is_valid, error_msg = validate_config()
    if not is_valid:
        st.error(error_msg)
    elif not sync_session_id.strip():
        st.warning("⚠️ Please specify a Session ID for the sync run")
    else:
        base_url_val = st.session_state.get("base_url", "").strip()
        user_id_val = st.session_state.get("user_id", "").strip()
        app_name_val = st.session_state.get("app_name", "basic_agent").strip()
        payload = {
            "appName": app_name_val,
            "userId": user_id_val,
            "sessionId": sync_session_id,
            "newMessage": {
                "role": "user",
                "parts": [{"text": sync_user_message}],
            },
        }

        with st.spinner("Running agent synchronously..."):
            result = safe_api_call(requests.post, f"{base_url_val}/run", json=payload)
            if result:
                st.success("✅ Agent run completed")
                st.subheader("Response:")
                pretty_json(result)

st.divider()

# 6. Run Agent (Streaming - SSE, streaming=true)
st.header("6️⃣ Run Agent (Streaming - SSE)")
st.markdown("Run the agent with streaming enabled using `/run_sse` endpoint with `streaming=true`.")

stream_session_id = st.text_input(
    "Session ID",
    value=st.session_state.get("last_created_session_id", st.session_state.get("session_id", "")),
    help="Enter the session ID for this streaming run",
    key="stream_session_id"
)

stream_user_message = st.text_area(
    "User Message",
    value="Explain OSPF routing protocol in detail",
    height=100,
    help="Enter your message to send to the agent",
    key="stream_user_message"
)

if st.button("⚡ Run /run_sse", type="primary", use_container_width=True):
    is_valid, error_msg = validate_config()
    if not is_valid:
        st.error(error_msg)
    elif not stream_session_id.strip():
        st.warning("⚠️ Please specify a Session ID for the streaming run")
    else:
        base_url_val = st.session_state.get("base_url", "").strip()
        user_id_val = st.session_state.get("user_id", "").strip()
        app_name_val = st.session_state.get("app_name", "basic_agent").strip()
        payload = {
            "appName": app_name_val,
            "userId": user_id_val,
            "sessionId": stream_session_id,
            "streaming": True,
            "newMessage": {
                "role": "user",
                "parts": [{"text": stream_user_message}],
            },
        }

        st.info("⚡ **Streaming response...**")
        
        # Container for streaming events
        stream_container = st.container()

        try:
            response = requests.post(
                f"{base_url_val}/run_sse",
                json=payload,
                stream=True,
                headers={"Accept": "text/event-stream"},
                timeout=300  # 5 minute timeout for streaming
            )
            response.raise_for_status()

            client = SSEClient(response)
            events = []
            complete_data = None

            with stream_container:
                for event in client.events():
                    if event.event == "message":
                        try:
                            data = json.loads(event.data)
                            events.append(data)
                            st.json(data)
                        except json.JSONDecodeError:
                            st.warning(f"⚠️ Could not parse event data: {event.data}")
                    elif event.event == "complete":
                        st.success("✅ **Streaming complete**")
                        try:
                            complete_data = json.loads(event.data)
                            st.subheader("Final Response:")
                            st.json(complete_data)
                        except json.JSONDecodeError:
                            complete_data = {"status": "complete", "raw_data": event.data}
                            st.subheader("Final Response:")
                            st.json(complete_data)
                        break
                    elif event.event == "error":
                        st.error(f"❌ **Streaming error:** {event.data}")
                        break

        except requests.exceptions.ConnectionError:
            st.error("❌ **Connection Error:** Could not connect to the ADK server for streaming.")
        except requests.exceptions.Timeout:
            st.error("❌ **Timeout Error:** The streaming request took too long.")
        except requests.exceptions.HTTPError as e:
            try:
                error_detail = e.response.json()
                st.error(f"❌ **HTTP Error {e.response.status_code}:** {json.dumps(error_detail, indent=2)}")
            except:
                st.error(f"❌ **HTTP Error:** {str(e)}")
        except Exception as e:
            st.error(f"❌ **Unexpected Error during streaming:** {str(e)}")
