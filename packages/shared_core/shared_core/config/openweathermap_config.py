"""
OpenWeatherMap Configuration Management

This module provides centralized OpenWeatherMap API configuration following project patterns.
It handles API credentials and environment-driven configuration.
"""

import os
from typing import Optional, Dict, Any, List
from urllib.parse import urlencode

from ..utils.centralized_logging import CentralizedLogger
from .unified_environment_loader import UnifiedEnvironmentLoader

# Initialize logger
logger = CentralizedLogger.get_logger("openweathermap_config")


class OpenWeatherMapConfig:
    """
    Centralized OpenWeatherMap API configuration management
    
    Follows project patterns for environment-driven configuration
    """
    
    _instance: Optional["OpenWeatherMapConfig"] = None
    
    def __new__(cls, *args, **kwargs):
        """Singleton pattern to ensure single instance"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize OpenWeatherMap configuration"""
        if hasattr(self, '_initialized'):
            return
        
        # Ensure environment is loaded
        UnifiedEnvironmentLoader.ensure_environment_loaded()
        
        self._initialized = True
        logger.info("OpenWeatherMap configuration initialized")
    
    @staticmethod
    def api_key() -> str:
        """
        Get OpenWeatherMap API key from environment
        
        Returns:
            str: OpenWeatherMap API key
        """
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            raise ValueError("OPENWEATHER_API_KEY environment variable is required")
        return api_key
    
    @staticmethod
    def default_units() -> str:
        """
        Get default units for weather data
        
        Returns:
            str: Default units (metric, imperial, kelvin)
        """
        return os.getenv("OPENWEATHER_UNITS", "metric")

    @staticmethod
    def validate_credentials() -> bool:
        """
        Validate that required OpenWeatherMap credentials are available
        
        Returns:
            bool: True if credentials are valid
        """
        try:
            OpenWeatherMapConfig.api_key()
            logger.info("OpenWeatherMap credentials validation successful")
            return True
        except ValueError as e:
            logger.error(f"OpenWeatherMap credentials validation failed: {e}")
            return False
    
    @staticmethod
    def get_config_summary() -> Dict[str, Any]:
        """
        Get OpenWeatherMap configuration summary for debugging
        
        Returns:
            Dict[str, Any]: Configuration summary
        """
        try:
            api_key = OpenWeatherMapConfig.api_key()
            masked_api_key = f"{api_key[:4]}...{api_key[-4:]}" if len(api_key) > 8 else "***MASKED***"
        except ValueError:
            masked_api_key = "NOT_SET"
        
        return {
            "api_key": masked_api_key,
            "default_units": OpenWeatherMapConfig.default_units(),
        }
    
    @classmethod
    def get_instance(cls) -> "OpenWeatherMapConfig":
        """Get the singleton instance of OpenWeatherMapConfig"""
        return cls()


# Convenience functions for backward compatibility
def get_openweather_api_key() -> str:
    """Get OpenWeatherMap API key"""
    return OpenWeatherMapConfig.api_key()


def validate_openweather_config() -> bool:
    """Validate OpenWeatherMap configuration"""
    return OpenWeatherMapConfig.validate_credentials()


# Initialize configuration on module import
_config = OpenWeatherMapConfig.get_instance()
logger.info("OpenWeatherMap configuration module loaded")
