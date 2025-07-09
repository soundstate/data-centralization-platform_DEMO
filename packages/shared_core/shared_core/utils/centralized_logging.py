import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


class CentralizedLogger:
    """Centralized logging configuration for all functions"""

    @staticmethod
    def get_logs_directory() -> Path:
        """Get the centralized logs directory path"""
        current_path = Path(__file__)
        repo_root = current_path

        while repo_root.parent != repo_root:
            if (repo_root / "packages").exists() and (repo_root / "functions").exists():
                break
            repo_root = repo_root.parent

        logs_dir = repo_root / "logs" / "functions"
        logs_dir.mkdir(parents=True, exist_ok=True)
        return logs_dir

    @classmethod
    def get_logger(
        cls,
        function_name: str,
        log_level: str | None = None,
        azure_integration: bool | None = None,
    ) -> logging.Logger:
        """Get configured logger for a function"""

        log_level = log_level or os.getenv("LOG_LEVEL", "INFO")
        azure_integration = (
            azure_integration
            or os.getenv("AZURE_LOG_INTEGRATION", "false").lower() == "true"
        )

        logger = logging.getLogger(function_name)
        logger.setLevel(getattr(logging, log_level.upper()))

        logger.handlers.clear()

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
        )

        if os.getenv("CENTRALIZED_LOGGING", "true").lower() == "true":
            log_file = cls.get_log_file_path(function_name)
            file_handler = TimedRotatingFileHandler(
                log_file,
                when="midnight",
                interval=1,
                backupCount=int(os.getenv("LOG_ROTATION_DAYS", "7")),
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        if os.getenv("LOG_TO_CONSOLE", "true").lower() == "true":
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        if azure_integration:
            cls._add_azure_handler(logger, formatter)

        return logger

    @classmethod
    def get_log_file_path(cls, function_name: str) -> Path:
        """Generate standardized log file path"""
        logs_dir = cls.get_logs_directory()
        date_str = datetime.now().strftime("%Y%m%d")
        return logs_dir / f"{function_name}_{date_str}.log"

    @staticmethod
    def _add_azure_handler(logger: logging.Logger, formatter: logging.Formatter):
        """Add Azure Application Insights handler if available"""
        try:
            # Try multiple Azure logging options in order of preference
            connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
            if connection_string:
                try:
                    # Option 1: OpenCensus Azure Monitor (more common in Azure Functions)
                    from opencensus.ext.azure.log_exporter import AzureLogHandler

                    azure_handler = AzureLogHandler(connection_string=connection_string)
                    azure_handler.setFormatter(formatter)
                    logger.addHandler(azure_handler)
                except ImportError:
                    try:
                        # Option 2: Azure Monitor OpenTelemetry (newer approach)
                        from azure.monitor.opentelemetry import configure_azure_monitor

                        configure_azure_monitor(connection_string=connection_string)
                    except ImportError:
                        # Option 3: Azure Functions built-in logging (fallback)
                        pass
        except Exception as e:
            # Log warning but don't fail - Azure integration is optional
            print(f"Warning: Could not configure Azure logging: {e}")
            pass
