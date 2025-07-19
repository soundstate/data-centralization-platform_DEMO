"""
LLM Chat Backend Server
A FastAPI server that provides chat functionality with various LLM models.
"""

import os
import logging
import asyncio
from datetime import datetime
from typing import List, Dict, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    model: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    timestamp: str
    model: str

class ModelInfo(BaseModel):
    name: str
    description: str
    available: bool = True

class SwitchModelRequest(BaseModel):
    modelName: str

# Global state
current_model = "microsoft/DialoGPT-medium"
available_models = [
    ModelInfo(
        name="microsoft/DialoGPT-medium",
        description="Conversational AI model - Medium size"
    ),
    ModelInfo(
        name="gpt2",
        description="GPT-2 text generation model"
    ),
    ModelInfo(
        name="distilbert-base-uncased",
        description="Lightweight BERT model for understanding"
    ),
    ModelInfo(
        name="openai-gpt",
        description="OpenAI GPT model"
    )
]

# Mock LLM responses (you can replace this with actual model integration)
def generate_mock_response(message: str, model_name: str) -> str:
    """
    Generate a mock response based on the input message and model.
    Replace this with actual LLM integration (OpenAI, Hugging Face, etc.)
    """
    responses = {
        "microsoft/DialoGPT-medium": f"DialoGPT: I understand you said '{message}'. How can I help you further?",
        "gpt2": f"GPT-2: Based on your message about '{message}', here's my generated response...",
        "distilbert-base-uncased": f"DistilBERT: I've analyzed your text '{message}' and here's my understanding...",
        "openai-gpt": f"OpenAI GPT: Thank you for your message '{message}'. Let me provide a helpful response..."
    }
    
    return responses.get(model_name, f"Model {model_name}: Thank you for your message. I'm processing: {message}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("🚀 LLM Chat Backend starting up...")
    logger.info(f"📋 Available models: {[model.name for model in available_models]}")
    logger.info(f"🤖 Current model: {current_model}")
    yield
    logger.info("📴 LLM Chat Backend shutting down...")

# Initialize FastAPI app
app = FastAPI(
    title="LLM Chat Backend",
    description="Backend API for LLM Chat Interface",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "current_model": current_model
    }

@app.get("/api/models")
async def get_available_models():
    """Get list of available models"""
    return {
        "available_models": [model.dict() for model in available_models],
        "current_model": current_model
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Handle chat messages"""
    try:
        # Use the specified model or fall back to current model
        model_to_use = request.model or current_model
        
        logger.info(f"💬 Processing chat message with model: {model_to_use}")
        logger.info(f"📝 Message: {request.message[:100]}...")  # Log first 100 chars
        
        # Simulate processing time (remove in production)
        await asyncio.sleep(0.5)
        
        # Generate response (replace with actual LLM integration)
        response_text = generate_mock_response(request.message, model_to_use)
        
        response = ChatResponse(
            response=response_text,
            timestamp=datetime.now().isoformat(),
            model=model_to_use
        )
        
        logger.info(f"✅ Generated response successfully")
        return response
        
    except Exception as e:
        logger.error(f"❌ Error processing chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.post("/api/switch-model")
async def switch_model(request: SwitchModelRequest):
    """Switch the current active model"""
    global current_model
    
    # Validate that the model exists
    model_names = [model.name for model in available_models]
    if request.modelName not in model_names:
        raise HTTPException(
            status_code=400, 
            detail=f"Model '{request.modelName}' not found. Available models: {model_names}"
        )
    
    old_model = current_model
    current_model = request.modelName
    
    logger.info(f"🔄 Model switched from '{old_model}' to '{current_model}'")
    
    return {
        "success": True,
        "previous_model": old_model,
        "current_model": current_model,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "LLM Chat Backend API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "health_check": "/health",
        "models_endpoint": "/api/models",
        "chat_endpoint": "/api/chat",
        "switch_model_endpoint": "/api/switch-model"
    }

if __name__ == "__main__":
    # Run the server
    port = int(os.getenv("PORT", 3001))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"🌐 Starting server on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=False,  # Disable auto-reload to prevent shutdown issues
        log_level="info"
    )
