#!/usr/bin/env python3
"""
Spotify Data Collection Service - Proof of Concept

This service demonstrates the usage of the SpotifyClient for data collection and correlation analysis.
It follows the established patterns from the existing codebase and shows how to:

1. Initialize the Spotify client with proper configuration
2. Handle OAuth authentication flow
3. Collect track data with audio features
4. Extract correlation-ready data
5. Store data for further analysis

Based on the existing pokemon_collector pattern and project documentation.
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

# Add the packages to the path for proper imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "packages" / "shared_core"))

from shared_core.config.spotify_config import SpotifyConfig
from shared_core.api.clients.spotify.spotify_client import SpotifyClient
from shared_core.utils.centralized_logging import CentralizedLogger

# Initialize logger
logger = CentralizedLogger.get_logger("spotify_collector")


class SpotifyCollectorService:
    """
    Spotify data collection service for correlation analysis
    
    This service demonstrates best practices for:
    - Environment-driven configuration
    - OAuth authentication handling
    - Rate-limited data collection
    - Correlation-ready data extraction
    """
    
    def __init__(self):
        """Initialize the Spotify collector service"""
        self.logger = logger
        self.config = SpotifyConfig.get_instance()
        self.client: Optional[SpotifyClient] = None
        self.collection_stats = {
            "tracks_collected": 0,
            "artists_collected": 0,
            "audio_features_collected": 0,
            "errors": 0,
            "start_time": None,
            "end_time": None
        }
        
    async def initialize_client(self) -> bool:
        """
        Initialize the Spotify client with proper configuration
        
        Returns:
            bool: True if initialization successful
        """
        try:
            # Validate configuration
            if not self.config.validate_credentials():
                self.logger.error("Spotify credentials validation failed")
                return False
            
            # Initialize client
            self.client = SpotifyClient(
                client_id=self.config.client_id(),
                client_secret=self.config.client_secret(),
                redirect_uri=self.config.redirect_uri(),
                debug_mode=True
            )
            
            # Check if we have stored tokens
            stored_access_token = self.config.access_token()
            stored_refresh_token = self.config.refresh_token()
            
            if stored_access_token:
                self.client.access_token = stored_access_token
                self.client.refresh_token = stored_refresh_token
                self.logger.info("✅ Using stored access token")
            else:
                self.logger.warning("⚠️  No stored access token found - OAuth flow required")
                self.logger.info("📝 Use the get_authorization_url() method to start OAuth flow")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Spotify client: {e}")
            return False
    
    def get_authorization_url(self) -> str:
        """
        Get the OAuth authorization URL for manual authentication
        
        Returns:
            str: Authorization URL for user to visit
        """
        if not self.client:
            raise RuntimeError("Client not initialized. Call initialize_client() first.")
        
        auth_url = self.client.get_authorization_url()
        
        self.logger.info("🔗 Spotify OAuth Authorization Required")
        self.logger.info(f"Please visit this URL to authorize the application:")
        self.logger.info(f"{auth_url}")
        self.logger.info("After authorization, you'll receive a code - use exchange_code_for_tokens()")
        
        return auth_url
    
    async def exchange_code_for_tokens(self, authorization_code: str) -> bool:
        """
        Exchange authorization code for access tokens
        
        Args:
            authorization_code: Code received from OAuth callback
            
        Returns:
            bool: True if successful
        """
        if not self.client:
            raise RuntimeError("Client not initialized. Call initialize_client() first.")
        
        success = await self.client.exchange_code_for_tokens(authorization_code)
        
        if success:
            self.logger.info("✅ Successfully obtained access tokens")
            self.logger.info("💾 Store these tokens in your environment for future use:")
            self.logger.info(f"SPOTIFY_ACCESS_TOKEN={self.client.access_token}")
            if self.client.refresh_token:
                self.logger.info(f"SPOTIFY_REFRESH_TOKEN={self.client.refresh_token}")
        else:
            self.logger.error("❌ Failed to exchange authorization code for tokens")
        
        return success
    
    async def test_api_connection(self) -> bool:
        """
        Test API connection by fetching user profile
        
        Returns:
            bool: True if connection successful
        """
        if not self.client or not self.client.access_token:
            self.logger.error("❌ No access token available - complete OAuth flow first")
            return False
        
        try:
            response = await self.client.get_user_profile()
            
            if response.success:
                user_data = response.data
                self.logger.info(f"✅ API connection successful!")
                self.logger.info(f"👤 Authenticated as: {user_data.get('display_name', 'Unknown')}")
                self.logger.info(f"🎵 Country: {user_data.get('country', 'Unknown')}")
                self.logger.info(f"👥 Followers: {user_data.get('followers', {}).get('total', 0)}")
                return True
            else:
                self.logger.error(f"❌ API connection failed: {response.errors}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ API connection test failed: {e}")
            return False
    
    async def collect_user_top_tracks(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Collect user's top tracks with audio features
        
        Args:
            limit: Number of tracks to collect
            
        Returns:
            List[Dict[str, Any]]: Tracks with audio features
        """
        if not self.client or not self.client.access_token:
            self.logger.error("❌ No access token available")
            return []
        
        try:
            self.logger.info(f"🎵 Collecting top {limit} tracks...")
            
            # Get user's top tracks
            tracks_response = await self.client.get_user_top_tracks(limit=limit)
            
            if not tracks_response.success:
                self.logger.error(f"❌ Failed to fetch top tracks: {tracks_response.errors}")
                return []
            
            tracks = tracks_response.data.get('items', [])
            self.logger.info(f"📥 Retrieved {len(tracks)} tracks")
            
            # Extract track IDs for audio features
            track_ids = [track['id'] for track in tracks]
            
            # Get audio features in batches
            enhanced_tracks = []
            batch_size = 100  # Spotify API limit
            
            for i in range(0, len(track_ids), batch_size):
                batch_ids = track_ids[i:i+batch_size]
                
                self.logger.info(f"📊 Fetching audio features for batch {i//batch_size + 1}")
                
                features_response = await self.client.get_multiple_tracks_audio_features(batch_ids)
                
                if features_response.success:
                    audio_features = features_response.data.get('audio_features', [])
                    
                    # Combine track data with audio features
                    for j, track in enumerate(tracks[i:i+batch_size]):
                        if j < len(audio_features) and audio_features[j]:
                            enhanced_track = {
                                **track,
                                'audio_features': audio_features[j],
                                'correlation_features': self.client.extract_audio_features_for_correlation(audio_features[j]),
                                'isrc': self.client.extract_isrc_for_cross_linking(track),
                                'collection_timestamp': datetime.now().isoformat()
                            }
                            enhanced_tracks.append(enhanced_track)
                            self.collection_stats['tracks_collected'] += 1
                            self.collection_stats['audio_features_collected'] += 1
                        else:
                            self.logger.warning(f"⚠️  No audio features for track: {track.get('name', 'Unknown')}")
                
                # Rate limiting courtesy
                await asyncio.sleep(0.1)
            
            self.logger.info(f"✅ Successfully collected {len(enhanced_tracks)} tracks with audio features")
            return enhanced_tracks
            
        except Exception as e:
            self.logger.error(f"❌ Error collecting top tracks: {e}")
            self.collection_stats['errors'] += 1
            return []
    
    async def collect_recently_played(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Collect recently played tracks with timestamps
        
        Args:
            limit: Number of tracks to collect
            
        Returns:
            List[Dict[str, Any]]: Recently played tracks with context
        """
        if not self.client or not self.client.access_token:
            self.logger.error("❌ No access token available")
            return []
        
        try:
            self.logger.info(f"🕐 Collecting {limit} recently played tracks...")
            
            response = await self.client.get_user_recently_played(limit=limit)
            
            if not response.success:
                self.logger.error(f"❌ Failed to fetch recently played: {response.errors}")
                return []
            
            items = response.data.get('items', [])
            self.logger.info(f"📥 Retrieved {len(items)} recently played tracks")
            
            # Extract tracks and add temporal context
            recent_tracks = []
            for item in items:
                track = item.get('track', {})
                played_at = item.get('played_at')
                
                enhanced_track = {
                    **track,
                    'played_at': played_at,
                    'context': item.get('context', {}),
                    'isrc': self.client.extract_isrc_for_cross_linking(track),
                    'collection_timestamp': datetime.now().isoformat()
                }
                recent_tracks.append(enhanced_track)
                self.collection_stats['tracks_collected'] += 1
            
            self.logger.info(f"✅ Successfully collected {len(recent_tracks)} recently played tracks")
            return recent_tracks
            
        except Exception as e:
            self.logger.error(f"❌ Error collecting recently played tracks: {e}")
            self.collection_stats['errors'] += 1
            return []
    
    async def search_and_analyze(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Search for tracks and analyze audio features
        
        Args:
            query: Search query
            limit: Number of results to analyze
            
        Returns:
            List[Dict[str, Any]]: Search results with audio features
        """
        if not self.client or not self.client.access_token:
            self.logger.error("❌ No access token available")
            return []
        
        try:
            self.logger.info(f"🔍 Searching for: '{query}'")
            
            # Search for tracks
            search_response = await self.client.search_tracks(query, limit=limit)
            
            if not search_response.success:
                self.logger.error(f"❌ Search failed: {search_response.errors}")
                return []
            
            tracks = search_response.data.get('tracks', {}).get('items', [])
            self.logger.info(f"📥 Found {len(tracks)} tracks")
            
            # Get audio features for search results
            track_ids = [track['id'] for track in tracks]
            enhanced_tracks = []
            
            if track_ids:
                features_response = await self.client.get_multiple_tracks_audio_features(track_ids)
                
                if features_response.success:
                    audio_features = features_response.data.get('audio_features', [])
                    
                    for i, track in enumerate(tracks):
                        if i < len(audio_features) and audio_features[i]:
                            enhanced_track = {
                                **track,
                                'audio_features': audio_features[i],
                                'correlation_features': self.client.extract_audio_features_for_correlation(audio_features[i]),
                                'isrc': self.client.extract_isrc_for_cross_linking(track),
                                'search_query': query,
                                'collection_timestamp': datetime.now().isoformat()
                            }
                            enhanced_tracks.append(enhanced_track)
                            self.collection_stats['tracks_collected'] += 1
                            self.collection_stats['audio_features_collected'] += 1
            
            self.logger.info(f"✅ Successfully analyzed {len(enhanced_tracks)} search results")
            return enhanced_tracks
            
        except Exception as e:
            self.logger.error(f"❌ Error in search and analyze: {e}")
            self.collection_stats['errors'] += 1
            return []
    
    def save_data_to_json(self, data: List[Dict[str, Any]], filename: str) -> bool:
        """
        Save collected data to JSON file
        
        Args:
            data: Data to save
            filename: Output filename
            
        Returns:
            bool: True if successful
        """
        try:
            output_path = Path(__file__).parent / "output" / filename
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"💾 Saved {len(data)} records to {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error saving data: {e}")
            return False
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get collection statistics"""
        return {
            **self.collection_stats,
            "client_metrics": self.client.get_metrics_summary() if self.client else {},
            "config_summary": self.config.get_config_summary()
        }
    
    async def run_proof_of_concept(self) -> bool:
        """
        Run the complete proof of concept demonstration
        
        Returns:
            bool: True if successful
        """
        self.collection_stats['start_time'] = datetime.now().isoformat()
        
        try:
            self.logger.info("🚀 Starting Spotify Data Collection Proof of Concept")
            self.logger.info("=" * 60)
            
            # Step 1: Initialize client
            self.logger.info("1️⃣ Initializing Spotify client...")
            if not await self.initialize_client():
                return False
            
            # Step 2: Test API connection
            self.logger.info("2️⃣ Testing API connection...")
            if not await self.test_api_connection():
                self.logger.error("❌ API connection failed - check your tokens")
                return False
            
            # Step 3: Collect user's top tracks
            self.logger.info("3️⃣ Collecting user's top tracks...")
            top_tracks = await self.collect_user_top_tracks(limit=20)
            if top_tracks:
                self.save_data_to_json(top_tracks, "top_tracks.json")
            
            # Step 4: Collect recently played tracks
            self.logger.info("4️⃣ Collecting recently played tracks...")
            recent_tracks = await self.collect_recently_played(limit=20)
            if recent_tracks:
                self.save_data_to_json(recent_tracks, "recent_tracks.json")
            
            # Step 5: Search and analyze
            self.logger.info("5️⃣ Searching and analyzing tracks...")
            search_results = await self.search_and_analyze("electronic dance music", limit=10)
            if search_results:
                self.save_data_to_json(search_results, "search_results.json")
            
            # Step 6: Generate summary
            self.logger.info("6️⃣ Generating collection summary...")
            stats = self.get_collection_stats()
            self.save_data_to_json([stats], "collection_stats.json")
            
            self.logger.info("=" * 60)
            self.logger.info("✅ Proof of Concept completed successfully!")
            self.logger.info(f"📊 Total tracks collected: {stats['tracks_collected']}")
            self.logger.info(f"📊 Audio features collected: {stats['audio_features_collected']}")
            self.logger.info(f"❌ Errors encountered: {stats['errors']}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Proof of concept failed: {e}")
            return False
        finally:
            self.collection_stats['end_time'] = datetime.now().isoformat()


async def main():
    """Main entry point for the proof of concept"""
    
    # Initialize the service
    service = SpotifyCollectorService()
    
    # Check if we need to start OAuth flow
    try:
        config = SpotifyConfig.get_instance()
        if not config.access_token():
            print("🔑 OAuth setup required:")
            print("1. Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in your environment")
            print("2. Run the service to get authorization URL")
            print("3. Complete OAuth flow and set SPOTIFY_ACCESS_TOKEN")
            print("\nExample .env file:")
            print("SPOTIFY_CLIENT_ID=your_client_id_here")
            print("SPOTIFY_CLIENT_SECRET=your_client_secret_here")
            print("SPOTIFY_REDIRECT_URI=http://localhost:8080/callback")
            print("# After OAuth:")
            print("SPOTIFY_ACCESS_TOKEN=your_access_token_here")
            print("SPOTIFY_REFRESH_TOKEN=your_refresh_token_here")
            
            # Initialize client to show auth URL
            if await service.initialize_client():
                service.get_authorization_url()
            
            return
        
        # Run the proof of concept
        success = await service.run_proof_of_concept()
        
        if success:
            print("\n🎉 Spotify client proof of concept completed successfully!")
            print("📁 Check the output/ directory for collected data files")
        else:
            print("\n❌ Proof of concept failed - check the logs for details")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return


if __name__ == "__main__":
    asyncio.run(main())
