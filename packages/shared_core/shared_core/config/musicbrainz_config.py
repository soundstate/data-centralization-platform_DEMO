"""
MusicBrainz Configuration Module

This module provides centralized configuration management for MusicBrainz API integration.
It follows the established patterns for environment-driven configuration in the shared_core package.

The configuration includes:
- User-Agent management
- Rate limiting configuration
- Debug mode settings

All configuration values are loaded from environment variables with sensible defaults.
"""

import os
import logging
from typing import Dict, Any

from shared_core.utils.centralized_logging import CentralizedLogger


class MusicBrainzConfig:
    """
    Centralized configuration for MusicBrainz API integration.
    
    This configuration class manages all MusicBrainz-related settings using environment variables.
    It provides validation, logging, and easy access to configuration values.
    
    Environment Variables:
    - MUSICBRAINZ_USER_AGENT: Custom User-Agent (required)
    - MUSICBRAINZ_CLIENT_ID: OAuth client ID (required for OAuth)
    - MUSICBRAINZ_CLIENT_SECRET: OAuth client secret (required for OAuth)
    - MUSICBRAINZ_REDIRECT_URI: OAuth redirect URI (default: http://localhost:8000/auth/musicbrainz/callback)
    - MUSICBRAINZ_RATE_LIMIT_PER_SECOND: Rate limit in requests per second (default: 1.0)
    - MUSICBRAINZ_DEBUG_MODE: Enable debug logging (default: false)
    
    Usage:
        # Get User-Agent
        user_agent = MusicBrainzConfig.user_agent()
        
        # Get full configuration
        config = MusicBrainzConfig.get_config_summary()
    """
    
    # OAuth URLs for MusicBrainz
    OAUTH_AUTHORIZE_URL = "https://musicbrainz.org/oauth2/authorize"
    OAUTH_TOKEN_URL = "https://musicbrainz.org/oauth2/token"
    OAUTH_DEFAULT_SCOPES = ["profile", "email", "collection", "submit_isrc", "submit_barcode"]
    
    _instance = None
    _logger = None
    
    def __new__(cls):
        """Singleton pattern to ensure single configuration instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._logger = CentralizedLogger.get_logger(__name__)
            cls._logger.info("MusicBrainz configuration initialized")
        return cls._instance
    
    @classmethod
    def user_agent(cls) -> str:
        """
        Get MusicBrainz User-Agent from environment.
        
        Returns:
            Custom User-Agent
            
        Raises:
            ValueError: If User-Agent is not found in environment
        """
        user_agent = os.getenv("MUSICBRAINZ_USER_AGENT", "").strip()
        if not user_agent:
            error_msg = "MUSICBRAINZ_USER_AGENT environment variable is required but not set"
            if cls._logger:
                cls._logger.error(error_msg)
            raise ValueError(error_msg)
        
        if cls._logger:
            cls._logger.debug("MusicBrainz User-Agent retrieved from environment")
        
        return user_agent
    
    @classmethod
    def rate_limit_per_second(cls) -> float:
        """
        Get rate limiting configuration.
        
        Returns:
            Rate limit in requests per second (default: 1.0)
        """
        try:
            return float(os.getenv("MUSICBRAINZ_RATE_LIMIT_PER_SECOND", "1.0"))
        except ValueError:
            if cls._logger:
                cls._logger.warning("Invalid MUSICBRAINZ_RATE_LIMIT_PER_SECOND value, using default: 1.0")
            return 1.0
    
    @classmethod
    def debug_mode(cls) -> bool:
        """
        Get debug mode setting.
        
        Returns:
            True if debug mode is enabled, False otherwise
        """
        return os.getenv("MUSICBRAINZ_DEBUG_MODE", "false").lower() in ("true", "1", "yes", "on")
    
    @classmethod
    def validate_credentials(cls) -> bool:
        """
        Validate MusicBrainz configuration.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        try:
            # Check if User-Agent is available
            user_agent = cls.user_agent()
            
            # Basic validation of User-Agent format
            if not user_agent or len(user_agent) < 5:
                if cls._logger:
                    cls._logger.error("User-Agent appears to be invalid (too short)")
                return False
            
            if cls._logger:
                cls._logger.info("MusicBrainz configuration validation successful")
            
            return True
            
        except Exception as e:
            if cls._logger:
                cls._logger.error(f"MusicBrainz configuration validation failed: {str(e)}")
            return False
    
    @classmethod
    def get_config_summary(cls) -> Dict[str, Any]:
        """
        Get a summary of all MusicBrainz configuration values.
        
        Returns:
            Dictionary containing all configuration values
        """
        try:
            user_agent = cls.user_agent()
        except ValueError:
            user_agent = "NOT_SET"
        
        return {
            "user_agent": user_agent,
            "rate_limit_per_second": cls.rate_limit_per_second(),
            "debug_mode": cls.debug_mode(),
            "is_valid": cls.validate_credentials()
        }
    
    @classmethod
    def log_configuration(cls) -> None:
        """
        Log current configuration settings (for debugging).
        """
        if not cls._logger:
            return
        
        config = cls.get_config_summary()
        cls._logger.info("MusicBrainz Configuration Summary:")
        for key, value in config.items():
            cls._logger.info(f"  {key}: {value}")
    
    @classmethod
    def get_client_config(cls) -> Dict[str, Any]:
        """
        Get configuration values formatted for MusicBrainzClient initialization.
        
        Returns:
            Dictionary with client configuration parameters
        """
        return {
            "user_agent": cls.user_agent(),
            "rate_limit_per_second": cls.rate_limit_per_second(),
            "debug_mode": cls.debug_mode()
        }
    
    @classmethod
    def get_default_params(cls) -> Dict[str, Any]:
        """
        Get default parameters for MusicBrainz API requests.
        
        Returns:
            Dictionary with default request parameters
        """
        return {}  # No default parameters for MusicBrainz API
    
    # OAuth-specific configuration methods
    
    @classmethod
    def client_id(cls) -> str:
        """
        Get OAuth client ID from environment.
        
        Returns:
            OAuth client ID
            
        Raises:
            ValueError: If client ID is not found in environment
        """
        client_id = os.getenv("MUSICBRAINZ_CLIENT_ID", "").strip()
        if not client_id:
            error_msg = "MUSICBRAINZ_CLIENT_ID environment variable is required for OAuth but not set"
            if cls._logger:
                cls._logger.error(error_msg)
            raise ValueError(error_msg)
        
        if cls._logger:
            cls._logger.debug("MusicBrainz OAuth client ID retrieved from environment")
        
        return client_id
    
    @classmethod
    def client_secret(cls) -> str:
        """
        Get OAuth client secret from environment.
        
        Returns:
            OAuth client secret
            
        Raises:
            ValueError: If client secret is not found in environment
        """
        client_secret = os.getenv("MUSICBRAINZ_CLIENT_SECRET", "").strip()
        if not client_secret:
            error_msg = "MUSICBRAINZ_CLIENT_SECRET environment variable is required for OAuth but not set"
            if cls._logger:
                cls._logger.error(error_msg)
            raise ValueError(error_msg)
        
        if cls._logger:
            cls._logger.debug("MusicBrainz OAuth client secret retrieved from environment")
        
        return client_secret
    
    @classmethod
    def redirect_uri(cls) -> str:
        """
        Get OAuth redirect URI from environment.
        
        Returns:
            OAuth redirect URI (default: http://localhost:8000/auth/musicbrainz/callback)
        """
        return os.getenv("MUSICBRAINZ_REDIRECT_URI", "http://localhost:8000/auth/musicbrainz/callback")
    
    @classmethod
    def validate_oauth_credentials(cls) -> bool:
        """
        Validate OAuth configuration credentials.
        
        Returns:
            True if OAuth configuration is valid, False otherwise
        """
        try:
            client_id = cls.client_id()
            client_secret = cls.client_secret()
            redirect_uri = cls.redirect_uri()
            
            # Basic validation
            if not client_id or len(client_id) < 10:
                if cls._logger:
                    cls._logger.error("OAuth client ID appears to be invalid")
                return False
            
            if not client_secret or len(client_secret) < 10:
                if cls._logger:
                    cls._logger.error("OAuth client secret appears to be invalid")
                return False
            
            if not redirect_uri.startswith(('http://', 'https://')):
                if cls._logger:
                    cls._logger.error("OAuth redirect URI must be a valid URL")
                return False
            
            if cls._logger:
                cls._logger.info("MusicBrainz OAuth configuration validation successful")
            
            return True
            
        except Exception as e:
            if cls._logger:
                cls._logger.error(f"MusicBrainz OAuth configuration validation failed: {str(e)}")
            return False
    
    @classmethod
    def get_oauth_config(cls) -> Dict[str, Any]:
        """
        Get OAuth configuration values.
        
        Returns:
            Dictionary with OAuth configuration parameters
        """
        try:
            client_id = cls.client_id()
        except ValueError:
            client_id = "NOT_SET"
        
        try:
            client_secret = cls.client_secret()
            # Don't expose the actual secret, just indicate if it's set
            client_secret_status = "SET" if client_secret else "NOT_SET"
        except ValueError:
            client_secret_status = "NOT_SET"
        
        return {
            "client_id": client_id,
            "client_secret": client_secret_status,
            "redirect_uri": cls.redirect_uri(),
            "authorize_url": cls.OAUTH_AUTHORIZE_URL,
            "token_url": cls.OAUTH_TOKEN_URL,
            "default_scopes": cls.OAUTH_DEFAULT_SCOPES,
            "oauth_valid": cls.validate_oauth_credentials()
        }
