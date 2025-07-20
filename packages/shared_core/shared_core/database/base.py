"""
Database Base Model

Provides base model class with common fields and pgvector support for all domain models.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, Optional
from sqlalchemy import Column, DateTime, String, text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector

# Create declarative base
Base = declarative_base()


class BaseModel(Base):
    """
    Abstract base model with common fields for all domain models
    """
    __abstract__ = True
    
    # Primary key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()")
    )
    
    # Audit timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        server_default=text("CURRENT_TIMESTAMP")
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=text("CURRENT_TIMESTAMP")
    )
    
    # Metadata for extensibility
    metadata_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        "metadata",
        JSONB,
        nullable=True
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model instance to dictionary"""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                result[column.name] = value.isoformat()
            elif isinstance(value, uuid.UUID):
                result[column.name] = str(value)
            else:
                result[column.name] = value
        return result
    
    def update_from_dict(self, data: Dict[str, Any]) -> None:
        """Update model instance from dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)


class EmbeddingMixin:
    """
    Mixin class to add vector embedding support to any model
    """
    
    # Text embedding for semantic search (OpenAI text-embedding-3-small: 1536 dimensions)
    text_embedding: Mapped[Optional[list]] = mapped_column(
        Vector(1536),
        nullable=True
    )
    
    # Content that was embedded
    embedded_content: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True
    )
    
    # Model used for embedding
    embedding_model: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        default="text-embedding-3-small"
    )


class CorrelationMixin:
    """
    Mixin class to add cross-domain correlation metadata to any model
    """
    
    # Cross-domain correlation metadata
    correlation_metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSONB,
        nullable=True,
        comment="Stores links and correlations to entities in other domains"
    )
    
    # Entity linking confidence scores
    entity_links: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSONB,
        nullable=True,
        comment="Stores entity resolution links with confidence scores"
    )


class TimestampMixin:
    """
    Mixin for models that need additional timestamp tracking
    """
    
    # Source-specific timestamps (e.g., created_at from API)
    source_created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    source_updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    # Last sync timestamp
    last_synced_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=datetime.utcnow
    )
