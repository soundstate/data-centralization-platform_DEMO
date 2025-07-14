"""
Spotify API Client

Comprehensive client for Spotify Web API with:
- OAuth 2.0 authentication flow
- Track audio features analysis
- Artist and album metadata
- Search functionality
- Cross-domain linking (ISRC codes)
"""

import base64
import secrets
import urllib.parse
from typing import Dict, List, Optional, Any

from .base_client import BaseAPIClient, APIResponse
from ...config.logging_config import get_logger


class SpotifyClient(BaseAPIClient):
    """
    Spotify Web API client with OAuth 2.0 support
    """
    
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str = "http://localhost:8080/callback",
        debug_mode: bool = True,
        **kwargs
    ):
        """
        Initialize Spotify client
        
        Args:
            client_id: Spotify app client ID
            client_secret: Spotify app client secret
            redirect_uri: OAuth redirect URI
            debug_mode: Enable debug logging
            **kwargs: Additional BaseAPIClient arguments
        """
        super().__init__(
            base_url="https://api.spotify.com/v1",
            debug_mode=debug_mode,
            rate_limit_per_minute=100,  # Spotify allows 100 requests per minute
            client_name="spotify",
            **kwargs
        )
        
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.token_expires_at: Optional[int] = None
        
        # Override headers for Spotify API
        self.auth_base_url = "https://accounts.spotify.com"
        
        if self.debug_mode:
            self.logger.info(f"🎵 Initialized Spotify client for app: {client_id}")
    
    def _get_default_headers(self) -> Dict[str, str]:
        """Override to use Spotify-specific headers"""
        headers = {
            "Content-Type": "application/json",
            "User-Agent": f"DataCentralization/spotify",
        }
        
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        
        return headers
    
    def get_authorization_url(self, scopes: List[str] = None) -> str:
        """
        Generate Spotify authorization URL for OAuth flow
        
        Args:
            scopes: List of Spotify scopes to request
            
        Returns:
            str: Authorization URL for user to visit
        """
        if scopes is None:
            scopes = [
                "user-read-private",
                "user-read-email", 
                "user-library-read",
                "user-top-read",
                "user-read-recently-played",
                "playlist-read-private"
            ]
        
        state = secrets.token_urlsafe(32)
        
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "scope": " ".join(scopes),
            "redirect_uri": self.redirect_uri,
            "state": state
        }
        
        auth_url = f"{self.auth_base_url}/authorize?" + urllib.parse.urlencode(params)
        
        if self.debug_mode:
            self.logger.info(f"🔗 Generated auth URL with scopes: {scopes}")
        
        return auth_url
    
    async def exchange_code_for_tokens(self, authorization_code: str) -> bool:
        """
        Exchange authorization code for access tokens
        
        Args:
            authorization_code: Code from Spotify OAuth callback
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Prepare token request
        auth_header = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()
        
        headers = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": self.redirect_uri
        }
        
        try:
            response = await self.client.post(
                f"{self.auth_base_url}/api/token",
                headers=headers,
                data=data
            )
            
            if response.is_success:
                token_data = response.json()
                self.access_token = token_data["access_token"]
                self.refresh_token = token_data.get("refresh_token")
                self.token_expires_at = token_data.get("expires_in")
                
                if self.debug_mode:
                    self.logger.info("✅ Successfully obtained access tokens")
                
                return True
            else:
                if self.debug_mode:
                    self.logger.error(f"❌ Token exchange failed: {response.text}")
                return False
                
        except Exception as e:
            if self.debug_mode:
                self.logger.error(f"❌ Token exchange error: {str(e)}")
            return False
    
    async def refresh_access_token(self) -> bool:
        """
        Refresh access token using refresh token
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.refresh_token:
            if self.debug_mode:
                self.logger.error("❌ No refresh token available")
            return False
        
        auth_header = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()
        
        headers = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }
        
        try:
            response = await self.client.post(
                f"{self.auth_base_url}/api/token",
                headers=headers,
                data=data
            )
            
            if response.is_success:
                token_data = response.json()
                self.access_token = token_data["access_token"]
                if token_data.get("refresh_token"):
                    self.refresh_token = token_data["refresh_token"]
                
                if self.debug_mode:
                    self.logger.info("🔄 Successfully refreshed access token")
                
                return True
            else:
                if self.debug_mode:
                    self.logger.error(f"❌ Token refresh failed: {response.text}")
                return False
                
        except Exception as e:
            if self.debug_mode:
                self.logger.error(f"❌ Token refresh error: {str(e)}")
            return False
    
    async def get_user_profile(self) -> APIResponse:
        """
        Get current user's profile information
        
        Returns:
            APIResponse: User profile data
        """
        return await self.request("GET", "/me")
    
    async def search_tracks(
        self, 
        query: str, 
        limit: int = 20, 
        offset: int = 0
    ) -> APIResponse:
        """
        Search for tracks on Spotify
        
        Args:
            query: Search query string
            limit: Number of results to return (max 50)
            offset: Index of first result to return
            
        Returns:
            APIResponse: Search results
        """
        params = {
            "q": query,
            "type": "track",
            "limit": min(limit, 50),
            "offset": offset
        }
        
        return await self.request("GET", "/search", params=params)
    
    async def get_track(self, track_id: str) -> APIResponse:
        """
        Get track metadata by Spotify ID
        
        Args:
            track_id: Spotify track ID
            
        Returns:
            APIResponse: Track metadata
        """
        return await self.request("GET", f"/tracks/{track_id}")
    
    async def get_track_audio_features(self, track_id: str) -> APIResponse:
        """
        Get audio features for a track (crucial for correlations!)
        
        Args:
            track_id: Spotify track ID
            
        Returns:
            APIResponse: Audio features including valence, energy, etc.
        """
        return await self.request("GET", f"/audio-features/{track_id}")
    
    async def get_multiple_tracks_audio_features(self, track_ids: List[str]) -> APIResponse:
        """
        Get audio features for multiple tracks (up to 100)
        
        Args:
            track_ids: List of Spotify track IDs
            
        Returns:
            APIResponse: Audio features for all tracks
        """
        # Spotify allows up to 100 IDs at once
        track_ids = track_ids[:100]
        params = {"ids": ",".join(track_ids)}
        
        return await self.request("GET", "/audio-features", params=params)
    
    async def get_artist(self, artist_id: str) -> APIResponse:
        """
        Get artist metadata by Spotify ID
        
        Args:
            artist_id: Spotify artist ID
            
        Returns:
            APIResponse: Artist metadata
        """
        return await self.request("GET", f"/artists/{artist_id}")
    
    async def get_artist_albums(
        self, 
        artist_id: str, 
        include_groups: List[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> APIResponse:
        """
        Get artist's albums
        
        Args:
            artist_id: Spotify artist ID
            include_groups: Types to include (album, single, appears_on, compilation)
            limit: Number of results to return
            offset: Index of first result to return
            
        Returns:
            APIResponse: Artist's albums
        """
        if include_groups is None:
            include_groups = ["album", "single"]
        
        params = {
            "include_groups": ",".join(include_groups),
            "limit": min(limit, 50),
            "offset": offset
        }
        
        return await self.request("GET", f"/artists/{artist_id}/albums", params=params)
    
    async def get_user_top_tracks(
        self, 
        time_range: str = "medium_term",
        limit: int = 20,
        offset: int = 0
    ) -> APIResponse:
        """
        Get user's top tracks (requires authentication)
        
        Args:
            time_range: Time period (short_term, medium_term, long_term)
            limit: Number of results to return
            offset: Index of first result to return
            
        Returns:
            APIResponse: User's top tracks
        """
        params = {
            "time_range": time_range,
            "limit": min(limit, 50),
            "offset": offset
        }
        
        return await self.request("GET", "/me/top/tracks", params=params)
    
    async def get_user_recently_played(
        self, 
        limit: int = 20,
        before: Optional[int] = None,
        after: Optional[int] = None
    ) -> APIResponse:
        """
        Get user's recently played tracks (requires authentication)
        
        Args:
            limit: Number of results to return (max 50)
            before: Unix timestamp for tracks played before this time
            after: Unix timestamp for tracks played after this time
            
        Returns:
            APIResponse: Recently played tracks with play times
        """
        params = {"limit": min(limit, 50)}
        
        if before:
            params["before"] = before
        if after:
            params["after"] = after
        
        return await self.request("GET", "/me/player/recently-played", params=params)
    
    async def get_recommendations(
        self,
        seed_tracks: List[str] = None,
        seed_artists: List[str] = None,
        seed_genres: List[str] = None,
        limit: int = 20,
        **audio_features
    ) -> APIResponse:
        """
        Get track recommendations based on seeds and audio features
        
        Args:
            seed_tracks: List of track IDs for recommendations
            seed_artists: List of artist IDs for recommendations
            seed_genres: List of genre strings for recommendations
            limit: Number of recommendations to return
            **audio_features: Audio feature targets (e.g., target_valence=0.8)
            
        Returns:
            APIResponse: Recommended tracks
        """
        params = {"limit": min(limit, 100)}
        
        if seed_tracks:
            params["seed_tracks"] = ",".join(seed_tracks[:5])
        if seed_artists:
            params["seed_artists"] = ",".join(seed_artists[:5])
        if seed_genres:
            params["seed_genres"] = ",".join(seed_genres[:5])
        
        # Add audio feature parameters
        for feature, value in audio_features.items():
            params[feature] = value
        
        return await self.request("GET", "/recommendations", params=params)
    
    async def get_available_genres(self) -> APIResponse:
        """
        Get available genre seeds for recommendations
        
        Returns:
            APIResponse: Available genres
        """
        return await self.request("GET", "/recommendations/available-genre-seeds")
    
    def extract_isrc_for_cross_linking(self, track_data: Dict[str, Any]) -> Optional[str]:
        """
        Extract ISRC code from track data for cross-domain linking
        
        Args:
            track_data: Track data from Spotify API
            
        Returns:
            Optional[str]: ISRC code if available
        """
        external_ids = track_data.get("external_ids", {})
        isrc = external_ids.get("isrc")
        
        if isrc and self.debug_mode:
            self.logger.debug(f"🔗 Found ISRC for cross-linking: {isrc}")
        
        return isrc
    
    def extract_audio_features_for_correlation(self, features_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Extract key audio features for correlation analysis
        
        Args:
            features_data: Audio features from Spotify API
            
        Returns:
            Dict[str, float]: Key features for correlation analysis
        """
        correlation_features = {
            "valence": features_data.get("valence"),  # Positivity (0.0-1.0)
            "energy": features_data.get("energy"),    # Energy (0.0-1.0)  
            "danceability": features_data.get("danceability"),  # Danceability (0.0-1.0)
            "acousticness": features_data.get("acousticness"),  # Acoustic vs electric
            "instrumentalness": features_data.get("instrumentalness"),  # Instrumental vs vocal
            "tempo": features_data.get("tempo"),      # BPM
            "loudness": features_data.get("loudness"), # Loudness in dB
            "speechiness": features_data.get("speechiness")  # Spoken word content
        }
        
        # Filter out None values
        correlation_features = {k: v for k, v in correlation_features.items() if v is not None}
        
        if self.debug_mode:
            self.logger.debug(f"📊 Extracted features for correlation: {list(correlation_features.keys())}")
        
        return correlation_features
