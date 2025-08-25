"""
Spotify OAuth 2.0 Client

This module provides OAuth 2.0 authentication capabilities for the Spotify Web API.
It handles the complete OAuth flow including authorization URL generation,
token exchange, and token refresh operations.

Features:
- Authorization URL generation with state parameter for security
- Authorization code exchange for access tokens
- Automatic token refresh capabilities
- Comprehensive error handling and logging
- Integration with the project's configuration patterns

Usage:
    from shared_core.auth import SpotifyOAuth
    from shared_core.config.spotify_config import SpotifyConfig
    
    # Initialize OAuth client
    oauth_client = SpotifyOAuth()
    
    # Generate authorization URL
    auth_url, state = oauth_client.get_authorization_url()
    print(f"Visit: {auth_url}")
    
    # After user authorization, exchange code for token
    token_data = await oauth_client.exchange_code_for_token(
        authorization_code, 
        state
    )
"""

import asyncio
import base64
import secrets
import urllib.parse
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple

import aiohttp

from ..config.spotify_config import SpotifyConfig
from ..utils.centralized_logging import CentralizedLogger


class SpotifyOAuthError(Exception):
    """Custom exception for Spotify OAuth errors."""
    pass


class SpotifyOAuth:
    """
    Spotify OAuth 2.0 Client
    
    Handles the complete OAuth 2.0 authorization code flow for Spotify Web API access.
    Provides secure token management with automatic refresh capabilities.
    """
    
    # Spotify OAuth endpoints
    OAUTH_AUTHORIZE_URL = "https://accounts.spotify.com/authorize"
    OAUTH_TOKEN_URL = "https://accounts.spotify.com/api/token"
    
    # Default OAuth scopes for data collection and analysis
    OAUTH_DEFAULT_SCOPES = [
        "user-read-private",
        "user-read-email", 
        "user-library-read",
        "user-top-read",
        "user-read-recently-played",
        "playlist-read-private",
        "user-read-playback-state",
        "user-read-currently-playing"
    ]
    
    def __init__(self, timeout: int = 30):
        """
        Initialize Spotify OAuth client.
        
        Args:
            timeout: HTTP request timeout in seconds (default: 30)
        """
        self.logger = CentralizedLogger.get_logger(__name__)
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session = None
        
        # Validate OAuth configuration on initialization
        try:
            self.config = SpotifyConfig()
            if not SpotifyConfig.validate_credentials():
                self.logger.warning("Spotify OAuth configuration validation failed - some operations may not work")
        except Exception as e:
            self.logger.error(f"Failed to initialize Spotify OAuth configuration: {e}")
            raise SpotifyOAuthError(f"Configuration error: {e}")
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """
        Get or create aiohttp session.
        
        Returns:
            Configured aiohttp ClientSession
        """
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                timeout=self.timeout,
                headers={"User-Agent": "DataCentralization/spotify"}
            )
        return self.session
    
    async def close(self) -> None:
        """Close the aiohttp session."""
        if self.session and not self.session.closed:
            await self.session.close()
            self.session = None
    
    def generate_state_parameter(self) -> str:
        """
        Generate a secure random state parameter for OAuth flow.
        
        Returns:
            Cryptographically secure random state string
        """
        return secrets.token_urlsafe(32)
    
    def get_authorization_url(
        self, 
        scopes: Optional[list] = None,
        state: Optional[str] = None,
        show_dialog: bool = True
    ) -> Tuple[str, str]:
        """
        Generate Spotify OAuth authorization URL.
        
        Args:
            scopes: List of OAuth scopes to request (default: standard data collection scopes)
            state: Custom state parameter (will generate secure one if not provided)
            show_dialog: Whether to always show the authorization dialog
            
        Returns:
            Tuple of (authorization_url, state_parameter)
            
        Raises:
            SpotifyOAuthError: If configuration is invalid
        """
        try:
            client_id = SpotifyConfig.client_id()
            redirect_uri = SpotifyConfig.redirect_uri()
            
            if scopes is None:
                scopes = self.OAUTH_DEFAULT_SCOPES
            
            if state is None:
                state = self.generate_state_parameter()
            
            # Build authorization URL parameters
            params = {
                "response_type": "code",
                "client_id": client_id,
                "redirect_uri": redirect_uri,
                "scope": " ".join(scopes),
                "state": state,
                "show_dialog": "true" if show_dialog else "false"
            }
            
            # Construct full authorization URL
            auth_url = f"{self.OAUTH_AUTHORIZE_URL}?{urllib.parse.urlencode(params)}"
            
            self.logger.info("Generated Spotify OAuth authorization URL")
            self.logger.debug(f"Requested scopes: {', '.join(scopes)}")
            
            return auth_url, state
            
        except Exception as e:
            error_msg = f"Failed to generate Spotify authorization URL: {e}"
            self.logger.error(error_msg)
            raise SpotifyOAuthError(error_msg)
    
    async def exchange_code_for_token(
        self,
        authorization_code: str,
        state: str,
        expected_state: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Exchange authorization code for access token.
        
        Args:
            authorization_code: Authorization code from Spotify callback
            state: State parameter from callback
            expected_state: Expected state value for validation (optional)
            
        Returns:
            Dictionary containing token information:
            {
                "access_token": str,
                "refresh_token": str,
                "expires_in": int,
                "expires_at": datetime,
                "token_type": str,
                "scope": str
            }
            
        Raises:
            SpotifyOAuthError: If token exchange fails or state validation fails
        """
        try:
            # Validate state parameter if expected_state is provided
            if expected_state and state != expected_state:
                error_msg = "State parameter validation failed - possible CSRF attack"
                self.logger.error(error_msg)
                raise SpotifyOAuthError(error_msg)
            
            # Prepare token exchange request using client credentials
            client_id = SpotifyConfig.client_id()
            client_secret = SpotifyConfig.client_secret()
            redirect_uri = SpotifyConfig.redirect_uri()
            
            # Create Basic auth header for Spotify
            auth_header = base64.b64encode(
                f"{client_id}:{client_secret}".encode()
            ).decode()
            
            token_data = {
                "grant_type": "authorization_code",
                "code": authorization_code,
                "redirect_uri": redirect_uri
            }
            
            headers = {
                "Authorization": f"Basic {auth_header}",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            
            self.logger.info("Exchanging authorization code for Spotify access token")
            
            session = await self._get_session()
            async with session.post(
                self.OAUTH_TOKEN_URL,
                data=token_data,
                headers=headers
            ) as response:
                
                if response.status != 200:
                    error_text = await response.text()
                    error_msg = f"Spotify token exchange failed: HTTP {response.status} - {error_text}"
                    self.logger.error(error_msg)
                    raise SpotifyOAuthError(error_msg)
                
                token_response = await response.json()
                
                # Calculate token expiration time
                expires_in = token_response.get("expires_in", 3600)  # Default 1 hour
                expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
                
                # Prepare structured token data
                token_info = {
                    "access_token": token_response["access_token"],
                    "refresh_token": token_response.get("refresh_token"),
                    "expires_in": expires_in,
                    "expires_at": expires_at,
                    "token_type": token_response.get("token_type", "Bearer"),
                    "scope": token_response.get("scope", ""),
                    "obtained_at": datetime.utcnow()
                }
                
                self.logger.info("Successfully obtained Spotify access token")
                self.logger.debug(f"Token expires at: {expires_at}")
                self.logger.debug(f"Granted scopes: {token_info['scope']}")
                
                return token_info
                
        except aiohttp.ClientError as e:
            error_msg = f"Network error during Spotify token exchange: {e}"
            self.logger.error(error_msg)
            raise SpotifyOAuthError(error_msg)
        except Exception as e:
            error_msg = f"Spotify token exchange failed: {e}"
            self.logger.error(error_msg)
            raise SpotifyOAuthError(error_msg)
    
    async def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh an expired access token using refresh token.
        
        Args:
            refresh_token: Valid refresh token
            
        Returns:
            Dictionary containing new token information
            
        Raises:
            SpotifyOAuthError: If token refresh fails
        """
        try:
            client_id = SpotifyConfig.client_id()
            client_secret = SpotifyConfig.client_secret()
            
            # Create Basic auth header for Spotify
            auth_header = base64.b64encode(
                f"{client_id}:{client_secret}".encode()
            ).decode()
            
            refresh_data = {
                "grant_type": "refresh_token",
                "refresh_token": refresh_token
            }
            
            headers = {
                "Authorization": f"Basic {auth_header}",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            
            self.logger.info("Refreshing Spotify access token")
            
            session = await self._get_session()
            async with session.post(
                self.OAUTH_TOKEN_URL,
                data=refresh_data,
                headers=headers
            ) as response:
                
                if response.status != 200:
                    error_text = await response.text()
                    error_msg = f"Spotify token refresh failed: HTTP {response.status} - {error_text}"
                    self.logger.error(error_msg)
                    raise SpotifyOAuthError(error_msg)
                
                token_response = await response.json()
                
                # Calculate new expiration time
                expires_in = token_response.get("expires_in", 3600)
                expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
                
                # Prepare refreshed token data
                token_info = {
                    "access_token": token_response["access_token"],
                    "refresh_token": token_response.get("refresh_token", refresh_token),
                    "expires_in": expires_in,
                    "expires_at": expires_at,
                    "token_type": token_response.get("token_type", "Bearer"),
                    "scope": token_response.get("scope", ""),
                    "refreshed_at": datetime.utcnow()
                }
                
                self.logger.info("Successfully refreshed Spotify access token")
                self.logger.debug(f"New token expires at: {expires_at}")
                
                return token_info
                
        except aiohttp.ClientError as e:
            error_msg = f"Network error during Spotify token refresh: {e}"
            self.logger.error(error_msg)
            raise SpotifyOAuthError(error_msg)
        except Exception as e:
            error_msg = f"Spotify token refresh failed: {e}"
            self.logger.error(error_msg)
            raise SpotifyOAuthError(error_msg)
    
    async def validate_token(self, access_token: str) -> bool:
        """
        Validate an access token by making a test API request.
        
        Args:
            access_token: Access token to validate
            
        Returns:
            True if token is valid, False otherwise
        """
        try:
            # Make a simple API request to test token validity
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json"
            }
            
            session = await self._get_session()
            # Test with user profile endpoint which requires authentication
            test_url = "https://api.spotify.com/v1/me"
            
            async with session.get(test_url, headers=headers) as response:
                if response.status == 200:
                    self.logger.debug("Spotify access token validation successful")
                    return True
                elif response.status == 401:
                    self.logger.debug("Spotify access token is invalid or expired")
                    return False
                else:
                    self.logger.warning(f"Unexpected response during Spotify token validation: {response.status}")
                    return False
                    
        except Exception as e:
            self.logger.error(f"Spotify token validation failed: {e}")
            return False
    
    def is_token_expired(self, token_info: Dict[str, Any], buffer_minutes: int = 5) -> bool:
        """
        Check if a token is expired or will expire soon.
        
        Args:
            token_info: Token information dictionary
            buffer_minutes: Minutes before expiration to consider token expired (default: 5)
            
        Returns:
            True if token is expired or will expire within buffer time
        """
        try:
            expires_at = token_info.get("expires_at")
            if not expires_at:
                return True  # No expiration info, consider expired
            
            # Convert string to datetime if needed
            if isinstance(expires_at, str):
                expires_at = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
            
            buffer_time = timedelta(minutes=buffer_minutes)
            return datetime.utcnow() + buffer_time >= expires_at
            
        except Exception as e:
            self.logger.error(f"Error checking Spotify token expiration: {e}")
            return True  # Error parsing, consider expired for safety
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()


# Convenience function for quick OAuth URL generation
def get_spotify_auth_url(scopes: Optional[list] = None) -> Tuple[str, str]:
    """
    Quick function to generate Spotify authorization URL.
    
    Args:
        scopes: List of OAuth scopes (optional)
        
    Returns:
        Tuple of (authorization_url, state_parameter)
    """
    oauth_client = SpotifyOAuth()
    return oauth_client.get_authorization_url(scopes=scopes)
