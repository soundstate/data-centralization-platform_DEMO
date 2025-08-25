"""
MusicBrainz OAuth 2.0 Client

This module provides OAuth 2.0 authentication capabilities for the MusicBrainz API.
It handles the complete OAuth flow including authorization URL generation,
token exchange, and token refresh operations.

Features:
- Authorization URL generation with state parameter for security
- Authorization code exchange for access tokens
- Automatic token refresh capabilities
- Comprehensive error handling and logging
- Integration with the project's configuration patterns

Usage:
    from shared_core.auth import MusicBrainzOAuth
    from shared_core.config.musicbrainz_config import MusicBrainzConfig
    
    # Initialize OAuth client
    oauth_client = MusicBrainzOAuth()
    
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
import secrets
import urllib.parse
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple

import aiohttp

from shared_core.config.musicbrainz_config import MusicBrainzConfig
from shared_core.utils.centralized_logging import CentralizedLogger


class MusicBrainzOAuthError(Exception):
    """Custom exception for MusicBrainz OAuth errors."""
    pass


class MusicBrainzOAuth:
    """
    MusicBrainz OAuth 2.0 Client
    
    Handles the complete OAuth 2.0 authorization code flow for MusicBrainz API access.
    Provides secure token management with automatic refresh capabilities.
    """
    
    def __init__(self, timeout: int = 30):
        """
        Initialize MusicBrainz OAuth client.
        
        Args:
            timeout: HTTP request timeout in seconds (default: 30)
        """
        self.logger = CentralizedLogger.get_logger(__name__)
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session = None
        
        # Validate OAuth configuration on initialization
        try:
            self.config = MusicBrainzConfig()
            oauth_config = MusicBrainzConfig.get_oauth_config()
            if not oauth_config.get("oauth_valid", False):
                self.logger.warning("OAuth configuration validation failed - some operations may not work")
        except Exception as e:
            self.logger.error(f"Failed to initialize OAuth configuration: {e}")
            raise MusicBrainzOAuthError(f"Configuration error: {e}")
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """
        Get or create aiohttp session.
        
        Returns:
            Configured aiohttp ClientSession
        """
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                timeout=self.timeout,
                headers={"User-Agent": MusicBrainzConfig.user_agent()}
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
        state: Optional[str] = None
    ) -> Tuple[str, str]:
        """
        Generate MusicBrainz OAuth authorization URL.
        
        Args:
            scopes: List of OAuth scopes to request (default: profile, email, collection)
            state: Custom state parameter (will generate secure one if not provided)
            
        Returns:
            Tuple of (authorization_url, state_parameter)
            
        Raises:
            MusicBrainzOAuthError: If configuration is invalid
        """
        try:
            client_id = MusicBrainzConfig.client_id()
            redirect_uri = MusicBrainzConfig.redirect_uri()
            
            if scopes is None:
                scopes = MusicBrainzConfig.OAUTH_DEFAULT_SCOPES
            
            if state is None:
                state = self.generate_state_parameter()
            
            # Build authorization URL parameters
            params = {
                "response_type": "code",
                "client_id": client_id,
                "redirect_uri": redirect_uri,
                "scope": " ".join(scopes),
                "state": state
            }
            
            # Construct full authorization URL
            base_url = MusicBrainzConfig.OAUTH_AUTHORIZE_URL
            auth_url = f"{base_url}?{urllib.parse.urlencode(params)}"
            
            self.logger.info("Generated MusicBrainz OAuth authorization URL")
            self.logger.debug(f"Requested scopes: {', '.join(scopes)}")
            
            return auth_url, state
            
        except Exception as e:
            error_msg = f"Failed to generate authorization URL: {e}"
            self.logger.error(error_msg)
            raise MusicBrainzOAuthError(error_msg)
    
    async def exchange_code_for_token(
        self,
        authorization_code: str,
        state: str,
        expected_state: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Exchange authorization code for access token.
        
        Args:
            authorization_code: Authorization code from MusicBrainz callback
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
            MusicBrainzOAuthError: If token exchange fails or state validation fails
        """
        try:
            # Validate state parameter if expected_state is provided
            if expected_state and state != expected_state:
                error_msg = "State parameter validation failed - possible CSRF attack"
                self.logger.error(error_msg)
                raise MusicBrainzOAuthError(error_msg)
            
            # Prepare token exchange request
            client_id = MusicBrainzConfig.client_id()
            client_secret = MusicBrainzConfig.client_secret()
            redirect_uri = MusicBrainzConfig.redirect_uri()
            
            token_data = {
                "grant_type": "authorization_code",
                "code": authorization_code,
                "redirect_uri": redirect_uri,
                "client_id": client_id,
                "client_secret": client_secret
            }
            
            self.logger.info("Exchanging authorization code for access token")
            
            session = await self._get_session()
            async with session.post(
                MusicBrainzConfig.OAUTH_TOKEN_URL,
                data=token_data,
                headers={"Accept": "application/json"}
            ) as response:
                
                if response.status != 200:
                    error_text = await response.text()
                    error_msg = f"Token exchange failed: HTTP {response.status} - {error_text}"
                    self.logger.error(error_msg)
                    raise MusicBrainzOAuthError(error_msg)
                
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
                
                self.logger.info("Successfully obtained access token")
                self.logger.debug(f"Token expires at: {expires_at}")
                self.logger.debug(f"Granted scopes: {token_info['scope']}")
                
                return token_info
                
        except aiohttp.ClientError as e:
            error_msg = f"Network error during token exchange: {e}"
            self.logger.error(error_msg)
            raise MusicBrainzOAuthError(error_msg)
        except Exception as e:
            error_msg = f"Token exchange failed: {e}"
            self.logger.error(error_msg)
            raise MusicBrainzOAuthError(error_msg)
    
    async def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh an expired access token using refresh token.
        
        Args:
            refresh_token: Valid refresh token
            
        Returns:
            Dictionary containing new token information
            
        Raises:
            MusicBrainzOAuthError: If token refresh fails
        """
        try:
            client_id = MusicBrainzConfig.client_id()
            client_secret = MusicBrainzConfig.client_secret()
            
            refresh_data = {
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": client_id,
                "client_secret": client_secret
            }
            
            self.logger.info("Refreshing access token")
            
            session = await self._get_session()
            async with session.post(
                MusicBrainzConfig.OAUTH_TOKEN_URL,
                data=refresh_data,
                headers={"Accept": "application/json"}
            ) as response:
                
                if response.status != 200:
                    error_text = await response.text()
                    error_msg = f"Token refresh failed: HTTP {response.status} - {error_text}"
                    self.logger.error(error_msg)
                    raise MusicBrainzOAuthError(error_msg)
                
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
                
                self.logger.info("Successfully refreshed access token")
                self.logger.debug(f"New token expires at: {expires_at}")
                
                return token_info
                
        except aiohttp.ClientError as e:
            error_msg = f"Network error during token refresh: {e}"
            self.logger.error(error_msg)
            raise MusicBrainzOAuthError(error_msg)
        except Exception as e:
            error_msg = f"Token refresh failed: {e}"
            self.logger.error(error_msg)
            raise MusicBrainzOAuthError(error_msg)
    
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
            # Test with a simple lookup that requires authentication
            test_url = "https://musicbrainz.org/ws/2/oauth-test"
            
            async with session.get(test_url, headers=headers) as response:
                if response.status == 200:
                    self.logger.debug("Access token validation successful")
                    return True
                elif response.status == 401:
                    self.logger.debug("Access token is invalid or expired")
                    return False
                else:
                    self.logger.warning(f"Unexpected response during token validation: {response.status}")
                    return False
                    
        except Exception as e:
            self.logger.error(f"Token validation failed: {e}")
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
            self.logger.error(f"Error checking token expiration: {e}")
            return True  # Error parsing, consider expired for safety
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()


# Convenience function for quick OAuth URL generation
def get_musicbrainz_auth_url(scopes: Optional[list] = None) -> Tuple[str, str]:
    """
    Quick function to generate MusicBrainz authorization URL.
    
    Args:
        scopes: List of OAuth scopes (optional)
        
    Returns:
        Tuple of (authorization_url, state_parameter)
    """
    oauth_client = MusicBrainzOAuth()
    return oauth_client.get_authorization_url(scopes=scopes)
