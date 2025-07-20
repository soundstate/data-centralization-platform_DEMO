"""
Embedding Service

Provides vector embedding generation and semantic search capabilities
across all data domains using OpenAI embeddings and pgvector.
"""

import asyncio
import os
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from openai import AsyncOpenAI
import pandas as pd
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.connection.database_manager import DatabaseManager
from ..database.models import *


class EmbeddingService:
    """
    Service for generating and managing vector embeddings across all domains
    """
    
    def __init__(self, 
                 model_name: str = "text-embedding-3-small",
                 api_key: Optional[str] = None):
        """
        Initialize the embedding service
        
        Args:
            model_name: OpenAI embedding model to use
            api_key: OpenAI API key (defaults to environment variable)
        """
        self.model_name = model_name
        self.dimension = 1536 if "large" in model_name else 384
        
        # Initialize OpenAI client
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY environment variable.")
        
        self.client = AsyncOpenAI(api_key=api_key)
        self.db_manager = DatabaseManager()
        
        # Rate limiting configuration
        self.max_tokens_per_minute = 1000000  # For text-embedding-3-small
        self.max_requests_per_minute = 3000
        self.batch_size = 100  # Reasonable batch size for API calls
    
    async def generate_embeddings_batch(self, 
                                       texts: List[str],
                                       batch_size: Optional[int] = None) -> List[List[float]]:
        """
        Generate embeddings for a batch of texts
        
        Args:
            texts: List of text strings to embed
            batch_size: Override default batch size
            
        Returns:
            List of embedding vectors
        """
        batch_size = batch_size or self.batch_size
        embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            
            try:
                response = await self.client.embeddings.create(
                    model=self.model_name,
                    input=batch
                )
                
                batch_embeddings = [item.embedding for item in response.data]
                embeddings.extend(batch_embeddings)
                
                # Rate limiting - conservative sleep
                await asyncio.sleep(0.1)
                
            except Exception as e:
                print(f"Error generating embeddings for batch {i//batch_size + 1}: {e}")
                # Add zero vectors for failed batch to maintain alignment
                embeddings.extend([[0.0] * self.dimension] * len(batch))
        
        return embeddings
    
    async def update_music_embeddings(self, limit: Optional[int] = None):
        """Update embeddings for music domain entities"""
        print("🎵 Updating music domain embeddings...")
        
        async with self.db_manager.async_session() as session:
            # Artists
            query = session.query(Artist)
            if limit:
                query = query.limit(limit)
            
            artists = await query.all()
            if artists:
                texts = [f"{artist.name} {' '.join(artist.genres or [])} music artist" 
                        for artist in artists]
                embeddings = await self.generate_embeddings_batch(texts)
                
                for artist, embedding in zip(artists, embeddings):
                    artist.embedded_content = f"{artist.name} {' '.join(artist.genres or [])} music artist"
                    artist.text_embedding = embedding
                
                await session.commit()
                print(f"✅ Updated embeddings for {len(artists)} artists")
            
            # Albums
            query = session.query(Album)
            if limit:
                query = query.limit(limit)
                
            albums = await query.all()
            if albums:
                texts = [f"{album.name} album by {album.artist.name if album.artist else 'Unknown'} {' '.join(album.genres or [])}"
                        for album in albums]
                embeddings = await self.generate_embeddings_batch(texts)
                
                for album, embedding in zip(albums, embeddings):
                    album.embedded_content = f"{album.name} album {' '.join(album.genres or [])}"
                    album.text_embedding = embedding
                
                await session.commit()
                print(f"✅ Updated embeddings for {len(albums)} albums")
            
            # Tracks
            query = session.query(Track)
            if limit:
                query = query.limit(limit)
                
            tracks = await query.all()
            if tracks:
                texts = []
                for track in tracks:
                    audio_features = track.audio_features or {}
                    mood = "energetic" if audio_features.get("energy", 0) > 0.6 else "calm"
                    dance = "danceable" if audio_features.get("danceability", 0) > 0.6 else "relaxed"
                    text = f"{track.name} song by {track.artist.name if track.artist else 'Unknown'} {mood} {dance} music track"
                    texts.append(text)
                
                embeddings = await self.generate_embeddings_batch(texts)
                
                for track, embedding, text in zip(tracks, embeddings, texts):
                    track.embedded_content = text
                    track.text_embedding = embedding
                
                await session.commit()
                print(f"✅ Updated embeddings for {len(tracks)} tracks")
    
    async def update_entertainment_embeddings(self, limit: Optional[int] = None):
        """Update embeddings for entertainment domain entities"""
        print("🎬 Updating entertainment domain embeddings...")
        
        async with self.db_manager.async_session() as session:
            # Movies
            query = session.query(Movie)
            if limit:
                query = query.limit(limit)
                
            movies = await query.all()
            if movies:
                texts = []
                for movie in movies:
                    genres_str = ' '.join(movie.genres or [])
                    overview = (movie.overview or '')[:200]  # Truncate for embedding
                    text = f"{movie.title} {genres_str} movie film {overview}"
                    texts.append(text)
                
                embeddings = await self.generate_embeddings_batch(texts)
                
                for movie, embedding, text in zip(movies, embeddings, texts):
                    movie.embedded_content = text
                    movie.text_embedding = embedding
                
                await session.commit()
                print(f"✅ Updated embeddings for {len(movies)} movies")
            
            # TV Shows
            query = session.query(TVShow)
            if limit:
                query = query.limit(limit)
                
            tv_shows = await query.all()
            if tv_shows:
                texts = []
                for show in tv_shows:
                    genres_str = ' '.join(show.genres or [])
                    overview = (show.overview or '')[:200]
                    text = f"{show.name} {genres_str} television show series {overview}"
                    texts.append(text)
                
                embeddings = await self.generate_embeddings_batch(texts)
                
                for show, embedding, text in zip(tv_shows, embeddings, texts):
                    show.embedded_content = text
                    show.text_embedding = embedding
                
                await session.commit()
                print(f"✅ Updated embeddings for {len(tv_shows)} TV shows")
    
    async def update_weather_embeddings(self, limit: Optional[int] = None):
        """Update embeddings for weather domain entities"""
        print("🌤️ Updating weather domain embeddings...")
        
        async with self.db_manager.async_session() as session:
            # Locations
            query = session.query(Location)
            if limit:
                query = query.limit(limit)
                
            locations = await query.all()
            if locations:
                texts = [f"{location.name} {location.state} {location.country} location city weather climate"
                        for location in locations]
                embeddings = await self.generate_embeddings_batch(texts)
                
                for location, embedding in zip(locations, embeddings):
                    location.embedded_content = f"{location.name} {location.state} {location.country} location weather"
                    location.text_embedding = embedding
                
                await session.commit()
                print(f"✅ Updated embeddings for {len(locations)} locations")
            
            # Current Weather (sample recent records)
            query = session.query(CurrentWeather).order_by(CurrentWeather.observed_at.desc())
            if limit:
                query = query.limit(limit * 5)  # More weather records since they're timestamped
                
            weather_records = await query.all()
            if weather_records:
                texts = []
                for weather in weather_records:
                    temp_desc = "hot" if weather.temperature > 25 else "cold" if weather.temperature < 10 else "mild"
                    text = f"{weather.weather_condition} {temp_desc} weather {weather.description} {weather.temperature}°C"
                    texts.append(text)
                
                embeddings = await self.generate_embeddings_batch(texts)
                
                for weather, embedding, text in zip(weather_records, embeddings, texts):
                    weather.embedded_content = text
                    weather.text_embedding = embedding
                
                await session.commit()
                print(f"✅ Updated embeddings for {len(weather_records)} weather records")
    
    async def update_gaming_embeddings(self, limit: Optional[int] = None):
        """Update embeddings for gaming domain entities"""
        print("🎮 Updating gaming domain embeddings...")
        
        async with self.db_manager.async_session() as session:
            # Pokemon
            query = session.query(Pokemon)
            if limit:
                query = query.limit(limit)
                
            pokemon = await query.all()
            if pokemon:
                texts = []
                for pkmn in pokemon:
                    types_str = ' '.join(pkmn.types or [])
                    abilities_str = ' '.join(pkmn.abilities or [])
                    text = f"{pkmn.name} {types_str} type pokemon {abilities_str} abilities gaming"
                    texts.append(text)
                
                embeddings = await self.generate_embeddings_batch(texts)
                
                for pkmn, embedding, text in zip(pokemon, embeddings, texts):
                    pkmn.embedded_content = text
                    pkmn.text_embedding = embedding
                
                await session.commit()
                print(f"✅ Updated embeddings for {len(pokemon)} Pokemon")
    
    async def update_development_embeddings(self, limit: Optional[int] = None):
        """Update embeddings for development domain entities"""
        print("💻 Updating development domain embeddings...")
        
        async with self.db_manager.async_session() as session:
            # GitHub Repositories
            query = session.query(GitHubRepository)
            if limit:
                query = query.limit(limit)
                
            repositories = await query.all()
            if repositories:
                texts = []
                for repo in repositories:
                    topics_str = ' '.join(repo.topics or [])
                    description = (repo.description or '')[:200]
                    text = f"{repo.name} {repo.language} programming repository {topics_str} {description} software development"
                    texts.append(text)
                
                embeddings = await self.generate_embeddings_batch(texts)
                
                for repo, embedding, text in zip(repositories, embeddings, texts):
                    repo.embedded_content = text
                    repo.text_embedding = embedding
                
                await session.commit()
                print(f"✅ Updated embeddings for {len(repositories)} repositories")
    
    async def update_productivity_embeddings(self, limit: Optional[int] = None):
        """Update embeddings for productivity domain entities"""
        print("📝 Updating productivity domain embeddings...")
        
        async with self.db_manager.async_session() as session:
            # Notion Pages
            query = session.query(NotionPage)
            if limit:
                query = query.limit(limit)
                
            pages = await query.all()
            if pages:
                texts = []
                for page in pages:
                    content = (page.content or '')[:300]  # Truncate content for embedding
                    text = f"{page.title} {page.page_type} notion page document {content}"
                    texts.append(text)
                
                embeddings = await self.generate_embeddings_batch(texts)
                
                for page, embedding, text in zip(pages, embeddings, texts):
                    page.embedded_content = text
                    page.text_embedding = embedding
                
                await session.commit()
                print(f"✅ Updated embeddings for {len(pages)} Notion pages")
    
    async def update_all_embeddings(self, limit_per_domain: Optional[int] = 50):
        """
        Update embeddings for all domains
        
        Args:
            limit_per_domain: Limit records per domain (useful for testing)
        """
        print("🚀 Starting comprehensive embedding update across all domains...")
        
        try:
            await self.update_music_embeddings(limit_per_domain)
            await self.update_entertainment_embeddings(limit_per_domain)
            await self.update_weather_embeddings(limit_per_domain)
            await self.update_gaming_embeddings(limit_per_domain)
            await self.update_development_embeddings(limit_per_domain)
            await self.update_productivity_embeddings(limit_per_domain)
            
            print("\n🎉 All domain embeddings updated successfully!")
            
        except Exception as e:
            print(f"❌ Error during embedding update: {e}")
            raise
    
    async def semantic_search(self, 
                            query: str, 
                            domain: Optional[str] = None,
                            k: int = 5) -> List[Dict[str, Any]]:
        """
        Perform semantic search across domains
        
        Args:
            query: Search query text
            domain: Specific domain to search (music, entertainment, weather, etc.)
            k: Number of results to return
            
        Returns:
            List of search results with similarity scores
        """
        # Generate query embedding
        query_embeddings = await self.generate_embeddings_batch([query])
        query_vector = query_embeddings[0]
        
        # Build search query based on domain
        search_tables = []
        
        if not domain or domain == "music":
            search_tables.extend([
                ("music.artists", "Artist"),
                ("music.albums", "Album"),
                ("music.tracks", "Track")
            ])
        
        if not domain or domain == "entertainment":
            search_tables.extend([
                ("entertainment.movies", "Movie"),
                ("entertainment.tv_shows", "TV Show")
            ])
        
        if not domain or domain == "weather":
            search_tables.extend([
                ("weather.locations", "Location"),
                ("weather.current_weather", "Weather")
            ])
        
        if not domain or domain == "gaming":
            search_tables.append(("gaming.pokemon", "Pokemon"))
        
        if not domain or domain == "development":
            search_tables.append(("development.github_repositories", "Repository"))
        
        if not domain or domain == "productivity":
            search_tables.append(("productivity.notion_pages", "Page"))
        
        # Perform vector similarity search
        results = []
        
        async with self.db_manager.async_session() as session:
            for table_name, entity_type in search_tables:
                try:
                    # Use pgvector cosine similarity
                    query_sql = text(f"""
                        SELECT 
                            id,
                            embedded_content,
                            text_embedding <=> :query_vector as similarity,
                            correlation_metadata
                        FROM {table_name}
                        WHERE text_embedding IS NOT NULL
                        ORDER BY text_embedding <=> :query_vector
                        LIMIT :limit
                    """)
                    
                    result = await session.execute(
                        query_sql, 
                        {
                            "query_vector": str(query_vector), 
                            "limit": k // len(search_tables) + 1
                        }
                    )
                    
                    for row in result:
                        results.append({
                            "id": str(row.id),
                            "content": row.embedded_content,
                            "similarity": float(row.similarity),
                            "entity_type": entity_type,
                            "domain": table_name.split('.')[0],
                            "metadata": row.correlation_metadata or {}
                        })
                
                except Exception as e:
                    print(f"Search error in {table_name}: {e}")
                    continue
        
        # Sort by similarity and return top k results
        results.sort(key=lambda x: x["similarity"])
        return results[:k]
    
    async def find_similar_entities(self, 
                                  entity_id: str, 
                                  entity_type: str,
                                  k: int = 5) -> List[Dict[str, Any]]:
        """
        Find entities similar to a given entity across all domains
        
        Args:
            entity_id: ID of the source entity
            entity_type: Type of entity (Artist, Movie, etc.)
            k: Number of similar entities to return
            
        Returns:
            List of similar entities with similarity scores
        """
        # Map entity types to tables
        entity_tables = {
            "Artist": "music.artists",
            "Album": "music.albums", 
            "Track": "music.tracks",
            "Movie": "entertainment.movies",
            "TVShow": "entertainment.tv_shows",
            "Location": "weather.locations",
            "Weather": "weather.current_weather",
            "Pokemon": "gaming.pokemon",
            "Repository": "development.github_repositories",
            "Page": "productivity.notion_pages"
        }
        
        source_table = entity_tables.get(entity_type)
        if not source_table:
            raise ValueError(f"Unknown entity type: {entity_type}")
        
        async with self.db_manager.async_session() as session:
            # Get source entity embedding
            source_query = text(f"""
                SELECT text_embedding, embedded_content
                FROM {source_table}
                WHERE id = :entity_id
            """)
            
            source_result = await session.execute(source_query, {"entity_id": entity_id})
            source_row = source_result.fetchone()
            
            if not source_row or not source_row.text_embedding:
                raise ValueError(f"Entity {entity_id} not found or has no embedding")
            
            source_embedding = source_row.text_embedding
            
            # Find similar entities across all tables
            results = []
            
            for table_name, table_entity_type in entity_tables.items():
                if table_name == entity_type:  # Skip same entity type
                    continue
                
                table_path = entity_tables[table_name]
                
                try:
                    similarity_query = text(f"""
                        SELECT 
                            id,
                            embedded_content,
                            text_embedding <=> :source_embedding as similarity,
                            correlation_metadata
                        FROM {table_path}
                        WHERE text_embedding IS NOT NULL
                        ORDER BY text_embedding <=> :source_embedding
                        LIMIT :limit
                    """)
                    
                    result = await session.execute(
                        similarity_query,
                        {"source_embedding": str(source_embedding), "limit": k}
                    )
                    
                    for row in result:
                        results.append({
                            "id": str(row.id),
                            "content": row.embedded_content,
                            "similarity": float(row.similarity),
                            "entity_type": table_name,
                            "domain": table_path.split('.')[0],
                            "metadata": row.correlation_metadata or {}
                        })
                
                except Exception as e:
                    print(f"Similarity search error in {table_path}: {e}")
                    continue
            
            # Sort by similarity and return top k results
            results.sort(key=lambda x: x["similarity"])
            return results[:k]


# Utility functions for embedding management
async def initialize_embeddings_demo(limit_per_domain: int = 20):
    """
    Initialize embeddings for demo data
    
    Args:
        limit_per_domain: Number of records per domain to embed (for demo)
    """
    embedding_service = EmbeddingService()
    await embedding_service.update_all_embeddings(limit_per_domain)


async def search_demo(query: str, domain: Optional[str] = None):
    """
    Demonstrate semantic search functionality
    
    Args:
        query: Search query
        domain: Optional domain filter
    """
    embedding_service = EmbeddingService()
    results = await embedding_service.semantic_search(query, domain)
    
    print(f"\n🔍 Search results for: '{query}'")
    if domain:
        print(f"Domain: {domain}")
    print("-" * 50)
    
    for i, result in enumerate(results, 1):
        print(f"{i}. [{result['entity_type']}] {result['content']}")
        print(f"   Domain: {result['domain']} | Similarity: {result['similarity']:.3f}")
        print()


if __name__ == "__main__":
    import asyncio
    
    async def main():
        """Demo script for embedding service"""
        print("🚀 Embedding Service Demo")
        print("=" * 50)
        
        # Note: This requires OPENAI_API_KEY environment variable
        try:
            # Initialize embeddings for demo data
            await initialize_embeddings_demo(limit_per_domain=10)
            
            # Perform sample searches
            await search_demo("upbeat energetic music")
            await search_demo("romantic comedy movie")
            await search_demo("rainy weather", domain="weather")
            
        except Exception as e:
            print(f"Demo failed: {e}")
            print("Make sure OPENAI_API_KEY is set and database is accessible")
    
    asyncio.run(main())
