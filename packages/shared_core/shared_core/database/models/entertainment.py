"""
Entertainment Domain Models

SQLAlchemy models for entertainment data from TMDB API.
Includes soundtrack ISRC codes for cross-domain linking with music domain.
"""

from typing import List, Optional, Dict, Any
from decimal import Decimal
from sqlalchemy import String, Integer, Boolean, Date, ARRAY, Numeric, Text, BigInteger
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from ..base import BaseModel, EmbeddingMixin, CorrelationMixin, TimestampMixin


class Movie(BaseModel, EmbeddingMixin, CorrelationMixin, TimestampMixin):
    """
    Movie model with soundtrack correlation support for music domain linking
    """
    __tablename__ = 'movies'
    __table_args__ = {'schema': 'entertainment'}
    
    # External IDs
    tmdb_id: Mapped[Optional[int]] = mapped_column(Integer, unique=True)
    imdb_id: Mapped[Optional[str]] = mapped_column(String(20), unique=True)
    
    # Basic movie information
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    original_title: Mapped[Optional[str]] = mapped_column(String(500))
    overview: Mapped[Optional[str]] = mapped_column(Text)
    tagline: Mapped[Optional[str]] = mapped_column(Text)
    
    # Release and runtime
    release_date: Mapped[Optional[Date]] = mapped_column(Date)
    runtime: Mapped[Optional[int]] = mapped_column(Integer)  # minutes
    
    # Financial data
    budget: Mapped[Optional[int]] = mapped_column(BigInteger)
    revenue: Mapped[Optional[int]] = mapped_column(BigInteger)
    
    # Categorization
    genres: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
    production_companies: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
    production_countries: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
    spoken_languages: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
    
    # Content rating
    adult: Mapped[Optional[bool]] = mapped_column(Boolean)
    status: Mapped[Optional[str]] = mapped_column(String(50))  # Released, In Production, etc.
    
    # Popularity metrics
    popularity: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 3))
    vote_average: Mapped[Optional[Decimal]] = mapped_column(Numeric(3, 1))
    vote_count: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Media paths
    poster_path: Mapped[Optional[str]] = mapped_column(String(200))
    backdrop_path: Mapped[Optional[str]] = mapped_column(String(200))
    
    # Soundtrack data for music correlation (stored in correlation_metadata)
    # ISRC codes for soundtrack tracks enable direct linking to music domain
    soundtrack_isrc_codes: Mapped[Optional[List[str]]] = mapped_column(
        ARRAY(String), 
        comment="ISRC codes for soundtrack tracks - enables music correlation"
    )
    
    # Box office performance categories for correlation analysis
    def get_box_office_performance(self) -> str:
        """Categorize box office performance for correlation analysis"""
        if not self.revenue:
            return "unknown"
        
        if self.revenue >= 1000000000:  # $1B+
            return "blockbuster"
        elif self.revenue >= 500000000:  # $500M+
            return "very_successful" 
        elif self.revenue >= 100000000:  # $100M+
            return "successful"
        elif self.revenue >= 50000000:   # $50M+
            return "moderate"
        else:
            return "limited"
    
    def get_genre_primary(self) -> Optional[str]:
        """Get primary genre for correlation analysis"""
        if self.genres and len(self.genres) > 0:
            return self.genres[0].lower()
        return None
    
    def __repr__(self):
        return f"<Movie(title='{self.title}', tmdb_id={self.tmdb_id}, release_date='{self.release_date}')>"


class TVShow(BaseModel, EmbeddingMixin, CorrelationMixin, TimestampMixin):
    """
    TV Show model with episode and season correlation potential
    """
    __tablename__ = 'tv_shows'
    __table_args__ = {'schema': 'entertainment'}
    
    # External IDs
    tmdb_id: Mapped[Optional[int]] = mapped_column(Integer, unique=True)
    imdb_id: Mapped[Optional[str]] = mapped_column(String(20), unique=True)
    
    # Basic show information
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    original_name: Mapped[Optional[str]] = mapped_column(String(500))
    overview: Mapped[Optional[str]] = mapped_column(Text)
    tagline: Mapped[Optional[str]] = mapped_column(Text)
    
    # Air dates
    first_air_date: Mapped[Optional[Date]] = mapped_column(Date)
    last_air_date: Mapped[Optional[Date]] = mapped_column(Date)
    
    # Show structure
    number_of_episodes: Mapped[Optional[int]] = mapped_column(Integer)
    number_of_seasons: Mapped[Optional[int]] = mapped_column(Integer)
    episode_run_time: Mapped[Optional[List[int]]] = mapped_column(ARRAY(Integer))
    
    # Categorization
    genres: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
    production_companies: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
    production_countries: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
    spoken_languages: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
    networks: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
    
    # Content rating
    adult: Mapped[Optional[bool]] = mapped_column(Boolean)
    status: Mapped[Optional[str]] = mapped_column(String(50))  # Ended, Returning Series, etc.
    
    # Popularity metrics
    popularity: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 3))
    vote_average: Mapped[Optional[Decimal]] = mapped_column(Numeric(3, 1))
    vote_count: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Media paths
    poster_path: Mapped[Optional[str]] = mapped_column(String(200))
    backdrop_path: Mapped[Optional[str]] = mapped_column(String(200))
    
    # Theme music and soundtrack correlation
    theme_music_isrc: Mapped[Optional[str]] = mapped_column(
        String(20),
        comment="ISRC code for theme music - enables music correlation"
    )
    
    def get_show_length_category(self) -> str:
        """Categorize show length for correlation analysis"""
        if not self.number_of_episodes:
            return "unknown"
        
        if self.number_of_episodes >= 100:
            return "long_running"  # 100+ episodes
        elif self.number_of_episodes >= 50:
            return "established"   # 50-99 episodes  
        elif self.number_of_episodes >= 20:
            return "medium"        # 20-49 episodes
        else:
            return "short"         # <20 episodes
    
    def get_average_episode_runtime(self) -> Optional[int]:
        """Calculate average episode runtime"""
        if self.episode_run_time and len(self.episode_run_time) > 0:
            return sum(self.episode_run_time) // len(self.episode_run_time)
        return None
    
    def __repr__(self):
        return f"<TVShow(name='{self.name}', tmdb_id={self.tmdb_id}, seasons={self.number_of_seasons})>"


class Person(BaseModel, EmbeddingMixin, CorrelationMixin, TimestampMixin):
    """
    Person model for actors, directors, and other entertainment industry figures
    """
    __tablename__ = 'people'
    __table_args__ = {'schema': 'entertainment'}
    
    # External IDs
    tmdb_id: Mapped[Optional[int]] = mapped_column(Integer, unique=True)
    imdb_id: Mapped[Optional[str]] = mapped_column(String(20), unique=True)
    
    # Basic information
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    biography: Mapped[Optional[str]] = mapped_column(Text)
    
    # Personal details
    birthday: Mapped[Optional[Date]] = mapped_column(Date)
    deathday: Mapped[Optional[Date]] = mapped_column(Date)
    place_of_birth: Mapped[Optional[str]] = mapped_column(String(200))
    
    # Professional information
    known_for_department: Mapped[Optional[str]] = mapped_column(String(100))  # Acting, Directing, etc.
    gender: Mapped[Optional[int]] = mapped_column(Integer)  # TMDB gender codes
    
    # Media
    profile_path: Mapped[Optional[str]] = mapped_column(String(200))
    
    # Popularity metrics
    popularity: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 3))
    
    # Also known as names
    also_known_as: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
    
    def __repr__(self):
        return f"<Person(name='{self.name}', tmdb_id={self.tmdb_id}, known_for='{self.known_for_department}')>"


class MovieCredit(BaseModel, CorrelationMixin):
    """
    Association table for movie-person relationships with role information
    """
    __tablename__ = 'movie_credits'
    __table_args__ = {'schema': 'entertainment'}
    
    movie_id: Mapped[str] = mapped_column(String, nullable=False)  # FK to movies
    person_id: Mapped[str] = mapped_column(String, nullable=False)  # FK to people
    
    # Credit information
    credit_type: Mapped[str] = mapped_column(String(20), nullable=False)  # 'cast' or 'crew'
    character: Mapped[Optional[str]] = mapped_column(String(500))  # For cast
    job: Mapped[Optional[str]] = mapped_column(String(200))  # For crew (Director, Producer, etc.)
    department: Mapped[Optional[str]] = mapped_column(String(100))  # For crew
    
    # Order and importance
    order: Mapped[Optional[int]] = mapped_column(Integer)  # Billing order
    
    def __repr__(self):
        if self.character:
            return f"<MovieCredit(movie_id='{self.movie_id}', person_id='{self.person_id}', character='{self.character}')>"
        else:
            return f"<MovieCredit(movie_id='{self.movie_id}', person_id='{self.person_id}', job='{self.job}')>"


class TVCredit(BaseModel, CorrelationMixin):
    """
    Association table for TV show-person relationships
    """
    __tablename__ = 'tv_credits'
    __table_args__ = {'schema': 'entertainment'}
    
    tv_show_id: Mapped[str] = mapped_column(String, nullable=False)  # FK to tv_shows
    person_id: Mapped[str] = mapped_column(String, nullable=False)  # FK to people
    
    # Credit information
    credit_type: Mapped[str] = mapped_column(String(20), nullable=False)  # 'cast' or 'crew'
    character: Mapped[Optional[str]] = mapped_column(String(500))  # For cast
    job: Mapped[Optional[str]] = mapped_column(String(200))  # For crew
    department: Mapped[Optional[str]] = mapped_column(String(100))  # For crew
    
    # TV-specific fields
    episode_count: Mapped[Optional[int]] = mapped_column(Integer)
    
    def __repr__(self):
        return f"<TVCredit(tv_show_id='{self.tv_show_id}', person_id='{self.person_id}', episodes={self.episode_count})>"
