# 5-agent-callbacks-guardrails

A base ReAct agent built with Google's Agent Development Kit (ADK)
Agent generated with [`googleCloudPlatform/agent-starter-pack`](https://github.com/GoogleCloudPlatform/agent-starter-pack) version `0.29.3`

---

## Network Use Case

**Production-Grade Security and Control System** - Demonstrates callback-based guardrails for enforcing security policies, access controls, and content validation in network operations. These patterns are essential for production environments where agents must comply with security policies, regulations, and operational constraints.

### Real-World Scenarios

**1. Pre-Execution Validation (Agent Callbacks)**
- **Scenario**: Block operations on offline routers
- **Problem**: Agent attempts to configure a router that's currently down
- **Solution**: Before-agent callback checks router health status
- **Result**: Operation blocked with clear message: "Router r1-sea3 is down"

**2. Sensitive Data Detection (Model Callbacks)**  
- **Scenario**: Prevent plaintext password exposure
- **Problem**: User requests contain passwords or responses leak credentials
- **Solution**: Before-model callback scans user input for keywords like "password"
- **Solution**: After-model callback detects unencrypted passwords (e.g., "PassWord")
- **Result**: Request/response blocked with policy violation message

**3. Access Control & Data Masking (Tool Callbacks)**
- **Scenario**: Restrict access to government cloud routers and mask passwords
- **Problem**: User attempts to access restricted router "r1-gov51"
- **Problem**: Tool returns configurations with plaintext passwords
- **Solution**: Before-tool callback blocks access to specific routers
- **Solution**: After-tool callback masks passwords ("PassWord" → "******")
- **Result**: Compliance enforcement + sensitive data protection

### Production Value

- **Compliance**: Enforce security policies without modifying agent logic
- **Auditability**: All callback decisions logged with context
- **Separation of Concerns**: Security logic separated from business logic
- **Zero-Touch Enforcement**: Guardrails activate automatically
- **Fail-Safe Design**: Operations blocked by default when policies violated

## ADK Features Demonstrated

This project showcases three callback interception points for implementing guardrails:

### 1. Agent-Level Callbacks (`before_after_agent_callback/`)

**Intercept Agent Execution Before/After Entire Run**

**Before Agent Callback** - `before_agent_callback`:
- **Trigger Point**: Before agent begins processing user message
- **Access**: Full session history, conversation events, state
- **Capabilities**:
  - Extract router name from user message using regex patterns
  - Check router health status (simulate up/down check)
  - Store extracted context in session state
  - **Override Execution**: Return `types.Content` to skip agent run entirely
- **Use Cases**: 
  - Pre-flight validation (router reachability, maintenance windows)
  - Context enrichment before agent execution
  - Request sanitization and normalization
  - Authorization checks

**After Agent Callback** - `after_agent_callback`:
- **Trigger Point**: After agent completes processing
- **Access**: Agent response, session state, conversation history
- **Capabilities**:
  - Validate agent response meets policy requirements
  - Add post-processing annotations
  - Log outcomes for audit trails
  - **Override Response**: Return modified `types.Content`
- **Use Cases**:
  - Response validation and augmentation
  - Success/failure notifications
  - Audit logging with context
  - Post-execution cleanup

**Key Code Pattern**:
```python
def check_router_health(callback_context: CallbackContext) -> Optional[types.Content]:
    router_name = extract_router_name(last_user_message)
    callback_context.state['router_name'] = router_name
    
    if router_status == 'down':
        return types.Content(
            parts=[types.Part(text=f"Router {router_name} is down")],
            role="model"
        )
    return None  # Proceed with agent execution

root_agent = Agent(
    before_agent_callback=check_router_health,
    after_agent_callback=validate_response,
    ...
)
```

### 2. Model-Level Callbacks (`before_after_model_callback/`)

**Intercept LLM Requests/Responses Before API Calls**

**Before Model Callback** - `before_model_callback`:
- **Trigger Point**: Before sending request to LLM API (Gemini)
- **Access**: `LlmRequest` object with full conversation context
- **Capabilities**:
  - Scan user input for sensitive keywords ("password", credentials)
  - Validate message content against policies
  - Block API call to save costs and enforce security
  - **Skip LLM Call**: Return `LlmResponse` to bypass model entirely
- **Use Cases**:
  - Content filtering (profanity, sensitive data)
  - Policy enforcement (forbidden operations)
  - Cost optimization (block invalid requests before API call)
  - Input validation and sanitization

**After Model Callback** - `after_model_callback`:
- **Trigger Point**: After receiving response from LLM API
- **Access**: `LlmResponse` object with model's generated content
- **Capabilities**:
  - Scan model output for policy violations
  - Detect unencrypted passwords, tokens, or credentials
  - Validate response quality and safety
  - **Replace Response**: Return modified `LlmResponse`
- **Use Cases**:
  - Output filtering (remove sensitive data)
  - Compliance validation (ensure responses meet standards)
  - Data loss prevention (DLP)
  - Response quality checks

**Key Code Pattern**:
```python
def check_sensitive_content_request(callback_context: CallbackContext,
                                    llm_request: LlmRequest) -> Optional[LlmResponse]:
    if "password" in last_user_message.lower():
        callback_context.state["password_found"] = True
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[types.Part(text="Password in plaintext violates policy")]
            )
        )
    return None  # Proceed with LLM call

def check_sensitive_content_response(callback_context: CallbackContext,
                                     llm_response: LlmResponse) -> Optional[LlmResponse]:
    if "PassWord" in response_text:
        return LlmResponse(  # Replace response
            content=types.Content(
                role="model",
                parts=[types.Part(text="Config violates encryption policy")]
            )
        )
    return None  # Use original response

root_agent = Agent(
    before_model_callback=check_sensitive_content_request,
    after_model_callback=check_sensitive_content_response,
    ...
)
```

### 3. Tool-Level Callbacks (`before_after_tool_callback/`)

**Intercept Individual Tool Executions**

**Before Tool Callback** - `before_tool_callback`:
- **Trigger Point**: Before executing a tool function
- **Access**: Tool object, arguments dict, ToolContext
- **Capabilities**:
  - Inspect tool name and arguments
  - Enforce access controls (e.g., block router "r1-gov51")
  - Modify tool arguments dynamically
  - **Skip Tool Execution**: Return dict to bypass tool entirely
- **Use Cases**:
  - Access control enforcement (restricted resources)
  - Argument validation and sanitization
  - Rate limiting and throttling
  - Cost controls (prevent expensive operations)

**After Tool Callback** - `after_tool_callback`:
- **Trigger Point**: After tool returns result
- **Access**: Tool object, arguments, ToolContext, tool response
- **Capabilities**:
  - Inspect and modify tool output
  - Mask sensitive data (passwords, tokens)
  - Validate response format and content
  - **Override Response**: Return modified dict
- **Use Cases**:
  - Data masking and redaction
  - Response normalization
  - Security content filtering
  - Result validation and enrichment

**Key Code Pattern**:
```python
def before_tool_access_control(tool: BaseTool,
                               args: Dict[str, Any],
                               tool_context: ToolContext) -> Optional[Dict]:
    if tool.name == "read_router_config" and args.get("router_name") == "r1-gov51":
        return {"result": "Access to government cloud router restricted"}
    return None  # Proceed with tool execution

def after_tool_mask_passwords(tool: BaseTool,
                              args: Dict[str, Any],
                              tool_context: ToolContext,
                              tool_response: Dict) -> Optional[Dict]:
    if "PassWord" in tool_response.get("config", ""):
        tool_response["config"] = tool_response["config"].replace("PassWord", "******")
        return tool_response
    return None  # Use original response

root_agent = Agent(
    tools=[read_router_config],
    before_tool_callback=before_tool_access_control,
    after_tool_callback=after_tool_mask_passwords,
    ...
)
```

### 4. Callback Context & State Management

**CallbackContext Object**:
- **`callback_context.state`**: Read/write session state
- **`callback_context._invocation_context.session`**: Access full session (events, history)
- **State Persistence**: Data stored in callbacks persists across agent turns

**Use Cases**:
- Store extracted entities (router names, error codes)
- Track validation decisions across callbacks
- Build audit trails with context
- Share data between before/after callbacks

---

## Callback Execution Order

Understanding when each callback fires:

```
User Message Received
    ↓
[before_agent_callback] ← Can skip entire agent execution
    ↓
Agent Planning Phase
    ↓
[before_model_callback] ← Can skip LLM API call
    ↓
LLM API Call (if not skipped)
    ↓
[after_model_callback] ← Can modify LLM response
    ↓
Agent decides to call tool
    ↓
[before_tool_callback] ← Can skip tool execution or modify args
    ↓
Tool Execution (if not skipped)
    ↓
[after_tool_callback] ← Can modify tool response
    ↓
Agent continues loop or finalizes response
    ↓
[after_agent_callback] ← Can modify final agent response
    ↓
Response Returned to User
```

---

## Callback Selection Guide

| Callback Type | When to Use | Granularity | Performance Impact |
|---------------|-------------|-------------|-------------------|
| **Agent** | Request validation, authorization, response augmentation | Coarse (entire agent run) | Low |
| **Model** | Content filtering, policy enforcement, cost optimization | Medium (per LLM call) | Medium |
| **Tool** | Access control, data masking, resource-level security | Fine (per tool call) | Low-Medium |

**Best Practices**:
- Use **Agent callbacks** for high-level validation and authorization
- Use **Model callbacks** for content policy enforcement
- Use **Tool callbacks** for resource-level access control and data protection
- Combine multiple callback types for defense-in-depth security