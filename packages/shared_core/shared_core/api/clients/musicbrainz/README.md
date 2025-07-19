# MusicBrainz API Client

This package contains a client for interacting with the [MusicBrainz](https://musicbrainz.org/) API. It provides asynchronous HTTP methods to access artist, album, and track information with comprehensive error handling and logging.

## Features

- Asynchronous support using `asyncio`
- Rate limiting compliance with MusicBrainz guidelines
- Comprehensive artist, release, and search methods
- Error handling and retry logic
- User-Agent headers required by MusicBrainz
- Correlation-ready data extraction for cross-domain analysis

## Requirements

- Python 3.7+
- `httpx`, `asyncio-throttle`, `tenacity`, `pydantic`
- Valid User-Agent string registered to a real application or personal use

## Installation

Include the `shared_core` package in your Python path and install dependencies:

```bash
pip install -e /path/to/shared_core
pip install -r /path/to/services/data_collection/musicbrainz_collector/requirements.txt
```

## Configuration

### Environment Variables

Make sure to set the following environment variables:

- `MUSICBRAINZ_USER_AGENT`: Required. A unique string identifying your application, including contact details. Example:
  
  ```plaintext
  YourApp/1.0 (your.email@example.com)
  ```

### Example Usage

```python
import asyncio
from shared_core.config.musicbrainz_config import MusicBrainzConfig
from shared_core.api.clients.musicbrainz import MusicBrainzClient

async def run():
    # Initialize client
    config = MusicBrainzConfig.get_client_config()
    client = MusicBrainzClient(**config)
    
    # Example: Search for an artist
    response = await client.search_artist(query="Coldplay")
    if response.success:
        artists = response.data['artists']
        for artist in artists:
            print(f"Artist: {artist['name']}, Country: {artist.get('country', 'Unknown')}")

asyncio.run(run())
```

## API Methods

### `get_artist`
Fetch detailed information about an artist using the MusicBrainz ID (MBID).

```python
await client.get_artist(mbid="artist-mbid")
```

### `search_artist`
Search for artists matching the given query string.

```python
await client.search_artist(query="The Beatles", limit=10)
```

### `get_release`
Fetch detailed information about a release (album) using its MBID.

```python
await client.get_release(mbid="release-mbid")
```

### `search_release`
Search for releases matching the given query string.

```python
await client.search_release(query="Abbey Road", limit=5)
```

## Error Handling
Errors are logged via the centralized logging system (`CentralizedLogger`). The client retries failed requests using exponential backoff, as configured.

## Rate Limiting
The client respects rate limits of 1 request per second. Exceeding this limit will result in API errors.

## Debug Mode
Enable debug logging by setting `MUSICBRAINZ_DEBUG_MODE=true`. This logs detailed information about all requests.

## Conclusion
This client provides a straightforward way to interact with the MusicBrainz API, allowing you to integrate rich music metadata seamlessly into your applications.
