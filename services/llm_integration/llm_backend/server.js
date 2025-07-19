const express = require('express');
const cors = require('cors');
const axios = require('axios');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3001;

// middleware
app.use(cors());
app.use(express.json());

// hugging face api configuration
const HUGGING_FACE_API_URL = 'https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium';
const HUGGING_FACE_TOKEN = process.env.HUGGING_FACE_TOKEN || ''; // optional token for higher rate limits

// health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok', message: 'LLM Backend is running' });
});

// llm chat endpoint
app.post('/api/chat', async (req, res) => {
  try {
    const { message } = req.body;
    
    if (!message) {
      return res.status(400).json({ error: 'Message is required' });
    }

    // prepare request headers
    const headers = {
      'Content-Type': 'application/json',
    };
    
    // add authorization header if token is provided
    if (HUGGING_FACE_TOKEN) {
      headers['Authorization'] = `Bearer ${HUGGING_FACE_TOKEN}`;
    }

    // make request to hugging face api
    const response = await axios.post(
      HUGGING_FACE_API_URL,
      {
        inputs: message,
        parameters: {
          max_length: 150,
          temperature: 0.7,
          do_sample: true,
          top_p: 0.9,
          return_full_text: false
        }
      },
      { headers }
    );

    // extract response text
    let responseText = 'Sorry, I could not generate a response.';
    
    if (response.data && Array.isArray(response.data) && response.data.length > 0) {
      responseText = response.data[0].generated_text || responseText;
    }

    res.json({
      response: responseText,
      model: 'microsoft/DialoGPT-medium',
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    console.error('Error calling LLM API:', error.response?.data || error.message);
    
    // handle specific error cases
    if (error.response?.status === 503) {
      return res.status(503).json({
        error: 'Model is currently loading. Please try again in a few moments.',
        retryAfter: 20
      });
    }
    
    if (error.response?.status === 429) {
      return res.status(429).json({
        error: 'Rate limit exceeded. Please try again later.',
        retryAfter: 60
      });
    }

    res.status(500).json({
      error: 'Failed to get response from LLM',
      details: error.message
    });
  }
});

// alternative models endpoint for experimentation
app.get('/api/models', (req, res) => {
  res.json({
    available_models: [
      {
        name: 'microsoft/DialoGPT-medium',
        description: 'Conversational AI model for chat applications',
        type: 'text-generation',
        free: true
      },
      {
        name: 'microsoft/DialoGPT-large',
        description: 'Larger conversational AI model (may be slower)',
        type: 'text-generation',
        free: true
      },
      {
        name: 'gpt2',
        description: 'GPT-2 model for general text generation',
        type: 'text-generation',
        free: true
      }
    ]
  });
});

// switch model endpoint
app.post('/api/switch-model', (req, res) => {
  const { modelName } = req.body;
  
  const validModels = [
    'microsoft/DialoGPT-medium',
    'microsoft/DialoGPT-large',
    'gpt2'
  ];
  
  if (!validModels.includes(modelName)) {
    return res.status(400).json({ error: 'Invalid model name' });
  }
  
  // in a real implementation, you would update the model URL
  // for now, we'll just return success
  res.json({ 
    message: `Model switched to ${modelName}`,
    current_model: modelName 
  });
});

app.listen(PORT, () => {
  console.log(`LLM Backend server running on port ${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/health`);
  console.log(`Chat endpoint: http://localhost:${PORT}/api/chat`);
});
