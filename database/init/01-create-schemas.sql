-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create domain schemas
CREATE SCHEMA IF NOT EXISTS music;
CREATE SCHEMA IF NOT EXISTS entertainment;
CREATE SCHEMA IF NOT EXISTS weather;
CREATE SCHEMA IF NOT EXISTS gaming;
CREATE SCHEMA IF NOT EXISTS development;
CREATE SCHEMA IF NOT EXISTS productivity;
CREATE SCHEMA IF NOT EXISTS general;

-- Create raw data storage schema for audit trail
CREATE SCHEMA IF NOT EXISTS raw_data;

-- Create correlation analysis schema
CREATE SCHEMA IF NOT EXISTS analytics;

-- Create LLM and embeddings schema
CREATE SCHEMA IF NOT EXISTS llm;

-- Grant permissions to postgres user
GRANT ALL ON ALL SCHEMAS TO postgres;

-- Create extension for UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Raw data audit table (stores all API responses)
CREATE TABLE IF NOT EXISTS raw_data.api_responses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    api_source VARCHAR(100) NOT NULL,
    endpoint VARCHAR(200) NOT NULL,
    request_params JSONB,
    response_data JSONB NOT NULL,
    status_code INTEGER,
    response_time_ms INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for raw data
CREATE INDEX IF NOT EXISTS idx_api_responses_source ON raw_data.api_responses (api_source);
CREATE INDEX IF NOT EXISTS idx_api_responses_endpoint ON raw_data.api_responses (endpoint);
CREATE INDEX IF NOT EXISTS idx_api_responses_created_at ON raw_data.api_responses (created_at);

-- Music domain tables
CREATE TABLE IF NOT EXISTS music.artists (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    spotify_id VARCHAR(100) UNIQUE,
    musicbrainz_id VARCHAR(100),
    name VARCHAR(500) NOT NULL,
    genres TEXT[],
    popularity INTEGER,
    followers INTEGER,
    external_urls JSONB,
    images JSONB,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS music.albums (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    spotify_id VARCHAR(100) UNIQUE,
    musicbrainz_id VARCHAR(100),
    name VARCHAR(500) NOT NULL,
    artist_id UUID REFERENCES music.artists(id),
    release_date DATE,
    total_tracks INTEGER,
    album_type VARCHAR(50),
    genres TEXT[],
    label VARCHAR(200),
    popularity INTEGER,
    images JSONB,
    external_urls JSONB,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS music.tracks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    spotify_id VARCHAR(100) UNIQUE,
    musicbrainz_id VARCHAR(100),
    name VARCHAR(500) NOT NULL,
    artist_id UUID REFERENCES music.artists(id),
    album_id UUID REFERENCES music.albums(id),
    duration_ms INTEGER,
    popularity INTEGER,
    track_number INTEGER,
    disc_number INTEGER,
    explicit BOOLEAN,
    audio_features JSONB,
    external_urls JSONB,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Entertainment domain tables
CREATE TABLE IF NOT EXISTS entertainment.movies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tmdb_id INTEGER UNIQUE,
    imdb_id VARCHAR(20),
    title VARCHAR(500) NOT NULL,
    original_title VARCHAR(500),
    overview TEXT,
    release_date DATE,
    runtime INTEGER,
    budget BIGINT,
    revenue BIGINT,
    genres TEXT[],
    production_companies TEXT[],
    production_countries TEXT[],
    spoken_languages TEXT[],
    adult BOOLEAN,
    popularity DECIMAL(10,3),
    vote_average DECIMAL(3,1),
    vote_count INTEGER,
    poster_path VARCHAR(200),
    backdrop_path VARCHAR(200),
    status VARCHAR(50),
    tagline TEXT,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS entertainment.tv_shows (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tmdb_id INTEGER UNIQUE,
    imdb_id VARCHAR(20),
    name VARCHAR(500) NOT NULL,
    original_name VARCHAR(500),
    overview TEXT,
    first_air_date DATE,
    last_air_date DATE,
    number_of_episodes INTEGER,
    number_of_seasons INTEGER,
    genres TEXT[],
    production_companies TEXT[],
    production_countries TEXT[],
    spoken_languages TEXT[],
    adult BOOLEAN,
    popularity DECIMAL(10,3),
    vote_average DECIMAL(3,1),
    vote_count INTEGER,
    poster_path VARCHAR(200),
    backdrop_path VARCHAR(200),
    status VARCHAR(50),
    tagline TEXT,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Weather domain tables
CREATE TABLE IF NOT EXISTS weather.locations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    country VARCHAR(100),
    state VARCHAR(100),
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    timezone VARCHAR(100),
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS weather.current_weather (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    location_id UUID REFERENCES weather.locations(id),
    temperature DECIMAL(5,2),
    feels_like DECIMAL(5,2),
    humidity INTEGER,
    pressure INTEGER,
    visibility INTEGER,
    uv_index DECIMAL(3,1),
    wind_speed DECIMAL(5,2),
    wind_direction INTEGER,
    weather_condition VARCHAR(100),
    description TEXT,
    icon VARCHAR(10),
    cloud_cover INTEGER,
    observed_at TIMESTAMP WITH TIME ZONE,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS weather.historical_weather (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    location_id UUID REFERENCES weather.locations(id),
    date DATE,
    temperature_min DECIMAL(5,2),
    temperature_max DECIMAL(5,2),
    temperature_avg DECIMAL(5,2),
    humidity_avg INTEGER,
    pressure_avg INTEGER,
    wind_speed_avg DECIMAL(5,2),
    precipitation DECIMAL(5,2),
    weather_condition VARCHAR(100),
    description TEXT,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Gaming domain tables
CREATE TABLE IF NOT EXISTS gaming.pokemon (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    pokemon_id INTEGER UNIQUE,
    name VARCHAR(100) NOT NULL,
    height INTEGER,
    weight INTEGER,
    base_experience INTEGER,
    types TEXT[],
    abilities TEXT[],
    stats JSONB,
    moves TEXT[],
    species_url VARCHAR(200),
    sprite_urls JSONB,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS gaming.pokemon_species (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    species_id INTEGER UNIQUE,
    name VARCHAR(100) NOT NULL,
    generation VARCHAR(50),
    color VARCHAR(50),
    shape VARCHAR(50),
    habitat VARCHAR(50),
    capture_rate INTEGER,
    base_happiness INTEGER,
    is_legendary BOOLEAN,
    is_mythical BOOLEAN,
    evolution_chain_id INTEGER,
    flavor_text TEXT,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Development domain tables
CREATE TABLE IF NOT EXISTS development.github_repositories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    github_id BIGINT UNIQUE,
    name VARCHAR(200) NOT NULL,
    full_name VARCHAR(400),
    owner_login VARCHAR(100),
    description TEXT,
    language VARCHAR(100),
    languages JSONB,
    size INTEGER,
    stargazers_count INTEGER,
    watchers_count INTEGER,
    forks_count INTEGER,
    open_issues_count INTEGER,
    topics TEXT[],
    license VARCHAR(100),
    is_private BOOLEAN,
    is_fork BOOLEAN,
    created_at_github TIMESTAMP WITH TIME ZONE,
    updated_at_github TIMESTAMP WITH TIME ZONE,
    pushed_at TIMESTAMP WITH TIME ZONE,
    clone_url VARCHAR(400),
    html_url VARCHAR(400),
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS development.github_commits (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    repository_id UUID REFERENCES development.github_repositories(id),
    sha VARCHAR(100) UNIQUE,
    message TEXT,
    author_name VARCHAR(200),
    author_email VARCHAR(200),
    committer_name VARCHAR(200),
    committer_email VARCHAR(200),
    commit_date TIMESTAMP WITH TIME ZONE,
    additions INTEGER,
    deletions INTEGER,
    changed_files INTEGER,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Productivity domain tables
CREATE TABLE IF NOT EXISTS productivity.notion_pages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    notion_id VARCHAR(100) UNIQUE,
    title VARCHAR(500),
    url VARCHAR(500),
    page_type VARCHAR(100),
    database_id VARCHAR(100),
    properties JSONB,
    content TEXT,
    created_time TIMESTAMP WITH TIME ZONE,
    last_edited_time TIMESTAMP WITH TIME ZONE,
    created_by VARCHAR(100),
    last_edited_by VARCHAR(100),
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS productivity.notion_databases (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    notion_id VARCHAR(100) UNIQUE,
    title VARCHAR(500),
    url VARCHAR(500),
    description TEXT,
    properties JSONB,
    created_time TIMESTAMP WITH TIME ZONE,
    last_edited_time TIMESTAMP WITH TIME ZONE,
    created_by VARCHAR(100),
    last_edited_by VARCHAR(100),
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- General domain tables for cross-domain entities
CREATE TABLE IF NOT EXISTS general.entities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_type VARCHAR(100) NOT NULL,
    entity_name VARCHAR(500) NOT NULL,
    entity_description TEXT,
    source_domain VARCHAR(100),
    source_id UUID,
    properties JSONB,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS general.entity_relationships (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity1_id UUID REFERENCES general.entities(id),
    entity2_id UUID REFERENCES general.entities(id),
    relationship_type VARCHAR(100) NOT NULL,
    relationship_strength DECIMAL(3,2),
    confidence_score DECIMAL(3,2),
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Analytics tables for correlation analysis
CREATE TABLE IF NOT EXISTS analytics.correlations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    correlation_type VARCHAR(100) NOT NULL,
    domain1 VARCHAR(100),
    domain2 VARCHAR(100),
    variable1 VARCHAR(200),
    variable2 VARCHAR(200),
    correlation_coefficient DECIMAL(10,8),
    p_value DECIMAL(10,8),
    confidence_interval JSONB,
    sample_size INTEGER,
    degrees_of_freedom INTEGER,
    analysis_method VARCHAR(100),
    is_significant BOOLEAN,
    effect_size DECIMAL(10,8),
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS analytics.time_series_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    domain VARCHAR(100),
    metric_name VARCHAR(200),
    metric_value DECIMAL(15,5),
    timestamp TIMESTAMP WITH TIME ZONE,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- LLM and embeddings tables
CREATE TABLE IF NOT EXISTS llm.embeddings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_domain VARCHAR(100),
    source_id UUID,
    content_type VARCHAR(100),
    content_text TEXT,
    embedding vector(1536), -- OpenAI embeddings are 1536 dimensions
    model_name VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS llm.generated_insights (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    insight_type VARCHAR(100),
    title VARCHAR(500),
    content TEXT,
    source_data_ids UUID[],
    correlation_ids UUID[],
    confidence_score DECIMAL(3,2),
    model_name VARCHAR(100),
    generation_parameters JSONB,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_music_artists_spotify_id ON music.artists (spotify_id);
CREATE INDEX IF NOT EXISTS idx_music_albums_artist_id ON music.albums (artist_id);
CREATE INDEX IF NOT EXISTS idx_music_tracks_artist_id ON music.tracks (artist_id);
CREATE INDEX IF NOT EXISTS idx_music_tracks_album_id ON music.tracks (album_id);

CREATE INDEX IF NOT EXISTS idx_entertainment_movies_tmdb_id ON entertainment.movies (tmdb_id);
CREATE INDEX IF NOT EXISTS idx_entertainment_tv_shows_tmdb_id ON entertainment.tv_shows (tmdb_id);

CREATE INDEX IF NOT EXISTS idx_weather_current_location_id ON weather.current_weather (location_id);
CREATE INDEX IF NOT EXISTS idx_weather_historical_location_id ON weather.historical_weather (location_id);
CREATE INDEX IF NOT EXISTS idx_weather_historical_date ON weather.historical_weather (date);

CREATE INDEX IF NOT EXISTS idx_gaming_pokemon_pokemon_id ON gaming.pokemon (pokemon_id);
CREATE INDEX IF NOT EXISTS idx_gaming_pokemon_species_species_id ON gaming.pokemon_species (species_id);

CREATE INDEX IF NOT EXISTS idx_development_repos_github_id ON development.github_repositories (github_id);
CREATE INDEX IF NOT EXISTS idx_development_commits_repo_id ON development.github_commits (repository_id);

CREATE INDEX IF NOT EXISTS idx_productivity_pages_notion_id ON productivity.notion_pages (notion_id);
CREATE INDEX IF NOT EXISTS idx_productivity_databases_notion_id ON productivity.notion_databases (notion_id);

CREATE INDEX IF NOT EXISTS idx_general_entities_type ON general.entities (entity_type);
CREATE INDEX IF NOT EXISTS idx_general_entities_source ON general.entities (source_domain, source_id);
CREATE INDEX IF NOT EXISTS idx_general_relationships_entity1 ON general.entity_relationships (entity1_id);
CREATE INDEX IF NOT EXISTS idx_general_relationships_entity2 ON general.entity_relationships (entity2_id);

CREATE INDEX IF NOT EXISTS idx_analytics_correlations_domains ON analytics.correlations (domain1, domain2);
CREATE INDEX IF NOT EXISTS idx_analytics_correlations_significant ON analytics.correlations (is_significant);
CREATE INDEX IF NOT EXISTS idx_analytics_time_series_domain ON analytics.time_series_data (domain);
CREATE INDEX IF NOT EXISTS idx_analytics_time_series_timestamp ON analytics.time_series_data (timestamp);

CREATE INDEX IF NOT EXISTS idx_llm_embeddings_source ON llm.embeddings (source_domain, source_id);
CREATE INDEX IF NOT EXISTS idx_llm_embeddings_vector ON llm.embeddings USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX IF NOT EXISTS idx_llm_insights_type ON llm.generated_insights (insight_type);

-- Create updated_at triggers for all tables
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply triggers to all tables with updated_at columns
DO $$
DECLARE
    table_name TEXT;
    schema_name TEXT;
BEGIN
    FOR schema_name, table_name IN 
        SELECT schemaname, tablename 
        FROM pg_tables 
        WHERE schemaname IN ('music', 'entertainment', 'weather', 'gaming', 'development', 'productivity', 'general', 'analytics', 'llm', 'raw_data')
    LOOP
        EXECUTE format('CREATE TRIGGER update_%I_%I_updated_at 
                       BEFORE UPDATE ON %I.%I 
                       FOR EACH ROW 
                       EXECUTE FUNCTION update_updated_at_column();', 
                       schema_name, table_name, schema_name, table_name);
    END LOOP;
END $$;

-- Create views for easier querying
CREATE OR REPLACE VIEW analytics.domain_summary AS
SELECT 
    'music' as domain,
    (SELECT COUNT(*) FROM music.artists) as artists,
    (SELECT COUNT(*) FROM music.albums) as albums,
    (SELECT COUNT(*) FROM music.tracks) as tracks,
    NULL::bigint as movies,
    NULL::bigint as tv_shows,
    NULL::bigint as weather_records,
    NULL::bigint as pokemon,
    NULL::bigint as repositories,
    NULL::bigint as notion_pages
UNION ALL
SELECT 
    'entertainment' as domain,
    NULL::bigint as artists,
    NULL::bigint as albums,
    NULL::bigint as tracks,
    (SELECT COUNT(*) FROM entertainment.movies) as movies,
    (SELECT COUNT(*) FROM entertainment.tv_shows) as tv_shows,
    NULL::bigint as weather_records,
    NULL::bigint as pokemon,
    NULL::bigint as repositories,
    NULL::bigint as notion_pages
UNION ALL
SELECT 
    'weather' as domain,
    NULL::bigint as artists,
    NULL::bigint as albums,
    NULL::bigint as tracks,
    NULL::bigint as movies,
    NULL::bigint as tv_shows,
    (SELECT COUNT(*) FROM weather.current_weather) as weather_records,
    NULL::bigint as pokemon,
    NULL::bigint as repositories,
    NULL::bigint as notion_pages
UNION ALL
SELECT 
    'gaming' as domain,
    NULL::bigint as artists,
    NULL::bigint as albums,
    NULL::bigint as tracks,
    NULL::bigint as movies,
    NULL::bigint as tv_shows,
    NULL::bigint as weather_records,
    (SELECT COUNT(*) FROM gaming.pokemon) as pokemon,
    NULL::bigint as repositories,
    NULL::bigint as notion_pages
UNION ALL
SELECT 
    'development' as domain,
    NULL::bigint as artists,
    NULL::bigint as albums,
    NULL::bigint as tracks,
    NULL::bigint as movies,
    NULL::bigint as tv_shows,
    NULL::bigint as weather_records,
    NULL::bigint as pokemon,
    (SELECT COUNT(*) FROM development.github_repositories) as repositories,
    NULL::bigint as notion_pages
UNION ALL
SELECT 
    'productivity' as domain,
    NULL::bigint as artists,
    NULL::bigint as albums,
    NULL::bigint as tracks,
    NULL::bigint as movies,
    NULL::bigint as tv_shows,
    NULL::bigint as weather_records,
    NULL::bigint as pokemon,
    NULL::bigint as repositories,
    (SELECT COUNT(*) FROM productivity.notion_pages) as notion_pages;

-- Create materialized view for correlation insights
CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.correlation_insights AS
SELECT 
    c.id,
    c.correlation_type,
    c.domain1,
    c.domain2,
    c.variable1,
    c.variable2,
    c.correlation_coefficient,
    c.p_value,
    c.is_significant,
    c.effect_size,
    c.sample_size,
    CASE 
        WHEN ABS(c.correlation_coefficient) >= 0.8 THEN 'Very Strong'
        WHEN ABS(c.correlation_coefficient) >= 0.6 THEN 'Strong'
        WHEN ABS(c.correlation_coefficient) >= 0.4 THEN 'Moderate'
        WHEN ABS(c.correlation_coefficient) >= 0.2 THEN 'Weak'
        ELSE 'Very Weak'
    END as correlation_strength,
    c.created_at
FROM analytics.correlations c
WHERE c.is_significant = true
ORDER BY ABS(c.correlation_coefficient) DESC;

-- Create indexes on the materialized view
CREATE INDEX IF NOT EXISTS idx_correlation_insights_domains ON analytics.correlation_insights (domain1, domain2);
CREATE INDEX IF NOT EXISTS idx_correlation_insights_strength ON analytics.correlation_insights (correlation_strength);

-- Grant permissions
GRANT USAGE ON ALL SCHEMAS TO postgres;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA music TO postgres;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA entertainment TO postgres;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA weather TO postgres;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA gaming TO postgres;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA development TO postgres;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA productivity TO postgres;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA general TO postgres;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA analytics TO postgres;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA llm TO postgres;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA raw_data TO postgres;

-- Refresh materialized views (for future updates)
REFRESH MATERIALIZED VIEW analytics.correlation_insights;

-- Final setup confirmation
SELECT 'Database initialization completed successfully' as status;
