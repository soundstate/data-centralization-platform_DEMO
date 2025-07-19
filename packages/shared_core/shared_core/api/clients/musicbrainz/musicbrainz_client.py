"""
MusicBrainz API Client

This module provides a client for interacting with the MusicBrainz API.
It follows the established patterns for API clients in the shared_core package.

The MusicBrainz API provides access to:
- Artist information
- Album information
- Track details
- Search functionality across all entities

Features:
- Rate limiting adherence per MusicBrainz guidelines
- Retry logic with exponential backoff
- Comprehensive error handling
- Correlation-ready data extraction
- Temporal and categorical context
"""

import asyncio
import logging
from typing import Dict, Optional, Any
from datetime import datetime

from shared_core.api.clients.base_client import BaseAPIClient, APIResponse


class MusicBrainzClient(BaseAPIClient):
    """
    MusicBrainz API Client for accessing the MusicBrainz database.
    
    This client provides comprehensive access to artist, album, and track data
    from MusicBrainz, with built-in rate limiting, error handling, and correlation-ready
    data extraction.
    
    Rate Limits:
    - An average of 1 request per second
    
    Authentication:
    - No API key required for standard requests
    - User-agent header required
    """

    def __init__(
        self,
        user_agent: str,
        base_url: str = "https://musicbrainz.org/ws/2",
        rate_limit_per_second: float = 1.0,
        max_retries: int = 3,
        timeout: int = 30,
        debug_mode: bool = False
    ):
        """
        Initialize MusicBrainz API client.
        
        Args:
            user_agent: Custom User-Agent string required by MusicBrainz
            base_url: Base URL for MusicBrainz API (default: https://musicbrainz.org/ws/2)
            rate_limit_per_second: Rate limit in requests per second (default: 1.0)
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

        self.logger = logging.getLogger(__name__)
        self.headers = {
            "User-Agent": user_agent
        }

        if debug_mode:
            self.logger.setLevel(logging.DEBUG)
            self.logger.debug("MusicBrainz client initialized in debug mode")

    async def _make_request(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None
    ) -> APIResponse:
        """
        Make a request to the MusicBrainz API.
        
        Args:
            endpoint: API endpoint (e.g., "/artist")
            params: Query parameters
            
        Returns:
            APIResponse object with success status and data
        """

        try:
            response = await self._request(
                method="GET",
                url=f"{self.base_url}/{endpoint}",
                params=params,
                headers=self.headers
            )

            if response.status_code == 200:
                data = response.json()
                return APIResponse(success=True, data=data, status_code=response.status_code)
            else:
                error_msg = f"MusicBrainz API error: {response.status_code}"
                if response.text:
                    error_msg += f" - {response.text}"

                self.logger.error(error_msg)
                return APIResponse(success=False, error=error_msg, status_code=response.status_code)

        except Exception as e:
            error_msg = f"Request failed: {str(e)}"
            self.logger.error(error_msg)
            return APIResponse(success=False, error=error_msg)

    async def get_artist(self, mbid: str, inc: Optional[str] = None) -> APIResponse:
        """
        Get information about an artist given their MBID (MusicBrainz ID).
        
        Args:
            mbid: MusicBrainz identifier for the artist
            inc: Include additional information (e.g., "releases", "discography")

        Returns:
            APIResponse with artist details
        """
        params = {"inc": inc} if inc else {}
        return await self._make_request(f"artist/{mbid}", params=params)

    async def get_release(self, mbid: str, inc: Optional[str] = None) -> APIResponse:
        """
        Get information about a release (album) given its MBID.
        
        Args:
            mbid: MusicBrainz identifier for the release
            inc: Include additional information (e.g., "recordings", "artists")

        Returns:
            APIResponse with release details
        """
        params = {"inc": inc} if inc else {}
        return await self._make_request(f"release/{mbid}", params=params)

    async def search_artist(self, query: str, limit: int = 10, offset: int = 0) -> APIResponse:
        """
        Search for artists.
        
        Args:
            query: Search query
            limit: Number of results to return (default: 10)
            offset: Offset for pagination (default: 0)

        Returns:
            APIResponse with search results
        """
        params = {
            "query": query,
            "limit": limit,
            "offset": offset
        }
        return await self._make_request("artist", params=params)

    async def search_release(self, query: str, limit: int = 10, offset: int = 0) -> APIResponse:
        """
        Search for releases (albums).
        
        Args:
            query: Search query
            limit: Number of results to return (default: 10)
            offset: Offset for pagination (default: 0)

        Returns:
            APIResponse with search results
        """
        params = {
            "query": query,
            "limit": limit,
            "offset": offset
        }
        return await self._make_request("release", params=params)

    def extract_correlation_features(self, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract correlation-ready features from MusicBrainz entity data.
        
        Args:
            entity_data: Raw MusicBrainz API response data

        Returns:
            Dictionary with correlation features
        """
        # Example implementation, can be expanded
        features = {}
        if "name" in entity_data:
            features["name"] = entity_data["name"]
        if "id" in entity_data:
            features["mbid"] = entity_data["id"]
        if "disambiguation" in entity_data:
            features["disambiguation"] = entity_data["disambiguation"]
        return features

    def extract_temporal_context(self, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract temporal context from MusicBrainz entity data.
        
        Args:
            entity_data: Raw MusicBrainz API response data

        Returns:
            Dictionary with temporal context
        """
        context = {}
        if "life-span" in entity_data:
            context["life_span"] = entity_data.get("life-span", {})
        return context

    def prepare_correlation_data(self, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare complete correlation-ready data structure.
        
        Args:
            entity_data: Raw MusicBrainz API response data

        Returns:
            Complete correlation data structure
        """
        return {
            "raw_data": entity_data,
            "correlation_features": self.extract_correlation_features(entity_data),
            "temporal_context": self.extract_temporal_context(entity_data),
            "data_source": "musicbrainz",
            "collection_timestamp": datetime.utcnow().isoformat() + "Z"
        }
