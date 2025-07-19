"""
TMDB Configuration Module

This module provides centralized configuration management for TMDB API integration.
It follows the established patterns for environment-driven configuration in the shared_core package.

The configuration includes:
- TMDB API key management
- Image size preferences
- Language settings
- Rate limiting configuration
- Debug mode settings

All configuration values are loaded from environment variables with sensible defaults.
"""

import os
import logging
from typing import Dict, Any, Optional

from shared_core.logging.centralized_logger import CentralizedLogger


class TMDBConfig:
    """
    Centralized configuration for TMDB API integration.
    
    This configuration class manages all TMDB-related settings using environment variables.
    It provides validation, logging, and easy access to configuration values.
    
    Environment Variables:
    - TMDB_API_KEY: TMDB API key (required)
    - TMDB_LANGUAGE: Default language for API requests (default: en-US)
    - TMDB_REGION: Default region for API requests (optional)
    - TMDB_IMAGE_SIZE: Default image size (default: w500)
    - TMDB_INCLUDE_ADULT: Include adult content in results (default: false)
    - TMDB_DEBUG_MODE: Enable debug logging (default: false)
    
    Usage:
        # Get API key
        api_key = TMDBConfig.api_key()
        
        # Get full configuration
        config = TMDBConfig.get_config_summary()
        
        # Validate configuration
        is_valid = TMDBConfig.validate_credentials()
    """
    
    _instance = None
    _logger = None
    
    def __new__(cls):
        """Singleton pattern to ensure single configuration instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._logger = CentralizedLogger.get_logger(__name__)
            cls._logger.info("TMDB configuration initialized")
        return cls._instance
    
    @classmethod
    def api_key(cls) -> str:
        """
        Get TMDB API key from environment.
        
        Returns:
            TMDB API key
            
        Raises:
            ValueError: If API key is not found in environment
        """
        api_key = os.getenv("TMDB_API_KEY", "").strip()
        if not api_key:
            error_msg = "TMDB_API_KEY environment variable is required but not set"
            if cls._logger:
                cls._logger.error(error_msg)
            raise ValueError(error_msg)
        
        if cls._logger:
            cls._logger.debug("TMDB API key retrieved from environment")
        
        return api_key
    
    @classmethod
    def language(cls) -> str:
        """
        Get default language for TMDB API requests.
        
        Returns:
            Language code (default: en-US)
        """
        return os.getenv("TMDB_LANGUAGE", "en-US").strip()
    
    @classmethod
    def region(cls) -> Optional[str]:
        """
        Get default region for TMDB API requests.
        
        Returns:
            Region code or None if not set
        """
        region = os.getenv("TMDB_REGION", "").strip()
        return region if region else None
    
    @classmethod
    def image_size(cls) -> str:
        """
        Get default image size for TMDB images.
        
        Returns:
            Image size (default: w500)
        """
        return os.getenv("TMDB_IMAGE_SIZE", "w500").strip()
    
    @classmethod
    def include_adult(cls) -> bool:
        """
        Get setting for including adult content in search results.
        
        Returns:
            True if adult content should be included, False otherwise
        """
        return os.getenv("TMDB_INCLUDE_ADULT", "false").lower() in ("true", "1", "yes", "on")
    
    @classmethod
    def debug_mode(cls) -> bool:
        """
        Get debug mode setting.
        
        Returns:
            True if debug mode is enabled, False otherwise
        """
        return os.getenv("TMDB_DEBUG_MODE", "false").lower() in ("true", "1", "yes", "on")
    
    @classmethod
    def base_url(cls) -> str:
        """
        Get TMDB API base URL.
        
        Returns:
            Base URL for TMDB API (default: https://api.themoviedb.org/3)
        """
        return os.getenv("TMDB_BASE_URL", "https://api.themoviedb.org/3").strip()
    
    @classmethod
    def image_base_url(cls) -> str:
        """
        Get TMDB image base URL.
        
        Returns:
            Base URL for TMDB images (default: https://image.tmdb.org/t/p)
        """
        return os.getenv("TMDB_IMAGE_BASE_URL", "https://image.tmdb.org/t/p").strip()
    
    @classmethod
    def rate_limit_per_second(cls) -> float:
        """
        Get rate limiting configuration.
        
        Returns:
            Rate limit in requests per second (default: 4.0)
        """
        try:
            return float(os.getenv("TMDB_RATE_LIMIT_PER_SECOND", "4.0"))
        except ValueError:
            if cls._logger:
                cls._logger.warning("Invalid TMDB_RATE_LIMIT_PER_SECOND value, using default: 4.0")
            return 4.0
    
    @classmethod
    def max_retries(cls) -> int:
        """
        Get maximum retry attempts for failed requests.
        
        Returns:
            Maximum retry attempts (default: 3)
        """
        try:
            return int(os.getenv("TMDB_MAX_RETRIES", "3"))
        except ValueError:
            if cls._logger:
                cls._logger.warning("Invalid TMDB_MAX_RETRIES value, using default: 3")
            return 3
    
    @classmethod
    def timeout(cls) -> int:
        """
        Get request timeout in seconds.
        
        Returns:
            Request timeout in seconds (default: 30)
        """
        try:
            return int(os.getenv("TMDB_TIMEOUT", "30"))
        except ValueError:
            if cls._logger:
                cls._logger.warning("Invalid TMDB_TIMEOUT value, using default: 30")
            return 30
    
    @classmethod
    def validate_credentials(cls) -> bool:
        """
        Validate TMDB configuration.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        try:
            # Check if API key is available
            api_key = cls.api_key()
            
            # Basic validation of API key format
            if not api_key or len(api_key) < 10:
                if cls._logger:
                    cls._logger.error("TMDB API key appears to be invalid (too short)")
                return False
            
            # Check if API key contains only valid characters
            if not api_key.replace("-", "").replace("_", "").isalnum():
                if cls._logger:
                    cls._logger.error("TMDB API key contains invalid characters")
                return False
            
            if cls._logger:
                cls._logger.info("TMDB configuration validation successful")
            
            return True
            
        except Exception as e:
            if cls._logger:
                cls._logger.error(f"TMDB configuration validation failed: {str(e)}")
            return False
    
    @classmethod
    def get_config_summary(cls) -> Dict[str, Any]:
        """
        Get a summary of all TMDB configuration values.
        
        Returns:
            Dictionary containing all configuration values (API key masked)
        """
        try:
            api_key = cls.api_key()
            masked_key = f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "***"
        except ValueError:
            masked_key = "NOT_SET"
        
        return {
            "api_key": masked_key,
            "language": cls.language(),
            "region": cls.region(),
            "image_size": cls.image_size(),
            "include_adult": cls.include_adult(),
            "debug_mode": cls.debug_mode(),
            "base_url": cls.base_url(),
            "image_base_url": cls.image_base_url(),
            "rate_limit_per_second": cls.rate_limit_per_second(),
            "max_retries": cls.max_retries(),
            "timeout": cls.timeout(),
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
        cls._logger.info("TMDB Configuration Summary:")
        for key, value in config.items():
            cls._logger.info(f"  {key}: {value}")
    
    @classmethod
    def get_client_config(cls) -> Dict[str, Any]:
        """
        Get configuration values formatted for TMDBClient initialization.
        
        Returns:
            Dictionary with client configuration parameters
        """
        return {
            "api_key": cls.api_key(),
            "base_url": cls.base_url(),
            "image_base_url": cls.image_base_url(),
            "rate_limit_per_second": cls.rate_limit_per_second(),
            "max_retries": cls.max_retries(),
            "timeout": cls.timeout(),
            "debug_mode": cls.debug_mode()
        }
    
    @classmethod
    def get_default_params(cls) -> Dict[str, Any]:
        """
        Get default parameters for TMDB API requests.
        
        Returns:
            Dictionary with default request parameters
        """
        params = {
            "language": cls.language(),
            "include_adult": cls.include_adult()
        }
        
        region = cls.region()
        if region:
            params["region"] = region
        
        return params
