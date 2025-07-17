# Repository Structure Guide

**Process Documentation - Data Centralization Platform**

*Version: 3.0*  
*Created: July 17, 2025*  
*Last Updated: July 17, 2025*  
*Status: Current Implementation*

> **Note**: Virtual environments (.venv) exist throughout the repository but are excluded from this structure outline for clarity.

## Root Level

Contains core project configuration and entry points:

- **`.vscode/`** - Visual Studio Code workspace settings and configuration
- **`.pytest_cache/`** - PyTest cache directory (excluded from version control)
- **Project files** - `.gitignore`, `README.md`, `pyproject.toml`, `requirements.txt`, `pytest.ini`, `.flake8`, `.prettierignore`
- **`validate_setup.py`** - Environment validation script

---

## 🎯 Project Overview

The **Data Centralization Platform** is a comprehensive system that transforms scattered public APIs into unified, LLM-ready knowledge while surfacing actionable insights through sophisticated correlation analysis and interactive visualizations.

### Core Mission
- **Multi-Domain Data Integration**: 6+ diverse APIs → unified PostgreSQL database
- **Cross-Domain Correlation Discovery**: Statistical analysis revealing unexpected relationships
- **LLM-Powered Intelligence**: Natural language interaction with complex data relationships
- **Production-Ready Architecture**: Microservices, containerization, CI/CD, comprehensive testing

---

## 🏗️ Architecture Overview

### System Components
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   External APIs │ -> │  Data Pipeline  │ -> │  Intelligence   │
│                 │    │                 │    │    Layer        │
│ • Spotify       │    │ • Collection    │    │ • Correlations  │
│ • GitHub        │    │ • Processing    │    │ • LLM Search    │
│ • TMDB          │    │ • Linking       │    │ • Visualizations│
│ • Weather       │    │ • Analysis      │    │ • Notion Export │
│ • Pokémon       │    │ • Storage       │    │ • API Gateway   │
│ • MusicBrainz   │    │                 │    │                 │
│ • Notion        │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Technology Stack
- **API Clients**: Python + httpx + pydantic
- **Data Processing**: pandas + SQLModel + SciPy
- **Database**: PostgreSQL + pgvector
- **LLM Services**: LangChain + Ollama + OpenAI
- **Visualization**: Plotly + Dash + D3.js
- **Delivery**: Notion SDK + FastAPI

---

## ☁️ `/azure` - Cloud Infrastructure

Azure deployment templates and cloud infrastructure configurations:

- **Infrastructure as Code** - Bicep and ARM templates for Azure resources
- **Environment configurations** - Development, staging, and production Azure resources
- **Container orchestration** - Azure Container Apps and Container Registry configurations
- **Database provisioning** - PostgreSQL and storage account templates
- **Monitoring setup** - Application Insights and logging configurations

---

## 🔧 `/development` - Development Tools & Testing

Development utilities, testing frameworks, and debugging tools:

- **`/examples`** - API usage examples and integration patterns
- **`/testing`** - Comprehensive testing infrastructure
  - **`/functional`** - End-to-end functional tests
  - **`/integration`** - Cross-service integration tests  
  - **`/unit`** - Individual component unit tests
- **`/tools`** - Development support tools
  - **`/debug_scripts`** - Debugging and troubleshooting utilities
  - **`/postman`** - API testing collections and archives

---

## 📊 `/data` - Data Storage & Processing

Centralized data storage organized by processing stage:

#### **`/raw/`** - Raw API Data
- **`/spotify/`** - Spotify API raw responses
- **`/github/`** - GitHub API raw data
- **`/tmdb/`** - TMDB API raw data
- **`/weather/`** - Weather API raw data
- **`/pokemon/`** - Pokémon API raw data
- **`/musicbrainz/`** - MusicBrainz API raw data
- **`/notion/`** - Notion API raw data

#### **`/processed/`** - Cleaned & Standardized Data
- **`/music/`** - Processed music data
- **`/entertainment/`** - Processed entertainment data
- **`/weather/`** - Processed weather data
- **`/pokemon/`** - Processed gaming data
- **`/github/`** - Processed development data

#### **`/correlations/`** - Correlation Analysis Results
- **`/daily/`** - Daily correlation outputs
- **`/weekly/`** - Weekly correlation summaries
- **`/historical/`** - Historical correlation data

#### **`/embeddings/`** - Vector Embeddings
- **`/text/`** - Text embeddings
- **`/entity/`** - Entity embeddings
- **`/correlation/`** - Correlation embeddings

#### **`/visualizations/`** - Generated Charts and Graphs
- **`/charts/`** - Statistical charts
- **`/maps/`** - Geographic visualizations
- **`/heatmaps/`** - Correlation heatmaps

#### **`/insights/`** - Generated Insights and Reports
- **`/reports/`** - Automated reports
- **`/alerts/`** - Correlation alerts
- **`/summaries/`** - Data summaries

---

## ⚡ `/flows` - Workflow Orchestration

Prefect-based workflow orchestration and scheduling:

#### **`/data_ingestion_flow/`** - Data Collection Workflows
- **Prefect flow definitions** - DAG-based data collection
- **Task definitions** - Individual data collection tasks
- **Configuration** - Flow-specific configuration

#### **`/processing_flow/`** - ETL and Analysis Pipeline
- **Data transformation workflows** - ETL processing
- **Cross-domain correlation discovery** - Statistical analysis
- **Processing orchestration** - Complex multi-step operations

#### **`/correlation_flow/`** - Daily Correlation Analysis
- **Automated correlation discovery** - Daily statistical analysis
- **Significance testing** - Statistical validation
- **Alert generation** - Correlation alerts

#### **`/insight_generation_flow/`** - Automated Reporting
- **Report generation** - Automated insight reports
- **Visualization creation** - Chart and graph generation
- **Notion export** - Automated Notion page creation

---

## 🔧 `/functions` - Utility Functions

Utility functions and helper scripts:

- **General-purpose utilities** - Data processing helpers
- **API integration utilities** - External API helpers
- **Statistical functions** - Correlation analysis utilities
- **Visualization helpers** - Chart generation utilities

---

## 🏗️ `/infrastructure` - Deployment & DevOps

Deployment pipelines and environment management:

- **`/environments/`** - Environment-specific configurations
  - **`/development/`** - Development environment settings
  - **`/staging/`** - Staging environment configuration
  - **`/production/`** - Production environment settings
- **`/github_actions/`** - GitHub Actions workflows for CI/CD
- **`/docker/`** - Docker configurations
- **`/kubernetes/`** - Kubernetes manifests for container orchestration

---

## 📦 `/packages` - Shared Python Libraries

Reusable Python packages installed across multiple services:

#### **`/shared_core/`** - Core Shared Package
Common utilities and API clients used by all services:

- **`/api/`** - API client implementations
  - **`/clients/`** - External API clients
    - **`/spotify/`** - Spotify REST API client
    - **`/github/`** - GitHub GraphQL API client
    - **`/tmdb/`** - TMDB REST API client
    - **`/weather/`** - Weather API client
    - **`/pokemon/`** - Pokémon API client
    - **`/musicbrainz/`** - MusicBrainz API client
    - **`/notion/`** - Notion API client
  - **`/graphql/`** - GraphQL utilities and helpers

- **`/models/`** - Pydantic data models
  - **`music.py`** - Music domain models
  - **`entertainment.py`** - Entertainment domain models
  - **`weather.py`** - Weather domain models
  - **`pokemon.py`** - Gaming/pop culture models
  - **`github.py`** - Development domain models
  - **`correlation.py`** - Statistical analysis models

- **`/config/`** - Configuration management
  - **`base_client.py`** - Base API client configuration
  - **`logging_config.py`** - Logging configuration
  - **`unified_environment_loader.py`** - Environment variables

- **`/utils/`** - Utility functions
  - **`centralized_logging.py`** - Logging utilities
  - **`startup.py`** - Application startup helpers
  - **`/statistical/`** - Statistical analysis utilities
  - **`/embedding/`** - Vector embedding utilities
  - **`/geographic/`** - Location-based utilities
  - **`/temporal/`** - Time-based utilities

- **`/database/`** - Database management
  - **`/models/`** - SQLModel database models
  - **`/migrations/`** - Alembic database migrations
  - **`/connection/`** - Database connection management

- **`/helper/`** - Helper functions and utilities
  - **`graphql_loader.py`** - GraphQL query loading

#### **`/workflows/`** - Workflow-Specific Package
Business logic and workflow implementations:

- **`/data_fusion/`** - Cross-domain data linking
- **`/knowledge_extraction/`** - Entity relationship mapping
- **`/training_prep/`** - LLM dataset formatting

---

## 📚 `/resources` - Non-Code Project Assets

Documentation, templates, and data assets supporting the overall project:

#### **`/bugs`** - Issue Tracking
- **Bug reports** - Documented issues and their resolutions
- **Feature requests** - Enhancement proposals and specifications

#### **`/docs`** - Project Documentation
- **`/archive`** - Historical documentation and deprecated guides
- **`/development`** - Development process documentation
  - **`/feature-planning`** - Feature planning templates and examples
  - **`/implementation`** - Implementation guides and examples
  - **`/testing`** - Testing strategies and methodologies
- **`/processes`** - Process documentation and workflows
- **`/technical`** - Technical documentation and architecture guides
- **`/user-guides`** - End-user documentation and guides

#### **`/docs-archive`** - Legacy Documentation
- **Historical guides** - Deprecated documentation for reference
- **Implementation archives** - Completed implementation documentation
- **Source documentation** - Original source code documentation

#### **`/sample`** - Test & Development Data
- **Sample data files** - Test fixtures and sample datasets
- **Mock data** - Development and testing data

#### **`/standards`** - Development Standards
- **Coding standards** - Code style and formatting guidelines
- **Color palettes** - UI/UX design standards
- **Region codes** - Standardized location and regional data

---

## 🌐 `/web` - Web Interface Components

Static web assets and customer-facing interfaces:

- **`/budget-doc`** - Budget document generation tools and templates
- **`/questionnaire`** - Client questionnaire interfaces and forms with supporting images and testing versions
- **`/ref`** - Reference materials and supporting documentation

---

## 🔧 **Additional Development Support**

#### **`/infrastructure`** - CI/CD & Deployment Orchestration
- **Environment configurations** - Development, staging, and production settings
- **Deployment pipelines** - Azure DevOps and GitHub Actions workflows
- **Kubernetes manifests** - Container orchestration configurations

#### **`/logs`** - Centralized Logging
- **Function logs** - Centralized log storage for all functions
- **System logs** - Application and system-level logging
- **Archive logs** - Historical log retention

#### **`/powershell`** - PowerShell Automation
- **PowerShell training materials** - Learning resources and command references
- **Development tools** - PowerShell-based development utilities
- **Git integration tools** - Source control automation scripts

#### **`/scripts`** - Utility Scripts
- **General-purpose automation** - Development and maintenance scripts
- **Deployment scripts** - Infrastructure and application deployment
- **Utility functions** - Common operational tasks

#### **`/server`** - Web Server Components
- **Flask applications** - Web service implementations
- **API endpoints** - Specialized web functionality
- **Static assets** - Web server resources

#### **`/templates`** - Development Templates
- **Project templates** - Standardized project structure templates
- **Function templates** - Azure Function project templates with complete structure
- **Infrastructure templates** - Bicep and ARM templates for common resources

---

## Key Integration Points

### **Package-Based Architecture**
Services import shared functionality via Python packages, eliminating path manipulation and enabling clean, maintainable code. Each SaaS provider follows a consistent `config/` and `functions/` pattern within the shared package structure.

### **Environment-Driven Configuration**
All configuration (API keys, database connections, Monday.com IDs) managed through environment variables for security and flexibility. Hardcoded values have been replaced with environment-based configuration classes.

### **Service Isolation with Shared Infrastructure**
Each service is independently deployable while leveraging shared Azure resources (databases, storage, registries). Services are organized by business domain for logical grouping.

### **Comprehensive API Integration**
Monday.com integration includes extensive GraphQL query library organized by functionality (boards, items, connections, etc.) with dedicated folders for application-specific operations and comprehensive item management capabilities.

### **Azure Data Factory Integration**
Complete data processing infrastructure with pipelines, datasets, triggers, and integration runtimes for comprehensive ETL operations across all connected systems.

### **Automated Deployment**
Individual services have dedicated CI/CD pipelines while shared infrastructure uses centralized deployment templates. Container-based deployment patterns support scalable, isolated execution.

## Full Folder Structure
This section contains the complete folder structure of the js-codebase repository, excluding virtual environments, cache directories, and other generated files.

Last updated: July 16, 2025

## Root Structure

```
js-codebase/
|-- .vscode/
|-- app/
|   |-- .vscode/
|   |-- archive/
|   |-- docs/
|   +-- environments/
|       |-- dev/
|       |   +-- JS-dashboard-sources/
|       |       |-- .vscode/
|       |       |-- Assets/
|       |       |   +-- Images/
|       |       |-- Connections/
|       |       |-- DataSources/
|       |       |-- Entropy/
|       |       |-- Other/
|       |       |   |-- References/
|       |       |   +-- Src/
|       |       |       +-- Components/
|       |       |-- pkgs/
|       |       |   |-- TableDefinitions/
|       |       |   +-- Wadl/
|       |       +-- Src/
|       |           |-- Components/
|       |           +-- EditorState/
|       |-- dev-Marc/
|       |   +-- JS-dashboard-sources/
|       |       |-- Assets/
|       |       |   +-- Images/
|       |       |-- Connections/
|       |       |-- DataSources/
|       |       |-- Entropy/
|       |       |-- Other/
|       |       |   |-- References/
|       |       |   +-- Src/
|       |       |       +-- Components/
|       |       |-- pkgs/
|       |       |   |-- TableDefinitions/
|       |       |   +-- Wadl/
|       |       +-- Src/
|       |           |-- Components/
|       |           +-- EditorState/
|       |-- production/
|       +-- staging/
|           +-- JS-dashboard-sources/
|               |-- Assets/
|               |-- Connections/
|               |-- DataSources/
|               |-- Entropy/
|               |-- Other/
|               |   |-- References/
|               |   +-- Src/
|               |       +-- Components/
|               |-- pkgs/
|               |   |-- TableDefinitions/
|               |   +-- Wadl/
|               +-- Src/
|                   |-- Components/
|                   +-- EditorState/
|-- azure/
|   |-- .vscode/
|   |-- containers/
|   |-- deployments/
|   |-- functions/
|   |-- scripts/
|   +-- shared/
|-- dataflow/
|-- dataset/
|-- development/
|   |-- examples/
|   |   |-- api_usage/
|   |   +-- integration_patterns/
|   |-- testing/
|   |   |-- functional/
|   |   |-- integration/
|   |   |-- jobe_shared_test_package/
|   |   |   +-- jobe_shared_test/
|   |   |       +-- api/
|   |   |           |-- helper/
|   |   |           +-- saas/
|   |   |               +-- monday/
|   |   |                   +-- graphql/
|   |   |                       |-- boards/
|   |   |                       |-- config/
|   |   |                       +-- items/
|   |   |                           +-- gather_specific_item_details/
|   |   +-- unit/
|   +-- tools/
|       |-- debug_scripts/
|       +-- postman/
|           |-- archive/
|           +-- collections/
|-- factory/
|-- functions/
|   |-- archive/
|   |   |-- create_cloud_project/
|   |   |   |-- .github/
|   |   |   |   +-- workflows/
|   |   |   |-- .vscode/
|   |   |   |-- app/
|   |   |   |   |-- config/
|   |   |   |   |-- core/
|   |   |   |   |-- logs/
|   |   |   |   +-- src/
|   |   |   |       |-- api/
|   |   |   |       |-- functions/
|   |   |   |       +-- utils/
|   |   |   |-- config/
|   |   |   |-- docker/
|   |   |   |-- docs/
|   |   |   |-- infrastructure/
|   |   |   |   |-- bicep/
|   |   |   |   +-- terraform/
|   |   |   |-- scripts/
|   |   |   +-- tests/
|   |   |-- financial_tools/
|   |   |   |-- pricing_ss_extractor/
|   |   |   |   |-- .github/
|   |   |   |   |   +-- workflows/
|   |   |   |   |-- .vscode/
|   |   |   |   |-- app/
|   |   |   |   |   |-- config/
|   |   |   |   |   |-- core/
|   |   |   |   |   |-- logs/
|   |   |   |   |   +-- src/
|   |   |   |   |       |-- api/
|   |   |   |   |       |-- functions/
|   |   |   |   |       +-- utils/
|   |   |   |   |-- config/
|   |   |   |   |-- docker/
|   |   |   |   |-- docs/
|   |   |   |   |-- infrastructure/
|   |   |   |   |   |-- bicep/
|   |   |   |   |   +-- terraform/
|   |   |   |   |-- scripts/
|   |   |   |   +-- tests/
|   |   |   +-- vistage_financial/
|   |   |       |-- .github/
|   |   |       |   +-- workflows/
|   |   |       |-- .vscode/
|   |   |       |-- app/
|   |   |       |   |-- config/
|   |   |       |   |-- core/
|   |   |       |   |-- logs/
|   |   |       |   +-- src/
|   |   |       |       |-- api/
|   |   |       |       |-- functions/
|   |   |       |       +-- utils/
|   |   |       |-- archive/
|   |   |       |   |-- forms_vistage_financial/
|   |   |       |   |   |-- format/
|   |   |       |   |   |-- function/
|   |   |       |   |   |-- mutations/
|   |   |       |   |   |-- queries/
|   |   |       |   |   +-- raw data/
|   |   |       |   +-- ref/
|   |   |       |-- config/
|   |   |       |-- docker/
|   |   |       |-- docs/
|   |   |       |-- infrastructure/
|   |   |       |   |-- bicep/
|   |   |       |   +-- terraform/
|   |   |       |-- scripts/
|   |   |       +-- tests/
|   |   +-- monday_tools/
|   |       |-- auto_connector/
|   |       |   |-- .github/
|   |       |   |   +-- workflows/
|   |       |   |-- .vscode/
|   |       |   |-- app/
|   |       |   |   |-- config/
|   |       |   |   |-- core/
|   |       |   |   |-- logs/
|   |       |   |   +-- src/
|   |       |   |       |-- api/
|   |       |   |       |-- functions/
|   |       |   |       +-- utils/
|   |       |   |-- config/
|   |       |   |-- docker/
|   |       |   |-- docs/
|   |       |   |-- infrastructure/
|   |       |   |   |-- bicep/
|   |       |   |   +-- terraform/
|   |       |   |-- scripts/
|   |       |   +-- tests/
|   |       |-- lutron_lighting_sync/
|   |       |   |-- .github/
|   |       |   |   +-- workflows/
|   |       |   |-- .vscode/
|   |       |   |-- app/
|   |       |   |   |-- config/
|   |       |   |   |-- core/
|   |       |   |   |-- logs/
|   |       |   |   +-- src/
|   |       |   |       |-- api/
|   |       |   |       |-- functions/
|   |       |   |       +-- utils/
|   |       |   |-- config/
|   |       |   |-- docker/
|   |       |   |-- docs/
|   |       |   |-- infrastructure/
|   |       |   |   |-- bicep/
|   |       |   |   +-- terraform/
|   |       |   |-- scripts/
|   |       |   +-- tests/
|   |       |-- populate_project_numbers/
|   |       |-- product_add_request/
|   |       |   |-- .github/
|   |       |   |   +-- workflows/
|   |       |   |-- .vscode/
|   |       |   |-- app/
|   |       |   |   |-- config/
|   |       |   |   |-- core/
|   |       |   |   |-- logs/
|   |       |   |   +-- src/
|   |       |   |       |-- api/
|   |       |   |       |-- functions/
|   |       |   |       +-- utils/
|   |       |   |-- config/
|   |       |   |-- docker/
|   |       |   |-- docs/
|   |       |   |-- infrastructure/
|   |       |   |   |-- bicep/
|   |       |   |   +-- terraform/
|   |       |   |-- scripts/
|   |       |   +-- tests/
|   |       |-- sync_cloud_project_number/
|   |       |   |-- .github/
|   |       |   |   +-- workflows/
|   |       |   |-- .vscode/
|   |       |   |-- app/
|   |       |   |   |-- config/
|   |       |   |   |-- core/
|   |       |   |   |-- logs/
|   |       |   |   +-- src/
|   |       |   |       |-- api/
|   |       |   |       |-- functions/
|   |       |   |       +-- utils/
|   |       |   |-- config/
|   |       |   |-- docker/
|   |       |   |-- docs/
|   |       |   |-- infrastructure/
|   |       |   |   |-- bicep/
|   |       |   |   +-- terraform/
|   |       |   |-- scripts/
|   |       |   +-- tests/
|   |       |-- template_task_creator/
|   |       |   |-- .github/
|   |       |   |   +-- workflows/
|   |       |   |-- .vscode/
|   |       |   |-- app/
|   |       |   |   |-- config/
|   |       |   |   |-- core/
|   |       |   |   |-- logs/
|   |       |   |   +-- src/
|   |       |   |       |-- api/
|   |       |   |       |-- functions/
|   |       |   |       +-- utils/
|   |       |   |-- config/
|   |       |   |-- docker/
|   |       |   |-- docs/
|   |       |   |-- infrastructure/
|   |       |   |   |-- bicep/
|   |       |   |   +-- terraform/
|   |       |   |-- scripts/
|   |       |   +-- tests/
|   |       +-- watchguard_renewal_board/
|   |           |-- .github/
|   |           |   +-- workflows/
|   |           |-- .vscode/
|   |           |-- app/
|   |           |   |-- config/
|   |           |   |-- core/
|   |           |   |-- logs/
|   |           |   +-- src/
|   |           |       |-- api/
|   |           |       |-- functions/
|   |           |       +-- utils/
|   |           |-- config/
|   |           |-- docker/
|   |           |-- docs/
|   |           |-- infrastructure/
|   |           |   |-- bicep/
|   |           |   +-- terraform/
|   |           |-- scripts/
|   |           +-- tests/
|   |-- crm_to_blob_storage/
|   |   |-- .github/
|   |   |   +-- workflows/
|   |   |-- .vscode/
|   |   |-- app/
|   |   |   |-- core/
|   |   |   +-- src/
|   |   |       +-- functions/
|   |   |           |-- blob_storage/
|   |   |           |-- format/
|   |   |           |   |-- crm/
|   |   |           |   |-- design/
|   |   |           |   +-- update_logs/
|   |   |           |       |-- crm/
|   |   |           |       +-- design/
|   |   |           +-- gather/
|   |   |-- docker/
|   |   |-- scripts/
|   |   +-- tests/
|   |-- detail_services/
|   |-- monday_tools/
|   |   |-- archive_deal/
|   |   |   |-- .github/
|   |   |   |-- app/
|   |   |   |   |-- config/
|   |   |   |   |-- core/
|   |   |   |   +-- src/
|   |   |   |-- infrastructure/
|   |   |   |   +-- bicep/
|   |   |   |       +-- parameters/
|   |   |   |-- models/
|   |   |   +-- tests/
|   |   |-- create_item/
|   |   |   |-- .github/
|   |   |   |-- app/
|   |   |   |   |-- config/
|   |   |   |   |-- core/
|   |   |   |   +-- src/
|   |   |   |-- infrastructure/
|   |   |   |   +-- parameters/
|   |   |   |-- models/
|   |   |   +-- tests/
|   |   +-- edit_item/
|   |       |-- .github/
|   |       |-- app/
|   |       |   |-- config/
|   |       |   |-- core/
|   |       |   +-- src/
|   |       |-- infrastructure/
|   |       |   +-- parameters/
|   |       |-- models/
|   |       +-- tests/
|   +-- workspace_creator/
|       |-- .github/
|       |   +-- workflows/
|       |-- .mypy_cache/
|       |   +-- 3.12/
|       |       |-- _typeshed/
|       |       |-- app/
|       |       |   |-- config/
|       |       |   |-- core/
|       |       |   +-- src/
|       |       |       +-- functions/
|       |       |           |-- check/
|       |       |           +-- create/
|       |       |-- collections/
|       |       |-- email/
|       |       |-- importlib/
|       |       |   |-- metadata/
|       |       |   +-- resources/
|       |       |-- logging/
|       |       |-- models/
|       |       |-- os/
|       |       |-- sys/
|       |       +-- zipfile/
|       |           +-- _path/
|       |-- app/
|       |   |-- config/
|       |   |-- core/
|       |   +-- src/
|       |       +-- functions/
|       |           |-- check/
|       |           +-- create/
|       |-- docker/
|       |-- models/
|       +-- tests/
|-- infrastructure/
|   |-- environments/
|   |   |-- development/
|   |   |   |-- config/
|   |   |   +-- secrets/
|   |   |-- production/
|   |   |   |-- config/
|   |   |   +-- secrets/
|   |   |-- shared/
|   |   |   |-- config/
|   |   |   +-- secrets/
|   |   +-- staging/
|   |       |-- config/
|   |       +-- secrets/
|   |-- github_actions/
|   |-- kubernetes/
|   |   |-- deployments/
|   |   |-- namespaces/
|   |   +-- services/
|   +-- pipelines/
|       |-- cd/
|       |-- ci/
|       +-- templates/
|-- integrationRuntime/
|-- ITDBDataFactory/
|   |-- globalParameters/
|   +-- linkedTemplates/
|-- jobs/
|-- linkedService/
|-- logs/
|   |-- archive/
|   |-- errors/
|   |-- functions/
|   +-- testing/
|-- packages/
|   |-- jobe_shared/
|   |   |-- .vscode/
|   |   |-- jobe_shared/
|   |   |   |-- .vscode/
|   |   |   |-- api/
|   |   |   |   |-- azure/
|   |   |   |   |-- helper/
|   |   |   |   |-- msoft_graph/
|   |   |   |   |   |-- config/
|   |   |   |   |   +-- functions/
|   |   |   |   |       |-- mutations/
|   |   |   |   |       |-- parse/
|   |   |   |   |       +-- queries/
|   |   |   |   +-- saas/
|   |   |   |       |-- cloud/
|   |   |   |       |   |-- config/
|   |   |   |       |   |-- parse/
|   |   |   |       |   +-- queries/
|   |   |   |       |-- fastfield/
|   |   |   |       |   |-- mutations/
|   |   |   |       |   |-- parse/
|   |   |   |       |   +-- queries/
|   |   |   |       |-- harvest/
|   |   |   |       |   |-- mutations/
|   |   |   |       |   |-- parse/
|   |   |   |       |   +-- queries/
|   |   |   |       |-- monday/
|   |   |   |       |   |-- config/
|   |   |   |       |   |-- graphql/
|   |   |   |       |   |   |-- activity_logs/
|   |   |   |       |   |   |-- app_specific/
|   |   |   |       |   |   |   |-- auto_connector/
|   |   |   |       |   |   |   +-- dataverse_sync/
|   |   |   |       |   |   |-- boards/
|   |   |   |       |   |   |-- columns/
|   |   |   |       |   |   |-- connections_links/
|   |   |   |       |   |   |-- crm_sql_sync/
|   |   |   |       |   |   |-- docs/
|   |   |   |       |   |   |-- emails_activities/
|   |   |   |       |   |   |-- folders/
|   |   |   |       |   |   |-- groups/
|   |   |   |       |   |   |-- items/
|   |   |   |       |   |   |   |-- edit_specific_item_type/
|   |   |   |       |   |   |   |-- filter_by_column_type/
|   |   |   |       |   |   |   |-- gather_specific_item_details/
|   |   |   |       |   |   |   |-- get_specific_item_type_details/
|   |   |   |       |   |   |   +-- update_specific_items/
|   |   |   |       |   |   |-- notifications/
|   |   |   |       |   |   |-- subitems/
|   |   |   |       |   |   |-- tags/
|   |   |   |       |   |   |-- teams/
|   |   |   |       |   |   |-- temp_testing/
|   |   |   |       |   |   |   +-- legacy/
|   |   |   |       |   |   |-- updates_comments/
|   |   |   |       |   |   |-- users/
|   |   |   |       |   |   |-- utilities_misc/
|   |   |   |       |   |   |-- views/
|   |   |   |       |   |   |-- webhooks/
|   |   |   |       |   |   +-- workspaces/
|   |   |   |       |   |-- helper/
|   |   |   |       |   |-- mutations/
|   |   |   |       |   |-- mutations_LEGACY/
|   |   |   |       |   |-- parse/
|   |   |   |       |   |-- queries/
|   |   |   |       |   +-- queries_LEGACY/
|   |   |   |       |-- si/
|   |   |   |       +-- zendesk/
|   |   |   |-- config/
|   |   |   |-- models/
|   |   |   |-- sql/
|   |   |   |   |-- migrations/
|   |   |   |   |-- queries/
|   |   |   |   +-- utils/
|   |   |   |-- ui/
|   |   |   +-- utils/
|   |   +-- tests/
|   +-- jobe_workflows/
|       +-- jobe_workflows/
|           |-- crm_sync/
|           +-- workspace_creation/
|-- pipeline/
|-- powershell/
|   |-- .vscode/
|   |-- powershell-training/
|   +-- tools/
|       |-- git/
|       +-- logs/
|-- resources/
|   |-- bugs/
|   |-- docs/
|   |   |-- archive/
|   |   |-- development/
|   |   |   |-- feature-planning/
|   |   |   |   +-- examples/
|   |   |   |-- implementation/
|   |   |   |   +-- examples/
|   |   |   +-- testing/
|   |   |-- processes/
|   |   |-- technical/
|   |   +-- user-guides/
|   |-- docs-archive/
|   |   |-- guides/
|   |   |-- implementation/
|   |   |   +-- complete/
|   |   |-- source/
|   |   |   +-- modules/
|   |   |       +-- queries/
|   |   +-- warp/
|   |-- sample/
|   +-- standards/
|-- scripts/
|-- server/
|-- templates/
|   +-- functions-folderstructure/
|       |-- .github/
|       |   +-- workflows/
|       |-- app/
|       |   |-- config/
|       |   |-- core/
|       |   |-- logs/
|       |   +-- src/
|       |       |-- api/
|       |       |-- functions/
|       |       +-- utils/
|       |-- config/
|       |-- docker/
|       |-- docs/
|       |-- infrastructure/
|       |   |-- bicep/
|       |   +-- terraform/
|       |-- scripts/
|       +-- tests/
|-- trigger/
+-- web/
    |-- budget-doc/
    |-- questionnaire/
    |   |-- qs-imgs/
    |   |   |-- homepage/
    |   |   |-- icons/
    |   |   +-- sideimages/
    |   +-- testing/
    |       |-- questionnaire_v0.1_extracted for testing/
    |       |   +-- version 0.1_extracted for testing/
    |       |       +-- img ref/
    |       |           |-- icons/
    |       |           +-- side images/
    |       +-- questionnaire_v0.2_extracted for testing/
    |           +-- img ref/
    |               |-- controloptionicons/
    |               |-- icons/
    |               +-- side images/
    +-- ref/
```

## Notes

- This structure excludes virtual environments (''.venv''), cache directories (''__pycache__'', ''.pytest_cache''), and other generated files
- Each function directory follows a consistent structure with ''app/'', ''config/'', ''docker/'', ''docs/'', ''infrastructure/'', ''scripts/'', and ''tests/'' subdirectories
- The repository contains extensive Monday.com API integration capabilities in the ''packages/jobe_shared/'' directory


## Usage

To regenerate this structure, run:
```powershell
.\scripts\generate_folder_structure.ps1
```

Or to include individual files:
```powershell
.\scripts\generate_folder_structure.ps1 -IncludeFiles
```

Or to specify a custom output path:
```powershell
.\scripts\generate_folder_structure.ps1 -OutputPath 'js-extracted-folder-structure.md'
```
