# Spotify Data Collection Service - Proof of Concept

This service demonstrates the implementation and usage of the Spotify API client following the established patterns in the Data Centralization Platform codebase.

## Overview

The Spotify Data Collection Service showcases:

- **Environment-driven configuration** following project standards
- **OAuth 2.0 authentication flow** with proper token management
- **Rate-limited API calls** with retry logic and error handling
- **Audio features extraction** for correlation analysis
- **Cross-domain linking** via ISRC codes
- **Comprehensive logging** and debugging capabilities

## Features

### 🎵 Data Collection Capabilities
- **User Profile**: Authenticated user information
- **Top Tracks**: User's most played tracks with audio features
- **Recently Played**: Listening history with timestamps
- **Search & Analyze**: Search tracks and extract audio features
- **Audio Features**: Valence, energy, danceability, tempo, etc.

### 🔗 Correlation Analysis Ready
- **ISRC Extraction**: For cross-domain music linking
- **Audio Features**: Standardized features for correlation
- **Temporal Data**: Timestamps for time-based analysis
- **Metadata**: Artist, album, genre information

### 🛡️ Enterprise-Ready Features
- **OAuth 2.0 Flow**: Secure authentication
- **Rate Limiting**: Respects Spotify API limits
- **Error Handling**: Comprehensive error management
- **Logging**: Detailed debugging and monitoring
- **Configuration**: Environment-driven settings

## Configuration

### Required Environment Variables

```bash
# Spotify App Credentials (Required)
SPOTIFY_CLIENT_ID=your_spotify_client_id_here
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here

# OAuth Configuration (Optional)
SPOTIFY_REDIRECT_URI=http://localhost:8080/callback

# Authentication Tokens (Set after OAuth)
SPOTIFY_ACCESS_TOKEN=your_access_token_here
SPOTIFY_REFRESH_TOKEN=your_refresh_token_here
```

### Setting Up Spotify App

1. **Create a Spotify App**:
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Create a new app
   - Note the Client ID and Client Secret

2. **Configure Redirect URI**:
   - In your Spotify app settings, add redirect URI: `http://localhost:8080/callback`
   - Or use your custom URI and set `SPOTIFY_REDIRECT_URI`

3. **Set Environment Variables**:
   ```bash
   export SPOTIFY_CLIENT_ID="your_client_id"
   export SPOTIFY_CLIENT_SECRET="your_client_secret"
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
# Run the proof of concept
python main.py
```

### OAuth Authentication Flow

1. **First Run** (without tokens):
   ```bash
   python main.py
   ```
   - The service will display an authorization URL
   - Visit the URL and authorize the application
   - Copy the authorization code from the callback

2. **Exchange Code for Tokens**:
   ```python
   # In Python interactive session
   import asyncio
   from main import SpotifyCollectorService
   
   async def get_tokens():
       service = SpotifyCollectorService()
       await service.initialize_client()
       success = await service.exchange_code_for_tokens("YOUR_AUTH_CODE_HERE")
       if success:
           print(f"Access Token: {service.client.access_token}")
           print(f"Refresh Token: {service.client.refresh_token}")
   
   asyncio.run(get_tokens())
   ```

3. **Set Tokens in Environment**:
   ```bash
   export SPOTIFY_ACCESS_TOKEN="your_access_token"
   export SPOTIFY_REFRESH_TOKEN="your_refresh_token"
   ```

4. **Run Full Proof of Concept**:
   ```bash
   python main.py
   ```

## API Usage Examples

### Basic Client Usage

```python
import asyncio
from shared_core.config.spotify_config import SpotifyConfig
from shared_core.api.clients.spotify import SpotifyClient

async def example_usage():
    # Initialize client
    client = SpotifyClient(
        client_id=SpotifyConfig.client_id(),
        client_secret=SpotifyConfig.client_secret()
    )
    
    # Set access token (after OAuth)
    client.access_token = "your_access_token"
    
    # Search for tracks
    response = await client.search_tracks("electronic music", limit=10)
    if response.success:
        tracks = response.data['tracks']['items']
        print(f"Found {len(tracks)} tracks")
    
    # Get audio features
    track_ids = [track['id'] for track in tracks]
    features_response = await client.get_multiple_tracks_audio_features(track_ids)
    
    if features_response.success:
        features = features_response.data['audio_features']
        for feature in features:
            if feature:
                correlation_data = client.extract_audio_features_for_correlation(feature)
                print(f"Valence: {correlation_data.get('valence', 'N/A')}")
                print(f"Energy: {correlation_data.get('energy', 'N/A')}")

asyncio.run(example_usage())
```

### Advanced Configuration

```python
from shared_core.config.spotify_config import SpotifyConfig

# Get configuration summary
config_summary = SpotifyConfig.get_config_summary()
print(f"Configuration: {config_summary}")

# Get correlation-specific configuration
correlation_config = SpotifyConfig.get_correlation_config()
print(f"Audio features available: {correlation_config['audio_features']}")
```

## Output Data Structure

### Track Data with Audio Features

```json
{
  "id": "spotify_track_id",
  "name": "Track Name",
  "artists": [...],
  "album": {...},
  "external_ids": {
    "isrc": "ISRC_CODE_FOR_LINKING"
  },
  "audio_features": {
    "valence": 0.85,
    "energy": 0.92,
    "danceability": 0.78,
    "tempo": 128.0,
    "acousticness": 0.12,
    "instrumentalness": 0.05,
    "loudness": -5.2,
    "speechiness": 0.08
  },
  "correlation_features": {
    "valence": 0.85,
    "energy": 0.92,
    "danceability": 0.78,
    "tempo": 128.0
  },
  "isrc": "ISRC_CODE_FOR_LINKING",
  "collection_timestamp": "2025-01-18T03:00:00Z"
}
```

## File Structure

```
spotify_collector/
├── main.py                    # Main proof of concept service
├── requirements.txt           # Python dependencies
├── README.md                 # This documentation
└── output/                   # Generated data files
    ├── top_tracks.json       # User's top tracks
    ├── recent_tracks.json    # Recently played tracks
    ├── search_results.json   # Search results
    └── collection_stats.json # Collection statistics
```

## Integration Points

### Following Project Patterns

1. **Configuration Management**:
   - Uses `SpotifyConfig` following `DatabaseConfig` pattern
   - Environment-driven configuration
   - Singleton pattern for config instances

2. **API Client Architecture**:
   - Extends `BaseAPIClient` for consistency
   - Built-in rate limiting and retry logic
   - Comprehensive logging and debugging

3. **Service Architecture**:
   - Follows existing `pokemon_collector` patterns
   - Centralized logging via `CentralizedLogger`
   - Proper error handling and recovery

### Correlation Analysis Ready

The collected data is structured for correlation analysis:

- **Audio Features**: Normalized 0-1 values for statistical analysis
- **Temporal Data**: Timestamps for time-based correlations
- **Cross-Domain Links**: ISRC codes for music industry linking
- **Metadata**: Genre, artist, album information

## Best Practices Demonstrated

### 🔐 Security
- OAuth 2.0 implementation
- Token refresh handling
- Environment variable management
- No hardcoded credentials

### 📊 Data Quality
- Comprehensive error handling
- Data validation and sanitization
- Structured output format
- Collection statistics tracking

### 🚀 Performance
- Rate limiting compliance
- Batch processing for efficiency
- Async/await patterns
- Connection pooling

### 📝 Observability
- Detailed logging at all levels
- Performance metrics tracking
- Error reporting and debugging
- Collection statistics

## Troubleshooting

### Common Issues

1. **OAuth Flow Issues**:
   - Ensure redirect URI matches exactly
   - Check Spotify app settings
   - Verify client credentials

2. **API Rate Limits**:
   - Service includes built-in rate limiting
   - Monitor response headers
   - Implement backoff strategies

3. **Token Expiration**:
   - Use refresh tokens for long-running processes
   - Implement token refresh logic
   - Handle 401 responses gracefully

### Debug Mode

Enable debug logging for detailed information:

```python
client = SpotifyClient(
    client_id=config.client_id(),
    client_secret=config.client_secret(),
    debug_mode=True  # Enable detailed logging
)
```

## Integration with Correlation Analysis

This service provides data in the format expected by the correlation analysis system:

```python
# Example correlation analysis usage
correlation_features = client.extract_audio_features_for_correlation(audio_features)

# Features ready for statistical analysis:
# - valence: 0.0-1.0 (happiness/positivity)
# - energy: 0.0-1.0 (intensity/power)
# - danceability: 0.0-1.0 (rhythm/beat)
# - tempo: BPM (beats per minute)
# - acousticness: 0.0-1.0 (acoustic vs electronic)
# - instrumentalness: 0.0-1.0 (vocal vs instrumental)
# - loudness: dB (decibels)
# - speechiness: 0.0-1.0 (spoken word content)
```

## Next Steps

1. **Database Integration**: Store collected data in PostgreSQL
2. **Correlation Engine**: Link with weather/entertainment data
3. **Visualization**: Create charts and insights
4. **Automation**: Schedule regular data collection
5. **Web Interface**: Build dashboard for results

## Related Documentation

- [LLM Technical Development Guide](../../../resources/docs/ai/llm-technical-development-guide.md)
- [LLM Coding Practices Guide](../../../resources/docs/ai/llm-coding-practices-guide.md)
- [Database Configuration](../../../packages/shared_core/shared_core/config/database_config.py)
- [Base API Client](../../../packages/shared_core/shared_core/config/base_client.py)

---

*This proof of concept demonstrates the implementation of enterprise-grade API clients following established patterns in the Data Centralization Platform codebase.*
