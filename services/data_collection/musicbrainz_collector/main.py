#!/usr/bin/env python3
"""
MusicBrainz Data Collection Service - Proof of Concept

This service demonstrates the implementation and usage of the MusicBrainz API client
following the established patterns in the Data Centralization Platform codebase.

Features:
- Environment-driven configuration following project standards
- Comprehensive music metadata collection
- Correlation-ready data extraction for cross-domain analysis
- Comprehensive logging and debugging capabilities

Usage:
    python main.py

Environment Variables:
    MUSICBRAINZ_USER_AGENT: Custom User-Agent string (required)
    MUSICBRAINZ_RATE_LIMIT_PER_SECOND: Rate limit in requests per second (default: 1.0)
    MUSICBRAINZ_DEBUG_MODE: Enable debug logging (default: false)
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# Add the shared_core package to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "packages" / "shared_core"))

from shared_core.config.musicbrainz_config import MusicBrainzConfig
from shared_core.api.clients.musicbrainz import MusicBrainzClient
from shared_core.logging.centralized_logger import CentralizedLogger


class MusicBrainzCollector:
    """
    MusicBrainz Data Collection Service.
    
    This service demonstrates comprehensive usage of the MusicBrainz API client
    for collecting music metadata and preparing it for correlation analysis.
    """
    
    def __init__(self):
        """Initialize the MusicBrainz collector."""
        self.logger = CentralizedLogger.get_logger(__name__)
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize client
        try:
            config = MusicBrainzConfig.get_client_config()
            self.client = MusicBrainzClient(**config)
            self.logger.info("MusicBrainz client initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize MusicBrainz client: {e}")
            raise
    
    async def test_connection(self) -> bool:
        """
        Test connection to the MusicBrainz API.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.logger.info("Testing MusicBrainz API connection...")
            
            # Test with a simple artist search
            response = await self.client.search_artist(query="The Beatles", limit=1)
            
            if response.success:
                self.logger.info("MusicBrainz API connection test successful")
                return True
            else:
                self.logger.error(f"MusicBrainz API connection test failed: {response.error}")
                return False
                
        except Exception as e:
            self.logger.error(f"Connection test failed: {e}")
            return False
    
    async def collect_artist_data(self, artist_query: str, limit: int = 5) -> Dict[str, Any]:
        """
        Collect artist data from MusicBrainz.
        
        Args:
            artist_query: Search query for artists
            limit: Maximum number of results to collect
            
        Returns:
            Dictionary containing collected artist data
        """
        self.logger.info(f"Collecting artist data for query: {artist_query}")
        
        try:
            # Search for artists
            response = await self.client.search_artist(query=artist_query, limit=limit)
            
            if not response.success:
                self.logger.error(f"Failed to search artists: {response.error}")
                return {}
            
            artists_data = response.data
            collected_data = {
                "query": artist_query,
                "total_results": artists_data.get("count", 0),
                "artists": [],
                "collection_timestamp": datetime.utcnow().isoformat() + "Z"
            }
            
            # Process each artist
            for artist in artists_data.get("artists", []):
                try:
                    # Prepare correlation data
                    correlation_data = self.client.prepare_correlation_data(artist)
                    
                    # Add additional metadata
                    correlation_data["search_query"] = artist_query
                    correlation_data["search_score"] = artist.get("score", 0)
                    
                    collected_data["artists"].append(correlation_data)
                    
                    self.logger.debug(f"Processed artist: {artist.get('name', 'Unknown')}")
                    
                except Exception as e:
                    self.logger.error(f"Error processing artist {artist.get('name', 'Unknown')}: {e}")
                    continue
            
            self.logger.info(f"Successfully collected data for {len(collected_data['artists'])} artists")
            return collected_data
            
        except Exception as e:
            self.logger.error(f"Error collecting artist data: {e}")
            return {}
    
    async def collect_release_data(self, release_query: str, limit: int = 5) -> Dict[str, Any]:
        """
        Collect release (album) data from MusicBrainz.
        
        Args:
            release_query: Search query for releases
            limit: Maximum number of results to collect
            
        Returns:
            Dictionary containing collected release data
        """
        self.logger.info(f"Collecting release data for query: {release_query}")
        
        try:
            # Search for releases
            response = await self.client.search_release(query=release_query, limit=limit)
            
            if not response.success:
                self.logger.error(f"Failed to search releases: {response.error}")
                return {}
            
            releases_data = response.data
            collected_data = {
                "query": release_query,
                "total_results": releases_data.get("count", 0),
                "releases": [],
                "collection_timestamp": datetime.utcnow().isoformat() + "Z"
            }
            
            # Process each release
            for release in releases_data.get("releases", []):
                try:
                    # Prepare correlation data
                    correlation_data = self.client.prepare_correlation_data(release)
                    
                    # Add additional metadata
                    correlation_data["search_query"] = release_query
                    correlation_data["search_score"] = release.get("score", 0)
                    
                    collected_data["releases"].append(correlation_data)
                    
                    self.logger.debug(f"Processed release: {release.get('title', 'Unknown')}")
                    
                except Exception as e:
                    self.logger.error(f"Error processing release {release.get('title', 'Unknown')}: {e}")
                    continue
            
            self.logger.info(f"Successfully collected data for {len(collected_data['releases'])} releases")
            return collected_data
            
        except Exception as e:
            self.logger.error(f"Error collecting release data: {e}")
            return {}
    
    async def save_data(self, data: Dict[str, Any], filename: str) -> None:
        """
        Save collected data to a JSON file.
        
        Args:
            data: Data to save
            filename: Output filename
        """
        try:
            filepath = self.output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Data saved to {filepath}")
            
        except Exception as e:
            self.logger.error(f"Error saving data to {filename}: {e}")
    
    async def generate_collection_stats(self, *datasets: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate collection statistics from collected datasets.
        
        Args:
            *datasets: Variable number of dataset dictionaries
            
        Returns:
            Dictionary containing collection statistics
        """
        stats = {
            "collection_timestamp": datetime.utcnow().isoformat() + "Z",
            "total_datasets": len(datasets),
            "datasets": [],
            "total_items": 0,
            "data_sources": ["musicbrainz"],
            "collection_duration": None
        }
        
        for dataset in datasets:
            dataset_stats = {
                "query": dataset.get("query", "unknown"),
                "total_results": dataset.get("total_results", 0),
                "items_collected": len(dataset.get("artists", dataset.get("releases", []))),
                "timestamp": dataset.get("collection_timestamp")
            }
            
            stats["datasets"].append(dataset_stats)
            stats["total_items"] += dataset_stats["items_collected"]
        
        return stats
    
    async def run_collection(self) -> None:
        """
        Run the complete data collection process.
        """
        start_time = datetime.utcnow()
        
        try:
            self.logger.info("Starting MusicBrainz data collection...")
            
            # Log configuration
            config_summary = MusicBrainzConfig.get_config_summary()
            self.logger.info(f"Configuration: {config_summary}")
            
            # Test connection
            if not await self.test_connection():
                self.logger.error("Connection test failed. Exiting.")
                return
            
            # Collect artist data
            artist_data = await self.collect_artist_data("Coldplay", limit=3)
            if artist_data:
                await self.save_data(artist_data, "artist_data.json")
            
            # Collect release data
            release_data = await self.collect_release_data("Parachutes", limit=3)
            if release_data:
                await self.save_data(release_data, "release_data.json")
            
            # Generate and save collection statistics
            stats = await self.generate_collection_stats(artist_data, release_data)
            stats["collection_duration"] = (datetime.utcnow() - start_time).total_seconds()
            await self.save_data(stats, "collection_stats.json")
            
            self.logger.info("MusicBrainz data collection completed successfully")
            
        except Exception as e:
            self.logger.error(f"Error during data collection: {e}")
            raise


async def main():
    """
    Main entry point for the MusicBrainz data collection service.
    """
    try:
        # Initialize collector
        collector = MusicBrainzCollector()
        
        # Run data collection
        await collector.run_collection()
        
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Load environment variables from .env file if it exists
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    # Run the collector
    asyncio.run(main())
