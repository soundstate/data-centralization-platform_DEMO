#!/usr/bin/env python3
"""
MusicBrainz OAuth Authentication Service

This FastAPI service handles the OAuth 2.0 authentication flow for MusicBrainz.
It provides endpoints for initiating authentication, handling callbacks,
and managing access tokens.

Features:
- OAuth 2.0 authorization code flow
- State parameter validation for CSRF protection
- Token storage and retrieval
- Automatic token refresh
- Session management using Redis
- CORS support for local development

Endpoints:
- GET /auth/musicbrainz/login - Initiate OAuth flow
- GET /auth/musicbrainz/callback - Handle OAuth callback
- POST /auth/musicbrainz/refresh - Refresh expired tokens
- GET /auth/musicbrainz/status - Check authentication status
- GET /health - Health check endpoint

Usage:
    python main.py
    
    Then visit http://localhost:8000/auth/musicbrainz/login to start OAuth flow
"""

import asyncio
import json
import os
import sys
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional

import redis.asyncio as redis
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel

# Add the shared_core package to the path
current_dir = Path(__file__).parent
shared_core_path = current_dir.parent.parent.parent / "packages" / "shared_core"
sys.path.insert(0, str(shared_core_path))

from shared_core.auth.musicbrainz_oauth import MusicBrainzOAuth, MusicBrainzOAuthError
from shared_core.config.musicbrainz_config import MusicBrainzConfig
from shared_core.logging.centralized_logger import CentralizedLogger

# Initialize logger
logger = CentralizedLogger.get_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="MusicBrainz OAuth Service",
    description="OAuth 2.0 authentication service for MusicBrainz API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
oauth_client: Optional[MusicBrainzOAuth] = None
redis_client: Optional[redis.Redis] = None


# Pydantic models for request/response
class TokenRefreshRequest(BaseModel):
    refresh_token: str


class AuthStatusResponse(BaseModel):
    authenticated: bool
    expires_at: Optional[datetime] = None
    scopes: Optional[str] = None
    user_id: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: int
    token_type: str = "Bearer"
    scope: str = ""


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    global oauth_client, redis_client
    
    logger.info("Starting MusicBrainz OAuth service...")
    
    try:
        # Initialize OAuth client
        oauth_client = MusicBrainzOAuth()
        logger.info("OAuth client initialized successfully")
        
        # Initialize Redis client for session storage
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        redis_client = redis.from_url(redis_url)
        
        # Test Redis connection
        await redis_client.ping()
        logger.info("Redis connection established successfully")
        
        # Log configuration
        oauth_config = MusicBrainzConfig.get_oauth_config()
        logger.info(f"OAuth configuration: {oauth_config}")
        
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    global oauth_client, redis_client
    
    logger.info("Shutting down MusicBrainz OAuth service...")
    
    if oauth_client:
        await oauth_client.close()
    
    if redis_client:
        await redis_client.close()


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "service": "musicbrainz-oauth"
    }


@app.get("/auth/musicbrainz/login")
async def login():
    """
    Initiate MusicBrainz OAuth flow.
    
    Generates authorization URL and redirects user to MusicBrainz for authentication.
    """
    try:
        # Generate session ID for this OAuth flow
        session_id = str(uuid.uuid4())
        
        # Generate authorization URL with state parameter
        auth_url, state = oauth_client.get_authorization_url()
        
        # Store state in Redis with expiration (10 minutes)
        session_data = {
            "state": state,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "session_id": session_id
        }
        
        await redis_client.setex(
            f"oauth_state:{state}",
            600,  # 10 minutes
            json.dumps(session_data)
        )
        
        logger.info(f"OAuth flow initiated for session: {session_id}")
        logger.debug(f"Generated state parameter: {state}")
        
        # Return redirect response to MusicBrainz
        return RedirectResponse(url=auth_url)
        
    except MusicBrainzOAuthError as e:
        logger.error(f"OAuth error during login: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during login: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/auth/musicbrainz/callback")
async def callback(code: Optional[str] = None, state: Optional[str] = None, error: Optional[str] = None):
    """
    Handle OAuth callback from MusicBrainz.
    
    Args:
        code: Authorization code from MusicBrainz
        state: State parameter for CSRF protection
        error: Error code if authorization failed
    """
    try:
        # Check for authorization errors
        if error:
            logger.error(f"OAuth authorization error: {error}")
            return JSONResponse(
                status_code=400,
                content={"error": "authorization_failed", "description": error}
            )
        
        # Validate required parameters
        if not code or not state:
            logger.error("Missing required parameters in OAuth callback")
            raise HTTPException(
                status_code=400,
                detail="Missing authorization code or state parameter"
            )
        
        # Retrieve and validate state from Redis
        session_data_json = await redis_client.get(f"oauth_state:{state}")
        if not session_data_json:
            logger.error("Invalid or expired state parameter")
            raise HTTPException(
                status_code=400,
                detail="Invalid or expired state parameter"
            )
        
        session_data = json.loads(session_data_json)
        expected_state = session_data["state"]
        session_id = session_data["session_id"]
        
        logger.info(f"Processing OAuth callback for session: {session_id}")
        
        # Exchange authorization code for access token
        token_info = await oauth_client.exchange_code_for_token(
            authorization_code=code,
            state=state,
            expected_state=expected_state
        )
        
        # Store token information in Redis (expires when token expires)
        token_data = {
            **token_info,
            "session_id": session_id,
            "expires_at": token_info["expires_at"].isoformat() + "Z"
        }
        
        # Store token with session ID as key
        await redis_client.setex(
            f"token:{session_id}",
            token_info["expires_in"],
            json.dumps(token_data, default=str)
        )
        
        # Clean up state data
        await redis_client.delete(f"oauth_state:{state}")
        
        logger.info(f"OAuth flow completed successfully for session: {session_id}")
        
        # Return token information
        return JSONResponse(
            content={
                "message": "Authentication successful",
                "session_id": session_id,
                "token": TokenResponse(
                    access_token=token_info["access_token"],
                    refresh_token=token_info.get("refresh_token"),
                    expires_in=token_info["expires_in"],
                    token_type=token_info["token_type"],
                    scope=token_info["scope"]
                ).dict(),
                "expires_at": token_info["expires_at"].isoformat() + "Z"
            }
        )
        
    except MusicBrainzOAuthError as e:
        logger.error(f"OAuth error during callback: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during callback: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/auth/musicbrainz/refresh")
async def refresh_token(request: TokenRefreshRequest):
    """
    Refresh an expired access token.
    
    Args:
        request: Token refresh request containing refresh token
    """
    try:
        # Refresh the token
        new_token_info = await oauth_client.refresh_access_token(request.refresh_token)
        
        logger.info("Token refreshed successfully")
        
        return TokenResponse(
            access_token=new_token_info["access_token"],
            refresh_token=new_token_info.get("refresh_token"),
            expires_in=new_token_info["expires_in"],
            token_type=new_token_info["token_type"],
            scope=new_token_info["scope"]
        )
        
    except MusicBrainzOAuthError as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during token refresh: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/auth/musicbrainz/status/{session_id}")
async def get_auth_status(session_id: str) -> AuthStatusResponse:
    """
    Check authentication status for a session.
    
    Args:
        session_id: Session ID from OAuth flow
    """
    try:
        # Retrieve token data from Redis
        token_data_json = await redis_client.get(f"token:{session_id}")
        
        if not token_data_json:
            return AuthStatusResponse(authenticated=False)
        
        token_data = json.loads(token_data_json)
        
        # Parse expiration time
        expires_at = datetime.fromisoformat(token_data["expires_at"].replace("Z", "+00:00"))
        
        # Check if token is still valid
        if datetime.utcnow() > expires_at.replace(tzinfo=None):
            # Token expired, remove from storage
            await redis_client.delete(f"token:{session_id}")
            return AuthStatusResponse(authenticated=False)
        
        return AuthStatusResponse(
            authenticated=True,
            expires_at=expires_at.replace(tzinfo=None),
            scopes=token_data.get("scope", ""),
            user_id=session_id
        )
        
    except Exception as e:
        logger.error(f"Error checking auth status: {e}")
        return AuthStatusResponse(authenticated=False)


@app.get("/auth/musicbrainz/token/{session_id}")
async def get_token(session_id: str):
    """
    Retrieve stored access token for a session.
    
    Args:
        session_id: Session ID from OAuth flow
    """
    try:
        # Retrieve token data from Redis
        token_data_json = await redis_client.get(f"token:{session_id}")
        
        if not token_data_json:
            raise HTTPException(status_code=404, detail="Token not found or expired")
        
        token_data = json.loads(token_data_json)
        
        # Parse expiration time
        expires_at = datetime.fromisoformat(token_data["expires_at"].replace("Z", "+00:00"))
        
        # Check if token is still valid
        if datetime.utcnow() > expires_at.replace(tzinfo=None):
            # Token expired, remove from storage
            await redis_client.delete(f"token:{session_id}")
            raise HTTPException(status_code=401, detail="Token expired")
        
        return {
            "access_token": token_data["access_token"],
            "token_type": token_data.get("token_type", "Bearer"),
            "expires_at": token_data["expires_at"],
            "scope": token_data.get("scope", "")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving token: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.delete("/auth/musicbrainz/logout/{session_id}")
async def logout(session_id: str):
    """
    Logout and remove stored tokens.
    
    Args:
        session_id: Session ID to logout
    """
    try:
        # Remove token from Redis
        result = await redis_client.delete(f"token:{session_id}")
        
        if result:
            logger.info(f"Successfully logged out session: {session_id}")
            return {"message": "Logged out successfully"}
        else:
            return {"message": "No active session found"}
            
    except Exception as e:
        logger.error(f"Error during logout: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Development helper endpoints
@app.get("/auth/musicbrainz/config")
async def get_oauth_config():
    """Get OAuth configuration (for debugging)."""
    config = MusicBrainzConfig.get_oauth_config()
    # Remove sensitive information
    config.pop("client_secret", None)
    return config


if __name__ == "__main__":
    import uvicorn
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    # Start the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
