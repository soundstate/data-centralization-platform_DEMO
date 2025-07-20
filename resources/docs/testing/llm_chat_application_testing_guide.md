# LLM Chat Application - Testing Guide

This guide will help you test the complete LLM chat application (React frontend + Node.js backend).

## Prerequisites

- Node.js installed
- Both frontend and backend dependencies installed
- Two terminal windows available

## Step-by-Step Testing Instructions

### 1. Start the Backend Server

Open **Terminal 1** and run:

```bash
# Navigate to backend directory
cd services/llm_integration/llm_backend

# Start the backend server
npm run dev
```

**Expected Output:**
```
LLM Backend server running on port 3001
Health check: http://localhost:3001/health
Chat endpoint: http://localhost:3001/api/chat
```

**Alternative:** Double-click `start-backend.bat` in the backend folder.

### 2. Test Backend API (Optional)

You can test the backend directly using your browser or a tool like Postman:

**Health Check:**
- Open browser to: `http://localhost:3001/health`
- Expected response: `{"status":"ok","message":"LLM Backend is running"}`

**Available Models:**
- Open browser to: `http://localhost:3001/api/models`
- Expected response: List of available LLM models

### 3. Start the Frontend Application

Open **Terminal 2** and run:

```bash
# Navigate to frontend directory
cd ui/llm-frontend

# Start the React application
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view llm-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

**Alternative:** Double-click `start-frontend.bat` in the frontend folder.

### 4. Test the Chat Interface

1. **Open your browser** to `http://localhost:3000`

2. **Check Connection Status:**
   - Look for a green dot with "Connected" status in the header
   - If you see a red dot with "Disconnected", the backend isn't running

3. **Test Basic Chat:**
   - Type a simple message like "Hello, how are you?"
   - Click "Send" or press Enter
   - Wait for the LLM response (may take 5-10 seconds initially)

4. **Test Model Information:**
   - Check the model dropdown shows available models
   - Verify the current model is displayed

5. **Test Error Handling:**
   - Try sending an empty message (should be disabled)
   - Stop the backend server and try sending a message (should show error)

## Expected Behavior

### Successful Chat Flow:
1. **User sends message** → Message appears on right side with blue background
2. **Loading indicator** → Shows "typing..." with animated dots
3. **LLM response** → Appears on left side with white background
4. **Model info** → Shows which model generated the response

### Common LLM Responses:
- The DialoGPT model is designed for conversation
- Initial responses might be slower (model cold start)
- Responses should be conversational and relevant to your input

## Troubleshooting

### Backend Issues:
- **Port 3001 in use:** Change `PORT` in `.env` file
- **Module not found:** Run `npm install` in backend directory
- **Server won't start:** Check console for error messages

### Frontend Issues:
- **Port 3000 in use:** React will offer to use a different port
- **Backend connection failed:** Ensure backend is running on port 3001
- **Module not found:** Run `npm install` in frontend directory

### LLM API Issues:
- **503 Error:** Model is loading, wait and try again
- **429 Error:** Rate limit exceeded, wait a minute
- **Slow responses:** Free tier models may have delays

## Testing Scenarios

### Basic Functionality:
- [ ] Backend starts without errors
- [ ] Frontend connects to backend
- [ ] Health check returns OK
- [ ] Models endpoint returns list
- [ ] Chat sends and receives messages
- [ ] Clear chat button works

### Error Handling:
- [ ] Empty message handling
- [ ] Backend disconnection handling
- [ ] LLM API error handling
- [ ] Network error handling

### UI/UX:
- [ ] Messages display correctly
- [ ] Timestamps are accurate
- [ ] Loading states work
- [ ] Mobile responsive design
- [ ] Model selector functions

## Sample Conversation

Try this conversation to test the LLM:

```
You: Hello! What can you help me with?
LLM: [Should respond with a greeting and offer assistance]

You: Tell me a joke
LLM: [Should provide a humorous response]

You: What's the weather like?
LLM: [May give a general response about weather or ask for location]
```

## Performance Notes

- **First message** may take 10-20 seconds (model loading)
- **Subsequent messages** should be faster (2-5 seconds)
- **Rate limits** apply to free tier usage
- **Model quality** varies between DialoGPT-medium/large and GPT-2

## Next Steps

After successful testing, you can:
1. Get a Hugging Face API token for higher rate limits
2. Implement complete model switching functionality
3. Add conversation persistence
4. Enhance the UI with additional features
5. Deploy to production environment

---

**Need Help?** Check the console logs in both terminal windows for detailed error messages.
