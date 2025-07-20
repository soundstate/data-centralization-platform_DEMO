"""
Database Models

Central imports for all SQLAlchemy models across domains.
Includes base models, mixins, and all domain-specific models.
"""

# Import base classes first
from ..base import Base, BaseModel, EmbeddingMixin, CorrelationMixin, TimestampMixin

# Music domain models
from .music import (
    Artist,
    Album, 
    Track,
    Playlist,
    PlaylistTrack
)

# Entertainment domain models
from .entertainment import (
    Movie,
    TVShow,
    Person,
    MovieCredit,
    TVCredit
)

# Weather domain models  
from .weather import (
    Location,
    CurrentWeather,
    HistoricalWeather,
    WeatherAlert
)

# Gaming, Development, and Productivity domain models
from .domains import (
    # Gaming
    Pokemon,
    PokemonSpecies,
    
    # Development
    GitHubRepository,
    GitHubCommit,
    
    # Productivity
    NotionPage,
    NotionDatabase
)

# Analytics and raw data models
from .analytics import (
    # Raw data and audit
    APIResponse,
    DataEntity,
    EntityRelationship,
    
    # Correlation analysis
    Correlation,
    TimeSeriesData,
    
    # Embeddings and LLM
    Embedding,
    CorrelationInsight
)

# All models for Alembic autogenerate
__all__ = [
    # Base classes
    "Base",
    "BaseModel", 
    "EmbeddingMixin",
    "CorrelationMixin",
    "TimestampMixin",
    
    # Music domain
    "Artist",
    "Album",
    "Track", 
    "Playlist",
    "PlaylistTrack",
    
    # Entertainment domain
    "Movie",
    "TVShow",
    "Person",
    "MovieCredit", 
    "TVCredit",
    
    # Weather domain
    "Location",
    "CurrentWeather",
    "HistoricalWeather", 
    "WeatherAlert",
    
    # Gaming domain
    "Pokemon",
    "PokemonSpecies",
    
    # Development domain
    "GitHubRepository",
    "GitHubCommit",
    
    # Productivity domain
    "NotionPage",
    "NotionDatabase",
    
    # Analytics and raw data
    "APIResponse",
    "DataEntity", 
    "EntityRelationship",
    "Correlation",
    "TimeSeriesData",
    "Embedding",
    "CorrelationInsight"
]

# Model registry by domain for dynamic access
DOMAIN_MODELS = {
    "music": [Artist, Album, Track, Playlist, PlaylistTrack],
    "entertainment": [Movie, TVShow, Person, MovieCredit, TVCredit],
    "weather": [Location, CurrentWeather, HistoricalWeather, WeatherAlert],
    "gaming": [Pokemon, PokemonSpecies],
    "development": [GitHubRepository, GitHubCommit],
    "productivity": [NotionPage, NotionDatabase],
    "analytics": [Correlation, TimeSeriesData],
    "general": [DataEntity, EntityRelationship],
    "raw_data": [APIResponse],
    "llm": [Embedding, CorrelationInsight]
}

# Models with embedding support for semantic search
EMBEDDING_MODELS = [
    Artist, Album, Track, Playlist,  # Music
    Movie, TVShow, Person,  # Entertainment 
    Location,  # Weather
    Pokemon, PokemonSpecies,  # Gaming
    GitHubRepository,  # Development
    NotionPage, NotionDatabase,  # Productivity
    DataEntity,  # General
    CorrelationInsight  # LLM
]

# Models with correlation metadata for cross-domain linking
CORRELATION_MODELS = [
    Artist, Album, Track, Playlist, PlaylistTrack,  # Music
    Movie, TVShow, Person, MovieCredit, TVCredit,  # Entertainment
    Location, CurrentWeather, HistoricalWeather, WeatherAlert,  # Weather  
    Pokemon, PokemonSpecies,  # Gaming
    GitHubRepository, GitHubCommit,  # Development
    NotionPage, NotionDatabase,  # Productivity
    DataEntity, EntityRelationship  # General
]

def get_models_by_domain(domain: str):
    """Get all models for a specific domain"""
    return DOMAIN_MODELS.get(domain, [])

def get_all_models():
    """Get all models across all domains"""
    models = []
    for domain_models in DOMAIN_MODELS.values():
        models.extend(domain_models)
    return models

def get_embedding_enabled_models():
    """Get all models that support vector embeddings"""
    return EMBEDDING_MODELS

def get_correlation_enabled_models():
    """Get all models that support correlation metadata"""
    return CORRELATION_MODELS
