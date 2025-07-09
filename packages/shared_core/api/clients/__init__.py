"""
API Clients Package

This package contains all external API clients with built-in debugging,
rate limiting, retry logic, and comprehensive error handling.
"""

from .base_client import BaseAPIClient
from .spotify_client import SpotifyClient
from .musicbrainz_client import MusicBrainzClient
from .tmdb_client import TMDBClient
from .weather_client import WeatherClient
from .pokemon_client import PokemonClient
from .github_client import GitHubClient
from .notion_client import NotionClient

__all__ = [
    "BaseAPIClient",
    "SpotifyClient", 
    "MusicBrainzClient",
    "TMDBClient",
    "WeatherClient",
    "PokemonClient",
    "GitHubClient",
    "NotionClient",
]
