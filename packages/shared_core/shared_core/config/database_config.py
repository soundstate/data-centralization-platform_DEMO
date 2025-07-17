"""
Database Configuration Management

This module provides centralized database configuration for the Data Centralization Platform.
It handles PostgreSQL connection management, including pgvector support for vector operations.
"""

import os
from typing import Optional, Dict, Any
from urllib.parse import urlparse

from ..utils.centralized_logging import CentralizedLogger
from .unified_environment_loader import UnifiedEnvironmentLoader

# Initialize logger
logger = CentralizedLogger.get_logger("database_config")

class DatabaseConfig:
    """
    Centralized database configuration management for PostgreSQL + pgvector
    """
    
    _instance: Optional["DatabaseConfig"] = None
    
    def __new__(cls, *args, **kwargs):
        """Singleton pattern to ensure single instance"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize database configuration"""
        if hasattr(self, '_initialized'):
            return
        
        # Ensure environment is loaded
        UnifiedEnvironmentLoader.ensure_environment_loaded()
        
        self._initialized = True
        logger.info("Database configuration initialized")
    
    @staticmethod
    def database_url() -> str:
        """
        Get the complete database URL for SQLAlchemy
        
        Returns:
            str: Complete database URL
        """
        # Check for complete DATABASE_URL first
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            # Ensure it's using postgresql+asyncpg for async support
            if database_url.startswith("postgresql://"):
                database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
            elif database_url.startswith("postgres://"):
                database_url = database_url.replace("postgres://", "postgresql+asyncpg://", 1)
            return database_url
        
        # Build URL from components
        host = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", "5432")
        database = os.getenv("POSTGRES_DB", "data_centralization")
        user = os.getenv("POSTGRES_USER", "postgres")
        password = os.getenv("POSTGRES_PASSWORD", "postgres")
        
        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
    
    @staticmethod
    def sync_database_url() -> str:
        """
        Get the synchronous database URL for SQLAlchemy
        
        Returns:
            str: Synchronous database URL
        """
        async_url = DatabaseConfig.database_url()
        return async_url.replace("postgresql+asyncpg://", "postgresql://", 1)
    
    @staticmethod
    def redis_url() -> str:
        """
        Get the Redis URL for caching and task queues
        
        Returns:
            str: Redis connection URL
        """
        redis_url = os.getenv("REDIS_URL")
        if redis_url:
            return redis_url
        
        # Build URL from components
        host = os.getenv("REDIS_HOST", "localhost")
        port = os.getenv("REDIS_PORT", "6379")
        db = os.getenv("REDIS_DB", "0")
        password = os.getenv("REDIS_PASSWORD", "")
        
        if password:
            return f"redis://:{password}@{host}:{port}/{db}"
        else:
            return f"redis://{host}:{port}/{db}"
    
    @staticmethod
    def get_database_info() -> Dict[str, Any]:
        """
        Get database connection information for debugging
        
        Returns:
            Dict[str, Any]: Database connection details (with masked password)
        """
        url = DatabaseConfig.database_url()
        parsed = urlparse(url)
        
        return {
            "scheme": parsed.scheme,
            "host": parsed.hostname,
            "port": parsed.port,
            "database": parsed.path.lstrip("/"),
            "username": parsed.username,
            "password": "***MASKED***" if parsed.password else None,
            "full_url": url.replace(parsed.password or "", "***MASKED***") if parsed.password else url
        }
    
    @staticmethod
    def get_redis_info() -> Dict[str, Any]:
        """
        Get Redis connection information for debugging
        
        Returns:
            Dict[str, Any]: Redis connection details (with masked password)
        """
        url = DatabaseConfig.redis_url()
        parsed = urlparse(url)
        
        return {
            "scheme": parsed.scheme,
            "host": parsed.hostname,
            "port": parsed.port,
            "database": parsed.path.lstrip("/"),
            "password": "***MASKED***" if parsed.password else None,
            "full_url": url.replace(parsed.password or "", "***MASKED***") if parsed.password else url
        }
    
    @staticmethod
    def validate_database_connection() -> bool:
        """
        Validate database connection parameters
        
        Returns:
            bool: True if all required parameters are available
        """
        required_vars = [
            "POSTGRES_HOST", "POSTGRES_PORT", "POSTGRES_DB", 
            "POSTGRES_USER", "POSTGRES_PASSWORD"
        ]
        
        # Check if DATABASE_URL is provided (overrides individual vars)
        if os.getenv("DATABASE_URL"):
            logger.info("Using DATABASE_URL for database connection")
            return True
        
        # Check individual variables
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            logger.error(f"Missing database configuration variables: {missing_vars}")
            return False
        
        logger.info("Database configuration validation successful")
        return True
    
    @staticmethod
    def get_sqlalchemy_config() -> Dict[str, Any]:
        """
        Get SQLAlchemy engine configuration
        
        Returns:
            Dict[str, Any]: SQLAlchemy engine configuration
        """
        return {
            "pool_size": int(os.getenv("DB_POOL_SIZE", "10")),
            "max_overflow": int(os.getenv("DB_MAX_OVERFLOW", "20")),
            "pool_pre_ping": True,
            "pool_recycle": int(os.getenv("DB_POOL_RECYCLE", "300")),
            "connect_args": {
                "server_settings": {
                    "application_name": "data_centralization_platform",
                    "statement_timeout": os.getenv("DB_STATEMENT_TIMEOUT", "30000")
                }
            }
        }
    
    @staticmethod
    def get_alembic_config() -> Dict[str, Any]:
        """
        Get Alembic configuration for database migrations
        
        Returns:
            Dict[str, Any]: Alembic configuration
        """
        return {
            "sqlalchemy.url": DatabaseConfig.sync_database_url(),
            "script_location": "packages/shared_core/shared_core/database/migrations",
            "file_template": "%%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s",
            "truncate_slug_length": 40,
            "version_table": "alembic_version",
            "version_table_schema": "public",
            "compare_type": True,
            "compare_server_default": True,
            "render_as_batch": False
        }
    
    @classmethod
    def get_instance(cls) -> "DatabaseConfig":
        """Get the singleton instance of DatabaseConfig"""
        return cls()

# Convenience functions for backward compatibility
def get_database_url() -> str:
    """Get the database URL"""
    return DatabaseConfig.database_url()

def get_sync_database_url() -> str:
    """Get the synchronous database URL"""
    return DatabaseConfig.sync_database_url()

def get_redis_url() -> str:
    """Get the Redis URL"""
    return DatabaseConfig.redis_url()

def validate_database_config() -> bool:
    """Validate database configuration"""
    return DatabaseConfig.validate_database_connection()

# Initialize configuration on module import
_config = DatabaseConfig.get_instance()
logger.info("Database configuration module loaded")
