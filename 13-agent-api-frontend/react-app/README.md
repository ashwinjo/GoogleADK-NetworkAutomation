# Network Assessment Agent - React Frontend

A React-based frontend for the Network Assessment Agent, built with Vite and Tailwind CSS.

## Features

- **Session Management**: Automatically creates and manages sessions with the ADK agent API
- **Real-time Streaming**: Receives agent responses via Server-Sent Events (SSE)
- **Session State Display**: Always visible session variables, user ID, session ID, and app name
- **Simple UI**: Clean, dark-themed interface with black, red, and white color scheme

## Prerequisites

- Node.js 18+ and npm/yarn/pnpm
- ADK API server running on `http://localhost:9000` (or configure via environment variable)

## Setup

1. Install dependencies:
```bash
cd react-app
npm install
```

2. Configure API URL (optional):
Create a `.env` file in the `react-app` directory:
```
VITE_API_URL=http://localhost:9000
```

If not set, it defaults to `http://localhost:9000`.

## Running the Application

1. Start the ADK API server (from the agent directory):
```bash
adk api_server /home/ubuntusand/GoogleADK-NetworkAutomation/1-basic-agent
```

2. Start the React development server:
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## Building for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## Configuration

The app uses the following fixed values:
- **App Name**: `basic_agent`
- **User ID**: `autocreate_123`
- **Session ID**: `autocreate_123`

These can be modified in `src/services/api.js`.

## Project Structure

```
react-app/
├── src/
│   ├── App.jsx          # Main application component
│   ├── main.jsx          # React entry point
│   ├── index.css         # Global styles with Tailwind
│   └── services/
│       └── api.js        # API service functions
├── public/               # Static assets
├── index.html            # HTML template
├── package.json          # Dependencies
├── vite.config.js        # Vite configuration
├── tailwind.config.js     # Tailwind CSS configuration
└── postcss.config.js     # PostCSS configuration
```

## Troubleshooting

### CORS Issues

If you encounter CORS errors, make sure the ADK API server has CORS enabled. Set the `ALLOW_ORIGINS` environment variable:

```bash
export ALLOW_ORIGINS="http://localhost:3000"
```

### Connection Refused

Ensure the ADK API server is running on the configured port (default: 9000).

### Session Not Found

Sessions may be in-memory only. The app will automatically create a new session if one doesn't exist.

