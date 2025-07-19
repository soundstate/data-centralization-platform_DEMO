#!/usr/bin/env python3
"""
OpenWeatherMap Data Collection Service - Proof of Concept

This service demonstrates the usage of the OpenWeatherMapClient for weather data collection and correlation analysis.
It follows the established patterns from the existing codebase and shows how to:

1. Initialize the OpenWeatherMap client with proper configuration
2. Fetch weather and air quality data
3. Extract correlation-ready weather data
4. Store data for further analysis

Based on project best practices and configuration standards.
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

# Add the packages to the path for proper imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "packages" / "shared_core"))

from shared_core.config.openweathermap_config import OpenWeatherMapConfig
from shared_core.api.clients.openweathermap import OpenWeatherMapClient
from shared_core.utils.centralized_logging import CentralizedLogger

# Initialize logger
logger = CentralizedLogger.get_logger("openweathermap_collector")


class OpenWeatherMapCollectorService:
    """
    OpenWeatherMap data collection service for correlation analysis
    
    This service demonstrates best practices for:
    - Environment-driven configuration
    - API data collection
    - Correlation-ready data extraction
    """
    
    def __init__(self):
        """Initialize the OpenWeatherMap collector service"""
        self.logger = logger
        self.config = OpenWeatherMapConfig.get_instance()
        self.client: Optional[OpenWeatherMapClient] = None
        self.collection_stats = {
            "data_collected": 0,
            "errors": 0,
            "start_time": None,
            "end_time": None
        }
        
    async def initialize_client(self) -> bool:
        """
        Initialize the OpenWeatherMap client with proper configuration
        
        Returns:
            bool: True if initialization successful
        """
        try:
            # Validate configuration
            if not self.config.validate_credentials():
                self.logger.error("OpenWeatherMap credentials validation failed")
                return False
            
            # Initialize client
            self.client = OpenWeatherMapClient(api_key=self.config.api_key(), debug_mode=True)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize OpenWeatherMap client: {e}")
            return False
    
    async def test_api_connection(self, lat: float = 0.0, lon: float = 0.0) -> bool:
        """
        Test API connection by fetching current weather
        
        Returns:
            bool: True if connection successful
        """
        if not self.client:
            self.logger.error("❌ Client not initialized")
            return False
        
        try:
            response = await self.client.get_current_weather(lat=lat, lon=lon)
            
            if response.success:
                weather_data = response.data
                self.logger.info(f"✅ API connection successful!")
                self.logger.info(f"🌡️ Temperature: {weather_data.get('main', {}).get('temp', 'Unknown')} °C")
                self.logger.info(f"🌬️ Wind Speed: {weather_data.get('wind', {}).get('speed', 'Unknown')} m/s")
                return True
            else:
                self.logger.error(f"❌ API connection failed: {response.errors}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ API connection test failed: {e}")
            return False
    
    async def collect_weather_data(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """
        Collect current weather data with correlation-ready features
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Optional[Dict[str, Any]]: Combined data including correlation features
        """
        if not self.client:
            self.logger.error("❌ Client not initialized")
            return None
        
        try:
            self.logger.info(f"🌍 Collecting weather data for coords: ({lat}, {lon})")
            
            weather_response = await self.client.get_current_weather(lat=lat, lon=lon)
            
            if not weather_response.success:
                self.logger.error(f"❌ Failed to fetch weather data: {weather_response.errors}")
                return None
            
            weather_data = weather_response.data
            
            # Prepare correlation data
            correlation_data = self.client.prepare_correlation_data(weather_data)
            
            self.collection_stats['data_collected'] += 1
            return correlation_data
            
        except Exception as e:
            self.logger.error(f"❌ Error collecting weather data: {e}")
            self.collection_stats['errors'] += 1
            return None
    
    async def collect_air_quality_data(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """
        Collect current air quality data
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Optional[Dict[str, Any]]: Air quality data
        """
        if not self.client:
            self.logger.error("❌ Client not initialized")
            return None
        
        try:
            self.logger.info(f"🛢️ Collecting air quality data for coords: ({lat}, {lon})")
            
            air_quality_response = await self.client.get_air_quality(lat=lat, lon=lon)
            
            if not air_quality_response.success:
                self.logger.error(f"❌ Failed to fetch air quality data: {air_quality_response.errors}")
                return None
            
            air_quality_data = air_quality_response.data
            
            # Combine with geographic context
            geographic_context = self.client.extract_geographic_context(air_quality_data)
            combined_data = {
                "air_quality_data": air_quality_data,
                **geographic_context,
                "data_source": "openweathermap",
                "collection_timestamp": datetime.now().isoformat()
            }
            
            self.collection_stats['data_collected'] += 1
            return combined_data
            
        except Exception as e:
            self.logger.error(f"❌ Error collecting air quality data: {e}")
            self.collection_stats['errors'] += 1
            return None
    
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
    
    async def run_proof_of_concept(self, lat: float, lon: float) -> bool:
        """
        Run the complete proof of concept demonstration
        
        Args:
            lat: Latitude for data collection
            lon: Longitude for data collection
            
        Returns:
            bool: True if successful
        """
        self.collection_stats['start_time'] = datetime.now().isoformat()
        
        try:
            self.logger.info("🚀 Starting OpenWeatherMap Data Collection Proof of Concept")
            self.logger.info("=" * 60)
            
            # Step 1: Initialize client
            self.logger.info("1️⃣ Initializing OpenWeatherMap client...")
            if not await self.initialize_client():
                return False
            
            # Step 2: Test API connection
            self.logger.info("2️⃣ Testing API connection...")
            if not await self.test_api_connection(lat=lat, lon=lon):
                self.logger.error("❌ API connection failed - check your API key")
                return False
            
            # Step 3: Collect current weather data
            self.logger.info("3️⃣ Collecting current weather data...")
            weather_data = await self.collect_weather_data(lat=lat, lon=lon)
            if weather_data:
                self.save_data_to_json([weather_data], "current_weather.json")
            
            # Step 4: Collect air quality data
            self.logger.info("4️⃣ Collecting air quality data...")
            air_quality_data = await self.collect_air_quality_data(lat=lat, lon=lon)
            if air_quality_data:
                self.save_data_to_json([air_quality_data], "air_quality.json")
            
            # Step 5: Generate summary
            self.logger.info("5️⃣ Generating collection summary...")
            stats = self.get_collection_stats()
            self.save_data_to_json([stats], "collection_stats.json")
            
            self.logger.info("=" * 60)
            self.logger.info("✅ Proof of Concept completed successfully!")
            self.logger.info(f"📊 Total data collected: {stats['data_collected']}")
            self.logger.info(f"❌ Errors encountered: {stats['errors']}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Proof of concept failed: {e}")
            return False
        finally:
            self.collection_stats['end_time'] = datetime.now().isoformat()


async def main():
    """Main entry point for the proof of concept"""
    service = OpenWeatherMapCollectorService()
    
    # Example coordinates for testing (London)
    lat, lon = 51.5074, -0.1278
    
    # Run the proof of concept
    success = await service.run_proof_of_concept(lat, lon)
    
    if success:
        print("\n🎉 OpenWeatherMap client proof of concept completed successfully!")
        print("📁 Check the output/ directory for collected data files")
    else:
        print("\n❌ Proof of concept failed - check the logs for details")


if __name__ == "__main__":
    asyncio.run(main())
