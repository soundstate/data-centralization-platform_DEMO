"""
Logging configuration for the shared_core package
"""

import logging
import sys
from typing import Optional


def get_logger(name: str, level: int = logging.DEBUG) -> logging.Logger:
    """
    Get a configured logger instance
    
    Args:
        name: Logger name
        level: Logging level
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Only add handlers if not already configured
    if not logger.handlers:
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(console_handler)
        logger.setLevel(level)
        
        # Prevent duplicate logs
        logger.propagate = False
    
    return logger
