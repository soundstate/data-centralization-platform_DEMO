import logging
import os
from datetime import datetime
from typing import Optional

from .centralized_logging import CentralizedLogger


def program_start(
    program_name: str,
    version: str = "1.0.0",
    last_updated: Optional[str] = None,
    creator: str = "System",
    log_level: str = "INFO",
    azure_integration: Optional[bool] = None,
    **kwargs,
) -> logging.Logger:
    """
    Initialize program startup with centralized logging and environment detection.

    Args:
        program_name: Name of the function/service
        version: Version string
        last_updated: Last update date
        creator: Developer name
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        azure_integration: Enable Azure Monitor integration (auto-detects if None)
        **kwargs: Additional arguments (for backward compatibility)

    Returns:
        Configured centralized logger instance
    """
    # Convert program name to standardized function name
    function_name = program_name.lower().replace(" ", "_")

    # Create centralized logger
    logger = CentralizedLogger.get_logger(
        function_name=function_name,
        log_level=log_level,
        azure_integration=azure_integration,
    )

    # Auto-detect environment and testing mode
    environment = os.getenv("ENVIRONMENT", "production").lower()
    is_testing = environment in ["development", "dev", "test", "testing"]
    mode = "testing" if is_testing else "production"

    # Format last_updated date
    if last_updated is None:
        last_updated = "Unknown"

    # Startup banner logging
    logger.info("=" * 60)
    logger.info(f"Starting Jobe Systems {program_name} v{version}")
    logger.info(f"Environment: {environment}")
    logger.info(f"Mode: {mode}")
    logger.info(f"Creator: {creator}")
    logger.info(f"Last updated: {last_updated}")
    logger.info(f"Started at: {datetime.now().isoformat()}")
    logger.info(f"Log level: {log_level}")
    logger.info(
        f"Azure integration: {'enabled' if azure_integration else 'disabled'}"
    )
    logger.info("=" * 60)

    return logger


def program_end(logger: logging.Logger, program_name: str) -> None:
    """
    Log program completion with centralized logging.

    Args:
        logger: Logger instance from program_start
        program_name: Name of the function/service
    """
    logger.info("=" * 60)
    logger.info(f"{program_name} completed successfully")
    logger.info(f"Finished at: {datetime.now().isoformat()}")
    logger.info("=" * 60)
