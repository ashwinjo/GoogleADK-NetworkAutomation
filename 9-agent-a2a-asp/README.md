# 9-agent-a2a-asp

Agent-to-Agent (A2A) Communication using Google's Agent Development Kit (ADK) and Agent Starter Pack (ASP)

```uvx agent-starter-pack create -p -a adk_a2a_base```

Please ensure you have your Goggle Gemini API key set in your environment variables.
export GOOGLE_API_KEY=<your-Google-Gemini-API-key>

---

## Network Use Case

**Distributed Network Operations Center** - A microservices-style architecture where specialized agents run independently and communicate over HTTP to coordinate complex network operations. This pattern mirrors real-world NOC architectures where different teams/systems handle specific domains (connectivity, security, compliance).

### Operational Architecture

**Three Independent Agents Running on Separate Ports:**

**1. Local Network Operation Agent** (Port 8080 - Main Coordinator)
- **Role**: Network Operations Coordinator
- **Responsibility**: Orchestrates comprehensive network health assessments
- **Coordinates**: Connectivity Agent + Security Agent
- **Use Case**: "Run complete network health check on router 8.8.8.8"
- **Action**: Calls both remote agents in parallel, aggregates results

**2. Remote Router Connectivity Agent** (Port 8000 - Specialist)
- **Role**: Connectivity Diagnostics Specialist
- **Tools**: `ping_router`, `traceroute_router`
- **Exposes**: Agent Card at `http://localhost:8000/a2a/app/.well-known/agent-card.json`
- **Use Case**: Network path analysis, latency testing, reachability checks

**3. Remote Router Security Agent** (Port 8001 - Specialist)
- **Role**: Security Assessment Specialist
- **Tools**: `check_router_firewall_status`, `scan_router_open_ports`, `check_router_firmware_security`
- **Exposes**: Agent Card at `http://localhost:8001/a2a/app/.well-known/agent-card.json`
- **Can Also Call**: Connectivity Agent (demonstrates agent chaining)
- **Use Case**: Security posture assessment, vulnerability detection

### Real-World Value

**Why Agent-to-Agent Communication?**

- **Microservices Architecture**: Each agent is an independent service with specialized expertise
- **Horizontal Scalability**: Add more specialist agents without modifying coordinator
- **Team Boundaries**: Different teams can own different agents (connectivity team, security team)
- **Language/Platform Agnostic**: Agents can be written in different languages, run on different infrastructure
- **Service Discovery**: Agent cards enable dynamic discovery of agent capabilities
- **Cross-Organization Collaboration**: Agents can call agents in different organizations (with proper auth)

**Comparison to Sub-Agents (Project 7)**:
- Sub-agents run in same process → A2A agents run as separate services
- Sub-agents share memory → A2A agents communicate over HTTP
- Sub-agents = tight coupling → A2A agents = loose coupling
- Sub-agents = monolith → A2A agents = microservices

---

## ADK Features Demonstrated

### 1. RemoteA2aAgent - HTTP-Based Agent Communication

**Core Concept**: Treat remote agents as if they were local sub-agents

**Configuration**:
```python
connectivity_agent = RemoteA2aAgent(
    name="router_connectivity_agent",
    description="Specialized agent for router connectivity testing",
    agent_card="http://localhost:8000/a2a/app/.well-known/agent-card.json"
)

root_agent = Agent(
    sub_agents=[connectivity_agent, security_agent],  # Mix remote and local
    ...
)
```

**How It Works**:
1. RemoteA2aAgent fetches agent card (JSON metadata about remote agent)
2. Agent card describes remote agent's tools, capabilities, API endpoints
3. When coordinator calls remote agent, ADK handles HTTP communication automatically
4. Remote agent executes tools and returns results
5. Coordinator receives results as if calling local sub-agent

### 2. Agent Cards - Service Discovery

**Agent Card Structure** (Auto-generated at `/.well-known/agent-card.json`):
```json
{
  "name": "RouterDiagnosticsAgent",
  "description": "Performs network diagnostics (ping, traceroute)",
  "tools": [
    {
      "name": "ping_router",
      "description": "Ping a router to check connectivity",
      "parameters": {"router_address": "string", "count": "int"}
    },
    {
      "name": "traceroute_router",
      "description": "Run traceroute to identify network path",
      "parameters": {"router_address": "string", "max_hops": "int"}
    }
  ],
  "endpoint": "http://localhost:8000/a2a/app"
}
```

**Benefits**:
- **Self-Documenting**: Agent card describes capabilities without manual docs
- **Dynamic Discovery**: Coordinator discovers tools at runtime
- **Version Management**: Agent card can include API versioning
- **Contract-First**: Agent card acts as API contract between services

### 3. Multi-Agent Orchestration Patterns

**Pattern 1: Parallel Delegation** (Local Network Operation Agent)
- Coordinator calls multiple remote agents simultaneously
- Aggregates results from connectivity + security checks
- Provides unified assessment

**Pattern 2: Sequential Chaining** (Remote Security Agent)
- Security agent calls connectivity agent when needed
- Demonstrates agent-to-agent-to-agent communication
- Example: Security issue detected → Call connectivity agent for diagnostics

**Pattern 3: Mixed Local/Remote**
- Agents can have both local sub-agents and remote A2A agents
- Transparent to the coordinator logic

### 4. Independent Deployment & Scaling

**Each Agent Runs Independently**:
- **Port 8000**: Connectivity Agent with FastAPI server
- **Port 8001**: Security Agent with FastAPI server  
- **Port 8080**: Coordinator Agent with FastAPI server

**Deployment Flexibility**:
- Agents can be deployed to different Cloud Run services
- Agents can run in different regions for latency optimization
- Agents can be updated/deployed independently
- Agents can be written in different languages (as long as they expose agent cards)

### 5. Tool Exposure via HTTP

**Connectivity Agent Tools**:
- `ping_router(router_address, count)` → Executes system ping command
- `traceroute_router(router_address, max_hops)` → Executes traceroute/tracepath

**Security Agent Tools**:
- `check_router_firewall_status(router_name)` → Simulated firewall check
- `scan_router_open_ports(router_name)` → Uses nmap for port scanning
- `check_router_firmware_security(router_name)` → Simulated firmware validation

**HTTP Invocation**:
- Coordinator sends HTTP POST to agent endpoint with tool name + arguments
- Remote agent executes tool locally
- Remote agent returns result as JSON
- ADK handles serialization/deserialization automatically

---

## Architecture Diagrams

### Request Flow: Complete Network Health Check

```
User Request: "Complete health check on 8.8.8.8"
    ↓
┌─────────────────────────────────────────────────┐
│  Local Network Operation Agent (Port 8080)     │
│  - Recognizes "complete health check"          │
│  - Decides to call both specialist agents      │
└─────────────────────────────────────────────────┘
    ↓
    ├─── HTTP POST to http://localhost:8000/a2a/app
    │    ┌───────────────────────────────────────┐
    │    │ Connectivity Agent (Port 8000)        │
    │    │ - ping_router(8.8.8.8)               │
    │    │ - traceroute_router(8.8.8.8)         │
    │    └───────────────────────────────────────┘
    │         ↓ Returns: Connectivity Report
    │
    └─── HTTP POST to http://localhost:8001/a2a/app
         ┌───────────────────────────────────────┐
         │ Security Agent (Port 8001)            │
         │ - check_router_firewall_status(...)   │
         │ - scan_router_open_ports(...)         │
         │ - check_router_firmware_security(...) │
         └───────────────────────────────────────┘
              ↓ Returns: Security Assessment
    
Coordinator aggregates both reports → Final unified report to user
```

### Agent Chaining: Security → Connectivity

```
Security Agent detects firewall issue
    ↓
Security Agent decides: "Need connectivity diagnostics"
    ↓
Security Agent calls Connectivity Agent (Port 8000)
    ↓ HTTP POST to http://localhost:8000/a2a/app
Connectivity Agent runs ping + traceroute
    ↓ Returns connectivity report
Security Agent incorporates connectivity data into security assessment
```

---

## Deployment Guide

### Running All Three Agents

**Terminal 1 - Connectivity Agent (Port 8000)**:
```bash
cd remoteRouterConnectivityAgent
make install
PORT=8000 make local-backend
# Runs on http://localhost:8000
# Agent card: http://localhost:8000/a2a/app/.well-known/agent-card.json
```

**Terminal 2 - Security Agent (Port 8001)**:
```bash
cd remoteRouterSecurityAgent
make install
PORT=8001 make local-backend
# Runs on http://localhost:8001
# Agent card: http://localhost:8001/a2a/app/.well-known/agent-card.json
```

**Terminal 3 - Local Coordinator (Port 8080)**:
```bash
cd localNetworkOperationAgent
make install
make playground 
# Runs on http://localhost:8501
# Connects to agents on 8000 and 8001

make inspector # start A2A visual client at port 5001 

```
---

## When to Use A2A vs Sub-Agents

| Factor | A2A Agents (This Project) | Sub-Agents (Project 7) |
|--------|---------------------------|------------------------|
| **Deployment** | Independent services | Single deployment |
| **Scaling** | Scale agents independently | Scale entire app |
| **Team Ownership** | Different teams own different agents | One team owns all |
| **Language** | Any language (via HTTP) | Must be Python/ADK |
| **Latency** | Higher (network calls) | Lower (in-process) |
| **Complexity** | Higher (service management) | Lower (monolith) |
| **Use When** | Microservices architecture needed | Simpler single-service app |

---

## Project Structure

```
9-agent-a2a-asp/
├── localNetworkOperationAgent/         # Coordinator agent (Port 8080)
│   ├── app/
│   │   ├── agent.py                    # Uses RemoteA2aAgent
│   │   └── fast_api_app.py             # FastAPI server
│   ├── Makefile
│   ├── pyproject.toml
│   └── README.md
│
├── remoteRouterConnectivityAgent/      # Connectivity specialist (Port 8000)
│   ├── app/
│   │   ├── agent.py                    # Exposes agent card
│   │   ├── app_utils/tools.py          # ping_router, traceroute_router
│   │   └── fast_api_app.py
│   ├── Makefile
│   ├── pyproject.toml
│   └── README.md
│
└── remoteRouterSecurityAgent/          # Security specialist (Port 8001)
    ├── app/
    │   ├── agent.py                    # Can also call connectivity agent
    │   ├── app_utils/tools.py          # Firewall, ports, firmware checks
    │   └── fast_api_app.py
    ├── Makefile
    ├── pyproject.toml
    └── README.md
```

---

## Key Takeaways

1. **A2A = Microservices for AI Agents**: Each agent is an independent service
2. **Agent Cards = API Contracts**: Self-documenting service discovery
3. **RemoteA2aAgent = Transparent HTTP**: Call remote agents like local sub-agents
4. **Loose Coupling**: Agents can be updated/deployed independently
5. **Horizontal Scalability**: Add specialist agents without changing coordinator
6. **Cross-Organization**: Agents can call agents in other organizations (with auth)
7. **Production-Ready**: Pattern used in enterprise microservices architectures

