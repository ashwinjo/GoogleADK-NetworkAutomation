# ADK API Integration Guide
## Building a Custom Frontend for Your Agent

This guide shows you how to interact with your ADK agent's API endpoints to build a custom frontend, similar to what `adk web` provides.

---

## Table of Contents
1. [Starting the API Server](#1-starting-the-api-server)
2. [Available Endpoints](#2-available-endpoints)
3. [API Request/Response Schema](#3-api-requestresponse-schema)
4. [Basic Examples with cURL](#4-basic-examples-with-curl)
5. [Python Client Examples](#5-python-client-examples)
6. [Building a Streaming Chat Interface](#6-building-a-streaming-chat-interface)
7. [Advanced Features](#7-advanced-features)

---

## 1. Starting the API Server

### Option A: Using the FastAPI app directly
```bash
cd /home/ubuntusand/GoogleADK-NetworkAutomation/1-basic-agent
uv run uvicorn basic_agent.fast_api_app:app --host 0.0.0.0 --port 8000 --reload
```

### Option B: Using the Makefile
```bash
make local-backend
```

**Default Server URL:** `http://<ip>:<port>`

**API Documentation:** Once running, visit:
- Swagger UI: `http://<ip>:<port>/docs`
- ReDoc: `http://<ip>:<port>/redoc`

---

API Docs: https://google.github.io/adk-docs/runtime/api-server/#local-testing

## 2. Available Endpoints

### Core Agent Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/list-apps` | GET | List all available agents/apps |
| `/run` | POST | Synchronous agent execution (waits for completion) |
| `/run_sse` | POST | Server-Sent Events streaming (real-time responses) |
| `/apps/{app_name}/users/{user_id}/sessions/{session_id}` | POST | Create a new session |
| `/apps/{app_name}/users/{user_id}/sessions/{session_id}` | GET | Retrieve session details and history |
| `/apps/{app_name}/users/{user_id}/sessions/{session_id}` | PATCH | Update session state |
| `/apps/{app_name}/users/{user_id}/sessions/{session_id}` | DELETE | Delete a session |
| `/feedback` | POST | Submit user feedback (custom endpoint) |

Server Web UI:
| `/dev-ui` | GET | Root endpoint (serve web UI) |

---

## 3. API Request/Response Schema

### 3.1 List Available Agents

**Request:**
```bash
curl -X GET http://localhost:8000/list-apps
```

**Response:**
```json
[
  "basic_agent",
  "basic_agent_advanced_config_and_cotrol",
  "no_web_agent_run",
  "tests"
]
```

---

### 3.2 Create a Session

Creates a new session with optional initial state.

**Method:** `POST`  
**Path:** `/apps/{app_name}/users/{user_id}/sessions/{session_id}`

**Request:**
```bash
curl -X POST http://localhost:8000/apps/basic_agent/users/u_123/sessions/s_123 \
  -H "Content-Type: application/json" \
  -d '{
    "key1": "value1",
    "key2": 42
  }'
```

**Response:**
```json
{
  "id": "s_123",
  "appName": "basic_agent",
  "userId": "u_123",
  "state": {
    "key1": "value1",
    "key2": 42
  },
  "events": [],
  "lastUpdateTime": 1767395964.8706188
}
```

---

### 3.3 Run Agent (Synchronous)

Send a message and wait for the complete response.

**Method:** `POST`  
**Path:** `/run`

**Request:**
```bash
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "appName": "basic_agent",
    "userId": "u_123",
    "sessionId": "s_123",
    "newMessage": {
      "role": "user",
      "parts": [
        {
          "text": "Hey what is meaning of BGP in networking"
        }
      ]
    }
  }'
```

**Response:**
```json
[
  {
    "modelVersion": "gemini-3-flash-preview",
    "content": {
      "parts": [
        {
          "text": "## Design Summary\nThe user has requested a conceptual definition of the **Border Gateway Protocol (BGP)** rather than submitting a specific network architecture for review. .**",
          "thoughtSignature": "CowV"
        }
      ],
      "role": "model"
    },
    "finishReason": "STOP",
    "usageMetadata": {
      "candidatesTokenCount": 636,
      "candidatesTokensDetails": [
        {
          "modality": "TEXT",
          "tokenCount": 636
        }
      ],
      "promptTokenCount": 480,
      "promptTokensDetails": [
        {
          "modality": "TEXT",
          "tokenCount": 480
        }
      ],
      "thoughtsTokenCount": 591,
      "totalTokenCount": 1707,
      "trafficType": "ON_DEMAND"
    },
    "invocationId": "e-37e657fa-93eb-4e53-8619-d36991199258",
    "author": "root_agent",
    "actions": {
      "stateDelta": {},
      "artifactDelta": {},
      "requestedAuthConfigs": {},
      "requestedToolConfirmations": {}
    },
    "id": "1388c4f5-531a-4896-822f-6269b645baae",
    "timestamp": 1767396209.297988
  }
]
```

---

### 3.4 Run Agent with Streaming (SSE)

Send a message and receive the response as a real-time stream.

**Method:** `POST`  
**Path:** `/run_sse`

**Request (Text Only):**
```bash
curl -X POST http://localhost:8000/run_sse \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  --no-buffer \
  -d '{
    "appName": "basic_agent",
    "userId": "u_123",
    "sessionId": "s_123",
    "streaming": true,
    "newMessage": {
      "role": "user",
      "parts": [
        {
          "text": "Hey what is meaning of BGP in networking. Answer in 50 words"
        }
      ]
    }
  }'
```

**Request (With Image - Base64 Encoded):**
```bash
curl -X POST http://localhost:8000/run_sse \
  -H "Content-Type: application/json" \
  -d '{
    "appName": "basic_agent",
    "userId": "u_123",
    "sessionId": "s_123",
    "newMessage": {
      "role": "user",
      "parts": [
        {
          "text": "Describe this image"
        },
        {
          "inlineData": {
            "displayName": "my_image.png",
            "data": "iVBORw0KGgoAAAANSUhEUgAAAgAAAAIACAYAAAD0eNT6AAAACXBIWXMAAAsTAAALEwEAmpw...",
            "mimeType": "image/png"
          }
        }
      ]
    },
    "streaming": false
  }'
```

**Response:** Server-Sent Events stream
```
event: message
data: {"event": {"id": "evt_001", "author": "user", "content": {...}}}

event: message
data: {"event": {"id": "evt_002", "author": "root_agent", "content": {"parts": [{"text": "Once"}]}}}

event: message
data: {"event": {"id": "evt_003", "author": "root_agent", "content": {"parts": [{"text": " upon"}]}}}

event: complete
data: {"sessionId": "s_123"}
```

---

## 4. Session Management

### 4.1 Get a Session

Retrieves a session by ID, including its state and conversation history.

**Method:** `GET`  
**Path:** `/apps/{app_name}/users/{user_id}/sessions/{session_id}`

**Request:**
```bash
curl -X GET http://localhost:8000/apps/basic_agent/users/u_123/sessions/s_abc
```

**Response:**
```json
{
  "id": "s_abc",
  "appName": "basic_agent",
  "userId": "u_123",
  "state": {
    "visit_count": 5
  },
  "events": [
    {
      "id": "evt_001",
      "author": "user",
      "content": {
        "role": "user",
        "parts": [{"text": "Hello"}]
      },
      "timestamp": 1743711420.0
    }
  ],
  "lastUpdateTime": 1743711430.022186
}
```

---

### 4.2 Update a Session

Updates an existing session's state using a delta.

**Method:** `PATCH`  
**Path:** `/apps/{app_name}/users/{user_id}/sessions/{session_id}`

**Request:**
```bash
curl -X PATCH http://localhost:8000/apps/basic_agent/users/u_123/sessions/s_abc \
  -H "Content-Type: application/json" \
  -d '{
    "stateDelta": {
      "key1": "value1",
      "key2": 42
    }
  }'
```

**Response:**
```json
{
  "id": "s_abc",
  "appName": "basic_agent",
  "userId": "u_123",
  "state": {
    "visit_count": 5,
    "key1": "value1",
    "key2": 42
  },
  "events": [],
  "lastUpdateTime": 1743711443.123456
}
```

---

### 4.3 Delete a Session

Deletes a session and all of its associated data permanently.

**Method:** `DELETE`  
**Path:** `/apps/{app_name}/users/{user_id}/sessions/{session_id}`

**Request:**
```bash
curl -X DELETE http://localhost:8000/apps/basic_agent/users/u_123/sessions/s_abc
```

**Response:**  
A successful deletion returns an empty response with a `204 No Content` status code.

---

## 8. Troubleshooting

### CORS Issues
If calling from a browser, set the `ALLOW_ORIGINS` environment variable:

```bash
export ALLOW_ORIGINS="http://localhost:3000,http://localhost:5173"
```

---
### Connection Refused
Ensure the server is running:

```bash
curl http://localhost:8000/health
```

---

### Invalid Session
Sessions may be in-memory only and lost on server restart. Create a new session if you get "session not found" errors.

---

## 9. Additional Resources

- **Official API Documentation:** https://google.github.io/adk-docs/runtime/api-server/
- **ADK Cheatsheet:** See `GEMINI.md` in this directory
- **Interactive API Docs:** http://localhost:8000/docs (when server is running)
- **OpenAPI Spec:** http://localhost:8000/openapi.json