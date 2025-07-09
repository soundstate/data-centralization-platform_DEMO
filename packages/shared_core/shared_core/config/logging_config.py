# packages/jobe_shared/jobe_shared/config/logging_config.py
"""
Logging Configuration Management

This module provides centralized configuration management for logging settings
across all services in the Jobe Systems API Codebase.
"""

import os
from typing import Optional


class LoggingConfig:
    """Environment-driven configuration for centralized logging system"""

    # ========================================================================
    # LOGGING CONFIGURATION
    # ========================================================================

    @staticmethod
    def log_level() -> str:
        """Get logging level from environment"""
        return os.getenv("LOG_LEVEL", "INFO").upper()

    @staticmethod
    def centralized_logging_enabled() -> bool:
        """Check if centralized logging is enabled"""
        return os.getenv("CENTRALIZED_LOGGING", "true").lower() == "true"

    @staticmethod
    def log_rotation_days() -> int:
        """Get number of days to keep logs"""
        try:
            return int(os.getenv("LOG_ROTATION_DAYS", "7"))
        except ValueError:
            return 7

    @staticmethod
    def azure_log_integration_enabled() -> bool:
        """Check if Azure Monitor integration is enabled"""
        return os.getenv("AZURE_LOG_INTEGRATION", "false").lower() == "true"

    @staticmethod
    def log_to_console_enabled() -> bool:
        """Check if console logging is enabled"""
        return os.getenv("LOG_TO_CONSOLE", "true").lower() == "true"

    @staticmethod
    def log_file_max_size() -> str:
        """Get maximum log file size before rotation"""
        return os.getenv("LOG_FILE_MAX_SIZE", "10MB")

    # ========================================================================
    # AZURE CONFIGURATION
    # ========================================================================

    @staticmethod
    def application_insights_connection_string() -> Optional[str]:
        """Get Application Insights connection string"""
        return os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")

    @staticmethod
    def azure_log_stream_enabled() -> bool:
        """Check if Azure log streaming is enabled"""
        return os.getenv("AZURE_LOG_STREAM", "true").lower() == "true"

    # ========================================================================
    # ENVIRONMENT DETECTION
    # ========================================================================

    @staticmethod
    def is_azure_environment() -> bool:
        """Check if running in Azure Functions environment"""
        return os.getenv("AZURE_FUNCTIONS_ENVIRONMENT") is not None

    @staticmethod
    def is_development_environment() -> bool:
        """Check if running in development environment"""
        environment = os.getenv("ENVIRONMENT", "").lower()
        return environment in ["development", "dev", "test", "testing"]

    @staticmethod
    def get_environment() -> str:
        """Get current environment name"""
        return os.getenv("ENVIRONMENT", "production").lower()

    # ========================================================================
    # CONFIGURATION VALIDATION
    # ========================================================================

    @classmethod
    def validate_configuration(cls) -> dict:
        """Validate logging configuration and return status"""
        validation_results = {"valid": True, "warnings": [], "errors": []}

        # Check if Azure integration is enabled but connection string is missing
        if (
            cls.azure_log_integration_enabled()
            and not cls.application_insights_connection_string()
        ):
            validation_results["warnings"].append(
                "Azure log integration enabled but APPLICATIONINSIGHTS_CONNECTION_STRING not set"
            )

        # Check log level validity
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if cls.log_level() not in valid_log_levels:
            validation_results["errors"].append(
                f"Invalid LOG_LEVEL: {cls.log_level()}. Must be one of {valid_log_levels}"
            )
            validation_results["valid"] = False

        # Check log rotation days
        if cls.log_rotation_days() < 1:
            validation_results["errors"].append(
                f"Invalid LOG_ROTATION_DAYS: {cls.log_rotation_days()}. Must be >= 1"
            )
            validation_results["valid"] = False

        return validation_results

    # ========================================================================
    # HELPER METHODS
    # ========================================================================

    @classmethod
    def get_configuration_summary(cls) -> dict:
        """Get complete configuration summary for debugging"""
        return {
            "log_level": cls.log_level(),
            "centralized_logging": cls.centralized_logging_enabled(),
            "log_rotation_days": cls.log_rotation_days(),
            "azure_integration": cls.azure_log_integration_enabled(),
            "console_logging": cls.log_to_console_enabled(),
            "max_file_size": cls.log_file_max_size(),
            "environment": cls.get_environment(),
            "is_azure": cls.is_azure_environment(),
            "is_development": cls.is_development_environment(),
            "azure_log_stream": cls.azure_log_stream_enabled(),
            "has_app_insights": cls.application_insights_connection_string()
            is not None,
        }


class LoggingSettings:
    """Application settings and constants for logging configuration"""

    # ========================================================================
    # LOGGING CONSTANTS
    # ========================================================================

    class LogLevels:
        """Standard logging levels"""

        DEBUG = "DEBUG"
        INFO = "INFO"
        WARNING = "WARNING"
        ERROR = "ERROR"
        CRITICAL = "CRITICAL"

    class LogFormats:
        """Standard log formats"""

        STANDARD = "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
        SIMPLE = "%(asctime)s - %(levelname)s - %(message)s"
        DETAILED = "%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(funcName)s() - %(message)s"

    class FileSettings:
        """File handling settings"""

        DEFAULT_ROTATION_DAYS = 7
        DEFAULT_MAX_SIZE = "10MB"
        DEFAULT_BACKUP_COUNT = 7

    # ========================================================================
    # FUNCTION NAME MAPPINGS
    # ========================================================================

    class FunctionNames:
        """Standardized function names for log files"""

        CRM_TO_BLOB = "crm_to_blob"
        PRICING_EXTRACTOR = "pricing_extractor"
        VISTAGE_FINANCIAL = "vistage_financial"
        AUTO_CONNECTOR = "auto_connector"
        WORKSPACE_CREATOR = "workspace_creator"
        CLOUD_PROJECT = "cloud_project"
        PROJECT_NUMBER_GEN = "project_number_gen"

    # ========================================================================
    # AZURE CONFIGURATION
    # ========================================================================

    class AzureSettings:
        """Azure-specific logging settings"""

        DEFAULT_LOG_LEVEL = "INFO"
        TELEMETRY_ENABLED = True
        TRACE_SAMPLING_RATE = 1.0  # 100% sampling for production
