"""
OpenWeatherMap API Client

Comprehensive client for OpenWeatherMap API with:
- Current weather data
- Historical weather data
- Weather forecasts
- Air quality data
- Geographic correlation support
- Temporal correlation ready data
"""

import time
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from urllib.parse import urlencode

from shared_core.config.base_client import BaseAPIClient, APIResponse
from shared_core.config.logging_config import get_logger


class OpenWeatherMapClient(BaseAPIClient):
    """
    OpenWeatherMap API client for weather data collection and correlation analysis
    """
    
    def __init__(
        self,
        api_key: str,
        debug_mode: bool = True,
        **kwargs
    ):
        """
        Initialize OpenWeatherMap client
        
        Args:
            api_key: OpenWeatherMap API key
            debug_mode: Enable debug logging
            **kwargs: Additional BaseAPIClient arguments
        """
        super().__init__(
            base_url="https://api.openweathermap.org/data/2.5",
            debug_mode=debug_mode,
            rate_limit_per_minute=60,  # Free tier: 60 calls/minute
            client_name="openweathermap",
            **kwargs
        )
        
        self.api_key = api_key
        self.geo_base_url = "https://api.openweathermap.org/geo/1.0"
        self.onecall_base_url = "https://api.openweathermap.org/data/3.0"
        
        if self.debug_mode:
            self.logger.info(f"🌤️ Initialized OpenWeatherMap client")
    
    def _get_default_headers(self) -> Dict[str, str]:
        """Override to use OpenWeatherMap-specific headers"""
        return {
            "Content-Type": "application/json",
            "User-Agent": f"DataCentralization/openweathermap",
        }
    
    def _add_api_key_to_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Add API key to request parameters"""
        params = params.copy() if params else {}
        params["appid"] = self.api_key
        return params
    
    async def get_current_weather(
        self,
        lat: float,
        lon: float,
        units: str = "metric"
    ) -> APIResponse:
        """
        Get current weather data by coordinates
        
        Args:
            lat: Latitude
            lon: Longitude
            units: Units (metric, imperial, kelvin)
            
        Returns:
            APIResponse: Current weather data
        """
        params = self._add_api_key_to_params({
            "lat": lat,
            "lon": lon,
            "units": units
        })
        
        return await self.request("GET", "/weather", params=params)
    
    async def get_current_weather_by_city(
        self,
        city_name: str,
        country_code: Optional[str] = None,
        units: str = "metric"
    ) -> APIResponse:
        """
        Get current weather data by city name
        
        Args:
            city_name: City name
            country_code: ISO 3166 country code (optional)
            units: Units (metric, imperial, kelvin)
            
        Returns:
            APIResponse: Current weather data
        """
        query = city_name
        if country_code:
            query = f"{city_name},{country_code}"
        
        params = self._add_api_key_to_params({
            "q": query,
            "units": units
        })
        
        return await self.request("GET", "/weather", params=params)
    
    async def get_forecast(
        self,
        lat: float,
        lon: float,
        units: str = "metric",
        cnt: int = 40  # Number of timestamps (max 40 for 5-day forecast)
    ) -> APIResponse:
        """
        Get 5-day weather forecast with 3-hour intervals
        
        Args:
            lat: Latitude
            lon: Longitude
            units: Units (metric, imperial, kelvin)
            cnt: Number of timestamps to return
            
        Returns:
            APIResponse: Weather forecast data
        """
        params = self._add_api_key_to_params({
            "lat": lat,
            "lon": lon,
            "units": units,
            "cnt": min(cnt, 40)  # API limit
        })
        
        return await self.request("GET", "/forecast", params=params)
    
    async def get_historical_weather(
        self,
        lat: float,
        lon: float,
        dt: int,
        units: str = "metric"
    ) -> APIResponse:
        """
        Get historical weather data for a specific timestamp
        Note: Requires subscription for historical data
        
        Args:
            lat: Latitude
            lon: Longitude
            dt: Unix timestamp for the date
            units: Units (metric, imperial, kelvin)
            
        Returns:
            APIResponse: Historical weather data
        """
        params = self._add_api_key_to_params({
            "lat": lat,
            "lon": lon,
            "dt": dt,
            "units": units
        })
        
        # Use timemachine endpoint for historical data
        endpoint = f"{self.onecall_base_url}/onecall/timemachine"
        
        return await self.request("GET", endpoint, params=params)
    
    async def get_air_quality(
        self,
        lat: float,
        lon: float
    ) -> APIResponse:
        """
        Get current air quality data
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            APIResponse: Air quality data
        """
        params = self._add_api_key_to_params({
            "lat": lat,
            "lon": lon
        })
        
        return await self.request("GET", "/air_pollution", params=params)
    
    async def get_air_quality_forecast(
        self,
        lat: float,
        lon: float
    ) -> APIResponse:
        """
        Get air quality forecast
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            APIResponse: Air quality forecast data
        """
        params = self._add_api_key_to_params({
            "lat": lat,
            "lon": lon
        })
        
        return await self.request("GET", "/air_pollution/forecast", params=params)
    
    async def get_air_quality_history(
        self,
        lat: float,
        lon: float,
        start: int,
        end: int
    ) -> APIResponse:
        """
        Get historical air quality data
        
        Args:
            lat: Latitude
            lon: Longitude
            start: Start timestamp (Unix)
            end: End timestamp (Unix)
            
        Returns:
            APIResponse: Historical air quality data
        """
        params = self._add_api_key_to_params({
            "lat": lat,
            "lon": lon,
            "start": start,
            "end": end
        })
        
        return await self.request("GET", "/air_pollution/history", params=params)
    
    async def geocode_city(
        self,
        city_name: str,
        country_code: Optional[str] = None,
        limit: int = 5
    ) -> APIResponse:
        """
        Get coordinates for a city name
        
        Args:
            city_name: City name
            country_code: ISO 3166 country code (optional)
            limit: Number of results to return
            
        Returns:
            APIResponse: Geocoding results
        """
        query = city_name
        if country_code:
            query = f"{city_name},{country_code}"
        
        params = self._add_api_key_to_params({
            "q": query,
            "limit": limit
        })
        
        endpoint = f"{self.geo_base_url}/direct"
        return await self.request("GET", endpoint, params=params)
    
    async def reverse_geocode(
        self,
        lat: float,
        lon: float,
        limit: int = 5
    ) -> APIResponse:
        """
        Get location names for coordinates
        
        Args:
            lat: Latitude
            lon: Longitude
            limit: Number of results to return
            
        Returns:
            APIResponse: Reverse geocoding results
        """
        params = self._add_api_key_to_params({
            "lat": lat,
            "lon": lon,
            "limit": limit
        })
        
        endpoint = f"{self.geo_base_url}/reverse"
        return await self.request("GET", endpoint, params=params)
    
    async def get_weather_for_multiple_cities(
        self,
        city_coords: List[Tuple[float, float]],
        units: str = "metric"
    ) -> List[APIResponse]:
        """
        Get current weather for multiple cities
        
        Args:
            city_coords: List of (lat, lon) tuples
            units: Units (metric, imperial, kelvin)
            
        Returns:
            List[APIResponse]: Weather data for each city
        """
        weather_data = []
        
        for lat, lon in city_coords:
            try:
                response = await self.get_current_weather(lat, lon, units)
                weather_data.append(response)
                
                # Rate limiting courtesy
                await self._rate_limit_delay()
                
            except Exception as e:
                self.logger.error(f"❌ Error getting weather for {lat}, {lon}: {e}")
                # Create error response
                error_response = APIResponse(
                    success=False,
                    status_code=500,
                    response_time_ms=0,
                    errors=[str(e)],
                    metadata={"lat": lat, "lon": lon}
                )
                weather_data.append(error_response)
        
        return weather_data
    
    async def _rate_limit_delay(self):
        """Add delay between requests to respect rate limits"""
        await self.client.aclose()
        time.sleep(1.1)  # Slightly over 1 second to ensure we stay under 60/minute
    
    def extract_correlation_features(self, weather_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Extract key weather features for correlation analysis
        
        Args:
            weather_data: Weather data from OpenWeatherMap API
            
        Returns:
            Dict[str, float]: Key features for correlation analysis
        """
        main = weather_data.get("main", {})
        wind = weather_data.get("wind", {})
        clouds = weather_data.get("clouds", {})
        
        correlation_features = {
            "temperature": main.get("temp"),           # Temperature in chosen units
            "feels_like": main.get("feels_like"),     # Feels like temperature
            "humidity": main.get("humidity"),         # Humidity percentage
            "pressure": main.get("pressure"),         # Atmospheric pressure
            "wind_speed": wind.get("speed"),          # Wind speed
            "wind_deg": wind.get("deg"),              # Wind direction
            "cloudiness": clouds.get("all"),          # Cloudiness percentage
            "visibility": weather_data.get("visibility", 10000) / 1000,  # Visibility in km
        }
        
        # Add weather condition codes
        if "weather" in weather_data and weather_data["weather"]:
            weather_condition = weather_data["weather"][0]
            correlation_features.update({
                "weather_id": weather_condition.get("id"),        # Weather condition ID
                "weather_main": weather_condition.get("main"),    # Main weather group
            })
        
        # Filter out None values
        correlation_features = {k: v for k, v in correlation_features.items() if v is not None}
        
        if self.debug_mode:
            self.logger.debug(f"🌡️ Extracted weather features: {list(correlation_features.keys())}")
        
        return correlation_features
    
    def extract_temporal_context(self, weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract temporal context for time-based correlation
        
        Args:
            weather_data: Weather data from OpenWeatherMap API
            
        Returns:
            Dict[str, Any]: Temporal context information
        """
        dt = weather_data.get("dt")
        sys_data = weather_data.get("sys", {})
        
        temporal_context = {
            "observation_time": dt,
            "observation_datetime": datetime.fromtimestamp(dt).isoformat() if dt else None,
            "sunrise": sys_data.get("sunrise"),
            "sunset": sys_data.get("sunset"),
            "timezone": weather_data.get("timezone"),
            "collection_timestamp": datetime.now().isoformat()
        }
        
        # Add sunrise/sunset times in ISO format
        if sys_data.get("sunrise"):
            temporal_context["sunrise_datetime"] = datetime.fromtimestamp(sys_data["sunrise"]).isoformat()
        if sys_data.get("sunset"):
            temporal_context["sunset_datetime"] = datetime.fromtimestamp(sys_data["sunset"]).isoformat()
        
        return temporal_context
    
    def extract_geographic_context(self, weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract geographic context for location-based correlation
        
        Args:
            weather_data: Weather data from OpenWeatherMap API
            
        Returns:
            Dict[str, Any]: Geographic context information
        """
        coord = weather_data.get("coord", {})
        sys_data = weather_data.get("sys", {})
        
        geographic_context = {
            "latitude": coord.get("lat"),
            "longitude": coord.get("lon"),
            "country": sys_data.get("country"),
            "city_name": weather_data.get("name"),
            "city_id": weather_data.get("id"),
        }
        
        if self.debug_mode:
            city_name = geographic_context.get("city_name", "Unknown")
            country = geographic_context.get("country", "Unknown")
            self.logger.debug(f"🌍 Geographic context: {city_name}, {country}")
        
        return geographic_context
    
    def categorize_weather_conditions(self, weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Categorize weather conditions for correlation analysis
        
        Args:
            weather_data: Weather data from OpenWeatherMap API
            
        Returns:
            Dict[str, Any]: Categorized weather conditions
        """
        if not weather_data.get("weather"):
            return {}
        
        weather_condition = weather_data["weather"][0]
        weather_id = weather_condition.get("id", 0)
        main_condition = weather_condition.get("main", "").lower()
        
        # Categorize based on OpenWeatherMap condition codes
        categories = {
            "is_clear": main_condition == "clear",
            "is_cloudy": main_condition == "clouds",
            "is_rainy": main_condition in ["rain", "drizzle"],
            "is_snowy": main_condition == "snow",
            "is_stormy": main_condition == "thunderstorm",
            "is_foggy": main_condition in ["mist", "fog", "haze"],
            "is_extreme": weather_id >= 900,  # Extreme conditions
            "precipitation_type": self._get_precipitation_type(weather_id),
            "intensity_level": self._get_intensity_level(weather_id),
        }
        
        return categories
    
    def _get_precipitation_type(self, weather_id: int) -> str:
        """Get precipitation type from weather ID"""
        if 200 <= weather_id < 300:
            return "thunderstorm"
        elif 300 <= weather_id < 400:
            return "drizzle"
        elif 500 <= weather_id < 600:
            return "rain"
        elif 600 <= weather_id < 700:
            return "snow"
        elif 700 <= weather_id < 800:
            return "atmosphere"  # Fog, haze, etc.
        else:
            return "none"
    
    def _get_intensity_level(self, weather_id: int) -> str:
        """Get weather intensity level from weather ID"""
        # Light conditions
        if weather_id in [500, 300, 600, 701]:
            return "light"
        # Heavy conditions
        elif weather_id in [502, 503, 504, 522, 531, 602, 622]:
            return "heavy"
        # Extreme conditions
        elif weather_id >= 900:
            return "extreme"
        else:
            return "moderate"
    
    def prepare_correlation_data(self, weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare complete weather data for correlation analysis
        
        Args:
            weather_data: Raw weather data from API
            
        Returns:
            Dict[str, Any]: Correlation-ready weather data
        """
        correlation_data = {
            "raw_data": weather_data,
            "correlation_features": self.extract_correlation_features(weather_data),
            "temporal_context": self.extract_temporal_context(weather_data),
            "geographic_context": self.extract_geographic_context(weather_data),
            "weather_categories": self.categorize_weather_conditions(weather_data),
            "data_source": "openweathermap",
            "api_version": "2.5",
            "collection_timestamp": datetime.now().isoformat()
        }
        
        if self.debug_mode:
            features_count = len(correlation_data["correlation_features"])
            self.logger.debug(f"📊 Prepared correlation data with {features_count} features")
        
        return correlation_data
