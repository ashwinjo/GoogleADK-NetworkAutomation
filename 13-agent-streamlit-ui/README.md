# 13-agent-streamlit-ui

We have a Streamlit UI that allows you to interact with the ADK agent. We start a local-agent using `make local-backend` and then we can interact with the agent through the Streamlit UI.

## What are we doing in this Streamlit UI?

The Streamlit UI in `chat_ui_streamlit_app.py` provides a full-featured, step-by-step web console to interact with the ADK agent backend. It lets you configure the agent server address, your user ID, and session ID in the sidebar. The UI walks you through core agent operations: listing available apps, creating a session (with optional initial state), retrieving or updating the session state, and running the agent either synchronously or with real-time streaming (SSE). Each section features rich feedback, status messages, and error handling, making this interface ideal for testing, debugging, and exploring ADK agent workflows visually.

![Streamlit UI](./images/streamlit_ui.png)


## File and Folder Structure:

`chat_ui_streamlit_app.py`: This is the main file that contains the Streamlit UI. 

`chat_ui_python_run.py`:  This file contains the Python code to talk to the agent using the API calls.

`fast_api_app.py`: This is the file that contains the FastAPI backend server.



Start the agent now with  : ```make local-backend```


Now, we can run the Streamlit UI with:

```bash
uv run streamlit run chat_ui_streamlit_app.py
```

This will open the Streamlit UI in your default browser.




**Note:** 

Since the name of the agent folder is `basic_agent` and not the default `app` that was created when we generated the agent with the Agent Starter Pack, we need to modify the make command in our Makefile to start the agent.

```bash
# Launch local development server with hot-reload
local-backend:
	uv run uvicorn basic_agent.fast_api_app:app --host localhost --port 8000 --reload
```

**Note**:  We will also need to modify 2 imports in  fast_api_app.py file to the correct one. <br/>

```python
from basic_agent.app_utils.telemetry import setup_telemetry
from basic_agent.app_utils.typing import Feedback
```







