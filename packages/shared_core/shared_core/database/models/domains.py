"""
Additional Domain Models

SQLAlchemy models for Gaming, Development, and Productivity domains.
Consolidated file for remaining domain models with correlation support.
"""

from typing import List, Optional, Dict, Any
from datetime import date, datetime
from sqlalchemy import String, Integer, Boolean, Date, DateTime, ARRAY, Text, BigInteger, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import BaseModel, EmbeddingMixin, CorrelationMixin, TimestampMixin


# ================================
# GAMING DOMAIN MODELS
# ================================

class Pokemon(BaseModel, EmbeddingMixin, CorrelationMixin, TimestampMixin):
    """
    Pokémon model with stats and characteristics for correlation analysis
    """
    __tablename__ = 'pokemon'
    __table_args__ = {'schema': 'gaming'}
    
    # External IDs
    pokemon_id: Mapped[Optional[int]] = mapped_column(Integer, unique=True)
    
    # Basic information
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    height: Mapped[Optional[int]] = mapped_column(Integer)  # decimeters
    weight: Mapped[Optional[int]] = mapped_column(Integer)  # hectograms
    base_experience: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Classification
    types: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
    abilities: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
    
    # Stats for correlation analysis
    stats: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, comment="""
    Pokémon base stats:
    - hp: Hit Points
    - attack: Physical attack power
    - defense: Physical defense
    - special-attack: Special attack power
    - special-defense: Special defense
    - speed: Speed stat
    """)
    
    # Move set
    moves: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
    
    # External references
    species_url: Mapped[Optional[str]] = mapped_column(String(200))
    sprite_urls: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB)
    
    def get_stat(self, stat_name: str) -> Optional[int]:
        """Get specific stat value"""
        if self.stats and stat_name in self.stats:
            return int(self.stats[stat_name])
        return None
    
    def get_total_stats(self) -> Optional[int]:
        """Calculate total base stats"""
        if not self.stats:
            return None
        
        stat_names = ['hp', 'attack', 'defense', 'special-attack', 'special-defense', 'speed']
        total = 0
        
        for stat in stat_names:
            value = self.get_stat(stat)
            if value:
                total += value
        
        return total if total > 0 else None
    
    def get_primary_type(self) -> Optional[str]:
        """Get primary type for correlation analysis"""
        if self.types and len(self.types) > 0:
            return self.types[0].lower()
        return None
    
    def __repr__(self):
        return f"<Pokemon(name='{self.name}', id={self.pokemon_id}, types={self.types})>"


class PokemonSpecies(BaseModel, EmbeddingMixin, CorrelationMixin, TimestampMixin):
    """
    Pokémon species model with evolutionary and habitat data
    """
    __tablename__ = 'pokemon_species'
    __table_args__ = {'schema': 'gaming'}
    
    # External IDs
    species_id: Mapped[Optional[int]] = mapped_column(Integer, unique=True)
    
    # Basic information
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    generation: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Physical characteristics
    color: Mapped[Optional[str]] = mapped_column(String(50))
    shape: Mapped[Optional[str]] = mapped_column(String(50))
    habitat: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Gameplay characteristics
    capture_rate: Mapped[Optional[int]] = mapped_column(Integer)
    base_happiness: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Special classifications
    is_legendary: Mapped[Optional[bool]] = mapped_column(Boolean)
    is_mythical: Mapped[Optional[bool]] = mapped_column(Boolean)
    
    # Evolution data
    evolution_chain_id: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Flavor text for embedding
    flavor_text: Mapped[Optional[str]] = mapped_column(Text)
    
    def __repr__(self):
        return f"<PokemonSpecies(name='{self.name}', generation='{self.generation}', legendary={self.is_legendary})>"


# ================================
# DEVELOPMENT DOMAIN MODELS
# ================================

class GitHubRepository(BaseModel, EmbeddingMixin, CorrelationMixin, TimestampMixin):
    """
    GitHub repository model with development metrics for correlation analysis
    """
    __tablename__ = 'github_repositories'
    __table_args__ = {'schema': 'development'}
    
    # External IDs
    github_id: Mapped[Optional[int]] = mapped_column(BigInteger, unique=True)
    
    # Repository identification
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(400))
    owner_login: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Repository information
    description: Mapped[Optional[str]] = mapped_column(Text)
    language: Mapped[Optional[str]] = mapped_column(String(100))
    languages: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB)  # Language breakdown
    
    # Repository metrics - key for correlation analysis
    size: Mapped[Optional[int]] = mapped_column(Integer)  # KB
    stargazers_count: Mapped[Optional[int]] = mapped_column(Integer)
    watchers_count: Mapped[Optional[int]] = mapped_column(Integer)
    forks_count: Mapped[Optional[int]] = mapped_column(Integer)
    open_issues_count: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Categorization
    topics: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
    license: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Repository properties
    is_private: Mapped[Optional[bool]] = mapped_column(Boolean)
    is_fork: Mapped[Optional[bool]] = mapped_column(Boolean)
    
    # Timestamps from GitHub
    created_at_github: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    updated_at_github: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    pushed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # URLs
    clone_url: Mapped[Optional[str]] = mapped_column(String(400))
    html_url: Mapped[Optional[str]] = mapped_column(String(400))
    
    # Relationships
    commits: Mapped[List["GitHubCommit"]] = relationship("GitHubCommit", back_populates="repository")
    
    def get_popularity_score(self) -> float:
        """Calculate popularity score for correlation analysis"""
        stars = self.stargazers_count or 0
        forks = self.forks_count or 0
        watchers = self.watchers_count or 0
        
        # Weighted popularity score
        return (stars * 1.0) + (forks * 2.0) + (watchers * 0.5)
    
    def get_activity_level(self) -> str:
        """Categorize repository activity level"""
        if not self.pushed_at:
            return "inactive"
        
        from datetime import datetime, timedelta
        now = datetime.utcnow().replace(tzinfo=self.pushed_at.tzinfo)
        days_since_push = (now - self.pushed_at).days
        
        if days_since_push <= 7:
            return "very_active"
        elif days_since_push <= 30:
            return "active"
        elif days_since_push <= 90:
            return "moderate"
        elif days_since_push <= 365:
            return "low"
        else:
            return "inactive"
    
    def __repr__(self):
        return f"<GitHubRepository(name='{self.full_name}', stars={self.stargazers_count}, language='{self.language}')>"


class GitHubCommit(BaseModel, CorrelationMixin, TimestampMixin):
    """
    GitHub commit model for development activity correlation analysis
    """
    __tablename__ = 'github_commits'
    __table_args__ = {'schema': 'development'}
    
    # Repository reference
    repository_id: Mapped[str] = mapped_column(ForeignKey('development.github_repositories.id'))
    
    # Commit identification
    sha: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
    message: Mapped[Optional[str]] = mapped_column(Text)
    
    # Author information
    author_name: Mapped[Optional[str]] = mapped_column(String(200))
    author_email: Mapped[Optional[str]] = mapped_column(String(200))
    committer_name: Mapped[Optional[str]] = mapped_column(String(200))
    committer_email: Mapped[Optional[str]] = mapped_column(String(200))
    
    # Commit timing
    commit_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Code change metrics
    additions: Mapped[Optional[int]] = mapped_column(Integer)
    deletions: Mapped[Optional[int]] = mapped_column(Integer)
    changed_files: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Relationship
    repository: Mapped["GitHubRepository"] = relationship("GitHubRepository", back_populates="commits")
    
    def get_change_magnitude(self) -> str:
        """Categorize commit size for correlation analysis"""
        total_changes = (self.additions or 0) + (self.deletions or 0)
        
        if total_changes == 0:
            return "no_change"
        elif total_changes <= 10:
            return "small"
        elif total_changes <= 100:
            return "medium"
        elif total_changes <= 1000:
            return "large"
        else:
            return "massive"
    
    def __repr__(self):
        return f"<GitHubCommit(sha='{self.sha}', repository_id='{self.repository_id}', additions={self.additions})>"


# ================================
# PRODUCTIVITY DOMAIN MODELS
# ================================

class NotionPage(BaseModel, EmbeddingMixin, CorrelationMixin, TimestampMixin):
    """
    Notion page model for productivity and content correlation analysis
    """
    __tablename__ = 'notion_pages'
    __table_args__ = {'schema': 'productivity'}
    
    # External IDs
    notion_id: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
    
    # Page information
    title: Mapped[Optional[str]] = mapped_column(String(500))
    url: Mapped[Optional[str]] = mapped_column(String(500))
    page_type: Mapped[Optional[str]] = mapped_column(String(100))  # page, database, etc.
    
    # Database reference (if this page is in a database)
    database_id: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Page properties and content
    properties: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB)
    content: Mapped[Optional[str]] = mapped_column(Text)  # For embedding and analysis
    
    # Notion timestamps
    created_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    last_edited_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # User references
    created_by: Mapped[Optional[str]] = mapped_column(String(100))
    last_edited_by: Mapped[Optional[str]] = mapped_column(String(100))
    
    def get_word_count(self) -> Optional[int]:
        """Calculate word count for content analysis"""
        if not self.content:
            return None
        
        return len(self.content.split())
    
    def get_content_category(self) -> str:
        """Categorize content type based on properties and content"""
        if not self.content:
            return "empty"
        
        word_count = self.get_word_count() or 0
        
        if word_count >= 1000:
            return "long_form"
        elif word_count >= 300:
            return "medium_form"
        elif word_count >= 50:
            return "short_form"
        else:
            return "minimal"
    
    def __repr__(self):
        return f"<NotionPage(title='{self.title}', notion_id='{self.notion_id}', type='{self.page_type}')>"


class NotionDatabase(BaseModel, EmbeddingMixin, CorrelationMixin, TimestampMixin):
    """
    Notion database model for structured content correlation analysis
    """
    __tablename__ = 'notion_databases'
    __table_args__ = {'schema': 'productivity'}
    
    # External IDs
    notion_id: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
    
    # Database information
    title: Mapped[Optional[str]] = mapped_column(String(500))
    url: Mapped[Optional[str]] = mapped_column(String(500))
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    # Database schema
    properties: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, comment="""
    Database property schema including:
    - Property names and types
    - Select options
    - Relation targets
    - Formula definitions
    """)
    
    # Notion timestamps
    created_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    last_edited_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # User references
    created_by: Mapped[Optional[str]] = mapped_column(String(100))
    last_edited_by: Mapped[Optional[str]] = mapped_column(String(100))
    
    def get_property_count(self) -> int:
        """Count number of properties in database"""
        if not self.properties:
            return 0
        return len(self.properties)
    
    def get_property_types(self) -> List[str]:
        """Get list of property types in database"""
        if not self.properties:
            return []
        
        types = []
        for prop_data in self.properties.values():
            if isinstance(prop_data, dict) and 'type' in prop_data:
                types.append(prop_data['type'])
        
        return list(set(types))  # Remove duplicates
    
    def __repr__(self):
        return f"<NotionDatabase(title='{self.title}', notion_id='{self.notion_id}', properties={self.get_property_count()})>"
