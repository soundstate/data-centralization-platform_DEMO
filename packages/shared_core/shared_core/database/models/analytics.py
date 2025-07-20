"""
Analytics and Raw Data Models

SQLAlchemy models for correlation analysis, time series data, embeddings, and API audit trail.
These models support the core analytical capabilities of the platform.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, Integer, Numeric, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

from ..base import BaseModel, EmbeddingMixin, CorrelationMixin, TimestampMixin


# ================================
# RAW DATA AND AUDIT MODELS
# ================================

class APIResponse(BaseModel):
    """
    Raw API response audit trail for all external API calls
    """
    __tablename__ = 'api_responses'
    __table_args__ = {'schema': 'raw_data'}
    
    # API identification
    api_source: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    endpoint: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    
    # Request details
    request_params: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB)
    request_method: Mapped[Optional[str]] = mapped_column(String(10))
    request_headers: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB)
    
    # Response details
    response_data: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)
    status_code: Mapped[Optional[int]] = mapped_column(Integer, index=True)
    response_time_ms: Mapped[Optional[int]] = mapped_column(Integer)
    response_headers: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB)
    
    # Processing information
    processed: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    processed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    processing_errors: Mapped[Optional[List[str]]] = mapped_column(JSONB)
    
    def is_successful(self) -> bool:
        """Check if API response was successful"""
        return self.status_code and 200 <= self.status_code < 300
    
    def get_response_size(self) -> Optional[int]:
        """Estimate response size in bytes"""
        if self.response_data:
            import json
            return len(json.dumps(self.response_data).encode('utf-8'))
        return None
    
    def __repr__(self):
        return f"<APIResponse(source='{self.api_source}', endpoint='{self.endpoint}', status={self.status_code})>"


class DataEntity(BaseModel, EmbeddingMixin, CorrelationMixin, TimestampMixin):
    """
    General cross-domain entity model for entity resolution and linking
    """
    __tablename__ = 'entities'
    __table_args__ = {'schema': 'general'}
    
    # Entity classification
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    entity_name: Mapped[str] = mapped_column(String(500), nullable=False)
    entity_description: Mapped[Optional[str]] = mapped_column(Text)
    
    # Source domain information
    source_domain: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    source_id: Mapped[Optional[str]] = mapped_column(String, index=True)  # ID in source domain
    source_external_id: Mapped[Optional[str]] = mapped_column(String(200))  # External API ID
    
    # Entity properties for correlation
    properties: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB)
    
    # Confidence scores for entity resolution
    resolution_confidence: Mapped[Optional[Decimal]] = mapped_column(Numeric(3, 2))
    
    # Relationships
    relationships_as_entity1: Mapped[List["EntityRelationship"]] = relationship(
        "EntityRelationship",
        foreign_keys="[EntityRelationship.entity1_id]",
        back_populates="entity1"
    )
    relationships_as_entity2: Mapped[List["EntityRelationship"]] = relationship(
        "EntityRelationship", 
        foreign_keys="[EntityRelationship.entity2_id]",
        back_populates="entity2"
    )
    
    def __repr__(self):
        return f"<DataEntity(type='{self.entity_type}', name='{self.entity_name}', domain='{self.source_domain}')>"


class EntityRelationship(BaseModel, CorrelationMixin):
    """
    Relationships between entities across different domains
    """
    __tablename__ = 'entity_relationships'
    __table_args__ = {'schema': 'general'}
    
    # Entity references
    entity1_id: Mapped[str] = mapped_column(ForeignKey('general.entities.id'), index=True)
    entity2_id: Mapped[str] = mapped_column(ForeignKey('general.entities.id'), index=True)
    
    # Relationship details
    relationship_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    relationship_strength: Mapped[Optional[Decimal]] = mapped_column(Numeric(3, 2))
    confidence_score: Mapped[Optional[Decimal]] = mapped_column(Numeric(3, 2))
    
    # Evidence for relationship
    evidence_type: Mapped[Optional[str]] = mapped_column(String(100))
    evidence_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB)
    
    # Bi-directional flag
    is_bidirectional: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Relationships
    entity1: Mapped["DataEntity"] = relationship(
        "DataEntity",
        foreign_keys=[entity1_id],
        back_populates="relationships_as_entity1"
    )
    entity2: Mapped["DataEntity"] = relationship(
        "DataEntity",
        foreign_keys=[entity2_id], 
        back_populates="relationships_as_entity2"
    )
    
    def __repr__(self):
        return f"<EntityRelationship(type='{self.relationship_type}', strength={self.relationship_strength})>"


# ================================
# CORRELATION ANALYSIS MODELS
# ================================

class Correlation(BaseModel):
    """
    Statistical correlation results between variables across domains
    """
    __tablename__ = 'correlations'
    __table_args__ = {'schema': 'analytics'}
    
    # Correlation identification
    correlation_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    correlation_id: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
    
    # Domain and variable information
    domain1: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    domain2: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    variable1: Mapped[str] = mapped_column(String(200), nullable=False)
    variable2: Mapped[str] = mapped_column(String(200), nullable=False)
    
    # Statistical measures
    correlation_coefficient: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 8))
    p_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 8))
    confidence_interval: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, comment="""
    Confidence interval data:
    - lower_bound: Lower CI bound
    - upper_bound: Upper CI bound
    - confidence_level: CI level (e.g., 0.95)
    """)
    
    # Sample and methodology information
    sample_size: Mapped[Optional[int]] = mapped_column(Integer)
    degrees_of_freedom: Mapped[Optional[int]] = mapped_column(Integer)
    analysis_method: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Significance testing
    is_significant: Mapped[Optional[bool]] = mapped_column(Boolean, index=True)
    significance_level: Mapped[Optional[Decimal]] = mapped_column(Numeric(3, 2))
    effect_size: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 8))
    
    # Multiple testing correction
    corrected_p_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 8))
    correction_method: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Time period for analysis
    analysis_start_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    analysis_end_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Additional analysis data
    outliers_removed: Mapped[Optional[int]] = mapped_column(Integer)
    data_transformations: Mapped[Optional[List[str]]] = mapped_column(JSONB)
    
    def get_correlation_strength(self) -> str:
        """Categorize correlation strength for interpretation"""
        if not self.correlation_coefficient:
            return "unknown"
        
        coeff = abs(float(self.correlation_coefficient))
        
        if coeff >= 0.7:
            return "strong"
        elif coeff >= 0.5:
            return "moderate"
        elif coeff >= 0.3:
            return "weak"
        else:
            return "very_weak"
    
    def is_statistically_significant(self, alpha: float = 0.05) -> bool:
        """Check statistical significance at given alpha level"""
        if self.corrected_p_value is not None:
            return float(self.corrected_p_value) < alpha
        elif self.p_value is not None:
            return float(self.p_value) < alpha
        else:
            return False
    
    def __repr__(self):
        return f"<Correlation({self.domain1}.{self.variable1} ↔ {self.domain2}.{self.variable2}, r={self.correlation_coefficient})>"


class TimeSeriesData(BaseModel):
    """
    Time series data for temporal correlation analysis
    """
    __tablename__ = 'time_series_data'
    __table_args__ = {'schema': 'analytics'}
    
    # Domain and metric identification
    domain: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    metric_name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    metric_category: Mapped[Optional[str]] = mapped_column(String(100), index=True)
    
    # Value and timestamp
    metric_value: Mapped[Decimal] = mapped_column(Numeric(15, 5), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    
    # Aggregation information
    aggregation_level: Mapped[Optional[str]] = mapped_column(String(50))  # hour, day, week, month
    aggregation_function: Mapped[Optional[str]] = mapped_column(String(50))  # mean, sum, count, etc.
    
    # Data quality indicators
    data_quality_score: Mapped[Optional[Decimal]] = mapped_column(Numeric(3, 2))
    is_outlier: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    imputed: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Source information
    source_entity_id: Mapped[Optional[str]] = mapped_column(String)
    source_api_response_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey('raw_data.api_responses.id')
    )
    
    def get_time_of_day_category(self) -> str:
        """Categorize time of day for temporal correlation analysis"""
        hour = self.timestamp.hour
        
        if 6 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon" 
        elif 17 <= hour < 21:
            return "evening"
        else:
            return "night"
    
    def get_day_of_week_category(self) -> str:
        """Get day of week category"""
        weekday = self.timestamp.weekday()
        
        if weekday < 5:  # Monday = 0, Friday = 4
            return "weekday"
        else:
            return "weekend"
    
    def __repr__(self):
        return f"<TimeSeriesData(domain='{self.domain}', metric='{self.metric_name}', value={self.metric_value}, time='{self.timestamp}')>"


# ================================
# EMBEDDING AND LLM MODELS
# ================================

class Embedding(BaseModel):
    """
    Vector embeddings for semantic search across all domains
    """
    __tablename__ = 'embeddings'
    __table_args__ = {'schema': 'llm'}
    
    # Source information
    source_domain: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    source_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    content_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    
    # Content and embedding
    content_text: Mapped[str] = mapped_column(Text, nullable=False)
    content_hash: Mapped[Optional[str]] = mapped_column(String(64), index=True)  # SHA-256 hash
    
    # Vector embedding (OpenAI text-embedding-3-small: 1536 dimensions)
    embedding: Mapped[List[float]] = mapped_column(Vector(1536), nullable=False)
    
    # Model information
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    model_version: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Processing information
    token_count: Mapped[Optional[int]] = mapped_column(Integer)
    processing_time_ms: Mapped[Optional[int]] = mapped_column(Integer)
    
    def __repr__(self):
        return f"<Embedding(domain='{self.source_domain}', type='{self.content_type}', model='{self.model_name}')>"


class CorrelationInsight(BaseModel, EmbeddingMixin):
    """
    Generated insights about correlations for LLM-powered analysis
    """
    __tablename__ = 'correlation_insights'
    __table_args__ = {'schema': 'llm'}
    
    # Reference to correlation
    correlation_id: Mapped[str] = mapped_column(ForeignKey('analytics.correlations.id'), index=True)
    
    # Insight content
    insight_title: Mapped[str] = mapped_column(String(500), nullable=False)
    insight_description: Mapped[str] = mapped_column(Text, nullable=False)
    insight_summary: Mapped[Optional[str]] = mapped_column(String(1000))
    
    # Insight categorization
    insight_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    significance_level: Mapped[str] = mapped_column(String(50))  # high, medium, low
    
    # Business relevance
    business_impact: Mapped[Optional[str]] = mapped_column(String(50))  # high, medium, low, none
    actionable_items: Mapped[Optional[List[str]]] = mapped_column(JSONB)
    
    # Generation information
    generated_by_model: Mapped[str] = mapped_column(String(100), nullable=False)
    generation_prompt: Mapped[Optional[str]] = mapped_column(Text)
    
    # Validation
    validated: Mapped[bool] = mapped_column(Boolean, default=False)
    validation_score: Mapped[Optional[Decimal]] = mapped_column(Numeric(3, 2))
    
    def __repr__(self):
        return f"<CorrelationInsight(title='{self.insight_title}', type='{self.insight_type}', impact='{self.business_impact}')>"
