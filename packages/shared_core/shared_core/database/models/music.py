"""
Music Domain Models

SQLAlchemy models for music-related data from Spotify and MusicBrainz APIs.
Includes vector embeddings for semantic search and correlation metadata.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy import String, Integer, Boolean, Date, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import BaseModel, EmbeddingMixin, CorrelationMixin, TimestampMixin


class Artist(BaseModel, EmbeddingMixin, CorrelationMixin, TimestampMixin):
    """
    Music artist model with cross-domain correlation support
    """
    __tablename__ = 'artists'
    __table_args__ = {'schema': 'music'}
    
    # External IDs for cross-platform linking
    spotify_id: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
    musicbrainz_id: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
    
    # Basic artist information
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    genres: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
    
    # Spotify-specific data
    popularity: Mapped[Optional[int]] = mapped_column(Integer)
    followers: Mapped[Optional[int]] = mapped_column(Integer)
    
    # External URLs and images
    external_urls: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB)
    images: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB)
    
    # ISRC codes for cross-domain linking (stored in correlation_metadata)
    # This enables linking to entertainment domain via soundtrack data
    
    # Relationships
    albums: Mapped[List["Album"]] = relationship("Album", back_populates="artist")
    tracks: Mapped[List["Track"]] = relationship("Track", back_populates="artist")
    
    def __repr__(self):
        return f"<Artist(name='{self.name}', spotify_id='{self.spotify_id}')>"


class Album(BaseModel, EmbeddingMixin, CorrelationMixin, TimestampMixin):
    """
    Music album model with release date correlation potential
    """
    __tablename__ = 'albums'
    __table_args__ = {'schema': 'music'}
    
    # External IDs
    spotify_id: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
    musicbrainz_id: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
    
    # Basic album information
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    artist_id: Mapped[Optional[str]] = mapped_column(ForeignKey('music.artists.id'))
    
    # Release information
    release_date: Mapped[Optional[Date]] = mapped_column(Date)
    total_tracks: Mapped[Optional[int]] = mapped_column(Integer)
    album_type: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Genre and label information
    genres: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
    label: Mapped[Optional[str]] = mapped_column(String(200))
    
    # Popularity metrics
    popularity: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Media data
    images: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB)
    external_urls: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB)
    
    # Relationships
    artist: Mapped[Optional["Artist"]] = relationship("Artist", back_populates="albums")
    tracks: Mapped[List["Track"]] = relationship("Track", back_populates="album")
    
    def __repr__(self):
        return f"<Album(name='{self.name}', artist_id='{self.artist_id}')>"


class Track(BaseModel, EmbeddingMixin, CorrelationMixin, TimestampMixin):
    """
    Music track model with advanced audio features for correlation analysis
    """
    __tablename__ = 'tracks'
    __table_args__ = {'schema': 'music'}
    
    # External IDs
    spotify_id: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
    musicbrainz_id: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
    isrc_code: Mapped[Optional[str]] = mapped_column(String(20), index=True)  # Critical for movie linking
    
    # Basic track information
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    artist_id: Mapped[Optional[str]] = mapped_column(ForeignKey('music.artists.id'))
    album_id: Mapped[Optional[str]] = mapped_column(ForeignKey('music.albums.id'))
    
    # Track details
    duration_ms: Mapped[Optional[int]] = mapped_column(Integer)
    popularity: Mapped[Optional[int]] = mapped_column(Integer)
    track_number: Mapped[Optional[int]] = mapped_column(Integer)
    disc_number: Mapped[Optional[int]] = mapped_column(Integer)
    explicit: Mapped[Optional[bool]] = mapped_column(Boolean)
    
    # Audio features for correlation analysis
    audio_features: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, comment="""
    Spotify audio features including:
    - danceability: 0.0-1.0
    - energy: 0.0-1.0
    - valence: 0.0-1.0 (musical positivity)
    - tempo: BPM
    - acousticness: 0.0-1.0
    - instrumentalness: 0.0-1.0
    - liveness: 0.0-1.0
    - speechiness: 0.0-1.0
    """)
    
    # External data
    external_urls: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB)
    preview_url: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Relationships
    artist: Mapped[Optional["Artist"]] = relationship("Artist", back_populates="tracks")
    album: Mapped[Optional["Album"]] = relationship("Album", back_populates="tracks")
    
    def get_audio_feature(self, feature_name: str) -> Optional[float]:
        """Extract specific audio feature value"""
        if self.audio_features and feature_name in self.audio_features:
            return float(self.audio_features[feature_name])
        return None
    
    def get_mood_score(self) -> Optional[float]:
        """
        Calculate mood score based on valence and energy
        High valence + high energy = happy/energetic
        Low valence + low energy = sad/mellow
        """
        valence = self.get_audio_feature('valence')
        energy = self.get_audio_feature('energy')
        
        if valence is not None and energy is not None:
            return (valence + energy) / 2.0
        return None
    
    def __repr__(self):
        return f"<Track(name='{self.name}', artist_id='{self.artist_id}', isrc='{self.isrc_code}')>"


class PlaylistTrack(BaseModel, CorrelationMixin):
    """
    Association table for playlist-track relationships with temporal data
    """
    __tablename__ = 'playlist_tracks'
    __table_args__ = {'schema': 'music'}
    
    playlist_id: Mapped[str] = mapped_column(ForeignKey('music.playlists.id'))
    track_id: Mapped[str] = mapped_column(ForeignKey('music.tracks.id'))
    
    # Position and timing data for analysis
    position: Mapped[Optional[int]] = mapped_column(Integer)
    added_at: Mapped[Optional[str]] = mapped_column(String)  # ISO datetime string
    added_by: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Relationships
    playlist: Mapped["Playlist"] = relationship("Playlist", back_populates="track_associations")
    track: Mapped["Track"] = relationship("Track")


class Playlist(BaseModel, EmbeddingMixin, CorrelationMixin, TimestampMixin):
    """
    Music playlist model for behavioral analysis
    """
    __tablename__ = 'playlists'
    __table_args__ = {'schema': 'music'}
    
    # External IDs
    spotify_id: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
    
    # Playlist information
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String)
    owner_id: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Playlist metrics
    followers: Mapped[Optional[int]] = mapped_column(Integer)
    total_tracks: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Playlist properties
    public: Mapped[Optional[bool]] = mapped_column(Boolean)
    collaborative: Mapped[Optional[bool]] = mapped_column(Boolean)
    
    # External data
    external_urls: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB)
    images: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB)
    
    # Relationships
    track_associations: Mapped[List["PlaylistTrack"]] = relationship(
        "PlaylistTrack", 
        back_populates="playlist"
    )
    
    def __repr__(self):
        return f"<Playlist(name='{self.name}', owner_id='{self.owner_id}')>"
