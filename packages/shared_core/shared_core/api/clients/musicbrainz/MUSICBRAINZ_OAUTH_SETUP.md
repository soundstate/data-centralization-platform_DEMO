# MusicBrainz OAuth 2.0 Setup Guide

This guide will help you set up OAuth 2.0 authentication for the MusicBrainz API in your data centralization platform.

## Prerequisites

1. **MusicBrainz Account**: You need a MusicBrainz account and registered OAuth application
2. **Redis Server**: Required for session storage during OAuth flow
3. **Python Dependencies**: FastAPI, aiohttp, redis, and other dependencies

## Step 1: Register Your Application with MusicBrainz

1. Go to [MusicBrainz Applications](https://musicbrainz.org/account/applications)
2. Click "Register application"
3. Fill in the form:
   - **Name**: `data-centralization-DEM` (or your preferred name)
   - **Type**: `Web application`
   - **Callback URI**: `http://localhost:8000/auth/musicbrainz/callback`
4. Save the **Client ID** and **Client Secret** - you'll need these for configuration

## Step 2: Configure Environment Variables

1. Copy the environment template:
```bash
cp infrastructure/environments/.env.example .env
```

2. Edit `.env` and add your MusicBrainz credentials:
```bash
# MusicBrainz API Configuration
MUSICBRAINZ_USER_AGENT=data-centralization-platform/1.0.0 (your-email@example.com)

# MusicBrainz OAuth 2.0 Configuration
MUSICBRAINZ_CLIENT_ID=your_oauth_client_id_here
MUSICBRAINZ_CLIENT_SECRET=your_oauth_client_secret_here
MUSICBRAINZ_REDIRECT_URI=http://localhost:8000/auth/musicbrainz/callback

# Redis Configuration
REDIS_URL=redis://localhost:6379/0
```

## Step 3: Start Required Services

1. **Start Redis server** (if not already running):
```bash
# On macOS with Homebrew
brew services start redis

# Or run directly
redis-server
```

2. **Start PostgreSQL** (if using database token storage):
```bash
make docker-up
```

## Step 4: Install Dependencies

```bash
# Install the OAuth service dependencies
cd services/auth/musicbrainz_auth_service
pip install -r requirements.txt
```

## Step 5: Test the OAuth Flow

### Option A: Run the Test Script (Recommended)
```bash
cd services/auth/musicbrainz_auth_service
python test_oauth_flow.py
```

This script will:
1. Start the FastAPI OAuth server
2. Open your browser to initiate authentication
3. Guide you through the OAuth flow
4. Save test results to `output/oauth_test_results.json`

### Option B: Manual Testing

1. **Start the OAuth server**:
```bash
cd services/auth/musicbrainz_auth_service
python main.py
```

2. **Open browser** to initiate OAuth:
```
http://localhost:8000/auth/musicbrainz/login
```

3. **Complete authentication** in MusicBrainz

4. **Check the callback response** for your session ID

5. **Test API endpoints**:
```bash
# Check authentication status
curl http://localhost:8000/auth/musicbrainz/status/{session_id}

# Get access token
curl http://localhost:8000/auth/musicbrainz/token/{session_id}
```

## Step 6: Use OAuth in Your Data Collection

Once you have a valid access token, you can use it with the MusicBrainz API:

```python
from shared_core.api.clients.musicbrainz.musicbrainz_client import MusicBrainzClient
from shared_core.config.musicbrainz_config import MusicBrainzConfig

# Initialize client with OAuth support
config = MusicBrainzConfig.get_client_config()
client = MusicBrainzClient(**config)

# Set OAuth token (you'd get this from the OAuth service)
client.set_oauth_token("your_access_token_here")

# Now make authenticated requests
response = await client.search_artist("The Beatles")
```

## Available OAuth Endpoints

The FastAPI OAuth service provides these endpoints:

- `GET /auth/musicbrainz/login` - Start OAuth flow
- `GET /auth/musicbrainz/callback` - Handle OAuth callback
- `GET /auth/musicbrainz/status/{session_id}` - Check auth status
- `GET /auth/musicbrainz/token/{session_id}` - Get access token
- `POST /auth/musicbrainz/refresh` - Refresh expired token
- `DELETE /auth/musicbrainz/logout/{session_id}` - Logout
- `GET /health` - Health check
- `GET /docs` - API documentation

## Troubleshooting

### Common Issues

1. **"OAuth configuration is invalid"**
   - Check that `MUSICBRAINZ_CLIENT_ID` and `MUSICBRAINZ_CLIENT_SECRET` are set
   - Verify the credentials are correct from MusicBrainz

2. **"Redis connection failed"**
   - Make sure Redis server is running on `localhost:6379`
   - Check the `REDIS_URL` environment variable

3. **"Invalid redirect URI"**
   - Ensure the callback URI in MusicBrainz matches exactly: `http://localhost:8000/auth/musicbrainz/callback`
   - Check that the OAuth server is running on port 8000

4. **"Token exchange failed"**
   - Check the server logs for detailed error messages
   - Verify that you completed the authentication flow correctly

### Debug Mode

Enable debug mode for more detailed logging:
```bash
MUSICBRAINZ_DEBUG_MODE=true python main.py
```

### Check Configuration

Test your configuration:
```bash
python -c "
from shared_core.config.musicbrainz_config import MusicBrainzConfig
config = MusicBrainzConfig.get_oauth_config()
print('OAuth Config:', config)
"
```

## Next Steps

Once OAuth is working:

1. **Integrate with data collection**: Update your MusicBrainz collector to use OAuth tokens
2. **Implement token storage**: Set up persistent token storage in PostgreSQL
3. **Add refresh logic**: Implement automatic token refresh in your services
4. **Monitor usage**: Track API usage and token expiration

## Security Notes

- Never commit your `.env` file or expose your `CLIENT_SECRET`
- Use HTTPS in production environments
- Implement proper token rotation and expiration handling
- Monitor for unauthorized access to your tokens

For more detailed information, see the inline documentation in the code files and the project's main README.md.
