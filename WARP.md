# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

# Data Centralization Platform - Developer Guide

Transform scattered public APIs into unified, LLM-ready knowledge with sophisticated correlation analysis and interactive visualizations.

## 🚀 Quick Reference Card

### Essential Commands
```bash
# Environment Setup
make setup                                    # Complete dev environment setup
make docker-up                              # Start PostgreSQL, Redis, pgAdmin
python validate_setup.py                    # Validate configuration

# Development
pip install -e packages/shared_core          # Install shared package in dev mode
python -m pytest development/testing/       # Run test suite with coverage
make test                                   # Run all tests via npm workspaces

# Database Operations
cd packages/shared_core && alembic upgrade head    # Run migrations
docker exec -it data-centralization-postgres psql -U postgres -d data_centralization

# Data Collection
python services/data_collection/spotify_collector/main.py     # Spotify data collection
python services/data_collection/github_collector/main.py      # GitHub data collection
python services/data_collection/pokemon_collector/main.py     # Pokémon data collection

# Utilities
python scripts/correlation_analysis_demo.py                   # Demo correlation analysis
python demo/interactive_demos/streamlit_dashboard.py          # Interactive dashboard
```

## 🏗️ Architecture Overview

**Technology Stack**: Python 3.11+, PostgreSQL 16 + pgvector, Redis, FastAPI, LangChain, Plotly/Dash, Prefect 2

### Service Topology
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   API Clients   │    │ Data Collection │    │ Data Processing │
│                 │    │   Services      │    │   Services      │
│ • Spotify       ├────┤ • Async Workers ├────┤ • ETL Pipeline  │
│ • GitHub        │    │ • Redis Queues  │    │ • Entity Linking│
│ • OpenWeather   │    │ • Rate Limiting │    │ • Geo Enricher  │
│ • TMDB          │    │ • Error Handling│    │ • Time Aligner  │
│ • Pokémon       │    │                 │    │                 │
│ • MusicBrainz   │    └─────────────────┘    └─────────────────┘
│ • Notion        │                                       │
└─────────────────┘                                       │
                                                          ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Delivery      │    │    Insights     │    │   PostgreSQL    │
│                 │    │                 │    │                 │
│ • GraphQL API   ├────┤ • Correlation   ├────┤ • Raw Data      │
│ • REST API      │    │   Analysis      │    │ • Processed     │
│ • Notion Export │    │ • Significance  │    │ • Correlations  │
│ • Visualizations│    │   Testing       │    │ • Vector Store  │
│ • Dashboards    │    │ • Pattern Detect│    │   (pgvector)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                 │                       │
                                 ▼                       ▼
                    ┌─────────────────┐    ┌─────────────────┐
                    │ LLM Integration │    │   Orchestration │
                    │                 │    │                 │
                    │ • Embeddings    │    │ • Prefect Flows │
                    │ • Vector Search │    │ • Celery/Drama  │
                    │ • RAG Pipeline  │    │ • Monitoring    │
                    │ • Chat Service  │    │ • Scheduling    │
                    └─────────────────┘    └─────────────────┘
```

### Key Directory Structure
```
data-centralization-platform/
├── packages/shared_core/        # Shared utilities, models, API clients
├── services/                    # Microservices architecture
│   ├── data_collection/         # API data ingestion services
│   ├── data_processing/         # ETL and transformation services
│   ├── insights/               # Analytics and correlation services
│   ├── delivery/               # Output and visualization services
│   └── llm_integration/        # LLM and embedding services
├── flows/                      # Prefect workflow definitions
├── infrastructure/             # Docker, deployment, configuration
├── data/                       # Raw, processed, and output data
├── development/testing/        # Test suites and fixtures
└── demo/                      # Interactive demos and examples
```

## 📦 Package Management & Dependencies

### Shared Core Package Installation
```bash
# Development installation (recommended)
pip install -e packages/shared_core

# Production installation
pip install packages/shared_core/

# With optional dependencies
pip install -e "packages/shared_core[dev,viz,ml,all]"
```

### Environment Setup
```bash
# Virtual environment setup
python -m venv .venv
source .venv/bin/activate  # Unix/macOS
# or
.venv\Scripts\activate     # Windows

# Install all dependencies
pip install -r requirements.txt

# Install development dependencies from pyproject.toml
pip install -e ".[dev,viz,ml]"
```

## 🗄️ Database Operations

### PostgreSQL with pgvector Setup
```bash
# Start database services
make docker-up
# or
docker-compose -f infrastructure/docker/docker-compose.yml up -d

# Initialize database and run migrations
cd packages/shared_core
alembic upgrade head

# Check database connection
docker exec -it data-centralization-postgres psql -U postgres -d data_centralization
```

### Database Schema Organization
- **public**: Core application tables, raw API data
- **llm**: Embeddings, vector store, LLM-related tables
- **analytics**: Correlation results, statistical analysis
- **audit**: Data lineage, processing metadata

### Alembic Migration Commands
```bash
cd packages/shared_core

# Generate new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback one version
alembic downgrade -1

# Show current revision
alembic current

# Show migration history
alembic history --verbose
```

## 🧪 Testing Framework

### Running Tests
```bash
# Run all tests with coverage
python -m pytest development/testing/ --cov=packages/shared_core --cov=services --cov-report=html

# Run specific test categories
python -m pytest -m unit                    # Unit tests only
python -m pytest -m integration             # Integration tests only
python -m pytest -m correlation             # Correlation analysis tests
python -m pytest -m llm                     # LLM integration tests
python -m pytest -m external                # External API tests (requires API keys)

# Run with specific verbosity
python -m pytest -v                         # Verbose output
python -m pytest -s                         # Show print statements
python -m pytest --tb=short                 # Short traceback format

# Coverage report
python -m pytest --cov-report=term-missing  # Show missing lines
python -m pytest --cov-report=html          # Generate HTML report
```

### Test Organization
```
development/testing/
├── unit/                       # Fast, isolated unit tests
├── integration/               # Service integration tests
├── fixtures/                  # Test data and fixtures
├── conftest.py               # Pytest configuration and fixtures
└── coverage_html/            # HTML coverage reports
```

### Test Markers (defined in pyproject.toml)
- `unit`: Unit tests (fast, no external dependencies)
- `integration`: Integration tests (database, services)
- `functional`: End-to-end functional tests
- `correlation`: Statistical correlation tests
- `llm`: LLM integration tests
- `api`: External API integration tests
- `database`: Database-dependent tests
- `slow`: Long-running tests
- `external`: Tests requiring external services/APIs
- `docker`: Tests requiring Docker containers

## 🔌 API Client Development Patterns

### Creating New API Clients
Follow the established pattern in `packages/shared_core/api/clients/`:

```python
from shared_core.api.base_client import BaseAPIClient
from shared_core.models.domain_models import YourDomainModel

class YourAPIClient(BaseAPIClient):
    def __init__(self, api_key: str, **kwargs):
        super().__init__(
            base_url="https://api.yourservice.com",
            headers={"Authorization": f"Bearer {api_key}"},
            **kwargs
        )
    
    async def get_data(self, params: dict) -> APIResponse:
        """Fetch data with automatic retry and rate limiting."""
        return await self.get("/endpoint", params=params)
    
    def prepare_correlation_data(self, raw_data: dict) -> dict:
        """Transform API response for correlation analysis."""
        return {
            "entity_id": raw_data.get("id"),
            "timestamp": raw_data.get("created_at"),
            "location": self._extract_location(raw_data),
            "numerical_features": self._extract_features(raw_data),
            "categorical_data": self._extract_categories(raw_data)
        }
```

### Configuration Pattern
```python
# In shared_core/config/your_service_config.py
from shared_core.config.base_config import BaseConfig

class YourServiceConfig(BaseConfig):
    SERVICE_PREFIX = "YOURSERVICE"
    
    @classmethod
    def api_key(cls) -> str:
        return cls._get_env_var("API_KEY")
    
    @classmethod
    def rate_limit(cls) -> float:
        return float(cls._get_env_var("RATE_LIMIT", "1.0"))
```

## 🔄 Data Collection Services

### Creating New Collectors
Pattern for services in `services/data_collection/your_service_collector/`:

```bash
# Create service directory structure
mkdir -p services/data_collection/your_service_collector
cd services/data_collection/your_service_collector

# Required files
touch __init__.py main.py requirements.txt Dockerfile
```

### Collector Implementation Pattern
```python
# main.py template
import asyncio
from pathlib import Path
from shared_core.api.clients.your_service import YourServiceClient
from shared_core.utils.centralized_logging import CentralizedLogger

class YourServiceCollector:
    def __init__(self):
        self.logger = CentralizedLogger.get_logger(__name__)
        self.client = YourServiceClient()
        self.output_dir = Path("data/raw/your_service")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    async def collect_data(self):
        """Main data collection logic."""
        self.logger.info("Starting data collection...")
        # Implementation here
    
    async def store_raw_data(self, data: dict):
        """Store raw API responses."""
        # Save to data/raw/your_service/
    
    async def store_correlation_ready_data(self, data: dict):
        """Store processed data ready for correlation analysis."""
        # Save to data/processed/your_service/

if __name__ == "__main__":
    collector = YourServiceCollector()
    asyncio.run(collector.collect_data())
```

### Service Containerization
```dockerfile
# Dockerfile template
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "main.py"]
```

## 📊 Correlation Analysis & Statistics

### Running Correlation Analysis
```bash
# Demo correlation analysis
python scripts/correlation_analysis_demo.py

# Custom correlation analysis
python -c "
from shared_core.utils.statistical.correlation_analyzer import CorrelationAnalyzer
analyzer = CorrelationAnalyzer()
results = analyzer.analyze_cross_domain_correlations()
print(results)
"
```

### Statistical Analysis Patterns
- **Correlation Detection**: Pearson, Spearman, Kendall correlations
- **Significance Testing**: p-value calculation with multiple testing corrections
- **Causation Evaluation**: Granger causality, confounding variable detection
- **Time Series Analysis**: Temporal correlation with lag analysis

### Correlation Data Requirements
Each domain should provide:
```python
{
    "entity_id": "unique_identifier",
    "timestamp": "ISO_8601_datetime",
    "location": {"lat": float, "lon": float},
    "numerical_features": {
        "feature_name": float_value,
        # e.g., "valence": 0.7, "energy": 0.8
    },
    "categorical_data": {
        "category_name": "category_value",
        # e.g., "genre": "rock", "weather": "rainy"
    }
}
```

## 🤖 LLM Integration & Vector Search

### Embedding Generation
```bash
# Generate embeddings for all collected data
python services/llm_integration/embedding_service/main.py

# Query vector store
python -c "
from shared_core.api.vector_search import VectorSearchClient
client = VectorSearchClient()
results = client.semantic_search('rainy day music patterns')
print(results)
"
```

### LLM Configuration
- **Local LLM**: Ollama with llama3:8b-instruct-q4_K_M
- **Embeddings**: Nomic Embed v1.5 (local) + OpenAI text-embedding-3-small
- **Vector Store**: PostgreSQL with pgvector extension
- **Context Window**: 8K tokens with retrieval-augmented generation

## 📈 Visualization & Dashboards

### Running Interactive Dashboards
```bash
# Streamlit dashboard
streamlit run demo/interactive_demos/streamlit_dashboard.py

# Plotly/Dash dashboard
python services/delivery/visualization_service/main.py
```

### Visualization Types Available
- Time series correlation charts
- Cross-correlation heatmaps
- Geographic correlation maps (using Folium/Mapbox)
- Bubble charts for multi-dimensional analysis
- Sankey diagrams for data flow visualization
- Interactive network graphs for entity relationships

## 🔧 Environment Configuration

### Required Environment Variables
```bash
# API Keys (Required for data collection)
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
GITHUB_ACCESS_TOKEN=your_github_token
OPENWEATHERMAP_API_KEY=your_weather_api_key
TMDB_API_KEY=your_tmdb_api_key
NOTION_API_TOKEN=your_notion_token
MUSICBRAINZ_USER_AGENT=YourApp/1.0.0

# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/data_centralization
POSTGRES_PASSWORD=postgres

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# LLM Configuration
OPENAI_API_KEY=your_openai_api_key  # Optional, for comparison embeddings
OLLAMA_BASE_URL=http://localhost:11434  # Local LLM server

# Development Settings
DEBUG_MODE=true
LOG_LEVEL=INFO
ENVIRONMENT=development
```

### Configuration Files
- `infrastructure/environments/.env.example`: Template file
- `infrastructure/environment/.env.development`: Development settings
- `.env`: Local development overrides (create from template)

## 🌊 Workflow Orchestration

### Prefect Flows
```bash
# Start Prefect server (development)
prefect server start

# Run specific flows
prefect run flows/data_ingestion_flow/main.py
prefect run flows/correlation_flow/main.py

# Schedule daily correlation analysis
python flows/correlation_flow/schedule.py
```

### Celery/Dramatiq Workers
```bash
# Start Redis (required for task queue)
redis-server

# Start Celery worker
celery -A services.data_processing.tasks worker --loglevel=info

# Start Dramatiq worker
dramatiq services.data_processing.tasks
```

## 🚨 Common Issues & Troubleshooting

### Database Issues
```bash
# Reset database completely
docker-compose -f infrastructure/docker/docker-compose.yml down -v
docker-compose -f infrastructure/docker/docker-compose.yml up -d
cd packages/shared_core && alembic upgrade head

# Check pgvector extension
docker exec -it data-centralization-postgres psql -U postgres -d data_centralization -c "SELECT * FROM pg_extension WHERE extname = 'vector';"
```

### API Rate Limiting
- Spotify: 100 requests per minute (built-in backoff)
- GitHub: 5000 requests per hour with token
- OpenWeatherMap: 60 requests per minute (free tier)
- TMDB: 40 requests per 10 seconds

### Memory Issues with Large Datasets
```python
# Use streaming/chunked processing
CHUNK_SIZE = 1000  # Process in batches
MEMORY_LIMIT_GB = 4  # Monitor memory usage
```

### Vector Search Performance
```sql
-- Create indexes for better performance
CREATE INDEX ON llm.embeddings USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
```

## 💡 Development Best Practices

### Code Organization
- Use `shared_core` package for reusable components
- Follow async/await patterns for I/O operations
- Implement comprehensive error handling with retry logic
- Use Pydantic models for data validation
- Follow the existing logging patterns with CentralizedLogger

### Data Processing Guidelines
- Always store raw API responses before processing
- Implement idempotent processing (safe to re-run)
- Add audit trails for data lineage tracking
- Use database transactions for multi-step operations
- Implement data quality validation checks

### Statistical Analysis Standards
- Always test for statistical significance (p < 0.05)
- Include confidence intervals in correlation results
- Implement multiple testing corrections (Bonferroni, FDR)
- Add prominent correlation vs. causation warnings
- Document assumptions and limitations

## 📚 Additional Resources

### Key Documentation Files
- `README.md`: Project overview and getting started
- `resources/docs/development/implementation/implementation-plan.md`: Detailed implementation phases
- `resources/archive/folder_structure_guide.md`: Complete directory structure reference

### External Dependencies Documentation
- [PostgreSQL + pgvector](https://github.com/pgvector/pgvector)
- [Prefect 2.0](https://docs.prefect.io/)
- [LangChain](https://python.langchain.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Plotly/Dash](https://dash.plotly.com/)

---

*This platform demonstrates enterprise-grade data intelligence capabilities with sophisticated correlation analysis, LLM integration, and statistical rigor - transforming scattered data sources into actionable business insights.*
