"""
Authentication Module for the Data Centralization Platform

This module provides OAuth authentication capabilities for various services.
It follows the established patterns for API clients and configuration management.

Available OAuth Clients:
- MusicBrainzOAuth: OAuth 2.0 implementation for MusicBrainz
- SpotifyOAuth: OAuth 2.0 implementation for Spotify Web API
"""

from .musicbrainz_oauth import MusicBrainzOAuth
from .spotify_oauth import SpotifyOAuth

__all__ = ["MusicBrainzOAuth", "SpotifyOAuth"]
