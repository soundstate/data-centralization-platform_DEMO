# LLM Backend - Node.js Express Server

A Node.js Express backend server for interacting with Large Language Models (LLMs) through the Hugging Face API.

## Features

- **Express.js Server**: Lightweight, high-performance server for handling API requests
- **LLM Integration**: Communicate with Hugging Face's free inference models
- **Model Switching**: Change between different available models dynamically
- **Configuration Driven**: Use environment variables for configuration
- **Centralized Logging**: Comprehensive logging for monitoring and troubleshooting

## Setup

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

1. Navigate to the backend directory:
   ```bash
   cd services/llm_integration/llm_backend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create an `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```
   Configure the `.env` file with your desired settings, such as `PORT` and `HUGGING_FACE_TOKEN`.

4. Start the development server:
   ```bash
   npm run dev
   ```

## Configuration

The server uses the following environment variables:

- `PORT`: The port number for the server (default: 3001)
- `HUGGING_FACE_TOKEN`: Optional token for the Hugging Face API

## API Endpoints

- `GET /health` - Health check
- `GET /api/models` - Retrieve available models
- `POST /api/chat` - Send a chat message to the LLM
- `POST /api/switch-model` - Switch the active LLM model

## Development & Testing

### Available Scripts

- `npm start` - Start the server in production mode
- `npm run dev` - Start the server in development mode (with nodemon)

### Project Structure

```
.
├── server.js         # Main server application
├── .env.example      # Sample environment configuration
├── package.json      # Project metadata and scripts
└── node_modules/     # Node.js dependencies
```

## Error Handling

The server handles various error scenarios:

- **Invalid Requests**: Responds with 400 errors for bad requests
- **Model Loading Errors**: 503 errors if a model is unavailable
- **Rate Limiting**: Handles 429 errors gracefully
- **Server Errors**: Responds with 500 errors for unexpected issues

## Troubleshooting

- **Port Conflicts**: Ensure the configured port is not in use
- **Model Issues**: Some models may take time to load due to API limitations
- **Missing Dependencies**: Run `npm install` to fetch any missing packages

## Future Enhancements

- [ ] Add more LLM models from Hugging Face
- [ ] Implement authentication
- [ ] Add monitoring and analytics integration
- [ ] Enhance error logging and alerts
- [ ] Support for additional languages and models

