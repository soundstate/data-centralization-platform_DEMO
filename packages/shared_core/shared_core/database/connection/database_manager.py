"""
Database Connection Management

This module provides centralized database connection management for the Data Centralization Platform.
It supports both synchronous and asynchronous connections with proper connection pooling.
"""

import asyncio
from contextlib import asynccontextmanager
from typing import Optional, AsyncGenerator, Dict, Any
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool

from ..config.database_config import DatabaseConfig
from ..utils.centralized_logging import CentralizedLogger

# Initialize logger
logger = CentralizedLogger.get_logger("database_manager")

class DatabaseManager:
    """
    Centralized database connection manager with async support
    """
    
    _instance: Optional["DatabaseManager"] = None
    _async_engine = None
    _sync_engine = None
    _async_session_maker = None
    _sync_session_maker = None
    
    def __new__(cls, *args, **kwargs):
        """Singleton pattern to ensure single instance"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize database manager"""
        if hasattr(self, '_initialized'):
            return
        
        self.config = DatabaseConfig.get_instance()
        self._initialized = True
        logger.info("Database manager initialized")
    
    def _create_async_engine(self):
        """Create async SQLAlchemy engine"""
        if self._async_engine is None:
            url = self.config.database_url()
            engine_config = self.config.get_sqlalchemy_config()
            
            # Remove synchronous-only config options
            async_config = {k: v for k, v in engine_config.items() 
                          if k not in ['connect_args']}
            
            logger.info(f"Creating async database engine: {url.split('@')[0]}@***")
            
            self._async_engine = create_async_engine(
                url,
                echo=False,  # Set to True for SQL debug logging
                **async_config
            )
            
            # Create async session maker
            self._async_session_maker = async_sessionmaker(
                self._async_engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
        
        return self._async_engine
    
    def _create_sync_engine(self):
        """Create synchronous SQLAlchemy engine"""
        if self._sync_engine is None:
            url = self.config.sync_database_url()
            engine_config = self.config.get_sqlalchemy_config()
            
            logger.info(f"Creating sync database engine: {url.split('@')[0]}@***")
            
            self._sync_engine = create_engine(
                url,
                echo=False,  # Set to True for SQL debug logging
                **engine_config
            )
            
            # Create session maker
            self._sync_session_maker = sessionmaker(
                self._sync_engine,
                expire_on_commit=False
            )
        
        return self._sync_engine
    
    @property
    def async_engine(self):
        """Get async SQLAlchemy engine"""
        return self._create_async_engine()
    
    @property
    def sync_engine(self):
        """Get sync SQLAlchemy engine"""
        return self._create_sync_engine()
    
    @asynccontextmanager
    async def async_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Async context manager for database sessions
        
        Usage:
            async with db_manager.async_session() as session:
                # Use session for database operations
        """
        if self._async_session_maker is None:
            self._create_async_engine()
        
        async with self._async_session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                logger.error(f"Database session error: {e}")
                raise
            finally:
                await session.close()
    
    @asynccontextmanager
    async def sync_session(self) -> AsyncGenerator[Session, None]:
        """
        Sync context manager for database sessions
        
        Usage:
            with db_manager.sync_session() as session:
                # Use session for database operations
        """
        if self._sync_session_maker is None:
            self._create_sync_engine()
        
        with self._sync_session_maker() as session:
            try:
                yield session
                session.commit()
            except Exception as e:
                session.rollback()
                logger.error(f"Database session error: {e}")
                raise
            finally:
                session.close()
    
    async def test_async_connection(self) -> bool:
        """
        Test async database connection
        
        Returns:
            bool: True if connection successful
        """
        try:
            async with self.async_session() as session:
                result = await session.execute(text("SELECT 1"))
                test_value = result.scalar()
                if test_value == 1:
                    logger.info("Async database connection test successful")
                    return True
                else:
                    logger.error("Async database connection test failed")
                    return False
        except Exception as e:
            logger.error(f"Async database connection test error: {e}")
            return False
    
    def test_sync_connection(self) -> bool:
        """
        Test sync database connection
        
        Returns:
            bool: True if connection successful
        """
        try:
            with self.sync_session() as session:
                result = session.execute(text("SELECT 1"))
                test_value = result.scalar()
                if test_value == 1:
                    logger.info("Sync database connection test successful")
                    return True
                else:
                    logger.error("Sync database connection test failed")
                    return False
        except Exception as e:
            logger.error(f"Sync database connection test error: {e}")
            return False
    
    async def check_pgvector_extension(self) -> bool:
        """
        Check if pgvector extension is available
        
        Returns:
            bool: True if pgvector is available
        """
        try:
            async with self.async_session() as session:
                result = await session.execute(
                    text("SELECT 1 FROM pg_extension WHERE extname = 'vector'")
                )
                if result.scalar():
                    logger.info("pgvector extension is available")
                    return True
                else:
                    logger.warning("pgvector extension is not installed")
                    return False
        except Exception as e:
            logger.error(f"Error checking pgvector extension: {e}")
            return False
    
    async def get_database_info(self) -> Dict[str, Any]:
        """
        Get database information for debugging
        
        Returns:
            Dict[str, Any]: Database information
        """
        try:
            async with self.async_session() as session:
                # Get PostgreSQL version
                version_result = await session.execute(text("SELECT version()"))
                version = version_result.scalar()
                
                # Get database size
                size_result = await session.execute(
                    text("SELECT pg_size_pretty(pg_database_size(current_database()))")
                )
                size = size_result.scalar()
                
                # Get schema count
                schema_result = await session.execute(
                    text("""
                    SELECT COUNT(*) FROM information_schema.schemata 
                    WHERE schema_name NOT IN ('information_schema', 'pg_catalog', 'pg_toast')
                    """)
                )
                schema_count = schema_result.scalar()
                
                # Get table count
                table_result = await session.execute(
                    text("""
                    SELECT COUNT(*) FROM information_schema.tables 
                    WHERE table_schema NOT IN ('information_schema', 'pg_catalog', 'pg_toast')
                    """)
                )
                table_count = table_result.scalar()
                
                # Check extensions
                extensions_result = await session.execute(
                    text("SELECT extname FROM pg_extension ORDER BY extname")
                )
                extensions = [row[0] for row in extensions_result.fetchall()]
                
                return {
                    "version": version,
                    "size": size,
                    "schema_count": schema_count,
                    "table_count": table_count,
                    "extensions": extensions,
                    "pgvector_available": "vector" in extensions
                }
        except Exception as e:
            logger.error(f"Error getting database info: {e}")
            return {"error": str(e)}
    
    async def close_connections(self):
        """Close all database connections"""
        try:
            if self._async_engine:
                await self._async_engine.dispose()
                logger.info("Async database connections closed")
            
            if self._sync_engine:
                self._sync_engine.dispose()
                logger.info("Sync database connections closed")
        except Exception as e:
            logger.error(f"Error closing database connections: {e}")
    
    @classmethod
    def get_instance(cls) -> "DatabaseManager":
        """Get the singleton instance of DatabaseManager"""
        return cls()

# Global database manager instance
db_manager = DatabaseManager.get_instance()

# Convenience functions
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session"""
    async with db_manager.async_session() as session:
        yield session

def get_sync_session() -> Session:
    """Get sync database session"""
    return db_manager._sync_session_maker()

async def test_database_connection() -> bool:
    """Test database connection"""
    return await db_manager.test_async_connection()

async def check_database_health() -> Dict[str, Any]:
    """Check database health and get info"""
    return await db_manager.get_database_info()

# Initialize on module import
logger.info("Database manager module loaded")
