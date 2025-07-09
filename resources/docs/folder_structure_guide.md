# Folder Structure Guide - Data Centralization Platform

This document provides a comprehensive overview of the project's folder structure, explaining the purpose of each directory and where different types of files should be placed.

---

## 📁 Root Directory Overview

```
demo-codebase/
├── 📄 README.md                    # Project overview and quick start
├── 📄 ARCHITECTURE.md              # Technical architecture documentation
├── 📄 LLM_TRAINING_GUIDE.md        # LLM integration and training guide
├── 📄 requirements.txt             # Python dependencies
├── 📄 .prettierignore             # Code formatting configuration
├── 📁 packages/                    # Shared libraries and core functionality
├── 📁 services/                    # Microservices for data processing
├── 📁 flows/                       # Prefect workflow orchestration
├── 📁 data/                        # Data storage and outputs
├── 📁 infrastructure/              # Deployment and containerization
├── 📁 ui/                          # User interfaces and dashboards
├── 📁 development/                 # Development tools and testing
├── 📁 resources/                   # Documentation and guides
├── 📁 training/                    # LLM training datasets and configs
├── 📁 scripts/                     # Utility scripts and automation
├── 📁 logs/                        # Application logs
└── 📁 templates/                   # Code templates and boilerplate
```

---

## 🏗️ Core Architecture Directories

### 📦 `/packages/` - Shared Libraries
**Purpose**: Reusable code components shared across multiple services

#### `packages/shared_core/` - Primary shared package
```
shared_core/
├── 📄 setup.py                     # Package installation configuration
├── 📄 requirements.txt             # Package dependencies
├── 📄 README.md                    # Package documentation
├── 📁 shared_core/                 # Core functionality
│   ├── 📁 api/                     # API integration components
│   │   ├── 📁 clients/             # External API clients
│   │   │   ├── 📁 spotify/         # Spotify REST API client
│   │   │   ├── 📁 musicbrainz/     # MusicBrainz REST API client
│   │   │   ├── 📁 tmdb/            # TMDB REST API client
│   │   │   ├── 📁 weather/         # OpenWeatherMap API client
│   │   │   ├── 📁 openweathermap/  # Extended weather API client
│   │   │   ├── 📁 pokemon/         # Pokémon API client
│   │   │   ├── 📁 github/          # GitHub GraphQL API client
│   │   │   └── 📁 notion/          # Notion API client
│   │   └── 📁 graphql/             # GraphQL utilities and helpers
│   ├── 📁 models/                  # Pydantic data models
│   │   ├── 📄 music.py             # Music domain models
│   │   ├── 📄 entertainment.py     # Entertainment domain models
│   │   ├── 📄 weather.py           # Weather domain models
│   │   ├── 📄 pokemon.py           # Gaming/pop culture models
│   │   ├── 📄 github.py            # Development domain models
│   │   └── 📄 correlation.py       # Statistical analysis models
│   ├── 📁 config/                  # Configuration management
│   │   ├── 📄 base_client.py       # Base API client configuration
│   │   ├── 📄 logging_config.py    # Logging configuration
│   │   └── 📄 unified_environment_loader.py # Environment variables
│   ├── 📁 utils/                   # Utility functions
│   │   ├── 📄 centralized_logging.py # Logging utilities
│   │   ├── 📄 startup.py           # Application startup helpers
│   │   ├── 📁 statistical/         # Statistical analysis utilities
│   │   ├── 📁 embedding/           # Vector embedding utilities
│   │   ├── 📁 geographic/          # Location-based utilities
│   │   └── 📁 temporal/            # Time-based utilities
│   ├── 📁 database/                # Database management
│   │   ├── 📁 models/              # SQLModel database models
│   │   ├── 📁 migrations/          # Alembic database migrations
│   │   └── 📁 connection/          # Database connection management
│   ├── 📁 helper/                  # Helper functions and utilities
│   │   └── 📄 graphql_loader.py    # GraphQL query loading
│   └── 📁 ui/                      # UI integration utilities
├── 📁 knowledge_workflows/         # LLM-specific workflows
│   ├── 📁 data_fusion/             # Cross-domain data linking
│   ├── 📁 knowledge_extraction/    # Entity relationship mapping
│   └── 📁 training_prep/           # LLM dataset formatting
└── 📁 tests/                       # Package-level tests
```

#### `packages/workflows/` - Business logic workflows
**Purpose**: Complex business logic and workflow orchestration

---

## 🔧 Services Architecture

### 🗂️ `/services/` - Microservices
**Purpose**: Independent, scalable services for different aspects of data processing

#### `services/data_collection/` - Data Ingestion Services
```
data_collection/
├── 📁 spotify_collector/           # Music streaming data ingestion
├── 📁 musicbrainz_collector/       # Music metadata collection
├── 📁 tmdb_collector/              # Entertainment data collection
├── 📁 weather_collector/           # Weather data historical + current
├── 📁 pokemon_collector/           # Gaming/pop culture data
└── 📁 github_collector/            # Development activity tracking
```

#### `services/data_processing/` - Data Transformation Services
```
data_processing/
├── 📁 entity_linker/               # Cross-domain entity matching
├── 📁 correlation_analyzer/        # Statistical correlation analysis
├── 📁 geographic_enricher/         # Location-based data enhancement
├── 📁 temporal_aligner/            # Time-based data synchronization
├── 📁 embedding_generator/         # Vector embedding creation
├── 📁 causation_evaluator/         # Correlation vs causation analysis
├── 📁 knowledge_grapher/           # Relationship mapping
└── 📁 llm_formatter/               # Training data preparation
```

#### `services/insights/` - Intelligence Services
```
insights/
├── 📁 correlation_engine/          # Real-time correlation discovery
├── 📁 significance_tester/         # Statistical validation
├── 📁 pattern_detector/            # Anomaly and trend detection
└── 📁 report_generator/            # Automated insight reporting
```

#### `services/delivery/` - Output Services
```
delivery/
├── 📁 api_gateway/                 # GraphQL + REST unified API
├── 📁 notion_exporter/             # Notion page generation
├── 📁 visualization_service/       # Chart and graph generation
└── 📁 alert_system/                # Real-time correlation alerts
```

#### `services/llm_integration/` - LLM Services
```
llm_integration/
├── 📁 embedding_service/           # Text embedding generation
├── 📁 vector_search/               # Semantic search over embeddings
├── 📁 retrieval_chain/             # RAG implementation
├── 📁 chat_service/                # LLM conversation interface
└── 📁 evaluation/                  # LLM response quality testing
```

---

## 🌊 Workflow Orchestration

### 🔄 `/flows/` - Prefect Workflows
**Purpose**: DAG-based workflow orchestration and scheduling

```
flows/
├── 📁 data_ingestion_flow/         # Prefect workflow for data collection
├── 📁 processing_flow/             # ETL and analysis pipeline
├── 📁 correlation_flow/            # Daily correlation analysis
├── 📁 insight_generation_flow/     # Automated reporting
└── 📁 notion_sync_flow/            # Notion page updates
```

**File Types in Each Flow**:
- `main.py` - Prefect flow definition
- `tasks.py` - Individual task definitions
- `config.yml` - Flow configuration
- `requirements.txt` - Flow-specific dependencies

---

## 📊 Data Storage

### 💾 `/data/` - Data Storage and Outputs
**Purpose**: Centralized data storage with clear organization by processing stage

```
data/
├── 📁 raw/                         # Original API responses (JSON)
│   ├── 📁 spotify/                 # Spotify API raw data
│   ├── 📁 musicbrainz/             # MusicBrainz API raw data
│   ├── 📁 tmdb/                    # TMDB API raw data
│   ├── 📁 weather/                 # Weather API raw data
│   ├── 📁 pokemon/                 # Pokémon API raw data
│   ├── 📁 github/                  # GitHub API raw data
│   └── 📁 notion/                  # Notion API raw data
├── 📁 processed/                   # Cleaned and standardized data
│   ├── 📁 music/                   # Processed music data
│   ├── 📁 entertainment/           # Processed entertainment data
│   ├── 📁 weather/                 # Processed weather data
│   ├── 📁 pokemon/                 # Processed gaming data
│   └── 📁 github/                  # Processed development data
├── 📁 correlations/                # Correlation analysis results
│   ├── 📁 daily/                   # Daily correlation outputs
│   ├── 📁 weekly/                  # Weekly correlation summaries
│   └── 📁 historical/              # Historical correlation data
├── 📁 embeddings/                  # Vector embeddings
│   ├── 📁 text/                    # Text embeddings
│   ├── 📁 entity/                  # Entity embeddings
│   └── 📁 correlation/             # Correlation embeddings
├── 📁 visualizations/              # Generated charts and graphs
│   ├── 📁 charts/                  # Statistical charts
│   ├── 📁 maps/                    # Geographic visualizations
│   └── 📁 heatmaps/                # Correlation heatmaps
├── 📁 insights/                    # Generated insights and reports
│   ├── 📁 reports/                 # Automated reports
│   ├── 📁 alerts/                  # Correlation alerts
│   └── 📁 summaries/               # Data summaries
├── 📁 statistics/                  # Statistical analysis results
│   ├── 📁 significance/            # Statistical significance tests
│   ├── 📁 bias_detection/          # Bias analysis results
│   └── 📁 validation/              # Data validation results
├── 📁 knowledge_graphs/            # Entity relationship data (Neo4j format)
└── 📁 llm_training/                # Formatted training datasets
    ├── 📁 conversational/          # Q&A datasets
    ├── 📁 entities/                # Entity relationship data
    └── 📁 temporal/                # Time-series data
```

---

## 🚀 Infrastructure & Deployment

### 🐳 `/infrastructure/` - Deployment and Containerization
**Purpose**: Infrastructure as code and deployment configurations

```
infrastructure/
├── 📁 docker/                      # Docker configurations
│   ├── 📁 services/                # Individual service containers
│   ├── 📁 databases/               # Database container configs
│   ├── 📁 monitoring/              # Monitoring container configs
│   └── 📄 docker-compose.yml       # Local development setup
├── 📁 azure/                       # Azure deployment templates
│   ├── 📁 bicep/                   # Azure Bicep templates
│   ├── 📁 terraform/               # Terraform configurations
│   └── 📁 container_apps/          # Azure Container Apps configs
├── 📁 kubernetes/                  # Kubernetes deployment configs
│   ├── 📁 manifests/               # K8s manifests
│   ├── 📁 helm/                    # Helm charts
│   └── 📁 operators/               # Custom operators
├── 📁 environments/                # Environment-specific configurations
│   ├── 📁 development/             # Development environment
│   │   ├── 📁 config/              # Development config files
│   │   └── 📁 secrets/             # Development secrets
│   ├── 📁 staging/                 # Staging environment
│   │   ├── 📁 config/              # Staging config files
│   │   └── 📁 secrets/             # Staging secrets
│   ├── 📁 production/              # Production environment
│   │   ├── 📁 config/              # Production config files
│   │   └── 📁 secrets/             # Production secrets
│   └── 📁 shared/                  # Shared configurations
│       ├── 📁 config/              # Shared config files
│       └── 📁 secrets/             # Shared secrets
├── 📁 github_actions/              # GitHub Actions CI/CD workflows
├── 📁 local/                       # Local development setup
└── 📁 pipeline/                    # CI/CD pipeline configurations
```

---

## 🎨 User Interface

### 🖥️ `/ui/` - User Interfaces and Dashboards
**Purpose**: Frontend applications and user interfaces

```
ui/
├── 📁 dashboard/                   # Web dashboard for data exploration
│   ├── 📁 components/              # React components
│   │   ├── 📁 charts/              # Chart components
│   │   ├── 📁 tables/              # Data table components
│   │   ├── 📁 maps/                # Geographic map components
│   │   └── 📁 forms/               # Form components
│   ├── 📁 pages/                   # Dashboard pages
│   │   ├── 📁 correlations/        # Correlation analysis pages
│   │   ├── 📁 insights/            # Insights dashboard pages
│   │   └── 📁 data/                # Data exploration pages
│   ├── 📁 hooks/                   # Custom React hooks
│   ├── 📁 services/                # Frontend API services
│   ├── 📄 package.json             # Frontend dependencies
│   └── 📄 webpack.config.js        # Build configuration
└── 📁 power_apps/                  # Power Apps demo files
    ├── 📄 connection_guide.md       # Power Apps integration guide
    └── 📁 demo_screenshots/         # Demo screenshots
```

---

## 🧪 Development & Testing

### 🔬 `/development/` - Development Tools and Testing
**Purpose**: Development utilities, testing frameworks, and debugging tools

```
development/
├── 📁 examples/                    # Development examples
│   ├── 📁 api_integration/         # How to add new data sources
│   │   ├── 📁 spotify/             # Spotify integration example
│   │   ├── 📁 github/              # GitHub integration example
│   │   └── 📁 custom/              # Custom API integration template
│   ├── 📁 integration_patterns/    # Common integration examples
│   │   ├── 📁 rest_api/            # REST API integration patterns
│   │   ├── 📁 graphql/             # GraphQL integration patterns
│   │   └── 📁 webhook/             # Webhook integration patterns
│   └── 📁 api_usage/               # API usage examples
├── 📁 testing/                     # Comprehensive test suites
│   ├── 📁 unit/                    # Unit tests
│   │   ├── 📁 api_clients/         # API client tests
│   │   ├── 📁 models/              # Data model tests
│   │   └── 📁 utils/               # Utility function tests
│   ├── 📁 integration/             # Integration tests
│   │   ├── 📁 api_integration/     # API integration tests
│   │   ├── 📁 database/            # Database integration tests
│   │   └── 📁 services/            # Service integration tests
│   ├── 📁 functional/              # Functional tests
│   │   ├── 📁 workflows/           # Workflow tests
│   │   ├── 📁 correlations/        # Correlation analysis tests
│   │   └── 📁 insights/            # Insight generation tests
│   ├── 📁 llm_eval/                # LLM evaluation tests
│   │   ├── 📁 embedding/           # Embedding quality tests
│   │   ├── 📁 retrieval/           # Retrieval accuracy tests
│   │   └── 📁 response/            # Response quality tests
│   ├── 📁 statistical/             # Statistical validation tests
│   │   ├── 📁 correlation/         # Correlation analysis tests
│   │   ├── 📁 significance/        # Statistical significance tests
│   │   └── 📁 bias/                # Bias detection tests
│   ├── 📁 correlation/             # Correlation-specific tests
│   └── 📁 visualization/           # Visualization tests
└── 📁 tools/                       # Development utilities
    ├── 📁 debug_scripts/           # Debugging utilities
    │   ├── 📄 test_api_clients.py  # API client debugging
    │   ├── 📄 validate_data.py     # Data validation scripts
    │   └── 📄 check_correlations.py # Correlation debugging
    └── 📁 postman/                 # API testing collections
        ├── 📁 collections/         # Postman collections
        └── 📁 archive/             # Archived collections
```

---

## 📚 Documentation & Resources

### 📖 `/resources/` - Documentation and Examples
**Purpose**: Technical documentation, guides, and examples

```
resources/
├── 📁 docs/                        # Technical documentation
│   ├── 📄 folder_structure_guide.md # This document
│   ├── 📄 implementation_plan.md   # Implementation roadmap
│   ├── 📄 data_sources_and_insights.md # Data sources & insights
│   ├── 📄 demo-extracted-folder-structure.md # Folder structure demo
│   └── 📄 folder-structure-details.md # Detailed folder structure
├── 📁 examples/                    # Usage examples
│   ├── 📁 api_integration/         # API integration examples
│   │   ├── 📁 spotify/             # Spotify API examples
│   │   ├── 📁 github/              # GitHub API examples
│   │   └── 📁 notion/              # Notion API examples
│   ├── 📁 data_exploration/        # Data analysis examples
│   │   ├── 📁 correlation/         # Correlation analysis examples
│   │   ├── 📁 visualization/       # Visualization examples
│   │   └── 📁 statistical/         # Statistical analysis examples
│   └── 📁 knowledge_queries/       # Example AI prompts and responses
│       ├── 📁 music_weather/       # Music-weather correlation examples
│       ├── 📁 entertainment_tech/  # Entertainment-tech correlation examples
│       └── 📁 pokemon_culture/     # Pokemon-culture correlation examples
└── 📁 guides/                      # User guides
    ├── 📄 demo-git-commit-guide.md # Git commit guide
    ├── 📄 api_setup_guide.md       # API setup instructions
    └── 📄 deployment_guide.md      # Deployment instructions
```

---

## 🎓 Training & AI

### 🧠 `/training/` - LLM Training Examples
**Purpose**: LLM training datasets, model configurations, and analysis notebooks

```
training/
├── 📁 datasets/                    # Sample training data
│   ├── 📁 conversational/          # Q&A datasets
│   ├── 📁 correlations/            # Correlation-based datasets
│   └── 📁 insights/                # Insight generation datasets
├── 📁 model_configs/               # Training configuration examples
│   ├── 📁 local/                   # Local model configurations
│   ├── 📁 openai/                  # OpenAI model configurations
│   └── 📁 embeddings/              # Embedding model configurations
└── 📁 notebooks/                   # Jupyter analysis examples
    ├── 📁 correlation_analysis/    # Correlation analysis notebooks
    ├── 📁 data_exploration/        # Data exploration notebooks
    └── 📁 model_evaluation/        # Model evaluation notebooks
```

---

## 🔧 Utility Directories

### 📜 `/scripts/` - Utility Scripts
**Purpose**: Automation scripts and utilities

```
scripts/
├── 📄 generate_folder_structure.ps1 # PowerShell folder generation
├── 📄 generate_structure.bat       # Batch folder generation
├── 📄 setup_environment.sh         # Environment setup script
├── 📄 deploy.sh                    # Deployment script
└── 📄 backup_data.py               # Data backup utility
```

### 📋 `/templates/` - Code Templates
**Purpose**: Boilerplate code and templates

```
templates/
├── 📁 api_clients/                 # API client templates
├── 📁 services/                    # Service templates
├── 📁 tests/                       # Test templates
└── 📁 workflows/                   # Workflow templates
```

### 📊 `/logs/` - Application Logs
**Purpose**: Application logging and monitoring

```
logs/
├── 📁 applications/                # Application logs
├── 📁 errors/                      # Error logs
├── 📁 performance/                 # Performance logs
└── 📁 audit/                       # Audit logs
```

---

## 🎯 File Placement Guidelines

### 📋 Where to Place New Files

| File Type | Location | Examples |
|-----------|----------|----------|
| **API Client** | `packages/shared_core/api/clients/{api_name}/` | `spotify_client.py`, `github_client.py` |
| **Data Model** | `packages/shared_core/models/` | `music.py`, `weather.py` |
| **Service Logic** | `services/{service_category}/{service_name}/` | `correlation_analyzer/main.py` |
| **Database Migration** | `packages/shared_core/database/migrations/` | `001_create_music_tables.py` |
| **Prefect Flow** | `flows/{flow_name}/` | `data_ingestion_flow/main.py` |
| **Test File** | `development/testing/{test_type}/` | `unit/test_spotify_client.py` |
| **Configuration** | `infrastructure/environments/{env}/config/` | `development/config/database.yml` |
| **Documentation** | `resources/docs/` | `api_integration_guide.md` |
| **Raw Data** | `data/raw/{api_name}/` | `spotify/tracks_2024_01.json` |
| **Processed Data** | `data/processed/{domain}/` | `music/processed_tracks.parquet` |
| **Correlation Results** | `data/correlations/` | `daily/music_weather_correlation.json` |
| **Visualization** | `data/visualizations/{type}/` | `charts/correlation_heatmap.png` |
| **LLM Training Data** | `data/llm_training/{format}/` | `conversational/music_qa_dataset.jsonl` |

### 📝 Naming Conventions

| Item | Convention | Example |
|------|------------|---------|
| **Files** | `snake_case.py` | `spotify_client.py` |
| **Directories** | `snake_case` | `correlation_analyzer` |
| **Classes** | `PascalCase` | `SpotifyClient` |
| **Functions** | `snake_case` | `analyze_correlation` |
| **Constants** | `UPPER_SNAKE_CASE` | `MAX_RETRY_ATTEMPTS` |
| **Environment Variables** | `UPPER_SNAKE_CASE` | `SPOTIFY_CLIENT_ID` |
| **Database Tables** | `snake_case` | `music_tracks` |
| **API Endpoints** | `kebab-case` | `/api/music-correlations` |

---

## 🔍 Quick Reference

### 📍 Common Development Tasks

| Task | Go To | Command |
|------|-------|---------|
| **Add new API client** | `packages/shared_core/api/clients/` | Create new folder + client.py |
| **Add data model** | `packages/shared_core/models/` | Create domain-specific .py file |
| **Create new service** | `services/{category}/` | Create service folder + main.py |
| **Add database migration** | `packages/shared_core/database/migrations/` | `alembic revision --autogenerate` |
| **Write unit test** | `development/testing/unit/` | Create test_*.py file |
| **Add workflow** | `flows/` | Create flow folder + main.py |
| **Add documentation** | `resources/docs/` | Create .md file |
| **Store raw data** | `data/raw/{api_name}/` | Save JSON/CSV files |
| **Generate insight** | `data/insights/` | Save analysis results |
| **Create visualization** | `data/visualizations/` | Save charts/graphs |

### 🚀 Next Steps

1. **Phase 0**: Set up basic folder structure ✅
2. **Phase 1**: Create API clients in `packages/shared_core/api/clients/`
3. **Phase 2**: Build data collection services in `services/data_collection/`
4. **Phase 3**: Implement processing services in `services/data_processing/`
5. **Phase 4**: Create correlation analysis in `services/insights/`
6. **Phase 5**: Build visualization services in `services/delivery/`
7. **Phase 6**: Implement LLM integration in `services/llm_integration/`

---

**This folder structure supports**:
- ✅ **Scalable microservices architecture**
- ✅ **Clear separation of concerns**
- ✅ **Easy navigation and maintenance**
- ✅ **Comprehensive testing strategy**
- ✅ **Enterprise-grade organization**
- ✅ **Consistent development patterns**

For questions about file placement or folder structure, refer to this guide or create an issue in the project repository.
