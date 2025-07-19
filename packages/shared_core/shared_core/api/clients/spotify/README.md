# Spotify API Client

This package contains a client for interacting with the [Spotify Web API](https://developer.spotify.com/documentation/web-api/). It provides asynchronous HTTP methods to access user data, playlists, tracks, and audio features with comprehensive error handling and logging.

## Features

- Asynchronous support using `asyncio`
- OAuth 2.0 authentication flow
- Rate limiting compliance with Spotify API guidelines
- Comprehensive user data, playlist, track, and audio feature methods
- Error handling and retry logic
- Token refresh handling
- Correlation-ready data extraction for cross-domain analysis

## Requirements

- Python 3.7+
- `httpx`, `asyncio-throttle`, `tenacity`, `pydantic`
- Valid Spotify application credentials (free registration required)

## Installation

Include the `shared_core` package in your Python path and install dependencies:

```bash
pip install -e /path/to/shared_core
pip install -r /path/to/services/data_collection/spotify_collector/requirements.txt
```

## Configuration

### Environment Variables

Make sure to set the following environment variables:

- `SPOTIFY_CLIENT_ID`: Required. Your Spotify app's client ID from [developer.spotify.com](https://developer.spotify.com/dashboard)
- `SPOTIFY_CLIENT_SECRET`: Required. Your Spotify app's client secret
- `SPOTIFY_REDIRECT_URI`: Required. Your app's redirect URI (must match what's configured in your Spotify app)
- `SPOTIFY_SCOPES`: Optional. Space-separated list of scopes (default: `user-read-private user-read-email`)

### Example Usage

```python
import asyncio
from shared_core.config.spotify_config import SpotifyConfig
from shared_core.api.clients.spotify import SpotifyClient

async def run():
    # Initialize client
    config = SpotifyConfig.get_client_config()
    client = SpotifyClient(**config)
    
    # Authenticate (this will open a browser for authorization)
    await client.authenticate()
    
    # Example: Get current user's profile
    response = await client.get_current_user()
    if response.success:
        user = response.data
        print(f"User: {user['display_name']}")
    
    # Example: Get user's top tracks
    top_tracks = await client.get_user_top_tracks(limit=10)
    if top_tracks.success:
        tracks = top_tracks.data['items']
        for track in tracks:
            print(f"Track: {track['name']} by {track['artists'][0]['name']}")

asyncio.run(run())
```

## API Methods

### User Methods

#### `get_current_user`
Get the current user's profile information.

```python
await client.get_current_user()
```

#### `get_user_top_tracks`
Get the current user's top tracks.

```python
await client.get_user_top_tracks(limit=20, time_range="medium_term")
```

#### `get_user_top_artists`
Get the current user's top artists.

```python
await client.get_user_top_artists(limit=20, time_range="medium_term")
```

#### `get_user_recently_played`
Get the current user's recently played tracks.

```python
await client.get_user_recently_played(limit=50)
```

### Playlist Methods

#### `get_user_playlists`
Get the current user's playlists.

```python
await client.get_user_playlists(limit=20)
```

#### `get_playlist`
Get a specific playlist by its ID.

```python
await client.get_playlist(playlist_id="37i9dQZF1DXcBWIGoYBM5M")
```

#### `get_playlist_tracks`
Get tracks from a specific playlist.

```python
await client.get_playlist_tracks(playlist_id="37i9dQZF1DXcBWIGoYBM5M", limit=100)
```

### Track Methods

#### `get_track`
Get information about a specific track.

```python
await client.get_track(track_id="4iV5W9uYEdYUVa79Axb7Rh")
```

#### `get_tracks`
Get information about multiple tracks.

```python
await client.get_tracks(track_ids=["4iV5W9uYEdYUVa79Axb7Rh", "1301WleyT98MSxVHPZCA6M"])
```

#### `get_track_audio_features`
Get audio features for a specific track.

```python
await client.get_track_audio_features(track_id="4iV5W9uYEdYUVa79Axb7Rh")
```

#### `get_tracks_audio_features`
Get audio features for multiple tracks.

```python
await client.get_tracks_audio_features(track_ids=["4iV5W9uYEdYUVa79Axb7Rh", "1301WleyT98MSxVHPZCA6M"])
```

### Artist Methods

#### `get_artist`
Get information about a specific artist.

```python
await client.get_artist(artist_id="4Z8W4fKeB5YxbusRsdQVPb")
```

#### `get_artists`
Get information about multiple artists.

```python
await client.get_artists(artist_ids=["4Z8W4fKeB5YxbusRsdQVPb", "1dfeR4HaWDbWqFHLkxsg1d"])
```

#### `get_artist_albums`
Get albums by a specific artist.

```python
await client.get_artist_albums(artist_id="4Z8W4fKeB5YxbusRsdQVPb", limit=20)
```

#### `get_artist_top_tracks`
Get the top tracks by a specific artist.

```python
await client.get_artist_top_tracks(artist_id="4Z8W4fKeB5YxbusRsdQVPb", market="US")
```

### Album Methods

#### `get_album`
Get information about a specific album.

```python
await client.get_album(album_id="4aawyAB9vmqN3uQ7FjRGTy")
```

#### `get_albums`
Get information about multiple albums.

```python
await client.get_albums(album_ids=["4aawyAB9vmqN3uQ7FjRGTy", "1A2GTWGtFfWp7KSQTwWOyo"])
```

#### `get_album_tracks`
Get tracks from a specific album.

```python
await client.get_album_tracks(album_id="4aawyAB9vmqN3uQ7FjRGTy", limit=50)
```

### Search Methods

#### `search`
Search for tracks, artists, albums, or playlists.

```python
await client.search(query="Bohemian Rhapsody", search_type="track", limit=10)
```

### Audio Analysis Methods

#### `get_track_audio_analysis`
Get detailed audio analysis for a specific track.

```python
await client.get_track_audio_analysis(track_id="4iV5W9uYEdYUVa79Axb7Rh")
```

## Authentication

The Spotify client uses OAuth 2.0 authentication. The authentication flow involves:

1. **Authorization URL**: The client generates an authorization URL
2. **User Consent**: User visits the URL and grants permissions
3. **Authorization Code**: User is redirected with an authorization code
4. **Access Token**: Client exchanges the code for an access token
5. **Token Refresh**: Client automatically refreshes tokens when needed

### Authentication Flow

```python
# Initialize client
client = SpotifyClient(client_id="your_id", client_secret="your_secret", redirect_uri="your_uri")

# Get authorization URL
auth_url = client.get_authorization_url()
print(f"Visit this URL to authorize: {auth_url}")

# After user authorizes, you'll get a code
# Exchange the code for tokens
await client.get_access_token(authorization_code="received_code")

# Now you can make authenticated requests
user_profile = await client.get_current_user()
```

## Token Management

The client automatically handles token refresh when tokens expire. You can also manually refresh tokens:

```python
await client.refresh_access_token()
```

## Correlation Analysis Methods

The client provides methods to extract correlation-ready data:

```python
# Extract correlation features from track data
features = client.extract_correlation_features(track_data)

# Extract temporal context from recently played tracks
temporal_context = client.extract_temporal_context(recently_played_data)

# Get complete correlation-ready data
correlation_data = client.prepare_correlation_data(track_data)
```

## Error Handling

Errors are logged via the centralized logging system (`CentralizedLogger`). The client retries failed requests using exponential backoff, as configured.

Common errors include:
- `401 Unauthorized`: Invalid or expired access token
- `403 Forbidden`: Insufficient permissions (check scopes)
- `429 Too Many Requests`: Rate limit exceeded
- `404 Not Found`: Resource not found

## Rate Limiting

The client respects Spotify's rate limits, which vary by endpoint but are generally around 100 requests per minute. The client includes built-in rate limiting to prevent exceeding these limits.

## Debug Mode

Enable debug logging by setting `SPOTIFY_DEBUG_MODE=true`. This logs detailed information about all requests and responses.

## Scopes

Different API endpoints require different scopes. Common scopes include:

- `user-read-private`: Read user profile data
- `user-read-email`: Read user email
- `user-top-read`: Read user's top tracks and artists
- `user-read-recently-played`: Read recently played tracks
- `playlist-read-private`: Read private playlists
- `playlist-read-collaborative`: Read collaborative playlists

## Data Structure

All API responses are wrapped in `APIResponse` objects with the following structure:

```python
class APIResponse:
    success: bool
    data: Optional[Dict[str, Any]]
    error: Optional[str]
    status_code: Optional[int]
```

## Audio Features

Spotify provides rich audio features for tracks, including:

- **Acousticness**: Confidence measure of whether the track is acoustic
- **Danceability**: How suitable a track is for dancing
- **Energy**: Perceptual measure of intensity and power
- **Instrumentalness**: Predicts whether a track contains no vocals
- **Liveness**: Detects the presence of an audience in the recording
- **Loudness**: Overall loudness of a track in decibels (dB)
- **Speechiness**: Detects the presence of spoken words in a track
- **Tempo**: Overall estimated tempo of a track in beats per minute (BPM)
- **Valence**: Musical positiveness conveyed by a track

## Conclusion

This client provides a comprehensive way to interact with the Spotify Web API, allowing you to integrate rich music data and user listening patterns seamlessly into your applications. The correlation-ready data extraction methods make it perfect for music analysis and recommendation systems.
