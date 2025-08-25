"""
API Clients Package

This package contains all external API clients with built-in debugging,
rate limiting, retry logic, and comprehensive error handling.
"""

from ...config.base_client import BaseAPIClient

# from .pokemon.pokemon_graphql_client import PokemonGraphQLClient  # Requires gql
from .spotify.spotify_client import SpotifyClient
from .openweathermap import OpenWeatherMapClient
from .tmdb import TMDBClient
from .musicbrainz import MusicBrainzClient
from .notion import NotionClient

__all__ = [
    "BaseAPIClient",
    "PokemonGraphQLClient",
    "SpotifyClient",
    "OpenWeatherMapClient",
    "TMDBClient",
    "MusicBrainzClient",
    "NotionClient",
]
