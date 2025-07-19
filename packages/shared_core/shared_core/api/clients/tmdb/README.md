# TMDB API Client

This package contains a client for interacting with [The Movie Database (TMDB)](https://www.themoviedb.org/) API v3. It provides asynchronous HTTP methods to access movie, TV show, and person information with comprehensive error handling and logging.

## Features

- Asynchronous support using `asyncio`
- Rate limiting compliance with TMDB API guidelines (40 requests per 10 seconds)
- Comprehensive movie, TV show, and person methods
- Search functionality across all content types
- Trending and discovery endpoints
- Image URL construction helpers
- Error handling and retry logic
- Bearer token authentication
- Correlation-ready data extraction for cross-domain analysis

## Requirements

- Python 3.7+
- `httpx`, `asyncio-throttle`, `tenacity`, `pydantic`
- Valid TMDB API key (free registration required)

## Installation

Include the `shared_core` package in your Python path and install dependencies:

```bash
pip install -e /path/to/shared_core
pip install -r /path/to/services/data_collection/tmdb_collector/requirements.txt
```

## Configuration

### Environment Variables

Make sure to set the following environment variables:

- `TMDB_API_KEY`: Required. Your TMDB API key from [themoviedb.org](https://www.themoviedb.org/settings/api)
- `TMDB_LANGUAGE`: Optional. Default language for API requests (default: `en-US`)
- `TMDB_REGION`: Optional. Default region for API requests
- `TMDB_INCLUDE_ADULT`: Optional. Include adult content in results (default: `false`)
- `TMDB_DEBUG_MODE`: Optional. Enable debug logging (default: `false`)

### Example Usage

```python
import asyncio
from shared_core.config.tmdb_config import TMDBConfig
from shared_core.api.clients.tmdb import TMDBClient

async def run():
    # Initialize client
    config = TMDBConfig.get_client_config()
    client = TMDBClient(**config)
    
    # Example: Get popular movies
    response = await client.get_popular_movies(page=1)
    if response.success:
        movies = response.data['results']
        for movie in movies:
            print(f"Movie: {movie['title']}, Rating: {movie['vote_average']}")
    
    # Example: Search for a movie
    search_response = await client.search_movies(query="The Matrix")
    if search_response.success:
        movies = search_response.data['results']
        for movie in movies:
            print(f"Found: {movie['title']} ({movie.get('release_date', 'Unknown')})")

asyncio.run(run())
```

## API Methods

### Movie Methods

#### `get_movie_details`
Get detailed information about a movie by its TMDB ID.

```python
await client.get_movie_details(movie_id=550, append_to_response="credits,reviews")
```

#### `get_popular_movies`
Get a list of currently popular movies.

```python
await client.get_popular_movies(page=1, region="US")
```

#### `get_top_rated_movies`
Get the top-rated movies on TMDB.

```python
await client.get_top_rated_movies(page=1)
```

#### `get_now_playing_movies`
Get movies currently playing in theaters.

```python
await client.get_now_playing_movies(page=1, region="US")
```

#### `get_upcoming_movies`
Get upcoming movies.

```python
await client.get_upcoming_movies(page=1, region="US")
```

#### `get_movie_credits`
Get cast and crew information for a movie.

```python
await client.get_movie_credits(movie_id=550)
```

#### `get_movie_reviews`
Get user reviews for a movie.

```python
await client.get_movie_reviews(movie_id=550, page=1)
```

#### `get_movie_recommendations`
Get movie recommendations based on a movie.

```python
await client.get_movie_recommendations(movie_id=550, page=1)
```

### TV Show Methods

#### `get_tv_details`
Get detailed information about a TV show by its TMDB ID.

```python
await client.get_tv_details(tv_id=1396, append_to_response="credits,reviews")
```

#### `get_popular_tv_shows`
Get a list of currently popular TV shows.

```python
await client.get_popular_tv_shows(page=1)
```

#### `get_top_rated_tv_shows`
Get the top-rated TV shows on TMDB.

```python
await client.get_top_rated_tv_shows(page=1)
```

#### `get_tv_on_the_air`
Get TV shows currently on the air.

```python
await client.get_tv_on_the_air(page=1)
```

#### `get_tv_airing_today`
Get TV shows airing today.

```python
await client.get_tv_airing_today(page=1)
```

### Person Methods

#### `get_person_details`
Get detailed information about a person by their TMDB ID.

```python
await client.get_person_details(person_id=287, append_to_response="movie_credits,tv_credits")
```

#### `get_popular_people`
Get a list of currently popular people.

```python
await client.get_popular_people(page=1)
```

### Search Methods

#### `search_movies`
Search for movies by title.

```python
await client.search_movies(query="The Matrix", page=1, year=1999)
```

#### `search_tv_shows`
Search for TV shows by title.

```python
await client.search_tv_shows(query="Breaking Bad", page=1)
```

#### `search_people`
Search for people by name.

```python
await client.search_people(query="Tom Hanks", page=1)
```

#### `multi_search`
Search for movies, TV shows, and people in a single request.

```python
await client.multi_search(query="Marvel", page=1)
```

### Trending Methods

#### `get_trending`
Get trending content for the day or week.

```python
await client.get_trending(media_type="movie", time_window="day")
await client.get_trending(media_type="tv", time_window="week")
await client.get_trending(media_type="all", time_window="day")
```

### Discovery Methods

#### `discover_movies`
Discover movies with various filters.

```python
await client.discover_movies(
    genre_ids="28,12",  # Action, Adventure
    primary_release_year=2023,
    sort_by="popularity.desc"
)
```

#### `discover_tv_shows`
Discover TV shows with various filters.

```python
await client.discover_tv_shows(
    genre_ids="18,80",  # Drama, Crime
    first_air_date_year=2023,
    sort_by="vote_average.desc"
)
```

### Genre Methods

#### `get_movie_genres`
Get the official list of movie genres.

```python
await client.get_movie_genres()
```

#### `get_tv_genres`
Get the official list of TV show genres.

```python
await client.get_tv_genres()
```

## Image URL Construction

The client provides a helper method to construct full image URLs:

```python
# Get image URL for a poster
poster_url = client.get_image_url(movie['poster_path'], size="w500")

# Available sizes: w92, w154, w185, w342, w500, w780, original
backdrop_url = client.get_image_url(movie['backdrop_path'], size="original")
```

## Correlation Analysis Methods

The client provides methods to extract correlation-ready data:

```python
# Extract correlation features from movie data
features = client.extract_correlation_features(movie_data)

# Extract temporal context
temporal_context = client.extract_temporal_context(movie_data)

# Categorize content
categories = client.categorize_content(movie_data)

# Get complete correlation-ready data
correlation_data = client.prepare_correlation_data(movie_data)
```

## Error Handling

Errors are logged via the centralized logging system (`CentralizedLogger`). The client retries failed requests using exponential backoff, as configured.

## Rate Limiting

The client respects TMDB's rate limits of 40 requests per 10 seconds (4 requests per second). Exceeding this limit will result in API errors.

## Debug Mode

Enable debug logging by setting `TMDB_DEBUG_MODE=true`. This logs detailed information about all requests.

## Authentication

The client uses Bearer token authentication. Your API key is automatically included in the `Authorization` header as `Bearer {api_key}`.

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

This client provides a comprehensive way to interact with the TMDB API, allowing you to integrate rich movie and TV show metadata seamlessly into your applications. The correlation-ready data extraction methods make it easy to analyze content patterns and relationships.
