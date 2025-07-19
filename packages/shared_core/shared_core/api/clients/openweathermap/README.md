# OpenWeatherMap API Client

This package contains a client for interacting with the [OpenWeatherMap](https://openweathermap.org/) API. It provides asynchronous HTTP methods to access current weather, forecasts, and air quality data with comprehensive error handling and logging.

## Features

- Asynchronous support using `asyncio`
- Rate limiting compliance with OpenWeatherMap guidelines (60 calls per minute)
- Comprehensive current weather, forecast, and air quality methods
- Error handling and retry logic
- API key authentication
- Correlation-ready data extraction for cross-domain analysis

## Requirements

- Python 3.7+
- `httpx`, `asyncio-throttle`, `tenacity`, `pydantic`
- Valid OpenWeatherMap API key (free registration required)

## Installation

Include the `shared_core` package in your Python path and install dependencies:

```bash
pip install -e /path/to/shared_core
pip install -r /path/to/services/data_collection/openweathermap_collector/requirements.txt
```

## Configuration

### Environment Variables

Make sure to set the following environment variables:

- `OPENWEATHER_API_KEY`: Required. Your OpenWeatherMap API key from [openweathermap.org](https://openweathermap.org/appid)
- `OPENWEATHER_UNITS`: Optional. Unit for temperature (`metric`, `imperial`, `kelvin`), default is `metric`

### Example Usage

```python
import asyncio
from shared_core.config.openweathermap_config import OpenWeatherMapConfig
from shared_core.api.clients.openweathermap import OpenWeatherMapClient

async def run():
    # Initialize client
    config = OpenWeatherMapConfig.get_client_config()
    client = OpenWeatherMapClient(**config)
    
    # Example: Get current weather
    response = await client.get_current_weather(lat=40.7128, lon=-74.0060)
    if response.success:
        weather = response.data
        print(f"Temperature: {weather['main']['temp']}°C")

asyncio.run(run())
```

## API Methods

### Weather Methods

#### `get_current_weather`
Get current weather conditions for a specified location.

```python
await client.get_current_weather(lat=40.7128, lon=-74.0060)
```

#### `get_forecast`
Get weather forecast for a specified location.

```python
await client.get_forecast(lat=40.7128, lon=-74.0060)
```

#### `get_historical_weather`
Get historical weather data for a specified location (requires subscription).

```python
await client.get_historical_weather(lat=40.7128, lon=-74.0060, dt=1618317040)
```

### Air Quality Methods

#### `get_air_quality`
Get current air quality data for a specified location.

```python
await client.get_air_quality(lat=40.7128, lon=-74.0060)
```

#### `get_air_quality_forecast`
Get air quality forecast for a specified location.

```python
await client.get_air_quality_forecast(lat=40.7128, lon=-74.0060)
```

#### `get_air_quality_history`
Get historical air quality data for a specified location (requires subscription).

```python
await client.get_air_quality_history(lat=40.7128, lon=-74.0060, start=1618317040, end=1618403440)
```

### Utility Methods

#### `extract_correlation_features`
Extract correlation-ready features from weather data.

```python
features = client.extract_correlation_features(weather_data)
```

#### `extract_temporal_context`
Extract temporal context from weather data.

```python
temporal_context = client.extract_temporal_context(weather_data)
```

#### `extract_geographic_context`
Extract geographic context from weather data.

```python
geographic_context = client.extract_geographic_context(weather_data)
```

## Error Handling

Errors are logged via the centralized logging system (`CentralizedLogger`). The client retries failed requests using exponential backoff, as configured.

## Rate Limiting

The client respects OpenWeatherMap's rate limits of 60 calls per minute. Exceeding this limit will result in API errors.

## Debug Mode

Enable debug logging by setting `OPENWEATHER_DEBUG_MODE=true`. This logs detailed information about all requests.

## Authentication

The client uses API key authentication by including your API key in the request headers.

## Data Structure

All API responses are wrapped in `APIResponse` objects with the following structure:

```python
class APIResponse:
    success: bool
    data: Optional[Dict[str, Any]]
    error: Optional[str]
    status_code: Optional[int]
```

## Conclusion

This client provides a comprehensive way to interact with the OpenWeatherMap API, allowing you to integrate rich weather and air quality data seamlessly into your applications.
