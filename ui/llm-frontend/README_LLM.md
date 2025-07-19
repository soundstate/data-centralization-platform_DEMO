# LLM Frontend - React Chat Interface

A React-based chat interface for interacting with Large Language Models (LLMs) through a Node.js backend.

## Features

- **Real-time Chat Interface**: Clean, responsive chat UI with message history
- **Multiple LLM Support**: Switch between different available models
- **Connection Status**: Visual indicators for backend connectivity
- **Error Handling**: Graceful error handling with user-friendly messages
- **Responsive Design**: Works on desktop and mobile devices
- **Free LLM Integration**: Uses Hugging Face's free inference API

## Setup

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Backend server running (see backend setup instructions)

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd ui/llm-frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Open your browser and navigate to `http://localhost:3000`

## Configuration

The frontend connects to the backend API at `http://localhost:3001` by default. You can configure this by setting the `REACT_APP_API_URL` environment variable:

```bash
# In .env file
REACT_APP_API_URL=http://localhost:3001
```

## Usage

1. **Start a Conversation**: Type your message in the input field and click "Send"
2. **Model Selection**: Use the dropdown to switch between available LLM models
3. **Clear Chat**: Click "Clear Chat" to reset the conversation
4. **Connection Status**: Check the status indicator to ensure backend connectivity

## Available Models

- **microsoft/DialoGPT-medium**: Conversational AI model optimized for chat
- **microsoft/DialoGPT-large**: Larger model with better responses (slower)
- **gpt2**: General-purpose text generation model

## API Endpoints

The frontend communicates with the following backend endpoints:

- `GET /health` - Health check
- `GET /api/models` - Get available models
- `POST /api/chat` - Send chat message
- `POST /api/switch-model` - Switch active model

## Error Handling

The app handles various error scenarios:

- **503 Service Unavailable**: Model is loading
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: General server errors
- **Network Errors**: Backend connectivity issues

## Development

### Available Scripts

- `npm start` - Start development server
- `npm run build` - Build for production
- `npm test` - Run test suite
- `npm run eject` - Eject from Create React App

### Project Structure

```
src/
├── components/
│   ├── Chat.js          # Main chat component
│   └── Chat.css         # Chat component styles
├── App.js               # Main app component
├── App.css              # App styles
└── index.js             # Entry point
```

## Customization

### Styling

The chat interface uses CSS custom properties for easy theming. Key components:

- `.chat-container` - Main chat wrapper
- `.chat-header` - Header with title and status
- `.chat-messages` - Messages container
- `.message` - Individual message styling
- `.chat-input` - Input area styling

### Adding New Models

To add support for new LLM models:

1. Update the backend to include the new model in the `/api/models` endpoint
2. Implement the model switching logic in the backend
3. The frontend will automatically pick up available models

## Troubleshooting

### Common Issues

1. **Backend Not Connected**: Ensure the backend server is running on port 3001
2. **Model Loading**: Some models may take time to load initially
3. **Rate Limits**: Free tier has usage limits; consider getting a Hugging Face token

### Getting Help

- Check the browser console for error messages
- Verify backend server logs
- Ensure all dependencies are properly installed

## Future Enhancements

- [ ] Message persistence (localStorage)
- [ ] File upload support
- [ ] Voice input/output
- [ ] Chat export functionality
- [ ] Dark mode theme
- [ ] Multi-language support
- [ ] Custom model configurations
