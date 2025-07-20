"""
Demo Data Generator

Generates realistic demo data for all domain models to support
proof-of-concept development and correlation analysis testing.
"""

import asyncio
import uuid
from datetime import datetime, timedelta, date
from decimal import Decimal
from typing import Dict, List, Any
import random
import json

# Import shared core components
try:
    from shared_core.database.models import *
    from shared_core.database.connection.database_manager import DatabaseManager
except ImportError:
    # For testing without database, create mock classes
    print("⚠️ Database models not available. Creating mock data only.")
    
    class MockDatabaseManager:
        def __init__(self):
            pass
        
        def async_session(self):
            return self
        
        def __enter__(self):
            return self
        
        def __exit__(self, *args):
            pass
        
        async def __aenter__(self):
            return self
        
        async def __aexit__(self, *args):
            pass
        
        def add(self, obj):
            pass
        
        async def flush(self):
            pass
        
        async def commit(self):
            pass
        
        async def rollback(self):
            pass
    
    DatabaseManager = MockDatabaseManager


class DemoDataGenerator:
    """
    Generates realistic demo data for proof-of-concept development
    """
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.generated_ids = {
            'artists': [],
            'albums': [],
            'tracks': [],
            'movies': [],
            'tv_shows': [],
            'locations': [],
            'pokemon': [],
            'repositories': []
        }
    
    async def generate_all_demo_data(self):
        """Generate demo data for all domains"""
        print("🚀 Starting demo data generation...")
        
        async with self.db_manager.async_session() as session:
            try:
                # Generate data in dependency order
                await self._generate_music_data(session)
                await self._generate_entertainment_data(session)
                await self._generate_weather_data(session)
                await self._generate_gaming_data(session)
                await self._generate_development_data(session)
                await self._generate_productivity_data(session)
                await self._generate_correlation_data(session)
                
                print("✅ Demo data generation completed successfully!")
                
            except Exception as e:
                print(f"❌ Error generating demo data: {e}")
                await session.rollback()
                raise
    
    async def _generate_music_data(self, session):
        """Generate music domain demo data"""
        print("🎵 Generating music domain data...")
        
        # Create artists
        artists_data = [
            {
                "spotify_id": "4gzpq5DPGxSnKTe4SA8HAU",
                "name": "Coldplay", 
                "genres": ["alternative rock", "british rock", "permanent wave"],
                "popularity": 88,
                "followers": 45123456,
                "external_urls": {"spotify": "https://open.spotify.com/artist/4gzpq5DPGxSnKTe4SA8HAU"},
                "embedded_content": "Coldplay British rock band alternative rock",
                "correlation_metadata": {"genre_primary": "alternative_rock", "mood_category": "uplifting"}
            },
            {
                "spotify_id": "06HL4z0CvFAxyc27GXpf02", 
                "name": "Taylor Swift",
                "genres": ["pop", "country pop", "indie folk"],
                "popularity": 100,
                "followers": 78654321,
                "external_urls": {"spotify": "https://open.spotify.com/artist/06HL4z0CvFAxyc27GXpf02"},
                "embedded_content": "Taylor Swift pop country indie folk music",
                "correlation_metadata": {"genre_primary": "pop", "mood_category": "emotional"}
            },
            {
                "spotify_id": "3WrFJ7ztbogyGnTHbHJFl2",
                "name": "The Beatles", 
                "genres": ["rock", "british invasion", "psychedelic rock"],
                "popularity": 85,
                "followers": 23456789,
                "external_urls": {"spotify": "https://open.spotify.com/artist/3WrFJ7ztbogyGnTHbHJFl2"},
                "embedded_content": "The Beatles rock british invasion legendary band",
                "correlation_metadata": {"genre_primary": "rock", "mood_category": "classic"}
            }
        ]
        
        for artist_data in artists_data:
            artist = Artist(**artist_data)
            session.add(artist)
            await session.flush()
            self.generated_ids['artists'].append(artist.id)
        
        # Create albums
        albums_data = [
            {
                "spotify_id": "7lQZVlh5Gf35LqNhGnr1Sb",
                "name": "A Head Full of Dreams",
                "artist_id": self.generated_ids['artists'][0],  # Coldplay
                "release_date": date(2015, 12, 4),
                "total_tracks": 11,
                "album_type": "album",
                "genres": ["alternative rock"],
                "label": "Warner Bros Records",
                "popularity": 75,
                "embedded_content": "A Head Full of Dreams Coldplay album alternative rock",
                "correlation_metadata": {"release_year": 2015, "chart_success": "high"}
            },
            {
                "spotify_id": "5eyZZoQEFQWRHkV2xgAeBw", 
                "name": "folklore",
                "artist_id": self.generated_ids['artists'][1],  # Taylor Swift
                "release_date": date(2020, 7, 24),
                "total_tracks": 16,
                "album_type": "album", 
                "genres": ["indie folk", "alternative"],
                "label": "Republic Records",
                "popularity": 88,
                "embedded_content": "folklore Taylor Swift indie folk alternative intimate",
                "correlation_metadata": {"release_year": 2020, "pandemic_release": True, "chart_success": "very_high"}
            }
        ]
        
        for album_data in albums_data:
            album = Album(**album_data)
            session.add(album)
            await session.flush()
            self.generated_ids['albums'].append(album.id)
        
        # Create tracks with ISRC codes for movie correlation
        tracks_data = [
            {
                "spotify_id": "5CQ30WqJwcep0pYcV4AMNc",
                "name": "Hymn for the Weekend",
                "artist_id": self.generated_ids['artists'][0],
                "album_id": self.generated_ids['albums'][0],
                "isrc_code": "GBAHS1500642",  # This will link to movies
                "duration_ms": 258266,
                "popularity": 82,
                "track_number": 3,
                "audio_features": {
                    "danceability": 0.748,
                    "energy": 0.652,
                    "valence": 0.825,
                    "tempo": 90.034,
                    "acousticness": 0.0473,
                    "instrumentalness": 0.000486,
                    "liveness": 0.0866,
                    "speechiness": 0.0362
                },
                "embedded_content": "Hymn for the Weekend Coldplay upbeat dance energetic",
                "correlation_metadata": {"mood_score": 0.7385, "energy_level": "high", "danceability": "high"}
            },
            {
                "spotify_id": "0V3wPSX9ygBnCm8psDIegu",
                "name": "the 1", 
                "artist_id": self.generated_ids['artists'][1],
                "album_id": self.generated_ids['albums'][1],
                "isrc_code": "USRC17607839",
                "duration_ms": 210829,
                "popularity": 77,
                "track_number": 1,
                "audio_features": {
                    "danceability": 0.555,
                    "energy": 0.425,
                    "valence": 0.289,
                    "tempo": 120.045,
                    "acousticness": 0.834,
                    "instrumentalness": 0.000294,
                    "liveness": 0.102,
                    "speechiness": 0.0455
                },
                "embedded_content": "the 1 Taylor Swift folklore acoustic introspective",
                "correlation_metadata": {"mood_score": 0.357, "energy_level": "medium", "acoustic": True}
            }
        ]
        
        for track_data in tracks_data:
            track = Track(**track_data)
            session.add(track)
            await session.flush()
            self.generated_ids['tracks'].append(track.id)
        
        await session.commit()
        print(f"✅ Generated {len(artists_data)} artists, {len(albums_data)} albums, {len(tracks_data)} tracks")
    
    async def _generate_entertainment_data(self, session):
        """Generate entertainment domain demo data with ISRC linking"""
        print("🎬 Generating entertainment domain data...")
        
        # Create movies with soundtrack ISRC codes that match music data
        movies_data = [
            {
                "tmdb_id": 284053,
                "imdb_id": "tt4154664",
                "title": "Thor: Ragnarok",
                "original_title": "Thor: Ragnarok", 
                "overview": "Thor is imprisoned on the other side of the universe and finds himself in a race against time to get back to Asgard...",
                "release_date": date(2017, 11, 3),
                "runtime": 130,
                "budget": 180000000,
                "revenue": 854000000,
                "genres": ["action", "adventure", "comedy"],
                "production_companies": ["Marvel Studios", "Walt Disney Pictures"],
                "popularity": Decimal('85.123'),
                "vote_average": Decimal('7.6'),
                "vote_count": 15432,
                "soundtrack_isrc_codes": ["GBAHS1500642"],  # Links to Coldplay track
                "embedded_content": "Thor Ragnarok Marvel superhero action adventure comedy",
                "correlation_metadata": {"box_office_category": "blockbuster", "genre_primary": "action", "marvel_phase": 3}
            },
            {
                "tmdb_id": 508442,
                "imdb_id": "tt9419884",
                "title": "Soul",
                "original_title": "Soul",
                "overview": "Joe Gardner is a middle school band teacher whose life hasn't quite gone the way he expected...",
                "release_date": date(2020, 12, 25),
                "runtime": 100,
                "budget": 150000000,
                "revenue": 121000000,
                "genres": ["animation", "family", "comedy"],
                "production_companies": ["Pixar Animation Studios", "Walt Disney Pictures"],
                "popularity": Decimal('78.456'),
                "vote_average": Decimal('8.2'),
                "vote_count": 8765,
                "soundtrack_isrc_codes": ["USRC17607839"],  # Links to Taylor Swift track
                "embedded_content": "Soul Pixar animation jazz music spiritual journey",
                "correlation_metadata": {"box_office_category": "successful", "genre_primary": "animation", "awards_potential": "high"}
            }
        ]
        
        for movie_data in movies_data:
            movie = Movie(**movie_data)
            session.add(movie)
            await session.flush()
            self.generated_ids['movies'].append(movie.id)
        
        # Create TV shows
        tv_shows_data = [
            {
                "tmdb_id": 94605,
                "name": "Arcane",
                "original_name": "Arcane",
                "overview": "Amid the stark discord of twin cities Piltover and Zaun, two sisters fight on rival sides of a war between magic technologies and clashing convictions.",
                "first_air_date": date(2021, 11, 6),
                "number_of_episodes": 9,
                "number_of_seasons": 1,
                "genres": ["animation", "action", "adventure"],
                "networks": ["Netflix"],
                "popularity": Decimal('89.234'),
                "vote_average": Decimal('9.0'),
                "vote_count": 2341,
                "embedded_content": "Arcane Netflix animation League of Legends Piltover Zaun",
                "correlation_metadata": {"genre_primary": "animation", "target_audience": "mature", "based_on": "video_game"}
            }
        ]
        
        for tv_data in tv_shows_data:
            tv_show = TVShow(**tv_data)
            session.add(tv_show)
            await session.flush()
            self.generated_ids['tv_shows'].append(tv_show.id)
        
        await session.commit()
        print(f"✅ Generated {len(movies_data)} movies, {len(tv_shows_data)} TV shows")
    
    async def _generate_weather_data(self, session):
        """Generate weather domain demo data with geographic coordinates"""
        print("🌤️ Generating weather domain data...")
        
        # Create locations
        locations_data = [
            {
                "name": "New York City",
                "country": "United States",
                "state": "New York", 
                "latitude": Decimal('40.7128'),
                "longitude": Decimal('-74.0060'),
                "timezone": "America/New_York",
                "population": 8336817,
                "embedded_content": "New York City NYC Manhattan urban metropolitan",
                "correlation_metadata": {"city_type": "major_metropolitan", "climate_zone": "humid_continental"}
            },
            {
                "name": "Los Angeles",
                "country": "United States",
                "state": "California",
                "latitude": Decimal('34.0522'),
                "longitude": Decimal('-118.2437'),
                "timezone": "America/Los_Angeles", 
                "population": 3979576,
                "embedded_content": "Los Angeles LA California sunshine entertainment",
                "correlation_metadata": {"city_type": "major_metropolitan", "climate_zone": "mediterranean"}
            },
            {
                "name": "London",
                "country": "United Kingdom",
                "state": "England",
                "latitude": Decimal('51.5074'),
                "longitude": Decimal('-0.1278'),
                "timezone": "Europe/London",
                "population": 9648110,
                "embedded_content": "London England UK Thames British capital",
                "correlation_metadata": {"city_type": "major_metropolitan", "climate_zone": "oceanic"}
            }
        ]
        
        for location_data in locations_data:
            location = Location(**location_data)
            session.add(location)
            await session.flush()
            self.generated_ids['locations'].append(location.id)
        
        # Generate current weather data for correlation analysis
        base_date = datetime.utcnow()
        weather_conditions = [
            ("clear", 22.5, 65, 1013, 0),  # sunny day
            ("rain", 15.8, 85, 1005, 2.5),  # rainy day  
            ("clouds", 18.2, 75, 1010, 0),  # cloudy day
            ("snow", -2.1, 90, 995, 5.2),  # snowy day
        ]
        
        current_weather_data = []
        for i, location_id in enumerate(self.generated_ids['locations']):
            condition, temp, humidity, pressure, precip = weather_conditions[i % len(weather_conditions)]
            
            weather_data = {
                "location_id": location_id,
                "temperature": Decimal(str(temp)),
                "feels_like": Decimal(str(temp - random.uniform(-2, 2))),
                "humidity": humidity,
                "pressure": pressure,
                "weather_condition": condition,
                "description": f"{condition} weather conditions",
                "observed_at": base_date - timedelta(hours=random.randint(1, 6)),
                "cloud_cover": random.randint(0, 100),
                "rain_1h": Decimal(str(precip)) if precip > 0 else None,
                "correlation_metadata": {
                    "weather_category": condition,
                    "temperature_category": self._get_temp_category(temp),
                    "comfort_index": self._calculate_comfort_index(temp, humidity)
                }
            }
            current_weather_data.append(weather_data)
        
        for weather_data in current_weather_data:
            weather = CurrentWeather(**weather_data)
            session.add(weather)
        
        await session.commit()
        print(f"✅ Generated {len(locations_data)} locations, {len(current_weather_data)} weather readings")
    
    async def _generate_gaming_data(self, session):
        """Generate gaming domain demo data"""
        print("🎮 Generating gaming domain data...")
        
        pokemon_data = [
            {
                "pokemon_id": 25,
                "name": "pikachu",
                "height": 4,  # decimeters
                "weight": 60,  # hectograms
                "base_experience": 112,
                "types": ["electric"],
                "abilities": ["static", "lightning-rod"],
                "stats": {
                    "hp": 35, "attack": 55, "defense": 40,
                    "special-attack": 50, "special-defense": 50, "speed": 90
                },
                "embedded_content": "pikachu electric pokemon mascot yellow lightning",
                "correlation_metadata": {"generation": 1, "popularity": "very_high", "type_primary": "electric"}
            },
            {
                "pokemon_id": 6,
                "name": "charizard",
                "height": 17,
                "weight": 905,
                "base_experience": 267,
                "types": ["fire", "flying"],
                "abilities": ["blaze", "solar-power"],
                "stats": {
                    "hp": 78, "attack": 84, "defense": 78,
                    "special-attack": 109, "special-defense": 85, "speed": 100
                },
                "embedded_content": "charizard fire flying dragon pokemon powerful",
                "correlation_metadata": {"generation": 1, "popularity": "very_high", "type_primary": "fire"}
            }
        ]
        
        for poke_data in pokemon_data:
            pokemon = Pokemon(**poke_data)
            session.add(pokemon)
            await session.flush()
            self.generated_ids['pokemon'].append(pokemon.id)
        
        await session.commit()
        print(f"✅ Generated {len(pokemon_data)} Pokemon")
    
    async def _generate_development_data(self, session):
        """Generate development domain demo data"""
        print("💻 Generating development domain data...")
        
        repositories_data = [
            {
                "github_id": 507775,
                "name": "react",
                "full_name": "facebook/react",
                "owner_login": "facebook",
                "description": "A declarative, efficient, and flexible JavaScript library for building user interfaces.",
                "language": "JavaScript",
                "size": 45632,
                "stargazers_count": 215000,
                "forks_count": 44500,
                "open_issues_count": 1024,
                "topics": ["javascript", "react", "frontend", "ui"],
                "license": "MIT",
                "is_private": False,
                "is_fork": False,
                "created_at_github": datetime(2013, 5, 24, 16, 15, 54),
                "pushed_at": datetime.utcnow() - timedelta(hours=3),
                "embedded_content": "React JavaScript library UI Facebook frontend declarative",
                "correlation_metadata": {"language_primary": "javascript", "category": "frontend", "company": "meta"}
            },
            {
                "github_id": 2126244,
                "name": "tensorflow",
                "full_name": "tensorflow/tensorflow", 
                "owner_login": "tensorflow",
                "description": "An Open Source Machine Learning Framework for Everyone",
                "language": "C++",
                "size": 287435,
                "stargazers_count": 185000,
                "forks_count": 74200,
                "open_issues_count": 2156,
                "topics": ["tensorflow", "machine-learning", "deep-learning", "python"],
                "license": "Apache-2.0",
                "is_private": False,
                "is_fork": False,
                "created_at_github": datetime(2015, 11, 9, 19, 44, 52),
                "pushed_at": datetime.utcnow() - timedelta(minutes=45),
                "embedded_content": "TensorFlow machine learning Google AI framework deep learning",
                "correlation_metadata": {"language_primary": "cpp", "category": "machine_learning", "company": "google"}
            }
        ]
        
        for repo_data in repositories_data:
            repo = GitHubRepository(**repo_data)
            session.add(repo)
            await session.flush()
            self.generated_ids['repositories'].append(repo.id)
        
        await session.commit()
        print(f"✅ Generated {len(repositories_data)} repositories")
    
    async def _generate_productivity_data(self, session):
        """Generate productivity domain demo data"""
        print("📝 Generating productivity domain data...")
        
        notion_pages_data = [
            {
                "notion_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                "title": "Project Planning Template",
                "page_type": "page",
                "content": "This is a comprehensive project planning template with sections for goals, timeline, resources, and deliverables. It helps organize complex projects and track progress effectively.",
                "created_time": datetime.utcnow() - timedelta(days=30),
                "last_edited_time": datetime.utcnow() - timedelta(days=2),
                "embedded_content": "project planning template goals timeline resources deliverables organization",
                "correlation_metadata": {"content_type": "template", "category": "project_management", "word_count": 156}
            },
            {
                "notion_id": "b2c3d4e5-f6g7-8901-bcde-f23456789012",
                "title": "Meeting Notes - Q1 Review",
                "page_type": "page", 
                "content": "Quarterly review meeting notes covering performance metrics, goals achieved, challenges faced, and plans for the next quarter.",
                "created_time": datetime.utcnow() - timedelta(days=7),
                "last_edited_time": datetime.utcnow() - timedelta(days=1),
                "embedded_content": "meeting notes quarterly review performance metrics goals challenges",
                "correlation_metadata": {"content_type": "meeting_notes", "category": "business", "word_count": 87}
            }
        ]
        
        for page_data in notion_pages_data:
            page = NotionPage(**page_data)
            session.add(page)
        
        await session.commit()
        print(f"✅ Generated {len(notion_pages_data)} Notion pages")
    
    async def _generate_correlation_data(self, session):
        """Generate sample correlation analysis data"""
        print("📊 Generating correlation analysis data...")
        
        # Sample correlations between domains
        correlations_data = [
            {
                "correlation_type": "pearson",
                "domain1": "weather",
                "domain2": "music", 
                "variable1": "temperature",
                "variable2": "audio_features.valence",
                "correlation_coefficient": Decimal('0.342'),
                "p_value": Decimal('0.0234'),
                "sample_size": 1250,
                "analysis_method": "pearson_correlation",
                "is_significant": True,
                "significance_level": Decimal('0.05'),
                "metadata_json": {
                    "interpretation": "Warmer weather correlates with more positive music valence",
                    "effect_size": "small_to_medium",
                    "business_relevance": "playlist_recommendations"
                }
            },
            {
                "correlation_type": "spearman",
                "domain1": "entertainment", 
                "domain2": "music",
                "variable1": "box_office_revenue",
                "variable2": "soundtrack_popularity",
                "correlation_coefficient": Decimal('0.567'),
                "p_value": Decimal('0.0012'),
                "sample_size": 324,
                "analysis_method": "spearman_correlation", 
                "is_significant": True,
                "significance_level": Decimal('0.01'),
                "metadata_json": {
                    "interpretation": "Higher box office correlates with soundtrack success",
                    "effect_size": "medium_to_large",
                    "business_relevance": "soundtrack_investment"
                }
            }
        ]
        
        for corr_data in correlations_data:
            correlation = Correlation(**corr_data)
            session.add(correlation)
        
        # Generate time series data for temporal correlation
        base_time = datetime.utcnow() - timedelta(days=30)
        time_series_data = []
        
        for i in range(30):  # 30 days of data
            timestamp = base_time + timedelta(days=i)
            
            # Music listening data
            time_series_data.append({
                "domain": "music",
                "metric_name": "daily_stream_count", 
                "metric_value": Decimal(str(random.randint(10000, 50000))),
                "timestamp": timestamp,
                "aggregation_level": "day",
                "aggregation_function": "sum",
                "metadata_json": {"source": "demo_generation"}
            })
            
            # Weather correlation
            time_series_data.append({
                "domain": "weather",
                "metric_name": "average_temperature",
                "metric_value": Decimal(str(round(20 + random.uniform(-10, 10), 2))),
                "timestamp": timestamp,
                "aggregation_level": "day", 
                "aggregation_function": "mean",
                "metadata_json": {"source": "demo_generation"}
            })
        
        for ts_data in time_series_data:
            ts_record = TimeSeriesData(**ts_data)
            session.add(ts_record)
        
        await session.commit()
        print(f"✅ Generated {len(correlations_data)} correlations, {len(time_series_data)} time series records")
    
    def _get_temp_category(self, temp: float) -> str:
        """Categorize temperature for correlation analysis"""
        if temp >= 30:
            return "very_hot"
        elif temp >= 20:
            return "warm" 
        elif temp >= 10:
            return "mild"
        elif temp >= 0:
            return "cool"
        else:
            return "cold"
    
    def _calculate_comfort_index(self, temp: float, humidity: int) -> float:
        """Simple comfort index calculation"""
        # Simplified heat index calculation
        if temp >= 20:
            heat_index = temp + (0.5 * humidity / 100) * (temp - 20)
            return max(0, min(1, (40 - heat_index) / 20))
        else:
            return max(0, min(1, (temp + 10) / 30))


async def export_demo_data_to_json():
    """Export demo data to JSON file for testing purposes"""
    print("📄 Exporting demo data to JSON file...")
    
    demo_data = {
        "music": {
            "artists": [
                {
                    "id": "uuid-1", "spotify_id": "4gzpq5DPGxSnKTe4SA8HAU", "name": "Coldplay",
                    "genres": ["alternative rock", "british rock"], "popularity": 88, "followers": 45123456
                },
                {
                    "id": "uuid-2", "spotify_id": "06HL4z0CvFAxyc27GXpf02", "name": "Taylor Swift",
                    "genres": ["pop", "country pop", "indie folk"], "popularity": 100, "followers": 78654321
                },
                {
                    "id": "uuid-3", "spotify_id": "3WrFJ7ztbogyGnTHbHJFl2", "name": "The Beatles",
                    "genres": ["rock", "british invasion"], "popularity": 85, "followers": 23456789
                }
            ],
            "tracks": [
                {
                    "id": "uuid-track-1", "name": "Hymn for the Weekend", "artist": "Coldplay",
                    "isrc_code": "GBAHS1500642", "duration_ms": 258266, "popularity": 82,
                    "audio_features": {"danceability": 0.748, "energy": 0.652, "valence": 0.825, "tempo": 90.034}
                },
                {
                    "id": "uuid-track-2", "name": "the 1", "artist": "Taylor Swift",
                    "isrc_code": "USRC17607839", "duration_ms": 210829, "popularity": 77,
                    "audio_features": {"danceability": 0.555, "energy": 0.425, "valence": 0.289, "tempo": 120.045}
                }
            ]
        },
        "entertainment": {
            "movies": [
                {
                    "id": "uuid-movie-1", "tmdb_id": 284053, "title": "Thor: Ragnarok",
                    "release_date": "2017-11-03", "runtime": 130, "budget": 180000000, "revenue": 854000000,
                    "genres": ["action", "adventure", "comedy"], "soundtrack_isrc_codes": ["GBAHS1500642"]
                },
                {
                    "id": "uuid-movie-2", "tmdb_id": 508442, "title": "Soul",
                    "release_date": "2020-12-25", "runtime": 100, "budget": 150000000, "revenue": 121000000,
                    "genres": ["animation", "family"], "soundtrack_isrc_codes": ["USRC17607839"]
                }
            ]
        },
        "weather": {
            "locations": [
                {"id": "uuid-loc-1", "name": "New York City", "country": "United States", "latitude": 40.7128, "longitude": -74.0060},
                {"id": "uuid-loc-2", "name": "Los Angeles", "country": "United States", "latitude": 34.0522, "longitude": -118.2437},
                {"id": "uuid-loc-3", "name": "London", "country": "United Kingdom", "latitude": 51.5074, "longitude": -0.1278}
            ],
            "current_weather": [
                {"location": "New York City", "temperature": 22.5, "humidity": 65, "condition": "clear"},
                {"location": "Los Angeles", "temperature": 15.8, "humidity": 85, "condition": "rain"},
                {"location": "London", "temperature": 18.2, "humidity": 75, "condition": "clouds"}
            ]
        },
        "gaming": {
            "pokemon": [
                {"id": "uuid-poke-1", "pokemon_id": 25, "name": "pikachu", "types": ["electric"], "base_experience": 112},
                {"id": "uuid-poke-2", "pokemon_id": 6, "name": "charizard", "types": ["fire", "flying"], "base_experience": 267}
            ]
        },
        "development": {
            "repositories": [
                {"id": "uuid-repo-1", "name": "react", "full_name": "facebook/react", "language": "JavaScript", "stargazers_count": 215000},
                {"id": "uuid-repo-2", "name": "tensorflow", "full_name": "tensorflow/tensorflow", "language": "C++", "stargazers_count": 185000}
            ]
        },
        "productivity": {
            "notion_pages": [
                {"id": "uuid-page-1", "title": "Project Planning Template", "content_preview": "This is a comprehensive project planning template..."},
                {"id": "uuid-page-2", "title": "Meeting Notes - Q1 Review", "content_preview": "Quarterly review meeting notes covering performance metrics..."}
            ]
        },
        "correlations": [
            {"domain1": "weather", "domain2": "music", "variable1": "temperature", "variable2": "valence", "correlation": 0.342, "p_value": 0.0234, "significant": True},
            {"domain1": "entertainment", "domain2": "music", "variable1": "box_office", "variable2": "soundtrack_popularity", "correlation": 0.567, "p_value": 0.0012, "significant": True}
        ],
        "metadata": {
            "total_records": 0,
            "domains": 6,
            "generated_at": datetime.now().isoformat(),
            "version": "1.0.0"
        }
    }
    
    # Calculate total records
    total = sum([
        len(demo_data["music"]["artists"]) + len(demo_data["music"]["tracks"]),
        len(demo_data["entertainment"]["movies"]),
        len(demo_data["weather"]["locations"]) + len(demo_data["weather"]["current_weather"]),
        len(demo_data["gaming"]["pokemon"]),
        len(demo_data["development"]["repositories"]),
        len(demo_data["productivity"]["notion_pages"]),
        len(demo_data["correlations"])
    ])
    demo_data["metadata"]["total_records"] = total
    
    # Export to JSON
    with open("demo_data.json", "w") as f:
        json.dump(demo_data, f, indent=2, default=str)
    
    print(f"✅ Exported {total} records across {demo_data['metadata']['domains']} domains to demo_data.json")
    return demo_data

async def main():
    """Main function to run demo data generation"""
    generator = DemoDataGenerator()
    
    try:
        # Generate data (with or without database)
        await generator.generate_all_demo_data()
        
        # Always export JSON for testing
        demo_data = await export_demo_data_to_json()
        
        print("\n🎉 Demo data generation complete!")
        print("Files created:")
        print("- demo_data.json (for testing and analysis)")
        print("\nYou can now test:")
        print("- Cross-domain entity linking (ISRC codes)")
        print("- Geographic correlations (weather + location)")
        print("- Temporal analysis (time series data)")
        print("- Statistical correlation analysis")
        print("- Vector embeddings and semantic search")
        
    except Exception as e:
        print(f"\n💥 Demo data generation failed: {e}")
        return False
    
    return True


if __name__ == "__main__":
    # Run the demo data generator
    success = asyncio.run(main())
