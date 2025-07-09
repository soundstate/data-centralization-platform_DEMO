## 📁 Project Structure
data-centralization-platform/
├── 📄 README.md
├── 📄 ARCHITECTURE.md
├── 📄 LLM_TRAINING_GUIDE.md
├── 📁 packages/
│   ├── shared_core/                   # Primary shared package
│   │   ├── knowledge_workflows/       # LLM-specific workflows
│   │   │   ├── data_fusion/           # Cross-domain data linking
│   │   │   ├── knowledge_extraction/  # Entity relationship mapping
│   │   │   └── training_prep/         # LLM dataset formatting
│   │   ├── shared_core/               # Core functionality
│   │   │   ├── api/
│   │   │   │   ├── clients/           # API client implementations
│   │   │   │   │   ├── spotify/       # Music streaming data
│   │   │   │   │   ├── musicbrainz/   # Open music database
│   │   │   │   │   ├── weather/       # Environmental data
│   │   │   │   │   ├── tmdb/          # Entertainment metadata
│   │   │   │   │   └── github/        # GraphQL integration demo
│   │   │   │   └── graphql/           # GraphQL utilities
│   │   │   ├── config/                # Environment-driven configuration
│   │   │   ├── models/                # Data models and schemas
│   │   │   ├── ui/                    # UI integration utilities
│   │   │   └── utils/                 # JSON writers, formatters
│   │   └── tests/                     # Package-level tests
│   └── workflows/                     # Business logic workflows
├── 📁 services/
│   ├── data_collection/               # API data gathering services
│   │   ├── music_collector/           # Spotify, MusicBrainz
│   │   ├── entertainment_collector/   # TMDb, cultural events
│   │   ├── environmental_collector/   # Weather, geographic data
│   │   └── reference_collector/       # GitHub, news, events
│   ├── data_processing/               # Data transformation and fusion
│   │   ├── entity_linker/             # Cross-domain entity matching
│   │   ├── knowledge_grapher/         # Relationship mapping
│   │   └── llm_formatter/             # Training data preparation
│   └── api_gateway/                   # Unified data access API
├── 📁 data/                           # Centralized output datasets
│   ├── raw/                           # Original API responses
│   ├── processed/                     # Cleaned and standardized data
│   ├── knowledge_graphs/              # Entity relationship data
│   └── llm_training/                  # Formatted training datasets
├── 📁 ui/
│   ├── power_apps/                    # Power Apps demo files
│   │   └── demo_screenshots/
│   └── dashboard/                     # Web dashboard for data exploration
├── 📁 training/                       # LLM training examples
│   ├── datasets/                      # Sample training data
│   ├── notebooks/                     # Jupyter analysis examples
│   └── model_configs/                 # Training configuration examples
├── 📁 infrastructure/                 # Deployment and containerization
│   ├── azure/                         # Cloud deployment templates
│   ├── docker/                        # Service containers
│   ├── environments/                  # Environment-specific configs
│   │   ├── development/
│   │   ├── staging/
│   │   └── production/
│   └── pipeline/                      # CI/CD automation
├── 📁 development/                    # Development tools and testing
│   ├── examples/
│   │   ├── api_integration/           # How to add new data sources
│   │   └── integration_patterns/      # Common integration examples
│   ├── testing/                       # Comprehensive test suites
│   │   ├── functional/
│   │   ├── integration/
│   │   └── unit/
│   └── tools/                         # Development utilities
│       ├── debug_scripts/
│       └── postman/                   # API testing collections
└── 📁 resources/                      # Documentation and examples
    ├── docs/                          # Technical documentation
    └── examples/
        ├── api_integration/           # Integration examples
        ├── data_exploration/          # Analysis and visualization
        └── knowledge_queries/         # Example AI prompts and responses