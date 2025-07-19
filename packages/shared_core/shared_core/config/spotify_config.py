"""
Spotify Configuration Management

This module provides centralized Spotify API configuration following project patterns.
It handles API credentials, OAuth configuration, and environment-driven configuration.
"""

import os
from typing import Optional, Dict, Any, List
from urllib.parse import urlencode

from ..utils.centralized_logging import CentralizedLogger
from .unified_environment_loader import UnifiedEnvironmentLoader

# Initialize logger
logger = CentralizedLogger.get_logger("spotify_config")


class SpotifyConfig:
    """
    Centralized Spotify API configuration management
    
    Follows project patterns for environment-driven configuration
    """
    
    _instance: Optional["SpotifyConfig"] = None
    
    def __new__(cls, *args, **kwargs):
        """Singleton pattern to ensure single instance"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize Spotify configuration"""
        if hasattr(self, '_initialized'):
            return
        
        # Ensure environment is loaded
        UnifiedEnvironmentLoader.ensure_environment_loaded()
        
        self._initialized = True
        logger.info("Spotify configuration initialized")
    
    @staticmethod
    def client_id() -> str:
        """
        Get Spotify client ID from environment
        
        Returns:
            str: Spotify client ID
        """
        client_id = os.getenv("SPOTIFY_CLIENT_ID")
        if not client_id:
            raise ValueError("SPOTIFY_CLIENT_ID environment variable is required")
        return client_id
    
    @staticmethod
    def client_secret() -> str:
        """
        Get Spotify client secret from environment
        
        Returns:
            str: Spotify client secret
        """
        client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        if not client_secret:
            raise ValueError("SPOTIFY_CLIENT_SECRET environment variable is required")
        return client_secret
    
    @staticmethod
    def redirect_uri() -> str:
        """
        Get Spotify OAuth redirect URI from environment
        
        Returns:
            str: Redirect URI for OAuth flow
        """
        return os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:8080/callback")
    
    @staticmethod
    def access_token() -> Optional[str]:
        """
        Get stored access token (if available)
        
        Returns:
            Optional[str]: Access token if available
        """
        return os.getenv("SPOTIFY_ACCESS_TOKEN")
    
    @staticmethod
    def refresh_token() -> Optional[str]:
        """
        Get stored refresh token (if available)
        
        Returns:
            Optional[str]: Refresh token if available
        """
        return os.getenv("SPOTIFY_REFRESH_TOKEN")
    
    @staticmethod
    def default_scopes() -> List[str]:
        """
        Get default OAuth scopes for data collection
        
        Returns:
            List[str]: Default scopes for correlation analysis
        """
        return [
            "user-read-private",
            "user-read-email",
            "user-library-read",
            "user-top-read",
            "user-read-recently-played",
            "playlist-read-private",
            "user-read-playback-state",
            "user-read-currently-playing"
        ]
    
    @staticmethod
    def get_authorization_url(scopes: Optional[List[str]] = None, state: Optional[str] = None) -> str:
        """
        Generate Spotify authorization URL
        
        Args:
            scopes: OAuth scopes to request
            state: State parameter for OAuth security
            
        Returns:
            str: Complete authorization URL
        """
        if scopes is None:
            scopes = SpotifyConfig.default_scopes()
        
        if state is None:
            import secrets
            state = secrets.token_urlsafe(32)
        
        params = {
            "response_type": "code",
            "client_id": SpotifyConfig.client_id(),
            "scope": " ".join(scopes),
            "redirect_uri": SpotifyConfig.redirect_uri(),
            "state": state,
            "show_dialog": "true"  # Always show consent dialog
        }
        
        auth_url = f"https://accounts.spotify.com/authorize?{urlencode(params)}"
        logger.debug(f"Generated Spotify authorization URL with {len(scopes)} scopes")
        
        return auth_url
    
    @staticmethod
    def validate_credentials() -> bool:
        """
        Validate that required Spotify credentials are available
        
        Returns:
            bool: True if credentials are valid
        """
        try:
            SpotifyConfig.client_id()
            SpotifyConfig.client_secret()
            logger.info("Spotify credentials validation successful")
            return True
        except ValueError as e:
            logger.error(f"Spotify credentials validation failed: {e}")
            return False
    
    @staticmethod
    def get_config_summary() -> Dict[str, Any]:
        """
        Get Spotify configuration summary for debugging
        
        Returns:
            Dict[str, Any]: Configuration summary (with masked secrets)
        """
        try:
            client_id = SpotifyConfig.client_id()
            masked_client_id = f"{client_id[:4]}...{client_id[-4:]}" if len(client_id) > 8 else "***MASKED***"
        except ValueError:
            masked_client_id = "NOT_SET"
        
        try:
            client_secret = SpotifyConfig.client_secret()
            masked_client_secret = "***MASKED***" if client_secret else "NOT_SET"
        except ValueError:
            masked_client_secret = "NOT_SET"
        
        return {
            "client_id": masked_client_id,
            "client_secret": masked_client_secret,
            "redirect_uri": SpotifyConfig.redirect_uri(),
            "has_access_token": bool(SpotifyConfig.access_token()),
            "has_refresh_token": bool(SpotifyConfig.refresh_token()),
            "default_scopes": SpotifyConfig.default_scopes()
        }
    
    @staticmethod
    def get_correlation_config() -> Dict[str, Any]:
        """
        Get configuration specific to correlation analysis
        
        Returns:
            Dict[str, Any]: Correlation analysis configuration
        """
        return {
            "audio_features": [
                "valence",      # Musical positivity (0.0-1.0)
                "energy",       # Energy level (0.0-1.0)
                "danceability", # Danceability (0.0-1.0)
                "acousticness", # Acoustic vs electric (0.0-1.0)
                "instrumentalness", # Instrumental vs vocal (0.0-1.0)
                "tempo",        # BPM
                "loudness",     # Loudness in dB
                "speechiness"   # Spoken word content (0.0-1.0)
            ],
            "correlation_fields": [
                "isrc",         # International Standard Recording Code
                "release_date", # Release date for temporal correlation
                "genres",       # Genre classification
                "popularity",   # Popularity score
                "duration_ms"   # Track duration
            ],
            "batch_size": 100,  # Maximum tracks per batch request
            "rate_limit_buffer": 0.1  # Buffer for rate limiting
        }
    
    @classmethod
    def get_instance(cls) -> "SpotifyConfig":
        """Get the singleton instance of SpotifyConfig"""
        return cls()


# Convenience functions for backward compatibility
def get_spotify_client_id() -> str:
    """Get Spotify client ID"""
    return SpotifyConfig.client_id()


def get_spotify_client_secret() -> str:
    """Get Spotify client secret"""
    return SpotifyConfig.client_secret()


def get_spotify_redirect_uri() -> str:
    """Get Spotify redirect URI"""
    return SpotifyConfig.redirect_uri()


def validate_spotify_config() -> bool:
    """Validate Spotify configuration"""
    return SpotifyConfig.validate_credentials()


# Initialize configuration on module import
_config = SpotifyConfig.get_instance()
logger.info("Spotify configuration module loaded")
