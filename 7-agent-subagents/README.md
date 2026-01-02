# 7-agent-subagents

A base ReAct agent built with Google's Agent Development Kit (ADK)
Agent generated with [`googleCloudPlatform/agent-starter-pack`](https://github.com/GoogleCloudPlatform/agent-starter-pack) version `0.29.3`

---

## Network Use Case

**Hierarchical Website Troubleshooting System** - An intelligent multi-agent orchestration pattern where a parent "Network Troubleshooting Agent" delegates specialized tasks to expert sub-agents, mimicking how a senior NOC engineer coordinates a team.

### Operational Workflow

**User Report**: "Website https://example.com is slow" or "Website is not responding"

**Orchestration Response**:
1. **Parent Agent** receives report and initiates hierarchical workflow
2. **MonitoringAgent** (Sub-Agent 1):
   - Checks website availability
   - Measures response time
   - Detects packet loss
   - **Reports findings back to parent**

3. **AnalysisAgent** (Sub-Agent 2):
   - Receives monitoring results from parent
   - Analyzes network traffic patterns
   - Examines latency distribution
   - Identifies bottlenecks (server, network, or routing)
   - **Reports root cause analysis to parent**

4. **RemediationAgent** (Sub-Agent 3):
   - Receives analysis from parent
   - Selects appropriate remediation action:
     - Restart web server (if server issue detected)
     - Clear cache (if cache problem identified)
     - Optimize routing (if latency/routing issue found)
   - **Reports remediation outcome to parent**

5. **ReportingAgent** (Sub-Agent 4):
   - Extracts conversation history from all prior agents
   - Collects monitoring, analysis, and remediation results
   - Formats comprehensive troubleshooting report
   - **Presents final summary to user**

### Real-World Value

- **Delegation Pattern**: Parent agent doesn't do the work—it orchestrates specialists
- **Expertise Separation**: Each sub-agent has specialized tools and knowledge domain
- **Dynamic Task Assignment**: Parent determines which sub-agent to invoke based on context
- **Result Aggregation**: ReportingAgent synthesizes entire workflow into actionable summary
- **Scalability**: Easy to add new specialist agents without changing parent logic

**Difference from Sequential Workflows**: 
- In sequential workflows, agents run automatically in predetermined order
- In sub-agent pattern, parent agent dynamically decides which sub-agent to call, when, and with what instructions
- Sub-agents report back to parent, not directly to next agent

## ADK Features Demonstrated

This project showcases advanced hierarchical multi-agent architecture:

### 1. Parent-Child Agent Hierarchy

**Parent Orchestration Agent**

- **sub_agents Parameter**: Declares available specialist agents
  ```python
  network_troubleshooting_agent = Agent(
      name="NetworkTroubleshootingAgent",
      sub_agents=[
          monitoring_agent,
          analysis_agent,
          remediation_agent,
          reporting_agent,
      ],
      ...
  )
  ```
- **No Tools Directly**: Parent delegates work rather than executing it
- **Dynamic Delegation**: Parent decides which sub-agent to invoke based on user request
- **Context Management**: Parent passes relevant information to each sub-agent
- **Result Aggregation**: Parent receives outputs from sub-agents and coordinates handoffs

### 2. Specialized Sub-Agent Design

**Four Expert Sub-Agents with Domain-Specific Tools**

**MonitoringAgent**:
- **Tools**: `check_website_availability`, `check_response_time`, `check_packet_loss`
- **Responsibility**: Detect symptoms and current state
- **Output Key**: `monitoring_results` stored in session state

**AnalysisAgent**:
- **Tools**: `analyze_network_traffic`, `analyze_latency`, `identify_bottlenecks`
- **Responsibility**: Diagnose root causes from monitoring data
- **Output Key**: `analysis_results` stored in session state

**RemediationAgent**:
- **Tools**: `restart_web_server`, `clear_cache`, `optimize_routing`
- **Responsibility**: Apply corrective actions based on analysis
- **Output Key**: `remediation_results` stored in session state

**ReportingAgent**:
- **Tools**: `format_report`
- **Responsibility**: Synthesize complete workflow into final report
- **Output Key**: `final_report` stored in session state

### 3. Task Delegation Pattern

**How Parent Orchestrates Sub-Agents**:

1. **Receives User Request**: Parent agent gets initial complaint
2. **Delegates to MonitoringAgent**: 
   - Parent: "Check the website status for https://example.com"
   - MonitoringAgent executes tools and returns results to parent
3. **Delegates to AnalysisAgent**:
   - Parent: "Here are the monitoring results, analyze the root cause"
   - AnalysisAgent receives monitoring data via conversation history
4. **Delegates to RemediationAgent**:
   - Parent: "Based on analysis, attempt remediation"
   - RemediationAgent selects appropriate fix based on identified issue
5. **Delegates to ReportingAgent**:
   - Parent: "Generate final report from all findings"
   - ReportingAgent extracts conversation history and formats summary

### 4. Conversation History Access

**ReportingAgent's Advanced Pattern**:

- **Reads Conversation History**: Accesses outputs from all prior sub-agents
- **Extracts Output Keys**: Pulls `monitoring_results`, `analysis_results`, `remediation_results` from state
- **Cross-Agent Data Flow**: Demonstrates how agents communicate through shared session state
- **Comprehensive Reporting**: Synthesizes multi-agent outputs into unified report

**Key Code Pattern**:
```python
instruction="""
1. Review entire conversation history
2. Extract monitoring_results from MonitoringAgent's output
3. Extract analysis_results from AnalysisAgent's output  
4. Extract remediation_results from RemediationAgent (direct input)
5. Use format_report tool with all collected data
"""
```

### 5. Instruction Engineering for Sub-Agents

**Specialized System Prompts**:

- **MonitoringAgent**: Told to extract website URL from task description
- **AnalysisAgent**: Instructed to identify actionable root causes for remediation
- **RemediationAgent**: Given conditional logic (server issues → restart, cache → clear, routing → optimize)
- **ReportingAgent**: Detailed instructions on extracting conversation history and formatting

### 6. Deterministic Behavior

- **Temperature**: `0.0` across all agents for consistent, repeatable troubleshooting
- **Retry Options**: `HttpRetryOptions(attempts=3)` for resilience
- **Structured Outputs**: Agents produce formatted markdown tables and reports

---

## Architecture Comparison

| Pattern | Control Flow | Best For |
|---------|--------------|----------|
| **Sequential** | Linear, predetermined order | Fixed diagnostic procedures |
| **Parallel** | Concurrent, independent execution | Multi-device comparisons |
| **Loop** | Iterative, condition-based | Auto-remediation cycles |
| **Sub-Agent (This)** | Hierarchical, dynamic delegation | Complex workflows requiring orchestration |

**When to Use Sub-Agent Pattern**:
- Need dynamic task routing based on user input
- Different request types require different agent combinations
- Want centralized orchestration logic
- Building agent "teams" with specialized expertise
- Need parent agent to make decisions about workflow progression

**Key Difference**: 
- Sequential/Parallel/Loop workflows are **predetermined and automatic**
- Sub-agent pattern gives parent **dynamic control** over which agents run and when

---