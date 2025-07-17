# Data Sources & LLM Relationship Insights

Detailed mapping of API data points and sophisticated cross-domain relationship analysis for LLM-powered insights.

---

## 📊 Key Data Points by API

### 🎵 Spotify Web API (REST)
**Core Entities:**
- **Tracks**: `id`, `name`, `artists[]`, `album`, `duration_ms`, `explicit`, `popularity`, `preview_url`
- **Albums**: `id`, `name`, `artists[]`, `release_date`, `release_date_precision`, `total_tracks`, `genres[]`
- **Artists**: `id`, `name`, `genres[]`, `popularity`, `followers`, `images[]`
- **Audio Features**: `danceability`, `energy`, `valence`, `tempo`, `acousticness`, `instrumentalness`
- **Playlists**: `id`, `name`, `description`, `public`, `collaborative`, `tracks[]`

**Linkable Fields**: `artist.id`, `album.id`, `track.isrc`, `external_ids.isrc`

### 🎼 MusicBrainz API (REST)
**Core Entities:**
- **Releases**: `mbid`, `title`, `artist-credit[]`, `date`, `country`, `barcode`, `label-info[]`
- **Recordings**: `mbid`, `title`, `artist-credit[]`, `length`, `disambiguation`, `isrcs[]`
- **Artists**: `mbid`, `name`, `sort-name`, `type`, `country`, `begin-area`, `life-span`
- **Release Groups**: `mbid`, `title`, `primary-type`, `secondary-types[]`
- **Labels**: `mbid`, `name`, `type`, `country`, `area`

**Linkable Fields**: `mbid`, `isrcs[]`, `artist-credit[].name`

### 🎬 TMDB API (REST)
**Core Entities:**
- **Movies**: `id`, `title`, `overview`, `release_date`, `genres[]`, `production_countries[]`, `budget`, `revenue`, `runtime`, `vote_average`
- **TV Shows**: `id`, `name`, `overview`, `first_air_date`, `genres[]`, `origin_country[]`, `episode_run_time[]`, `vote_average`
- **People**: `id`, `name`, `biography`, `birthday`, `place_of_birth`, `known_for_department`
- **Production Companies**: `id`, `name`, `headquarters`, `origin_country`
- **Genres**: `id`, `name`

**Linkable Fields**: `id`, `imdb_id`, `release_date`, `first_air_date`, `production_countries[].iso_3166_1`

### 🌤️ OpenWeatherMap API (REST)
**Core Entities:**
- **Current Weather**: `coord.lat`, `coord.lon`, `weather[]`, `main.temp`, `main.humidity`, `main.pressure`, `dt`
- **Historical Weather**: `lat`, `lon`, `dt`, `temp`, `humidity`, `pressure`, `weather[]`
- **Weather Conditions**: `id`, `main`, `description`, `icon`
- **Geographic**: `coord.lat`, `coord.lon`, `country`, `name`, `timezone`

**Linkable Fields**: `coord.lat`, `coord.lon`, `dt` (timestamp), `country`

### 🐾 Pokémon API (REST)
**Core Entities:**
- **Pokémon**: `id`, `name`, `height`, `weight`, `types[]`, `abilities[]`, `stats[]`, `species`
- **Species**: `id`, `name`, `color`, `habitat`, `generation`, `evolution_chain`
- **Abilities**: `id`, `name`, `effect`, `short_effect`, `generation`
- **Types**: `id`, `name`, `damage_relations`, `generation`
- **Moves**: `id`, `name`, `power`, `accuracy`, `type`, `damage_class`

**Linkable Fields**: `id`, `name`, `types[].type.name`, `habitat.name`

### 🔧 GitHub GraphQL API
**Core Entities:**
- **Repositories**: `id`, `name`, `owner`, `description`, `primaryLanguage`, `stargazerCount`, `forkCount`, `createdAt`, `pushedAt`, `topics[]`
- **Commits**: `oid`, `author`, `committedDate`, `message`, `repository`
- **Users**: `login`, `name`, `location`, `company`, `bio`, `contributionsCollection`
- **Issues/PRs**: `id`, `title`, `body`, `createdAt`, `closedAt`, `labels[]`, `state`
- **Releases**: `id`, `name`, `description`, `publishedAt`, `isPrerelease`

**Linkable Fields**: `owner.login`, `createdAt`, `pushedAt`, `primaryLanguage.name`, `topics[].topic.name`

### 📝 Notion API (REST)
**Core Entities:**
- **Pages**: `id`, `title`, `properties{}`, `parent`, `created_time`, `last_edited_time`
- **Databases**: `id`, `title`, `properties{}`, `parent`, `created_time`
- **Blocks**: `id`, `type`, `content`, `parent`, `created_time`
- **Properties**: `id`, `name`, `type`, `configuration{}`

**Linkable Fields**: `id`, `parent.database_id`, `created_time`, `properties[].content`

---

## 🤖 LLM Relationship Analysis Examples

### 🎵 Music & Weather Patterns

**Correlation Discovery:**
```json
{
  "insight": "Rainy Day Blues: 67% increase in melancholic music releases during extended precipitation periods",
  "data_sources": ["Spotify", "MusicBrainz", "OpenWeatherMap"],
  "analysis": {
    "time_period": "2020-2023",
    "correlation_strength": 0.73,
    "sample_size": 15420,
    "pattern": "Albums with audio features: low valence (0.2-0.4), high acousticness (0.6+) release 67% more frequently during 7+ day precipitation periods"
  },
  "examples": [
    {
      "album": "Folklore - Taylor Swift",
      "release_date": "2020-07-24",
      "weather_context": "London: 14 consecutive rainy days",
      "audio_features": {"valence": 0.28, "acousticness": 0.84}
    }
  ],
  "causation_warning": "Weather may influence artist mood, but correlation could also reflect seasonal marketing strategies or coincidental timing."
}
```

**LLM Query**: *"Analyze the relationship between weather patterns and music emotional content across different regions and seasons."*

### 🎬 Entertainment & Developer Productivity

**Correlation Discovery:**
```json
{
  "insight": "Marvel Movie Paradox: 34% decrease in GitHub commits during major superhero film releases, but 156% spike in React component libraries",
  "data_sources": ["TMDB", "GitHub"],
  "analysis": {
    "time_period": "2019-2023",
    "correlation_strength": -0.45,
    "sample_size": 89234,
    "pattern": "Weekend commits drop during blockbuster releases, but specific tech domains see increased activity"
  },
  "examples": [
    {
      "movie": "Avengers: Endgame",
      "release_date": "2019-04-26",
      "github_impact": {
        "overall_commits": "-34%",
        "react_projects": "+156%",
        "ui_libraries": "+89%",
        "data_visualization": "+234%"
      }
    }
  ],
  "causation_warning": "Decreased commits may reflect leisure time allocation, while increased React activity could indicate inspiration or demand for movie-related web projects."
}
```

**LLM Query**: *"How do major entertainment events impact different aspects of software development activity?"*

### 🎮 Pokémon & Cultural Zeitgeist

**Correlation Discovery:**
```json
{
  "insight": "Electric Storm Surge: 289% increase in Electric-type Pokémon API requests during thunderstorm seasons",
  "data_sources": ["Pokémon API", "OpenWeatherMap", "GitHub"],
  "analysis": {
    "time_period": "2022-2023",
    "correlation_strength": 0.81,
    "sample_size": 45670,
    "pattern": "API requests for specific Pokémon types correlate with regional weather conditions"
  },
  "examples": [
    {
      "region": "Southeast US",
      "weather_event": "Hurricane season (June-November)",
      "pokemon_trends": {
        "water_types": "+245%",
        "electric_types": "+189%",
        "flying_types": "-67%"
      }
    }
  ],
  "causation_warning": "Weather correlation may reflect thematic associations rather than direct causation. Could indicate media consumption patterns or psychological connections to environmental conditions."
}
```

**LLM Query**: *"Explore how environmental conditions influence pop culture consumption patterns and API usage trends."*

### 🎼 Music Production & Tech Innovation

**Correlation Discovery:**
```json
{
  "insight": "Digital Audio Renaissance: 178% increase in music production GitHub repos during electronic music chart peaks",
  "data_sources": ["Spotify", "GitHub", "MusicBrainz"],
  "analysis": {
    "time_period": "2020-2023",
    "correlation_strength": 0.65,
    "sample_size": 23456,
    "pattern": "Electronic music popularity correlates with increased development of audio processing tools and DAW plugins"
  },
  "examples": [
    {
      "trend": "EDM Summer 2022",
      "spotify_data": "Electronic genres: +234% playlist additions",
      "github_impact": {
        "audio_libraries": "+178%",
        "daw_plugins": "+145%",
        "midi_tools": "+156%",
        "web_audio_api": "+289%"
      }
    }
  ],
  "causation_warning": "Correlation may reflect seasonal trends, increased interest in music production, or availability of development time during summer months."
}
```

**LLM Query**: *"What relationships exist between music genre popularity and technology development in audio processing?"*

---

## 📈 Data Visualization & Chart Generation

### 📊 Chart Types for Relationship Discovery

**1. Time Series Correlation Charts**
```python
# Technology: Plotly + Dash for interactive dashboards
# Example: GitHub commits vs. weather conditions over time
fig = px.line(df, x='date', y='commit_count', color='weather_condition')
fig.add_trace(px.scatter(df, x='date', y='album_releases').data[0])
```

**2. Correlation Heatmaps**
```python
# Technology: Seaborn for statistical visualizations
# Example: Cross-correlation matrix between all data sources
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
```

**3. Bubble Charts for Multi-Dimensional Analysis**
```python
# Technology: Plotly for interactive 3D visualizations
# Example: Movie popularity vs. GitHub activity vs. weather conditions
fig = px.scatter_3d(df, x='movie_popularity', y='github_commits', z='temperature',
                   size='correlation_strength', color='genre')
```

**4. Sankey Diagrams for Data Flow**
```python
# Technology: Plotly for flow visualizations
# Example: How different data sources contribute to insights
fig = go.Figure(data=[go.Sankey(node={"label": sources}, link={"source": source_ids, "target": target_ids})])
```

**5. Geographic Correlation Maps**
```python
# Technology: Folium + Plotly for geographic visualizations
# Example: Regional music trends vs. weather patterns
fig = px.scatter_geo(df, lat='latitude', lon='longitude', color='music_genre',
                    size='weather_correlation', hover_data=['temperature'])
```

### 🎯 Interactive Dashboard Features

**Real-time Correlation Discovery:**
- **Sliding Time Windows**: Adjust analysis periods to see how correlations change
- **Significance Testing**: Display p-values and confidence intervals
- **Causation Warnings**: Automated alerts about correlation vs. causation
- **Data Quality Indicators**: Show sample sizes and data completeness

**User-Driven Exploration:**
- **Custom Query Builder**: Let users define their own relationship hypotheses
- **Correlation Threshold Controls**: Filter out weak correlations
- **Multi-dimensional Filtering**: Slice data by genre, region, time period
- **Export Functionality**: Save insights as reports or share visualizations

### 📱 Notion Integration for Insights

**Automated Report Generation:**
```json
{
  "notion_page": {
    "title": "Weekly Data Insights - March 2024",
    "properties": {
      "Correlation Strength": 0.73,
      "Data Sources": ["Spotify", "OpenWeatherMap"],
      "Significance Level": "p < 0.01"
    },
    "content": [
      {
        "type": "callout",
        "text": "🚨 Correlation Alert: Strong relationship detected between rainy weather and acoustic music releases"
      },
      {
        "type": "embed",
        "url": "https://charts.example.com/correlation-viz-123"
      },
      {
        "type": "toggle",
        "title": "Methodology & Limitations",
        "content": "Analysis based on 15,420 data points. Correlation does not imply causation..."
      }
    ]
  }
}
```

---

## ⚠️ Correlation vs. Causation Framework

### 🧠 Critical Thinking Prompts for LLM

**Automated Causation Analysis:**
```json
{
  "correlation_detected": {
    "variables": ["rainy_weather", "melancholic_music_releases"],
    "strength": 0.73,
    "sample_size": 15420
  },
  "causation_evaluation": {
    "potential_confounds": [
      "Seasonal marketing strategies",
      "Artist personal factors",
      "Cultural events during rainy periods",
      "Data collection bias"
    ],
    "alternative_explanations": [
      "Recording studio availability during indoor weather",
      "Listener mood preferences during specific seasons",
      "Label release timing strategies"
    ],
    "strength_of_causal_claim": "Weak - Multiple confounding variables present",
    "recommended_analysis": "Controlled experiments or longitudinal studies needed"
  }
}
```

**LLM Prompt Framework:**
```
"When analyzing the correlation between {variable_1} and {variable_2}:

1. What alternative explanations could account for this relationship?
2. What confounding variables might be present?
3. How could this correlation be misleading?
4. What additional data would strengthen or weaken a causal claim?
5. How might sampling bias affect these results?

Always conclude with: 'This correlation suggests a relationship but does not establish causation.'"
```

### 📊 Statistical Rigor Indicators

**Confidence Metrics:**
- **Sample Size**: Minimum thresholds for statistical significance
- **Effect Size**: Practical significance beyond statistical significance
- **P-values**: Multiple testing corrections
- **Confidence Intervals**: Uncertainty quantification
- **Replication**: Cross-validation across different time periods

**Bias Detection:**
- **Survivorship Bias**: Are we only seeing successful correlations?
- **Confirmation Bias**: Are we seeking patterns that confirm expectations?
- **Temporal Bias**: Do correlations hold across different time periods?
- **Geographic Bias**: Do patterns vary by region?

---

## 🎯 Technical Implementation Notes

### 🛠️ Visualization Stack
- **Backend**: FastAPI + SQLAlchemy for data serving
- **Frontend**: React + D3.js for custom visualizations
- **Interactive Charts**: Plotly.js for scientific plotting
- **Geographic Maps**: Mapbox + Deck.gl for spatial analysis
- **Real-time Updates**: WebSocket connections for live correlation updates

### 🔄 Data Pipeline for Insights
1. **Ingestion**: Raw API data → PostgreSQL
2. **Processing**: Cross-correlation analysis → pgvector embeddings
3. **Analysis**: Statistical significance testing → Redis cache
4. **Visualization**: Chart generation → S3 static hosting
5. **Delivery**: Notion API updates → Dashboard refresh

### 🧪 A/B Testing Framework
- **Hypothesis Testing**: Automated statistical tests for correlations
- **Confidence Intervals**: Bayesian inference for uncertainty quantification
- **Multiple Testing**: Bonferroni correction for false discovery rates
- **Effect Size**: Cohen's d and other practical significance measures

---

**Remember**: The goal is not to find causation, but to demonstrate sophisticated data analysis, critical thinking, and the ability to surface interesting patterns while maintaining scientific rigor. Every insight should include appropriate caveats about correlation vs. causation.
