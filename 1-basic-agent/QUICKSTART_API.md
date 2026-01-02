# Quick Start: Building a Custom Frontend

Follow these steps to interact with your ADK agent via API and build a custom frontend.

## Step 1: Start the API Server

Open a terminal and start the server:

```bash
cd /home/ubuntusand/GoogleADK-NetworkAutomation/1-basic-agent
adk api_server .
```

The server will start at `http://localhost:8000`

**Keep this terminal open!** The server needs to run while you test.

---

## Step 2: Test the API

Open a **new terminal** and run the test script:

```bash
cd /home/ubuntusand/GoogleADK-NetworkAutomation/1-basic-agent
uv run python test_api.py
```

This will verify:
- ✓ Server is running
- ✓ Agents are available
- ✓ Sessions can be created
- ✓ Messages work (both sync and streaming)

---

## Step 3: Try the Examples

### A. Simple Client (Synchronous)
```bash
uv run python simple_client.py
```

This demonstrates:
- Listing agents
- Creating sessions
- Sending messages
- Extracting responses
- Retrieving conversation history

### B. Interactive Chat (Streaming)
```bash
uv run python chat_interface.py
```

This provides a terminal chat interface with real-time streaming responses!

---

## Step 4: Explore the API Docs

While the server is running, open your browser:

**Swagger UI:** http://localhost:8000/docs

Here you can:
- See all available endpoints
- Test API calls directly in the browser
- View request/response schemas
- Download the OpenAPI spec

---

## Step 5: Make Your Own API Calls

### Using cURL

```bash
# Create a session
curl -X POST http://localhost:8000/create_session \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "basic_agent",
    "user_id": "my_user"
  }'

# Send a message (replace SESSION_ID with the one from above)
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "basic_agent",
    "user_id": "my_user",
    "session_id": "SESSION_ID",
    "new_message": {
      "role": "user",
      "parts": [{"text": "Hello!"}]
    }
  }'
```

### Using Python

```python
import requests

# Create session
session = requests.post(
    "http://localhost:8000/create_session",
    json={"app_name": "basic_agent", "user_id": "test"}
).json()

session_id = session["session_id"]

# Send message
response = requests.post(
    "http://localhost:8000/run",
    json={
        "app_name": "basic_agent",
        "user_id": "test",
        "session_id": session_id,
        "new_message": {
            "role": "user",
            "parts": [{"text": "What can you do?"}]
        }
    }
).json()

# Extract agent response
for event in response["events"]:
    if event["author"] != "user":
        for part in event["content"]["parts"]:
            if "text" in part:
                print(part["text"])
```

---

## Key API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/list-apps` | GET | List available agents |
| `/create_session` | POST | Start a new conversation |
| `/run` | POST | Send message (wait for complete response) |
| `/run_sse` | POST | Send message (streaming response) |
| `/get_session/{id}` | GET | Get conversation history |
| `/docs` | GET | Interactive API documentation |

---

## Request/Response Format

### Creating a Session
**Request:**
```json
{
  "app_name": "basic_agent",
  "user_id": "your_user_id"
}
```

**Response:**
```json
{
  "session_id": "abc123...",
  "user_id": "your_user_id",
  "app_name": "basic_agent",
  "state": {},
  "events": []
}
```

### Sending a Message
**Request:**
```json
{
  "app_name": "basic_agent",
  "user_id": "your_user_id",
  "session_id": "abc123...",
  "new_message": {
    "role": "user",
    "parts": [
      {"text": "Your message here"}
    ]
  }
}
```

**Response:**
```json
{
  "events": [
    {
      "id": "evt_1",
      "author": "user",
      "content": {
        "role": "user",
        "parts": [{"text": "Your message here"}]
      }
    },
    {
      "id": "evt_2",
      "author": "root_agent",
      "content": {
        "role": "model",
        "parts": [{"text": "Agent's response here"}]
      }
    }
  ],
  "session_id": "abc123..."
}
```

---

## Building a Web Frontend

### Using JavaScript/React

```javascript
// Create session
const session = await fetch('http://localhost:8000/create_session', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    app_name: 'basic_agent',
    user_id: 'web_user'
  })
}).then(r => r.json());

// Send message
const response = await fetch('http://localhost:8000/run', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    app_name: 'basic_agent',
    user_id: 'web_user',
    session_id: session.session_id,
    new_message: {
      role: 'user',
      parts: [{ text: userInput }]
    }
  })
}).then(r => r.json());

// Extract response
const agentMessage = response.events
  .find(e => e.author !== 'user')
  ?.content?.parts[0]?.text;
```

### Using Server-Sent Events (Streaming)

```javascript
const eventSource = new EventSource('http://localhost:8000/run_sse');

eventSource.addEventListener('message', (e) => {
  const data = JSON.parse(e.data);
  const event = data.event;
  
  if (event.author !== 'user') {
    const text = event.content?.parts[0]?.text;
    if (text) {
      // Append to UI
      messageElement.textContent += text;
    }
  }
});

eventSource.addEventListener('complete', () => {
  eventSource.close();
});
```

**Note:** For browser requests, you may need to handle CORS. Set the `ALLOW_ORIGINS` environment variable when starting the server:

```bash
export ALLOW_ORIGINS="http://localhost:3000,http://localhost:5173"
adk api_server .
```

---

## Next Steps

1. **Read the full guide:** `cat API_INTEGRATION_GUIDE.md`
2. **Experiment with the examples** - modify `simple_client.py` or `chat_interface.py`
3. **Build your frontend:**
   - Use the provided Python clients as reference
   - Adapt the request/response handling for your language/framework
   - Implement streaming for better UX
4. **Add authentication** if needed (JWT, API keys, etc.)
5. **Deploy your agent** (see `README.md` for deployment options)

---

## Troubleshooting

**Server not starting?**
- Check if port 8000 is already in use
- Try: `adk api_server . --port 8080`

**Connection refused?**
- Ensure the server is running in another terminal
- Test with: `curl http://localhost:8000/health`

**CORS errors in browser?**
- Set `ALLOW_ORIGINS` environment variable
- Or use a backend proxy to call the API

**Session not found?**
- Sessions may be in-memory only (lost on restart)
- Create a new session for each test

---

## Resources

- **Full API Guide:** `API_INTEGRATION_GUIDE.md`
- **ADK Documentation:** `GEMINI.md`
- **Interactive API Docs:** http://localhost:8000/docs (when server is running)
- **Example Code:** `simple_client.py`, `chat_interface.py`, `test_api.py`

Happy building! 🚀


