// Configuration from environment variables (set in .env file or at build time)
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:9000';
const appName = import.meta.env.VITE_APP_NAME || 'basic_agent';
const userId = import.meta.env.VITE_USER_ID || 'autocreate_123';
const sessionId = import.meta.env.VITE_SESSION_ID || 'autocreate_123';

// Log configuration in development
if (import.meta.env.DEV) {
  console.log('API Config:', { API_BASE_URL, appName, userId, sessionId });
}

/**
 * Create or get a session
 */
export async function createOrGetSession() {
  try {
    // Try to get existing session first
    const response = await fetch(
      `${API_BASE_URL}/apps/${appName}/users/${userId}/sessions/${sessionId}`
    );
    
    if (response.ok) {
      return await response.json();
    }
    
    // If session doesn't exist, create it
    if (response.status === 404) {
      const createResponse = await fetch(
        `${API_BASE_URL}/apps/${appName}/users/${userId}/sessions/${sessionId}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({}),
        }
      );
      
      if (createResponse.ok) {
        return await createResponse.json();
      }
      
      // Handle 409 Conflict (session was created by another request - race condition)
      if (createResponse.status === 409) {
        // Session exists now, fetch it
        const retryResponse = await fetch(
          `${API_BASE_URL}/apps/${appName}/users/${userId}/sessions/${sessionId}`
        );
        if (retryResponse.ok) {
          return await retryResponse.json();
        }
        throw new Error(`Failed to get session after conflict: ${retryResponse.statusText}`);
      }
      
      throw new Error(`Failed to create session: ${createResponse.statusText}`);
    }
    
    throw new Error(`Failed to get session: ${response.statusText}`);
  } catch (error) {
    console.error('Error creating/getting session:', error);
    throw error;
  }
}

/**
 * Get session details
 */
export async function getSession() {
  try {
    const response = await fetch(
      `${API_BASE_URL}/apps/${appName}/users/${userId}/sessions/${sessionId}`
    );
    
    if (!response.ok) {
      throw new Error(`Failed to get session: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error getting session:', error);
    throw error;
  }
}

/**
 * Send a message to the agent using SSE streaming
 */
export async function sendMessage(message, onChunk) {
  try {
    const response = await fetch(`${API_BASE_URL}/run_sse`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream',
      },
      body: JSON.stringify({
        appName,
        userId,
        sessionId,
        streaming: true,
        newMessage: {
          role: 'user',
          parts: [
            {
              text: message,
            },
          ],
        },
      }),
    });

    if (!response.ok) {
      throw new Error(`Failed to send message: ${response.statusText}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    let fullResponse = '';

    while (true) {
      const { done, value } = await reader.read();
      
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6));
            
            // Handle direct event format (data.content) - used by ADK server
            if (data.content && data.content.parts) {
              // Extract text from agent responses only (not user messages)
              if (data.author === 'root_agent' || data.author === 'model') {
                // Only process non-partial (final) events to avoid duplicates
                if (!data.partial) {
                  for (const part of data.content.parts) {
                    if (part.text) {
                      fullResponse = part.text; // Use full text from final event
                      if (onChunk) {
                        onChunk(fullResponse);
                      }
                    }
                  }
                }
              }
            }
            
            // Handle wrapped event format (data.event.content) - alternative format
            if (data.event && data.event.content && data.event.content.parts) {
              if (data.event.author === 'root_agent' || data.event.author === 'model') {
                for (const part of data.event.content.parts) {
                  if (part.text) {
                    fullResponse += part.text;
                    if (onChunk) {
                      onChunk(fullResponse);
                    }
                  }
                }
              }
            }
            
            // Check for completion event
            if (data.sessionId) {
              return fullResponse;
            }
          } catch (e) {
            // Skip invalid JSON
            console.warn('Failed to parse SSE data:', e);
          }
        }
      }
    }

    return fullResponse;
  } catch (error) {
    console.error('Error sending message:', error);
    throw error;
  }
}

export { API_BASE_URL, appName, userId, sessionId };

