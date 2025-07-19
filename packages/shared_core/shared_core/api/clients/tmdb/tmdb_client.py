"""
TMDB API Client

This module provides a client for interacting with The Movie Database (TMDB) API v3.
It follows the established patterns for API clients in the shared_core package.

The TMDB API provides access to:
- Movie information (details, credits, reviews, images)
- TV Show information (details, credits, seasons, episodes)
- Person information (actors, directors, crew)
- Search functionality across movies, TV shows, and people
- Trending content and popular items
- Movie/TV show recommendations
- Collection and genre information

Features:
- Rate limiting (40 requests per 10 seconds for free tier)
- Retry logic with exponential backoff
- Comprehensive error handling
- Correlation-ready data extraction
- Temporal and categorical context
- Image URL construction
- Multiple data formats (JSON, TMDb objects)
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from urllib.parse import urljoin

from shared_core.api.clients.base_client import BaseAPIClient, APIResponse
from shared_core.logging.centralized_logger import CentralizedLogger


class TMDBClient(BaseAPIClient):
    """
    TMDB API Client for accessing The Movie Database API v3.
    
    This client provides comprehensive access to movie, TV show, and person data
    from TMDB, with built-in rate limiting, error handling, and correlation-ready
    data extraction.
    
    Rate Limits:
    - Free tier: 40 requests per 10 seconds
    - Paid tier: Higher limits available
    
    Authentication:
    - API Key (v3 auth) - Required for all requests
    - Session tokens for user-specific operations (optional)
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.themoviedb.org/3",
        image_base_url: str = "https://image.tmdb.org/t/p",
        rate_limit_per_second: float = 4.0,  # 40 requests per 10 seconds
        max_retries: int = 3,
        timeout: int = 30,
        debug_mode: bool = False
    ):
        """
        Initialize TMDB API client.
        
        Args:
            api_key: TMDB API key (required)
            base_url: Base URL for TMDB API (default: https://api.themoviedb.org/3)
            image_base_url: Base URL for TMDB images (default: https://image.tmdb.org/t/p)
            rate_limit_per_second: Rate limit in requests per second (default: 4.0)
            max_retries: Maximum number of retry attempts (default: 3)
            timeout: Request timeout in seconds (default: 30)
            debug_mode: Enable debug logging (default: False)
        """
        super().__init__(
            base_url=base_url,
            rate_limit_per_second=rate_limit_per_second,
            max_retries=max_retries,
            timeout=timeout,
            debug_mode=debug_mode
        )
        
        self.api_key = api_key
        self.image_base_url = image_base_url
        self.logger = CentralizedLogger.get_logger(__name__)
        
        # Default headers for all requests
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        if debug_mode:
            self.logger.setLevel(logging.DEBUG)
            self.logger.debug("TMDB client initialized in debug mode")
    
    async def _make_request(
        self,
        endpoint: str,
        method: str = "GET",
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> APIResponse:
        """
        Make a request to the TMDB API.
        
        Args:
            endpoint: API endpoint (e.g., "/movie/popular")
            method: HTTP method (default: GET)
            params: Query parameters
            data: Request body data
            
        Returns:
            APIResponse object with success status and data
        """
        # Add API key to params if not using Bearer token
        if params is None:
            params = {}
        
        # Add default language if not specified
        if "language" not in params:
            params["language"] = "en-US"
        
        url = urljoin(self.base_url, endpoint.lstrip('/'))
        
        try:
            response = await self._request(
                method=method,
                url=url,
                params=params,
                json=data,
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                return APIResponse(success=True, data=data, status_code=response.status_code)
            else:
                error_msg = f"TMDB API error: {response.status_code}"
                if response.text:
                    error_msg += f" - {response.text}"
                
                self.logger.error(error_msg)
                return APIResponse(
                    success=False,
                    error=error_msg,
                    status_code=response.status_code
                )
                
        except Exception as e:
            error_msg = f"Request failed: {str(e)}"
            self.logger.error(error_msg)
            return APIResponse(success=False, error=error_msg)
    
    # Movie Methods
    async def get_movie_details(self, movie_id: int, append_to_response: Optional[str] = None) -> APIResponse:
        """
        Get detailed information about a movie.
        
        Args:
            movie_id: TMDB movie ID
            append_to_response: Comma-separated list of additional data to include
                              (e.g., "credits,reviews,videos,images")
        
        Returns:
            APIResponse with movie details
        """
        params = {}
        if append_to_response:
            params["append_to_response"] = append_to_response
        
        return await self._make_request(f"/movie/{movie_id}", params=params)
    
    async def get_popular_movies(self, page: int = 1, region: Optional[str] = None) -> APIResponse:
        """
        Get popular movies.
        
        Args:
            page: Page number (default: 1)
            region: ISO 3166-1 region code (optional)
        
        Returns:
            APIResponse with popular movies list
        """
        params = {"page": page}
        if region:
            params["region"] = region
        
        return await self._make_request("/movie/popular", params=params)
    
    async def get_top_rated_movies(self, page: int = 1, region: Optional[str] = None) -> APIResponse:
        """
        Get top-rated movies.
        
        Args:
            page: Page number (default: 1)
            region: ISO 3166-1 region code (optional)
        
        Returns:
            APIResponse with top-rated movies list
        """
        params = {"page": page}
        if region:
            params["region"] = region
        
        return await self._make_request("/movie/top_rated", params=params)
    
    async def get_now_playing_movies(self, page: int = 1, region: Optional[str] = None) -> APIResponse:
        """
        Get movies currently playing in theaters.
        
        Args:
            page: Page number (default: 1)
            region: ISO 3166-1 region code (optional)
        
        Returns:
            APIResponse with now playing movies list
        """
        params = {"page": page}
        if region:
            params["region"] = region
        
        return await self._make_request("/movie/now_playing", params=params)
    
    async def get_upcoming_movies(self, page: int = 1, region: Optional[str] = None) -> APIResponse:
        """
        Get upcoming movies.
        
        Args:
            page: Page number (default: 1)
            region: ISO 3166-1 region code (optional)
        
        Returns:
            APIResponse with upcoming movies list
        """
        params = {"page": page}
        if region:
            params["region"] = region
        
        return await self._make_request("/movie/upcoming", params=params)
    
    async def get_movie_credits(self, movie_id: int) -> APIResponse:
        """
        Get cast and crew information for a movie.
        
        Args:
            movie_id: TMDB movie ID
        
        Returns:
            APIResponse with movie credits
        """
        return await self._make_request(f"/movie/{movie_id}/credits")
    
    async def get_movie_reviews(self, movie_id: int, page: int = 1) -> APIResponse:
        """
        Get reviews for a movie.
        
        Args:
            movie_id: TMDB movie ID
            page: Page number (default: 1)
        
        Returns:
            APIResponse with movie reviews
        """
        params = {"page": page}
        return await self._make_request(f"/movie/{movie_id}/reviews", params=params)
    
    async def get_movie_recommendations(self, movie_id: int, page: int = 1) -> APIResponse:
        """
        Get movie recommendations based on a movie.
        
        Args:
            movie_id: TMDB movie ID
            page: Page number (default: 1)
        
        Returns:
            APIResponse with recommended movies
        """
        params = {"page": page}
        return await self._make_request(f"/movie/{movie_id}/recommendations", params=params)
    
    # TV Show Methods
    async def get_tv_details(self, tv_id: int, append_to_response: Optional[str] = None) -> APIResponse:
        """
        Get detailed information about a TV show.
        
        Args:
            tv_id: TMDB TV show ID
            append_to_response: Comma-separated list of additional data to include
        
        Returns:
            APIResponse with TV show details
        """
        params = {}
        if append_to_response:
            params["append_to_response"] = append_to_response
        
        return await self._make_request(f"/tv/{tv_id}", params=params)
    
    async def get_popular_tv_shows(self, page: int = 1) -> APIResponse:
        """
        Get popular TV shows.
        
        Args:
            page: Page number (default: 1)
        
        Returns:
            APIResponse with popular TV shows list
        """
        params = {"page": page}
        return await self._make_request("/tv/popular", params=params)
    
    async def get_top_rated_tv_shows(self, page: int = 1) -> APIResponse:
        """
        Get top-rated TV shows.
        
        Args:
            page: Page number (default: 1)
        
        Returns:
            APIResponse with top-rated TV shows list
        """
        params = {"page": page}
        return await self._make_request("/tv/top_rated", params=params)
    
    async def get_tv_on_the_air(self, page: int = 1) -> APIResponse:
        """
        Get TV shows currently on the air.
        
        Args:
            page: Page number (default: 1)
        
        Returns:
            APIResponse with on-the-air TV shows list
        """
        params = {"page": page}
        return await self._make_request("/tv/on_the_air", params=params)
    
    async def get_tv_airing_today(self, page: int = 1) -> APIResponse:
        """
        Get TV shows airing today.
        
        Args:
            page: Page number (default: 1)
        
        Returns:
            APIResponse with TV shows airing today
        """
        params = {"page": page}
        return await self._make_request("/tv/airing_today", params=params)
    
    # Person Methods
    async def get_person_details(self, person_id: int, append_to_response: Optional[str] = None) -> APIResponse:
        """
        Get detailed information about a person.
        
        Args:
            person_id: TMDB person ID
            append_to_response: Comma-separated list of additional data to include
        
        Returns:
            APIResponse with person details
        """
        params = {}
        if append_to_response:
            params["append_to_response"] = append_to_response
        
        return await self._make_request(f"/person/{person_id}", params=params)
    
    async def get_popular_people(self, page: int = 1) -> APIResponse:
        """
        Get popular people.
        
        Args:
            page: Page number (default: 1)
        
        Returns:
            APIResponse with popular people list
        """
        params = {"page": page}
        return await self._make_request("/person/popular", params=params)
    
    # Search Methods
    async def search_movies(self, query: str, page: int = 1, year: Optional[int] = None) -> APIResponse:
        """
        Search for movies.
        
        Args:
            query: Search query
            page: Page number (default: 1)
            year: Release year filter (optional)
        
        Returns:
            APIResponse with search results
        """
        params = {"query": query, "page": page}
        if year:
            params["year"] = year
        
        return await self._make_request("/search/movie", params=params)
    
    async def search_tv_shows(self, query: str, page: int = 1, first_air_date_year: Optional[int] = None) -> APIResponse:
        """
        Search for TV shows.
        
        Args:
            query: Search query
            page: Page number (default: 1)
            first_air_date_year: First air date year filter (optional)
        
        Returns:
            APIResponse with search results
        """
        params = {"query": query, "page": page}
        if first_air_date_year:
            params["first_air_date_year"] = first_air_date_year
        
        return await self._make_request("/search/tv", params=params)
    
    async def search_people(self, query: str, page: int = 1) -> APIResponse:
        """
        Search for people.
        
        Args:
            query: Search query
            page: Page number (default: 1)
        
        Returns:
            APIResponse with search results
        """
        params = {"query": query, "page": page}
        return await self._make_request("/search/person", params=params)
    
    async def multi_search(self, query: str, page: int = 1) -> APIResponse:
        """
        Search for movies, TV shows, and people in a single request.
        
        Args:
            query: Search query
            page: Page number (default: 1)
        
        Returns:
            APIResponse with mixed search results
        """
        params = {"query": query, "page": page}
        return await self._make_request("/search/multi", params=params)
    
    # Trending Methods
    async def get_trending(self, media_type: str = "all", time_window: str = "day") -> APIResponse:
        """
        Get trending movies, TV shows, or people.
        
        Args:
            media_type: Type of media ('all', 'movie', 'tv', 'person')
            time_window: Time window ('day' or 'week')
        
        Returns:
            APIResponse with trending items
        """
        return await self._make_request(f"/trending/{media_type}/{time_window}")
    
    # Discover Methods
    async def discover_movies(self, **kwargs) -> APIResponse:
        """
        Discover movies with various filters.
        
        Args:
            **kwargs: Filter parameters (genre, year, rating, etc.)
        
        Returns:
            APIResponse with discovered movies
        """
        return await self._make_request("/discover/movie", params=kwargs)
    
    async def discover_tv_shows(self, **kwargs) -> APIResponse:
        """
        Discover TV shows with various filters.
        
        Args:
            **kwargs: Filter parameters (genre, year, rating, etc.)
        
        Returns:
            APIResponse with discovered TV shows
        """
        return await self._make_request("/discover/tv", params=kwargs)
    
    # Genre Methods
    async def get_movie_genres(self) -> APIResponse:
        """
        Get the list of official movie genres.
        
        Returns:
            APIResponse with movie genres list
        """
        return await self._make_request("/genre/movie/list")
    
    async def get_tv_genres(self) -> APIResponse:
        """
        Get the list of official TV show genres.
        
        Returns:
            APIResponse with TV show genres list
        """
        return await self._make_request("/genre/tv/list")
    
    # Image URL Construction
    def get_image_url(self, path: str, size: str = "w500") -> str:
        """
        Construct full image URL from TMDB image path.
        
        Args:
            path: Image path from TMDB API response
            size: Image size ('w92', 'w154', 'w185', 'w342', 'w500', 'w780', 'original')
        
        Returns:
            Full image URL
        """
        if not path:
            return ""
        
        return f"{self.image_base_url}/{size}{path}"
    
    # Correlation Analysis Methods
    def extract_correlation_features(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract correlation-ready features from TMDB item data.
        
        Args:
            item_data: Raw TMDB API response data
        
        Returns:
            Dictionary with correlation features
        """
        features = {}
        
        # Common features for movies and TV shows
        if "vote_average" in item_data:
            features["rating"] = item_data["vote_average"]
        
        if "vote_count" in item_data:
            features["vote_count"] = item_data["vote_count"]
        
        if "popularity" in item_data:
            features["popularity"] = item_data["popularity"]
        
        if "genre_ids" in item_data:
            features["genre_ids"] = item_data["genre_ids"]
            features["genre_count"] = len(item_data["genre_ids"])
        
        if "adult" in item_data:
            features["is_adult"] = item_data["adult"]
        
        if "original_language" in item_data:
            features["original_language"] = item_data["original_language"]
            features["is_english"] = item_data["original_language"] == "en"
        
        # Movie-specific features
        if "release_date" in item_data and item_data["release_date"]:
            try:
                release_date = datetime.strptime(item_data["release_date"], "%Y-%m-%d")
                features["release_year"] = release_date.year
                features["release_month"] = release_date.month
                features["release_decade"] = (release_date.year // 10) * 10
            except ValueError:
                pass
        
        if "runtime" in item_data:
            features["runtime"] = item_data["runtime"]
        
        if "budget" in item_data:
            features["budget"] = item_data["budget"]
        
        if "revenue" in item_data:
            features["revenue"] = item_data["revenue"]
            if item_data["budget"] > 0:
                features["profit"] = item_data["revenue"] - item_data["budget"]
                features["roi"] = item_data["revenue"] / item_data["budget"]
        
        # TV-specific features
        if "first_air_date" in item_data and item_data["first_air_date"]:
            try:
                first_air_date = datetime.strptime(item_data["first_air_date"], "%Y-%m-%d")
                features["first_air_year"] = first_air_date.year
                features["first_air_month"] = first_air_date.month
                features["first_air_decade"] = (first_air_date.year // 10) * 10
            except ValueError:
                pass
        
        if "number_of_seasons" in item_data:
            features["season_count"] = item_data["number_of_seasons"]
        
        if "number_of_episodes" in item_data:
            features["episode_count"] = item_data["number_of_episodes"]
        
        if "episode_run_time" in item_data and item_data["episode_run_time"]:
            features["avg_episode_runtime"] = sum(item_data["episode_run_time"]) / len(item_data["episode_run_time"])
        
        return features
    
    def extract_temporal_context(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract temporal context from TMDB item data.
        
        Args:
            item_data: Raw TMDB API response data
        
        Returns:
            Dictionary with temporal context
        """
        context = {
            "collection_timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        # Movie release dates
        if "release_date" in item_data and item_data["release_date"]:
            try:
                release_date = datetime.strptime(item_data["release_date"], "%Y-%m-%d")
                context["release_date"] = item_data["release_date"]
                context["release_timestamp"] = int(release_date.timestamp())
                context["release_year"] = release_date.year
                context["release_month"] = release_date.month
                context["release_day"] = release_date.day
            except ValueError:
                pass
        
        # TV show air dates
        if "first_air_date" in item_data and item_data["first_air_date"]:
            try:
                first_air_date = datetime.strptime(item_data["first_air_date"], "%Y-%m-%d")
                context["first_air_date"] = item_data["first_air_date"]
                context["first_air_timestamp"] = int(first_air_date.timestamp())
                context["first_air_year"] = first_air_date.year
                context["first_air_month"] = first_air_date.month
                context["first_air_day"] = first_air_date.day
            except ValueError:
                pass
        
        if "last_air_date" in item_data and item_data["last_air_date"]:
            try:
                last_air_date = datetime.strptime(item_data["last_air_date"], "%Y-%m-%d")
                context["last_air_date"] = item_data["last_air_date"]
                context["last_air_timestamp"] = int(last_air_date.timestamp())
                context["last_air_year"] = last_air_date.year
                context["last_air_month"] = last_air_date.month
                context["last_air_day"] = last_air_date.day
            except ValueError:
                pass
        
        return context
    
    def categorize_content(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Categorize TMDB content for correlation analysis.
        
        Args:
            item_data: Raw TMDB API response data
        
        Returns:
            Dictionary with content categories
        """
        categories = {}
        
        # Content type
        if "media_type" in item_data:
            categories["media_type"] = item_data["media_type"]
        elif "first_air_date" in item_data:
            categories["media_type"] = "tv"
        elif "release_date" in item_data:
            categories["media_type"] = "movie"
        
        # Rating categories
        if "vote_average" in item_data:
            rating = item_data["vote_average"]
            categories["rating_category"] = (
                "excellent" if rating >= 8.0 else
                "good" if rating >= 7.0 else
                "average" if rating >= 6.0 else
                "poor"
            )
        
        # Popularity categories
        if "popularity" in item_data:
            popularity = item_data["popularity"]
            categories["popularity_category"] = (
                "viral" if popularity >= 100 else
                "trending" if popularity >= 50 else
                "popular" if popularity >= 20 else
                "moderate" if popularity >= 5 else
                "niche"
            )
        
        # Adult content
        if "adult" in item_data:
            categories["is_adult"] = item_data["adult"]
            categories["content_rating"] = "adult" if item_data["adult"] else "general"
        
        # Language categories
        if "original_language" in item_data:
            lang = item_data["original_language"]
            categories["language_category"] = (
                "english" if lang == "en" else
                "spanish" if lang == "es" else
                "french" if lang == "fr" else
                "international"
            )
        
        return categories
    
    def prepare_correlation_data(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare complete correlation-ready data structure.
        
        Args:
            item_data: Raw TMDB API response data
        
        Returns:
            Complete correlation data structure
        """
        return {
            "raw_data": item_data,
            "correlation_features": self.extract_correlation_features(item_data),
            "temporal_context": self.extract_temporal_context(item_data),
            "content_categories": self.categorize_content(item_data),
            "data_source": "tmdb",
            "api_version": "3",
            "collection_timestamp": datetime.utcnow().isoformat() + "Z"
        }
