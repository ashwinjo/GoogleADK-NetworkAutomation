# Sample Queries for Google ADK Network Automation Agents

This document provides sample queries for testing each agent in this repository. Each agent has 3 example queries that demonstrate its capabilities.


---

## 1. Basic Agent Examples

### 1.1 Basic Agent (`1-basic-agent/basic_agent`)
**Purpose:** Network Design Review Agent that analyzes network architectures and identifies risks.

| # | Sample Query |
|---|-------------|
| 1 | "Review my network design: We have a single core switch connecting to two distribution switches, each serving 10 access switches. All traffic goes through a single firewall for internet access. We're using OSPF for routing." |
| 2 | "Please review this design: Our data center has dual spine switches with 4 leaf switches. We're using BGP for underlay and VXLAN for overlay. There's no dedicated out-of-band management network." |
| 3 | "Analyze our branch office design: One router connected to ISP with no backup WAN link. Local servers on a flat network with no VLANs. Remote users VPN directly to the branch router." |

---

### 1.2 Advanced Config Agent (`1-basic-agent/basic_agent_advanced_config_and_cotrol`)
**Purpose:** Network Command Screening Agent that converts natural language to safe network commands while blocking dangerous operations.

| # | Sample Query |
|---|-------------|
| 1 | "Show me the command to display the BGP neighbor summary on a Cisco router" |
| 2 | "How do I delete all routes from the routing table?" |
| 3 | "Give me the command to shut down interface GigabitEthernet0/1" |

---

### 1.3 No Web Agent (`1-basic-agent/no_web_agent_run`)
**Purpose:** Direct agent execution without web interface for network operations assistance.

| # | Sample Query |
|---|-------------|
| 1 | "How can I configure OSPF on a Cisco Router?" |
| 2 | "What are the best practices for configuring BGP between two autonomous systems?" |
| 3 | "Explain the difference between EIGRP and OSPF routing protocols" |

---

## 2. Agent with Tools Examples

### 2.1 Custom Tools Agent (`2-basic-agent-with-tools/agent_custom_tools`)
**Purpose:** BGP Troubleshooting Assistant using custom tools for BGP summary, routes, and interface status.

| # | Sample Query |
|---|-------------|
| 1 | "Troubleshoot BGP on router r1-sea3" |
| 2 | "Check the BGP neighbor status for router r2-edge01 and identify any unhealthy peers" |
| 3 | "Analyze BGP routes from neighbor 192.168.1.2 on router core-router1" |

---

### 2.2 Builtin Tools Agent (`2-basic-agent-with-tools/agent_builtin_tools`)
**Purpose:** BGP troubleshooting using Google Search for knowledge-based assistance.

| # | Sample Query |
|---|-------------|
| 1 | "What are common reasons for BGP neighbor stuck in Active state?" |
| 2 | "How do I troubleshoot BGP route flapping?" |
| 3 | "What does the BGP notification error 'HOLD TIMER EXPIRED' mean and how to fix it?" |

---

### 2.3 Agent as Tool (`2-basic-agent-with-tools/agent_as_tool`)
**Purpose:** Demonstrates using agents as tools - combines BGP summary agent with Google Search agent.

| # | Sample Query |
|---|-------------|
| 1 | "Get the BGP summary for router r1-sea3 and also search for best practices on BGP route filtering" |
| 2 | "Check BGP status on core-router1 and find information about BGP route aggregation" |
| 3 | "What is the BGP neighbor state on router r2-edge01? Also search for BGP troubleshooting flowcharts" |

---

### 2.4 MCP Tools Agent (`2-basic-agent-with-tools/agent_mcp_tools_calls`)
**Purpose:** MCP (Model Context Protocol) integration - Subnet Calculator and Hugging Face tools.

| # | Sample Query |
|---|-------------|
| 1 | "Calculate subnet details for 192.168.1.0/24" |
| 2 | "What is the broadcast address and usable host range for 10.0.0.0/16?" |
| 3 | "Search Hugging Face for network automation models" |

---

### 2.5 Google Cloud Tools Agent (`2-basic-agent-with-tools/agent_google_cloud_tools_WIP`)
**Purpose:** Google Maps integration agent (Work in Progress).

| # | Sample Query |
|---|-------------|
| 1 | "Find the distance between our data center in Seattle and the branch office in Portland" |
| 2 | "What are the directions from San Francisco to Los Angeles?" |
| 3 | "Search for data center locations near New York City" |

---

### 2.6 Parallel Functions Agent (`2-basic-agent-with-tools/parallel_functions_calls`)
**Purpose:** Parallel network diagnostics - runs multiple health checks simultaneously.

| # | Sample Query |
|---|-------------|
| 1 | "Check the health of router1, router2, and fw1 devices" |
| 2 | "Measure network latency and link utilization between dc1 and dc2" |
| 3 | "Perform a comprehensive network diagnostic: check device health for router1, measure latency from dc1 to branch1, and check link utilization between dc2 and branch1" |

---

## 3. Session & Context Examples

### 3.1 Session Context Agent (`3-agent-session-context/app`)
**Purpose:** Multi-turn BGP troubleshooting with session state persistence.

| # | Sample Query (Multi-turn Conversation) |
|---|-------------|
| 1 | **Turn 1:** "Check BGP summary for router r1-core01" <br> **Turn 2:** "What was the state of neighbor 192.168.1.3?" |
| 2 | **Turn 1:** "Get BGP status on edge-router1" <br> **Turn 2:** "Tell me more about the idle neighbor" |
| 3 | **Turn 1:** "Analyze BGP on router r2-sea3" <br> **Turn 2:** "Based on the previous results, which neighbor needs attention?" |

---

## 4. Human-in-the-Loop Examples

### 4.1 HITL Boolean Confirmation (`4-agent-human-in-the-loop/agent_hitl_boolean`)
**Purpose:** Requires human approval for configuration changes on SPOF (Single Point of Failure) routers.

| # | Sample Query |
|---|-------------|
| 1 | "Read the configuration of router edge-router1" |
| 2 | "Write new configuration to router r1-sea3" *(This will require human approval - it's a SPOF router)* |
| 3 | "Update the configuration on router non-critical-router5" *(Auto-approved - not a SPOF)* |

---

### 4.2 HITL Tool Confirmation (`4-agent-human-in-the-loop/agent_hitl_tool_use`)
**Purpose:** Configuration wizard with explicit human confirmation before any write operations.

| # | Sample Query |
|---|-------------|
| 1 | "Read the current configuration from router core-router1" |
| 2 | "Apply new BGP configuration to router r2-edge01" *(Will pause for explicit approval)* |
| 3 | "Update the OSPF settings on router branch-router3" *(Requires confirmation with payload)* |

---

## 5. Callbacks & Guardrails Examples

### 5.1 Before/After Agent Callback (`5-agent-callbacks-guardrails/before_after_agent_callback`)
**Purpose:** Router health validation guardrails - blocks operations on unhealthy routers.

| # | Sample Query |
|---|-------------|
| 1 | "Read configuration from router r1-core01" *(May be blocked if router is detected as down)* |
| 2 | "Get the running config for router r2-edge05" |
| 3 | "Show me the configuration of router cor01" |

---

### 5.2 Before/After Tool Callback (`5-agent-callbacks-guardrails/before_after_tool_callback`)
**Purpose:** Access control and content security - blocks restricted routers and masks passwords.

| # | Sample Query |
|---|-------------|
| 1 | "Read configuration from router r1-gov51" *(Will be blocked - restricted gov cloud router)* |
| 2 | "Show me the running config of router edge-router1" *(Passwords will be masked in response)* |
| 3 | "Get configuration from router core-router2" |

---

### 5.3 Before/After Model Callback (`5-agent-callbacks-guardrails/before_after_model_callback`)
**Purpose:** Sensitive content detection - blocks plaintext passwords in requests and responses.

| # | Sample Query |
|---|-------------|
| 1 | "Configure router with password cisco123" *(Will be blocked - password in plaintext)* |
| 2 | "Read configuration from router r1-sea3" *(Response filtered if contains unencrypted passwords)* |
| 3 | "Show me the interface configuration for router edge01" |

---

## 6. Workflow Examples

### 6.1 Sequential Workflow (`6-agent-workflows/sequential`)
**Purpose:** Step-by-step network troubleshooting - device info → status check → ping → traceroute → firewall → summary.

| # | Sample Query |
|---|-------------|
| 1 | "I'm experiencing connectivity issues with router R1-core01. The interfaces seem to be flapping." |
| 2 | "Our BGP neighbor on router edge-router1 keeps going down. Please diagnose." |
| 3 | "Network latency to branch office is very high. Investigate router branch-gw1." |

---

### 6.2 Parallel Workflow (`6-agent-workflows/parallel`)
**Purpose:** Parallel CPU utilization checks on multiple routers simultaneously.

| # | Sample Query |
|---|-------------|
| 1 | "Customer complaint: Throughput is low on our Seattle network segment" |
| 2 | "We're seeing performance degradation. Check CPU on r1-sea3 and r2-sea3" |
| 3 | "Investigate high CPU usage affecting network performance in the SEA3 datacenter" |

---

### 6.3 Loop Workflow (`6-agent-workflows/loop`)
**Purpose:** Continuous monitoring and auto-remediation loop until network is healthy.

| # | Sample Query |
|---|-------------|
| 1 | "Customer reports: Internet connection is unstable" |
| 2 | "Network service is intermittent. Monitor and fix automatically." |
| 3 | "We have multiple network alerts. Please diagnose and remediate until the network is stable." |

---

## 7. Sub-Agents Examples

### 7.1 Hierarchical Sub-Agents (`7-agent-subagents/app`)
**Purpose:** Orchestrated website troubleshooting with monitoring → analysis → remediation → reporting.

| # | Sample Query |
|---|-------------|
| 1 | "Website https://example.com is slow for users. Please investigate and fix." |
| 2 | "Our web application at https://myapp.internal.com is not responding. Diagnose and remediate." |
| 3 | "Users are complaining about high latency when accessing https://portal.company.com" |

---

## 8. RAG Agent Examples

### 8.1 RAG Document Retrieval (`8-agent-rag-WIP/app`)
**Purpose:** Question-answering using document retrieval and re-ranking.

| # | Sample Query |
|---|-------------|
| 1 | "What is the recommended MTU size for VXLAN overlays according to our documentation?" |
| 2 | "How do we configure BGP route reflectors in our network?" |
| 3 | "What are our company's firewall change request procedures?" |

---

## 9. Agent-to-Agent (A2A) Examples

### 9.1 Local Network Operations Agent (`9-agent-a2a-asp/localNetworkOperationAgent`)
**Purpose:** Coordinator agent that orchestrates connectivity and security agents.

| # | Sample Query |
|---|-------------|
| 1 | "Perform a complete network health check on 8.8.8.8" |
| 2 | "Run comprehensive security and connectivity assessment for router 10.0.0.1" |
| 3 | "Do a full network audit including ping, traceroute, and security scan for 192.168.1.1" |

---

### 9.2 Remote Router Connectivity Agent (`9-agent-a2a-asp/remoteRouterConnectivityAgent`)
**Purpose:** Remote agent for ping and traceroute diagnostics.

| # | Sample Query |
|---|-------------|
| 1 | "Ping router at 8.8.8.8 and measure latency" |
| 2 | "Run a traceroute to 10.0.0.1 to identify the network path" |
| 3 | "Test connectivity to 192.168.1.1 and report any packet loss" |

---

### 9.3 Remote Router Security Agent (`9-agent-a2a-asp/remoteRouterSecurityAgent`)
**Purpose:** Remote agent for security assessment - firewall, port scanning, firmware checks.

| # | Sample Query |
|---|-------------|
| 1 | "Check the firewall status on router 192.168.1.1" |
| 2 | "Scan for open ports on router 10.0.0.1 and identify vulnerabilities" |
| 3 | "Verify firmware security and patch level for router at 8.8.8.8" |

---

## 10. Observability Examples

### 10.1 Basic Logging Agent (`10-agent-observability/basic_logging`)
**Purpose:** Demonstrates basic Python logging with weather and time tools.

| # | Sample Query |
|---|-------------|
| 1 | "What's the weather in San Francisco?" |
| 2 | "What time is it in SF right now?" |
| 3 | "Tell me the weather and current time in San Francisco" |

---

### 10.2 Third-Party Logging Agent (`10-agent-observability/third_party_logging`)
**Purpose:** Integration with Opik for observability and tracing.

| # | Sample Query |
|---|-------------|
| 1 | "What's the weather like in San Francisco today?" |
| 2 | "Get me the current time in SF" |
| 3 | "What's the weather and time in San Francisco?" |

---

## 11. Cloud Run Deployment Examples

### 11.1 Cloud Run Agent (`11-agent-deployment-cloudrun/app`)
**Purpose:** Network Design Review Agent deployed on Google Cloud Run.

| # | Sample Query |
|---|-------------|
| 1 | "Review our cloud network: We have a hub VPC with 4 spoke VPCs connected via VPC peering. All egress goes through a centralized NAT gateway." |
| 2 | "Analyze this hybrid design: On-prem data center connects to GCP via a single Cloud VPN tunnel. We use Cloud Router for dynamic routing." |
| 3 | "Review: Three-tier application with web, app, and database tiers in separate subnets. All traffic flows through a single Cloud Load Balancer." |

---

## 12. Vertex AI Deployment Examples

### 12.1 Vertex AI Agent (`12-agent-deployment-vtxai/basic_agent`)
**Purpose:** Network Design Review Agent deployed on Vertex AI Agent Builder.

| # | Sample Query |
|---|-------------|
| 1 | "Review my GKE network design: Pods use private IP ranges, services exposed via Internal Load Balancer, and we have a single NAT gateway for all egress." |
| 2 | "Analyze this multi-region design: Primary in us-central1, DR in us-east1, connected via Cloud Interconnect. No automated failover configured." |
| 3 | "Review: Kubernetes cluster with Istio service mesh, all inter-service traffic encrypted with mTLS, single ingress gateway." |

---

## 13. Frontend Examples

### 13.1 API Frontend Agent (`13-agent-api-frontend/basic_agent`)
**Purpose:** Network Design Review Agent with REST API frontend.

| # | Sample Query |
|---|-------------|
| 1 | "Review: Campus network with collapsed core, 100 access switches, and centralized firewalling. No redundant uplinks from access to distribution." |
| 2 | "Analyze our SD-WAN design: 50 branches with dual ISP links, centralized controller in AWS, and local internet breakout enabled." |
| 3 | "Review: Data center spine-leaf with 2 spines and 8 leaves. VXLAN over eBGP underlay. No dedicated out-of-band management." |

---

### 13.2 Streamlit UI Agent (`13-agent-streamlit-ui/basic_agent`)
**Purpose:** Network Design Review Agent with Streamlit web interface.

| # | Sample Query |
|---|-------------|
| 1 | "Review this design: Two data centers with active-active configuration. GSLB for traffic distribution. Single MPLS circuit between sites." |
| 2 | "Analyze: Small office network with a single router, flat Layer 2, no VLAN segmentation, and direct internet access." |
| 3 | "Review our wireless design: Centralized controller managing 500 APs. Single management VLAN. No RF planning performed." |

---

## 14. Ollama Examples

### 14.1 Ollama Local LLM Agent (`14-agent-ollama/app`)
**Purpose:** Network Design Review Agent using local Ollama LLM (e.g., Gemma3n).

| # | Sample Query |
|---|-------------|
| 1 | "Review: Simple home network with ISP router, one switch, and 10 devices. No firewall, using default ISP DNS." |
| 2 | "Analyze: Lab network with 3 routers running OSPF, connected in a triangle topology. No authentication configured." |
| 3 | "Review this student project: BGP between two ASNs with single peering link. No route filtering. Using default timers." |

---

## Quick Reference: How to Run

```bash
# Navigate to the specific agent directory
cd <agent-directory>

# Run with ADK web interface
adk web

# Or run with ADK API server
adk api_server

# For no-web agents, run directly
python agent.py
```

## Notes

- Some agents require additional setup (e.g., environment variables, MCP servers, remote agents)
- Multi-turn queries require the same session to be maintained
- HITL agents will pause execution waiting for human approval
- Loop workflows will continue until exit conditions are met or max iterations reached
- A2A agents require the remote agents to be running on their respective ports

