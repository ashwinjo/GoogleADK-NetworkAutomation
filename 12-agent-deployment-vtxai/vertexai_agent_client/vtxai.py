import vertexai
from vertexai import agent_engines
from dotenv import load_dotenv
load_dotenv()

PROJECT_ID = 'adkstuff'
deployed_region = 'us-central1'
vertexai.init(project=PROJECT_ID, location=deployed_region)


agents_list = list(agent_engines.list())
if agents_list:
    remote_agent = agents_list[0]  # Get the first (most recent) agent
    client = agent_engines
    print(f"✅ Connected to deployed agent: {remote_agent.resource_name}")
else:
    print("❌ No agents found. Please deploy first.")
    
"""
Output:

✅ Connected to deployed agent: projects/216136305446/locations/us-central1/reasoningEngines/417890284857196544

{
  "model_version": "gemini-3-flash-preview",
  "content": {
    "parts": [
      {
        "text": "As a Senior Network Architect, I am treating your inquiry as a request for a high-level deployment strategy review.\n\n## Design Summary\nA general request for optimal VPN client deployment methodologies across an enterprise.\n\n## Identified Risks\n- **Inconsistency**: Manual deployments lead to configuration drift and security gaps.\n- **Shadow IT**: Unmanaged clients bypass endpoint compliance policies.\n\n## Missing Information\n- Presence of Mobile Device Management (MDM) or Unified Endpoint Management (UEM) tools.\n- Scale of deployment and target Operating Systems.\n\n## Clarifying Questions\n- Is there an existing MDM/UEM for automated provisioning?\n- Are endpoint posture checks and MFA required?\n\n## Suggested Improvements\n- **Automate via MDM/UEM**: Push pre-configured profiles for zero-touch deployment.\n- **Transition to ZTNA**: Consider Zero Trust Network Access to replace traditional VPN clients.\n\n## Overall Assessment\n**Medium Risk** - Deployment without centralized management increases operational overhead and security exposure.",
        "thought_signature": "Cpg6AY89a18dKCEzKlsCugk_jy1CRtJi489-qsbodaM89EemrAsFXk_"
      }
    ],
    "role": "model"
  },
  "finish_reason": "STOP",
  "usage_metadata": {
    "candidates_token_count": 208,
    "candidates_tokens_details": [
      {
        "modality": "TEXT",
        "token_count": 208
      }
    ],
    "prompt_token_count": 489,
    "prompt_tokens_details": [
      {
        "modality": "TEXT",
        "token_count": 489
      }
    ],
    "thoughts_token_count": 1768,
    "total_token_count": 2465,
    "traffic_type": "ON_DEMAND"
  },
  "invocation_id": "e-1d072bb1-a2c4-4ab8-9162-b25eb936c61f",
  "author": "root_agent",
  "actions": {
    "state_delta": {},
    "artifact_delta": {},
    "requested_auth_configs": {},
    "requested_tool_confirmations": {}
  },
  "id": "878b2f13-2025-483d-8ed1-a4d8047bf1de",
  "timestamp": 1767390902.339204
}
"""

async def get_agent_response(message):
    async for item in remote_agent.async_stream_query(
        message=message,
        user_id="user_42",
    ):
        print(item)

import asyncio
if __name__ == "__main__":
    asyncio.run(get_agent_response("What are best ways to deploy VPN clients. Answer in 20 words or less."))