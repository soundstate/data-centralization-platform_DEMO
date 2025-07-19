# OpenWeatherMap Data Collection Service - Proof of Concept

This service demonstrates the implementation and usage of the OpenWeatherMap API client following the established patterns in the Data Centralization Platform codebase.

## Overview

The OpenWeatherMap Data Collection Service showcases:

- **Environment-driven configuration** following project standards
- **Comprehensive weather data collection** with current conditions, forecasts, and air quality
- **Correlation-ready data extraction** for cross-domain analysis
- **Geographic and temporal context** for location-based correlations
- **Comprehensive logging** and debugging capabilities

## Features

### 🌤️ Data Collection Capabilities
- **Current Weather**: Temperature, humidity, pressure, wind conditions
- **Air Quality**: Pollution levels and air quality index
- **Weather Forecasts**: 5-day forecast with 3-hour intervals
- **Geographic Data**: Coordinates, city names, country codes
- **Temporal Context**: Timestamps, sunrise/sunset times

### 🔗 Correlation Analysis Ready
- **Weather Features**: Temperature, humidity, pressure, wind speed
- **Categorical Data**: Weather conditions (clear, cloudy, rainy, etc.)
- **Temporal Data**: Timestamps for time-based correlations
- **Geographic Context**: Coordinates for location-based analysis

### 🛡️ Enterprise-Ready Features
- **Rate Limiting**: Respects OpenWeatherMap API limits (60 calls/minute)
- **Error Handling**: Comprehensive error management and retry logic
- **Logging**: Detailed debugging and monitoring
- **Configuration**: Environment-driven settings

## Configuration

### Required Environment Variables

```bash
# OpenWeatherMap API Key (Required)
OPENWEATHER_API_KEY=your_api_key_here

# Units Configuration (Optional)
OPENWEATHER_UNITS=metric  # Options: metric, imperial, kelvin (default: metric)
```

### Setting Up OpenWeatherMap API

1. **Create an OpenWeatherMap Account**:
   - Go to [OpenWeatherMap](https://openweathermap.org/api)
   - Sign up for a free account
   - Subscribe to the Current Weather Data API (free tier available)

2. **Get Your API Key**:
   - Go to your API keys section
   - Copy your API key

3. **Set Environment Variables**:
   ```bash
   export OPENWEATHER_API_KEY="your_api_key_here"
   export OPENWEATHER_UNITS="metric"
   ```

## Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Shared Core Package**:
   ```bash
   pip install -e ../../../packages/shared_core
   ```

## Usage

### Quick Start

```bash
# Set your API key
export OPENWEATHER_API_KEY="your_api_key_here"

# Run the proof of concept
python main.py
```

### API Usage Examples

#### Basic Client Usage

```python
import asyncio
from shared_core.config.openweathermap_config import OpenWeatherMapConfig
from shared_core.api.clients.openweathermap import OpenWeatherMapClient

async def example_usage():
    # Initialize client
    client = OpenWeatherMapClient(
        api_key=OpenWeatherMapConfig.api_key(),
        debug_mode=True
    )
    
    # Get current weather
    response = await client.get_current_weather(lat=51.5074, lon=-0.1278)
    if response.success:
        weather_data = response.data
        print(f"Temperature: {weather_data['main']['temp']}°C")
        print(f"Humidity: {weather_data['main']['humidity']}%")
    
    # Get air quality
    air_response = await client.get_air_quality(lat=51.5074, lon=-0.1278)
    if air_response.success:
        air_data = air_response.data
        print(f"Air Quality Index: {air_data['list'][0]['main']['aqi']}")
    
    # Extract correlation features
    correlation_features = client.extract_correlation_features(weather_data)
    print(f"Correlation features: {correlation_features}")

asyncio.run(example_usage())
```

#### Advanced Configuration

```python
from shared_core.config.openweathermap_config import OpenWeatherMapConfig

# Get configuration summary
config_summary = OpenWeatherMapConfig.get_config_summary()
print(f"Configuration: {config_summary}")

# Validate configuration
is_valid = OpenWeatherMapConfig.validate_credentials()
print(f"Configuration valid: {is_valid}")
```

## Output Data Structure

### Weather Data with Correlation Features

```json
{
  "raw_data": {
    "coord": {"lon": -0.1278, "lat": 51.5074},
    "weather": [{"id": 800, "main": "Clear", "description": "clear sky"}],
    "main": {
      "temp": 15.2,
      "feels_like": 14.8,
      "temp_min": 13.1,
      "temp_max": 17.3,
      "pressure": 1013,
      "humidity": 72
    },
    "wind": {"speed": 3.6, "deg": 230},
    "clouds": {"all": 0},
    "visibility": 10000,
    "dt": 1642521600,
    "sys": {"sunrise": 1642497600, "sunset": 1642531200},
    "name": "London",
    "cod": 200
  },
  "correlation_features": {
    "temperature": 15.2,
    "feels_like": 14.8,
    "humidity": 72,
    "pressure": 1013,
    "wind_speed": 3.6,
    "wind_deg": 230,
    "cloudiness": 0,
    "visibility": 10.0,
    "weather_id": 800,
    "weather_main": "Clear"
  },
  "temporal_context": {
    "observation_time": 1642521600,
    "observation_datetime": "2022-01-18T12:00:00",
    "sunrise": 1642497600,
    "sunset": 1642531200,
    "sunrise_datetime": "2022-01-18T05:20:00",
    "sunset_datetime": "2022-01-18T15:20:00",
    "collection_timestamp": "2025-01-18T03:00:00Z"
  },
  "geographic_context": {
    "latitude": 51.5074,
    "longitude": -0.1278,
    "country": "GB",
    "city_name": "London",
    "city_id": 2643743
  },
  "weather_categories": {
    "is_clear": true,
    "is_cloudy": false,
    "is_rainy": false,
    "is_snowy": false,
    "is_stormy": false,
    "is_foggy": false,
    "is_extreme": false,
    "precipitation_type": "none",
    "intensity_level": "moderate"
  },
  "data_source": "openweathermap",
  "api_version": "2.5",
  "collection_timestamp": "2025-01-18T03:00:00Z"
}
```

## File Structure

```
openweathermap_collector/
├── main.py                    # Main proof of concept service
├── requirements.txt           # Python dependencies
├── README.md                 # This documentation
├── .env.example              # Environment variables example
└── output/                   # Generated data files
    ├── current_weather.json  # Current weather data
    ├── air_quality.json      # Air quality data
    └── collection_stats.json # Collection statistics
```

## API Methods Available

### Weather Data
- `get_current_weather(lat, lon)` - Current weather conditions
- `get_current_weather_by_city(city_name)` - Weather by city name
- `get_forecast(lat, lon)` - 5-day forecast with 3-hour intervals
- `get_historical_weather(lat, lon, dt)` - Historical weather data (subscription required)

### Air Quality
- `get_air_quality(lat, lon)` - Current air quality
- `get_air_quality_forecast(lat, lon)` - Air quality forecast
- `get_air_quality_history(lat, lon, start, end)` - Historical air quality

### Geocoding
- `geocode_city(city_name)` - Get coordinates for city name
- `reverse_geocode(lat, lon)` - Get location names for coordinates

### Utility Methods
- `extract_correlation_features(weather_data)` - Extract features for correlation analysis
- `extract_temporal_context(weather_data)` - Extract temporal information
- `extract_geographic_context(weather_data)` - Extract geographic information
- `categorize_weather_conditions(weather_data)` - Categorize weather conditions
- `prepare_correlation_data(weather_data)` - Prepare complete correlation-ready data

## Integration Points

### Following Project Patterns

1. **Configuration Management**:
   - Uses `OpenWeatherMapConfig` following `DatabaseConfig` pattern
   - Environment-driven configuration
   - Singleton pattern for config instances

2. **API Client Architecture**:
   - Extends `BaseAPIClient` for consistency
   - Built-in rate limiting and retry logic
   - Comprehensive logging and debugging

3. **Service Architecture**:
   - Follows existing collector patterns
   - Centralized logging via `CentralizedLogger`
   - Proper error handling and recovery

### Correlation Analysis Ready

The collected data is structured for correlation analysis:

- **Weather Features**: Temperature, humidity, pressure, wind speed
- **Categorical Data**: Weather conditions (clear/cloudy/rainy/etc.)
- **Temporal Data**: Timestamps for time-based correlations
- **Geographic Context**: Coordinates for location-based analysis

## Best Practices Demonstrated

### 🔐 Security
- API key stored in environment variables
- No hardcoded credentials
- Secure configuration management

### 📊 Data Quality
- Comprehensive error handling
- Data validation and sanitization
- Structured output format
- Collection statistics tracking

### 🚀 Performance
- Rate limiting compliance (60 calls/minute)
- Efficient data collection
- Async/await patterns
- Connection pooling

### 📝 Observability
- Detailed logging at all levels
- Performance metrics tracking
- Error reporting and debugging
- Collection statistics

## Troubleshooting

### Common Issues

1. **API Key Issues**:
   - Ensure API key is valid and active
   - Check if you've exceeded the free tier limits
   - Verify the API key is set in environment variables

2. **Rate Limiting**:
   - Free tier allows 60 calls/minute
   - Service includes built-in rate limiting
   - Monitor API usage in your OpenWeatherMap dashboard

3. **Geographic Issues**:
   - Ensure coordinates are valid (-90 to 90 for latitude, -180 to 180 for longitude)
   - City names should be in English or local language
   - Use ISO 3166 country codes for better accuracy

### Debug Mode

Enable debug logging for detailed information:

```python
client = OpenWeatherMapClient(
    api_key=config.api_key(),
    debug_mode=True  # Enable detailed logging
)
```

## Integration with Correlation Analysis

This service provides data in the format expected by the correlation analysis system:

```python
# Example correlation analysis usage
correlation_features = client.extract_correlation_features(weather_data)

# Features ready for statistical analysis:
# - temperature: Celsius/Fahrenheit/Kelvin
# - humidity: 0-100 percentage
# - pressure: hPa (hectopascals)
# - wind_speed: m/s or mph
# - cloudiness: 0-100 percentage
# - visibility: kilometers
# - weather_id: OpenWeatherMap condition code
```

## Weather-Music Correlation Examples

The collected weather data is perfect for correlating with music data:

```python
# Example correlation scenarios:
# 1. Rainy weather → More melancholic music (low valence)
# 2. Sunny weather → More energetic music (high energy)
# 3. Cold weather → More acoustic music (high acousticness)
# 4. High humidity → Different tempo preferences
# 5. Wind conditions → Correlation with danceability
```

## Next Steps

1. **Database Integration**: Store collected data in PostgreSQL
2. **Correlation Engine**: Link with music/entertainment data
3. **Visualization**: Create weather-music correlation charts
4. **Automation**: Schedule regular data collection
5. **Geographic Analysis**: Analyze weather patterns by location

## Related Documentation

- [LLM Technical Development Guide](../../../resources/docs/ai/llm-technical-development-guide.md)
- [LLM Coding Practices Guide](../../../resources/docs/ai/llm-coding-practices-guide.md)
- [Database Configuration](../../../packages/shared_core/shared_core/config/database_config.py)
- [Base API Client](../../../packages/shared_core/shared_core/config/base_client.py)

---

*This proof of concept demonstrates the implementation of enterprise-grade weather data collection following established patterns in the Data Centralization Platform codebase.*
