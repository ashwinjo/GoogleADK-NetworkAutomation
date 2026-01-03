import { useState, useEffect } from 'react';
import { createOrGetSession, getSession, sendMessage, appName, userId, sessionId } from './services/api';

function App() {
  const [session, setSession] = useState(null);
  const [sessionState, setSessionState] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [userInput, setUserInput] = useState('');
  const [agentResponse, setAgentResponse] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);

  // Initialize session on mount
  useEffect(() => {
    initializeSession();
  }, []);

  const initializeSession = async () => {
    try {
      setLoading(true);
      const sessionData = await createOrGetSession();
      setSession(sessionData);
      setSessionState(sessionData.state || {});
    } catch (err) {
      setError(`Failed to initialize session: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const refreshSession = async () => {
    try {
      const sessionData = await getSession();
      setSession(sessionData);
      setSessionState(sessionData.state || {});
    } catch (err) {
      console.error('Failed to refresh session:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!userInput.trim() || isStreaming) return;

    setError(null);
    setAgentResponse('');
    setIsStreaming(true);

    try {
      await sendMessage(userInput, (chunk) => {
        setAgentResponse(chunk);
      });

      // Refresh session after message to get updated state
      await refreshSession();
      setUserInput('');
    } catch (err) {
      setError(`Failed to send message: ${err.message}`);
    } finally {
      setIsStreaming(false);
    }
  };

  return (
    <div className="min-h-screen bg-dark-bg text-white">
      {/* Header */}
      <header className="bg-dark-panel border-b border-red-600">
        <div className="container mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-red-500">Network Assessment Agent</h1>
        </div>
      </header>

      <div className="container mx-auto px-4 py-6 max-w-6xl">
        {/* Session Info Panel */}
        <div className="bg-dark-panel border border-red-600 rounded-lg p-4 mb-6">
          <h2 className="text-lg font-semibold text-red-500 mb-4">Session Information</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div>
              <span className="text-gray-400 text-sm">App Name:</span>
              <p className="text-white font-mono">{appName}</p>
            </div>
            <div>
              <span className="text-gray-400 text-sm">User ID:</span>
              <p className="text-white font-mono">{userId}</p>
            </div>
            <div>
              <span className="text-gray-400 text-sm">Session ID:</span>
              <p className="text-white font-mono">{sessionId}</p>
            </div>
          </div>

          {/* Session State */}
          <div className="mt-4">
            <span className="text-gray-400 text-sm">Session Variables:</span>
            <div className="mt-2 bg-black rounded p-3 border border-gray-700">
              {Object.keys(sessionState).length === 0 ? (
                <p className="text-gray-500 text-sm italic">No session variables set</p>
              ) : (
                <pre className="text-white text-sm font-mono overflow-x-auto">
                  {JSON.stringify(sessionState, null, 2)}
                </pre>
              )}
            </div>
          </div>
        </div>

        {/* Search Bar */}
        <div className="mb-6">
          <form onSubmit={handleSubmit} className="flex gap-2">
            <input
              type="text"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              placeholder="Enter your use case or question..."
              className="flex-1 bg-dark-panel border border-red-600 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent"
              disabled={isStreaming || loading}
            />
            <button
              type="submit"
              disabled={!userInput.trim() || isStreaming || loading}
              className="bg-red-600 hover:bg-red-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white font-semibold px-6 py-3 rounded-lg transition-colors"
            >
              {isStreaming ? 'Sending...' : 'Send'}
            </button>
          </form>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-900 border border-red-600 rounded-lg p-4 mb-6">
            <p className="text-red-200">{error}</p>
          </div>
        )}

        {/* Agent Response */}
        {agentResponse && (
          <div className="bg-dark-panel border border-red-600 rounded-lg p-6">
            <h2 className="text-lg font-semibold text-red-500 mb-4">Agent Response</h2>
            <div className="prose prose-invert max-w-none">
              <div className="text-white whitespace-pre-wrap">
                {agentResponse}
              </div>
            </div>
            {isStreaming && (
              <div className="mt-2 text-red-400 text-sm">Streaming...</div>
            )}
          </div>
        )}

        {/* Loading State */}
        {loading && !session && (
          <div className="text-center py-8">
            <p className="text-gray-400">Initializing session...</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;

