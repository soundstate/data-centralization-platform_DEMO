"""
Alembic Environment Configuration

Sets up the migration environment for the Data Centralization Platform
with support for multiple schemas and pgvector extension.
"""

import asyncio
from logging.config import fileConfig

from sqlalchemy import pool, text
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Import all models for autogenerate support
from shared_core.database.models import Base
from shared_core.config.database_config import DatabaseConfig

# This is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add model's MetaData object for 'autogenerate' support
target_metadata = Base.metadata

# Get database URL from configuration
db_config = DatabaseConfig.get_instance()
database_url = db_config.database_url()

# Update Alembic config with actual database URL
config.set_main_option('sqlalchemy.url', database_url)

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # Include all schemas in migration
        include_schemas=True,
        # Support for schema creation
        version_table_schema='public'
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Run migrations with database connection."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        # Include all schemas
        include_schemas=True,
        # Create schemas if they don't exist
        compare_type=True,
        compare_server_default=True,
        version_table_schema='public'
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in async mode."""
    
    # Create async engine configuration
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # Enable pgvector extension if not exists
        await connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        await connection.execute(text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"))
        
        # Create schemas if they don't exist
        schemas = ['music', 'entertainment', 'weather', 'gaming', 'development', 
                  'productivity', 'general', 'raw_data', 'analytics', 'llm']
        
        for schema in schemas:
            await connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema};"))
        
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
