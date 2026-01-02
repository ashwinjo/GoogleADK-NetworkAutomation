# 6-agent-workflows

A base ReAct agent built with Google's Agent Development Kit (ADK)
Agent generated with [`googleCloudPlatform/agent-starter-pack`](https://github.com/GoogleCloudPlatform/agent-starter-pack) version `0.29.3`

---

## Network Use Case

**Automated Network Troubleshooting Workflows** - Demonstrates three distinct workflow orchestration patterns for network operations, each solving different operational challenges:

### 1. Parallel Workflows - Concurrent Device Diagnostics

**Scenario**: High CPU utilization investigation across multiple routers
- Check CPU/memory on **r1-sea3** and **r2-sea3** simultaneously
- Compare health metrics in parallel to identify performance bottlenecks
- Correlate results to pinpoint the problematic device

**Real-World Value**: 
- Reduces diagnostic time from minutes to seconds
- Enables side-by-side comparison of device health
- Essential for identifying which router in a redundant pair is causing issues

### 2. Sequential Workflows - Systematic Troubleshooting

**Scenario**: Comprehensive connectivity and routing diagnostics
1. **Gather Context**: Collect reported issue details
2. **Health Check**: Validate device operational status
3. **Reachability**: Test ICMP connectivity
4. **Path Analysis**: Run traceroute for hop-by-hop diagnosis
5. **Security Validation**: Check firewall rules and ACLs
6. **Summary**: Correlate findings across all layers

**Real-World Value**:
- Mirrors standard NOC troubleshooting runbooks
- Each step builds on prior findings
- Eliminates manual copy-paste between tools

### 3. Loop Workflows - Self-Healing Network Operations

**Scenario**: Autonomous monitoring and remediation cycles
- **Monitor**: Check connectivity, latency, security alerts, overall status
- **Assess**: Determine if network is healthy/degraded/unstable
- **Remediate**: Apply fixes (restart services, adjust firewall, optimize routing)
- **Re-evaluate**: Loop until healthy or max iterations reached

**Real-World Value**:
- Implements closed-loop automation for common issues
- Reduces MTTR (Mean Time To Resolution) for standard problems
- Frees NOC engineers to focus on complex incidents

## ADK Features Demonstrated

This project showcases three fundamental workflow orchestration patterns:

### 1. ParallelAgent (`parallel/`)

**Concurrent Multi-Device Diagnostics**

- **Parallel Execution**: Multiple agents run simultaneously, not sequentially
- **Resource Efficiency**: Agents execute concurrently for faster results
- **Independent Sub-Agents**: Each with specialized tools and instructions
  - `check_cpu_utilization_r1_sea3_agent` → Validates normal CPU on first router
  - `check_cpu_utilization_r2_sea3_agent` → Detects high CPU on second router
- **Output Key Management**: Each parallel agent stores results in session state
- **Result Correlation**: Summary agent receives both outputs via state injection
- **Nested Workflows**: ParallelAgent embedded within SequentialAgent for complex flows

**Architecture**:
```
SequentialAgent [
  StartAgent → ParallelAgent [
                 check_r1_agent (cpu tool)
                 check_r2_agent (cpu tool)
               ] → SummaryAgent
]
```

**Key Learning**: Parallel workflows reduce diagnostic time but require proper output key management for result aggregation.

### 2. SequentialAgent (`sequential/`)

**Step-by-Step Systematic Diagnostics**

- **Sequential Execution**: Agents run in strict order
- **Context Propagation**: Each agent accesses prior outputs via state
- **Multi-Stage Workflow**: 6-agent pipeline
  1. **StartAgent**: Decision gate (greeting vs troubleshooting)
  2. **GatherInfoAgent**: Collect reported symptoms
  3. **DeviceStatusAgent**: Validate NMS health data
  4. **PingTestAgent**: Test Layer 3 reachability
  5. **TracerouteAgent**: Analyze hop-by-hop path
  6. **FirewallAgent**: Validate security policies
  7. **SummaryAgent**: Correlate findings across layers
- **Output Keys**: Each agent stores findings for downstream consumption
- **Conditional Logic**: StartAgent determines whether to proceed based on user input

**Architecture**:
```
SequentialAgent [
  StartAgent → GatherInfo → DeviceStatus → PingTest → 
  Traceroute → FirewallRules → Summary
]
```

**Key Learning**: Sequential workflows mirror human troubleshooting logic and enable sophisticated multi-layer diagnostics.

### 3. LoopAgent (`loop/`)

**Iterative Self-Healing Cycles**

- **Bounded Iteration**: `max_iterations=3` prevents infinite loops
- **Two-Agent Cycle**:
  - **MonitoringAgent**: Assesses network health (connectivity, latency, alerts, status)
  - **RemediationAgent**: Applies fixes if degraded/unstable
- **Exit Control**: Custom `exit_loop()` tool via `tool_context.actions.escalate = True`
- **State Classification**: Monitoring agent explicitly sets `overall_health` state
- **Exit Condition**: RemediationAgent calls `exit_loop()` only when `overall_health = "healthy"`
- **Wrapped in Sequential**: Loop embedded in larger pipeline (Start → Loop → Summary)

**Architecture**:
```
SequentialAgent [
  StartAgent → LoopAgent (max_iterations=3) [
                 MonitoringAgent (tools: check_connectivity, check_latency, etc.)
                 RemediationAgent (tools: restart_service, fix_connectivity, exit_loop)
               ] → SummaryAgent
]
```

**Key Learning**: Loop workflows enable autonomous remediation but require careful exit condition design to avoid infinite loops.

### 4. Cross-Cutting Features

**Shared Across All Implementations**:

- **Specialized Agent Instructions**: Each agent has detailed system prompts defining scope and constraints
- **Temperature Control**: `temperature=0.0` for deterministic, repeatable behavior
- **Output Key Strategy**: Explicit state management via `output_key` parameters
- **Tool Isolation**: Each agent receives only the tools relevant to its role
- **Structured Outputs**: Agents produce markdown tables and formatted reports
- **Fact-Based Reasoning**: Agents instructed to avoid assumptions, only report observed data

---

## Workflow Selection Guide

| Use Case | Workflow Type | When to Use |
|----------|---------------|-------------|
| **Multi-device comparison** | Parallel | Need to check multiple devices simultaneously |
| **Standard troubleshooting** | Sequential | Following established diagnostic procedures |
| **Auto-remediation** | Loop | Common, repeatable issues with known fixes |
| **Complex diagnostics** | Nested (Parallel + Sequential) | Multi-stage workflows with concurrent checks |

---