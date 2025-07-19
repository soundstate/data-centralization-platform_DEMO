# TMDB Data Collection Service - Proof of Concept

This service demonstrates the implementation and usage of the TMDB API client following the established patterns in the Data Centralization Platform codebase.

## Overview

The TMDB Data Collection Service showcases:

- **Environment-driven configuration** following project standards
- **Comprehensive movie and TV show data collection**
- **Correlation-ready data extraction** for cross-domain analysis
- **Comprehensive logging** and debugging capabilities

## Features

### 🎥 Data Collection Capabilities
- **Movie Information**: Details, credits, reviews, and recommendations
- **TV Show Information**: Details, credits, airing schedules, and recommendations
- **Person Information**: Actors, directors, and crew details
- **Search Functionality**: Search across movies, TV shows, and people
- **Trending and Popular Content**: Latest trends and popular items
- **Image URL Construction**

### 🔗 Correlation Analysis Ready
- **Media Features**: Ratings, vote counts, popularity
- **Categorical Data**: Genre IDs, language
- **Temporal Data**: Release dates, air dates
- **Content Categorization**: Media type, popularity level

### 🛡️ Enterprise-Ready Features
- **Rate Limiting**: Respects TMDB API limits
- **Error Handling**: Comprehensive error management and retry logic
- **Logging**: Detailed debugging and monitoring
- **Configuration**: Environment-driven settings

## Configuration

### Required Environment Variables

```bash
# TMDB API Key (Required)
TMDB_API_KEY=your_api_key_here

# Language Configuration (Optional)
TMDB_LANGUAGE=en-US  # Options: en-US, es-ES, etc.
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
export TMDB_API_KEY="your_api_key_here"

# Run the proof of concept
python main.py
```

### API Usage Examples

#### Basic Client Usage

```python
import asyncio
from shared_core.config.tmdb_config import TMDBConfig
from shared_core.api.clients.tmdb import TMDBClient

async def example_usage():
    # Initialize client
    client = TMDBClient(
        api_key=TMDBConfig.api_key(),
        debug_mode=True
    )
    
    # Get popular movies
    response = await client.get_popular_movies(page=1, region=None)
    if response.success:
        popular_movies = response.data
        for movie in popular_movies['results']:
            print(f"Title: {movie['title']}, Rating: {movie['vote_average']}")
    
    # Extract correlation features
    for movie in popular_movies['results']:
        correlation_features = client.extract_correlation_features(movie)
        print(f"Correlation features: {correlation_features}")

asyncio.run(example_usage())
```

#### Advanced Configuration

```python
from shared_core.config.tmdb_config import TMDBConfig

# Get configuration summary
config_summary = TMDBConfig.get_config_summary()
print(f"Configuration: {config_summary}")

# Validate configuration
is_valid = TMDBConfig.validate_credentials()
print(f"Configuration valid: {is_valid}")
```

## Output Data Structure

### Media Data with Correlation Features

```json
{
  "raw_data": {
    "id": 550,
    "title": "Fight Club",
    "vote_average": 8.4,
    "vote_count": 17926,
    "popularity": 30.0,
    "genre_ids": [18, 28],
    "release_date": "1999-10-15",
    "language": "en"
  },
  "correlation_features": {
    "rating": 8.4,
    "vote_count": 17926,
    "popularity": 30.0,
    "genre_ids": [18, 28],
    "genre_count": 2,
    "is_adult": false,
    "original_language": "en",
    "is_english": true,
    "release_year": 1999,
    "release_month": 10,
    "release_decade": 1990
  },
  "temporal_context": {
    "release_date": "1999-10-15",
    "release_year": 1999,
    "release_month": 10
  },
  "content_categories": {
    "media_type": "movie",
    "rating_category": "excellent",
    "popularity_category": "popular",
    "content_rating": "general",
    "language_category": "english"
  },
  "data_source": "tmdb",
  "api_version": "3",
  "collection_timestamp": "2025-07-18T03:00:00Z"
}
```

---

*This proof of concept demonstrates the implementation of TMDB data collection using the shared_core framework.*
