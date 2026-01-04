# 13-agent-react-frontend

This is a React-based web UI that allows you to interact with the ADK agent API server.

 To use this frontend, first start your ADK agent backend (for example, using `make local-backend` or the appropriate command for your setup). Then, start the React app in `react-app/` to interact with your agent in the browser.


Refer to the [API Integration Guide](API_INTEGRATION_GUIDE.md) for more details on the API endpoints and how to use them.

## File and Folder Structure:

`react-app/`: This is the folder that contains the React app. 	

`chat_ui_python_run.py`:  This file contains the Python code to talk to the agent using the API calls.

`fast_api_app.py`: This is the file that contains the FastAPI backend server.



Start the agent now with  : ```make local-backend```

Now, we can run the Streamlit UI with:

```bash
# Install dependencies and start the React app
cd react-app/ && npm install && uv run npm run dev
```

This will open the React UI in your default browser.

Commands:

```bash
The available scripts in this project are:
npm run dev - Start development server
npm run build - Build for production
npm run preview - Preview production build
```

**Note:** 

Since the name of the agent folder is `basic_agent` and not the default `app` that was created when we generated the agent with the Agent Starter Pack, we need to modify the make command in our Makefile to start the agent.

```bash
# Launch local development server with hot-reload
local-backend:
	uv run uvicorn basic_agent.fast_api_app:app --host localhost --port 9000 --reload
```

Since this is a JS app , we will need to to handle the CORS issues.

```bash
local-backend:
	ALLOW_ORIGINS="http://localhost:3000" uv run uvicorn basic_agent.fast_api_app:app --host localhost --port 8000 --reload
```

**Note**:  We will also need to modify 2 imports in  fast_api_app.py file to the correct one. <br/>

```python
from basic_agent.app_utils.telemetry import setup_telemetry
from basic_agent.app_utils.typing import Feedback
```







