# Spotify API Client

This package contains a comprehensive client for interacting with the [Spotify Web API](https://developer.spotify.com/documentation/web-api/). It provides modern asynchronous OAuth 2.0 authentication, rich data extraction capabilities, and correlation-ready features for cross-domain music analysis.

## Features

- Modern async OAuth 2.0 authentication flow with automatic token management
- Comprehensive error handling and retry logic with exponential backoff
- Rate limiting compliance (100 requests/minute) with built-in throttling
- Rich audio features extraction for correlation analysis
- Cross-domain linking via ISRC codes
- Async context manager support for proper resource cleanup
- Debug logging with centralized logger integration
- Token validation and refresh automation
- Comprehensive scope management

## Requirements

- Python 3.9+
- Dependencies: `httpx`, `aiohttp`, `tenacity`, `pydantic`
- Valid Spotify application credentials (free registration required)
- Environment variables for configuration

## Quick Start Guide

### 1. Create Spotify App (First Time Setup)

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Click "Create an app"
3. Fill in app name and description
4. Note your **Client ID** and **Client Secret**
5. Add redirect URI: `http://localhost:8080/callback`

### 2. Environment Setup

Create a `.env` file or set environment variables:

```bash
# Required Spotify OAuth credentials
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REDIRECT_URI=http://localhost:8080/callback

# Optional: Enable debug logging
LOG_LEVEL=DEBUG
```

### 3. Installation

```bash
# Install the shared_core package
cd /path/to/shared_core
pip install -e .

# Install additional dependencies if needed
pip install aiohttp httpx tenacity
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

---

# 🧪 Testing and Authentication Guide

This section provides step-by-step instructions for testing the Spotify API client and completing OAuth authentication.

## Prerequisites Checklist

- [ ] Spotify Developer account created at [developer.spotify.com](https://developer.spotify.com/dashboard)
- [ ] Spotify app created with redirect URI: `http://localhost:8080/callback`
- [ ] Environment variables set: `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, `SPOTIFY_REDIRECT_URI`
- [ ] Python 3.9+ installed
- [ ] Required dependencies installed

## Testing Methods

### Method 1: Quick Configuration Test

First, verify your configuration is set up correctly:

```python
# File: test_spotify_config.py
import asyncio
from shared_core.config.spotify_config import SpotifyConfig
from shared_core.auth.spotify_oauth import SpotifyOAuth

def test_config():
    """Test Spotify configuration setup"""
    print("🎵 Testing Spotify Configuration...\n")
    
    # Test basic config
    config = SpotifyConfig()
    summary = config.get_config_summary()
    
    print("Configuration Summary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    # Test OAuth config
    oauth_config = config.get_oauth_config()
    print(f"\nOAuth Valid: {oauth_config.get('oauth_valid', False)}")
    
    if oauth_config.get('oauth_valid'):
        print("✅ Configuration looks good!")
    else:
        print("❌ Configuration issues detected")
        if 'error' in oauth_config:
            print(f"Error: {oauth_config['error']}")

if __name__ == "__main__":
    test_config()
```

### Method 2: OAuth Flow Test

Test the complete OAuth authentication flow:

```python
# File: test_spotify_oauth.py
import asyncio
from shared_core.auth.spotify_oauth import SpotifyOAuth
from shared_core.config.spotify_config import SpotifyConfig

async def test_oauth_flow():
    """Test OAuth authentication flow"""
    print("🔐 Testing Spotify OAuth Flow...\n")
    
    # Initialize OAuth client
    async with SpotifyOAuth() as oauth_client:
        try:
            # Generate authorization URL
            auth_url, state = oauth_client.get_authorization_url()
            
            print(f"🔗 Authorization URL Generated:")
            print(f"{auth_url}\n")
            print(f"🔑 State parameter: {state}\n")
            
            print("📋 Next Steps:")
            print("1. Copy the authorization URL above")
            print("2. Paste it in your browser")
            print("3. Log in to Spotify and authorize the app")
            print("4. Copy the 'code' parameter from the callback URL")
            print("5. Use the code in the next test\n")
            
        except Exception as e:
            print(f"❌ OAuth flow test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_oauth_flow())
```

### Method 3: Token Exchange Test

After getting the authorization code, test token exchange:

```python
# File: test_token_exchange.py
import asyncio
from shared_core.auth.spotify_oauth import SpotifyOAuth

async def test_token_exchange():
    """Test exchanging authorization code for tokens"""
    print("🎟️ Testing Token Exchange...\n")
    
    # Get authorization code from user
    auth_code = input("Enter the authorization code from callback URL: ").strip()
    state = input("Enter the state parameter (optional): ").strip() or None
    
    if not auth_code:
        print("❌ Authorization code is required")
        return
    
    async with SpotifyOAuth() as oauth_client:
        try:
            # Exchange code for tokens
            token_info = await oauth_client.exchange_code_for_token(
                authorization_code=auth_code,
                state=state
            )
            
            print("✅ Token exchange successful!")
            print(f"Access token: {token_info['access_token'][:20]}...")
            print(f"Refresh token: {token_info.get('refresh_token', 'N/A')[:20]}..." if token_info.get('refresh_token') else "Refresh token: N/A")
            print(f"Expires at: {token_info['expires_at']}")
            print(f"Scopes: {token_info['scope']}")
            
            # Test token validation
            is_valid = await oauth_client.validate_token(token_info['access_token'])
            print(f"Token valid: {is_valid}")
            
            return token_info
            
        except Exception as e:
            print(f"❌ Token exchange failed: {e}")
            return None

if __name__ == "__main__":
    asyncio.run(test_token_exchange())
```

### Method 4: Complete Client Test

Test the full Spotify client with authentication:

```python
# File: test_spotify_client.py
import asyncio
from shared_core.api.clients.spotify.spotify_client import SpotifyClient
from shared_core.config.spotify_config import SpotifyConfig

async def test_spotify_client():
    """Test complete Spotify client functionality"""
    print("🎵 Testing Spotify Client...\n")
    
    try:
        # Initialize client using config
        client_id = SpotifyConfig.client_id()
        client_secret = SpotifyConfig.client_secret()
        redirect_uri = SpotifyConfig.redirect_uri()
        
        async with SpotifyClient(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            debug_mode=True
        ) as client:
            
            # Step 1: Get OAuth URL
            auth_url, state = await client.get_oauth_authorization_url()
            print(f"🔗 Visit this URL to authorize: {auth_url}\n")
            
            # Step 2: Get authorization code from user
            auth_code = input("Enter authorization code from callback: ").strip()
            if not auth_code:
                print("❌ Authorization code required")
                return
            
            # Step 3: Exchange for tokens
            success = await client.oauth_exchange_code_for_tokens(
                authorization_code=auth_code,
                state=state,
                expected_state=state
            )
            
            if not success:
                print("❌ Failed to exchange code for tokens")
                return
            
            print("✅ Authentication successful!\n")
            
            # Step 4: Test API endpoints
            print("🧪 Testing API endpoints...")
            
            # Test user profile
            profile_response = await client.get_user_profile()
            if profile_response.success:
                user = profile_response.data
                print(f"👤 User: {user.get('display_name', 'N/A')} ({user.get('id')})")
                print(f"📧 Email: {user.get('email', 'N/A')}")
                print(f"🎵 Followers: {user.get('followers', {}).get('total', 0)}")
            else:
                print(f"❌ Failed to get user profile: {profile_response.errors}")
            
            # Test top tracks
            top_tracks_response = await client.get_user_top_tracks(limit=5)
            if top_tracks_response.success:
                tracks = top_tracks_response.data.get('items', [])
                print(f"\n🔥 Your Top {len(tracks)} Tracks:")
                for i, track in enumerate(tracks, 1):
                    artists = ', '.join([a['name'] for a in track.get('artists', [])])
                    print(f"  {i}. {track.get('name')} - {artists}")
                    
                    # Test audio features for first track
                    if i == 1:
                        track_id = track['id']
                        features_response = await client.get_track_audio_features(track_id)
                        if features_response.success:
                            features = features_response.data
                            correlation_features = client.extract_audio_features_for_correlation(features)
                            print(f"    🎶 Audio Features: {correlation_features}")
            else:
                print(f"❌ Failed to get top tracks: {top_tracks_response.errors}")
            
            # Test recently played
            recent_response = await client.get_user_recently_played(limit=3)
            if recent_response.success:
                recent_tracks = recent_response.data.get('items', [])
                print(f"\n🕐 Recently Played ({len(recent_tracks)} tracks):")
                for item in recent_tracks:
                    track = item.get('track', {})
                    played_at = item.get('played_at')
                    artists = ', '.join([a['name'] for a in track.get('artists', [])])
                    print(f"  • {track.get('name')} - {artists} (played: {played_at})")
            else:
                print(f"❌ Failed to get recently played: {recent_response.errors}")
            
            print("\n✅ All tests completed successfully!")
            
    except Exception as e:
        print(f"❌ Client test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_spotify_client())
```

## Step-by-Step Authentication Guide

### Step 1: Environment Setup

1. **Create `.env` file** in your project root:
```bash
# Spotify OAuth Configuration
SPOTIFY_CLIENT_ID=your_actual_client_id_here
SPOTIFY_CLIENT_SECRET=your_actual_client_secret_here
SPOTIFY_REDIRECT_URI=http://localhost:8080/callback

# Debug settings
LOG_LEVEL=DEBUG
CENTRALIZED_LOGGING=true
```

2. **Load environment** in your scripts:
```python
from dotenv import load_dotenv
load_dotenv()  # Add this at the top of your test files
```

### Step 2: Run Configuration Test

```bash
cd /path/to/your/project
python test_spotify_config.py
```

Expected output:
```
🎵 Testing Spotify Configuration...

Configuration Summary:
  client_id: abcd...wxyz
  client_secret: ***MASKED***
  redirect_uri: http://localhost:8080/callback
  has_access_token: False
  has_refresh_token: False
  default_scopes: ['user-read-private', 'user-read-email', ...]

OAuth Valid: True
✅ Configuration looks good!
```

### Step 3: Run OAuth Flow Test

```bash
python test_spotify_oauth.py
```

This will output an authorization URL. **Copy it and paste in your browser.**

### Step 4: Authorize in Browser

1. **Paste the URL** in your browser
2. **Log in to Spotify** if not already logged in
3. **Click "Agree"** to authorize the app
4. **Copy the code** from the callback URL (e.g., `http://localhost:8080/callback?code=AQA...&state=...`)

### Step 5: Exchange Code for Tokens

```bash
python test_token_exchange.py
```

Paste the authorization code when prompted.

### Step 6: Run Full Client Test

```bash
python test_spotify_client.py
```

This will run through the complete authentication flow and test API endpoints.

## Troubleshooting Guide

### Common Issues

#### ❌ "SPOTIFY_CLIENT_ID environment variable is required"
**Solution:** Check your `.env` file and environment variable loading:
```python
import os
print("Environment variables:")
print(f"CLIENT_ID: {os.getenv('SPOTIFY_CLIENT_ID')[:10]}..." if os.getenv('SPOTIFY_CLIENT_ID') else "CLIENT_ID: NOT SET")
```

#### ❌ "Invalid redirect URI"
**Solution:** 
1. Go to your [Spotify App Dashboard](https://developer.spotify.com/dashboard)
2. Edit your app settings
3. Add redirect URI: `http://localhost:8080/callback`
4. Save changes

#### ❌ "Invalid client credentials"
**Solution:**
1. Double-check your Client ID and Client Secret
2. Make sure there are no extra spaces or newlines
3. Regenerate client secret if necessary

#### ❌ "HTTP 429 Too Many Requests"
**Solution:** 
- Wait a few minutes for rate limit to reset
- The client has built-in rate limiting, but manual testing can exceed limits

#### ❌ "HTTP 401 Unauthorized"
**Solution:**
- Token may be expired - run token refresh test
- Check if required scopes are granted
- Re-authenticate if necessary

### Debug Mode

Enable detailed logging by setting:
```bash
LOG_LEVEL=DEBUG
CENTRALIZED_LOGGING=true
```

This will show all HTTP requests/responses and token operations.

### Scope Requirements

Different endpoints require different scopes. Default scopes include:
- `user-read-private` - Basic profile info
- `user-read-email` - Email address
- `user-top-read` - Top tracks/artists
- `user-read-recently-played` - Listening history
- `playlist-read-private` - Private playlists

If you get 403 Forbidden errors, you may need additional scopes.

---

## Next Steps

Once authentication is working:

1. **Integrate with data collection** services
2. **Set up token persistence** (database, file, etc.)
3. **Build automated workflows** for data extraction
4. **Implement correlation analysis** using audio features
5. **Create dashboards** and visualization tools

## Conclusion

This client provides a comprehensive way to interact with the Spotify Web API, allowing you to integrate rich music data and user listening patterns seamlessly into your applications. The correlation-ready data extraction methods make it perfect for music analysis and recommendation systems.

**Happy coding! 🎵**
