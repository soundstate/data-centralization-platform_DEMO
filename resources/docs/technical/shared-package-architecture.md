# Jobe Shared Package

**Technical Documentation - Jobe Systems API Codebase**

*Version: 2.0*  
*Created: June 30, 2025*  
*Last Updated: July 17, 2025*  
*Status: Implemented*

---

## Executive Summary

The Jobe Shared Package (`jobe_shared`) serves as the foundation for the Jobe Systems API, offering standardized utilities, API clients, and configuration management across all Azure Functions and services. This package reduces code duplication and ensures uniform integration with external SaaS providers, Azure services, and internal systems.

  

## Table of Contents

  

- [What It Contains](#what-it-contains)

- [Package Structure](#package-structure)

- [Installation & Setup](#installation--setup)

- [Usage Examples](#usage-examples)

- [API Modules](#api-modules)

- [Configuration Management](#configuration-management)

- [Development Guidelines](#development-guidelines)

- [Technical Details](#technical-details)

  

## What It Contains

  

### Primary Functionality

  

The jobe_shared package provides comprehensive functionality across several categories:

  

**API Integration Libraries:**

- **Azure Services** - Blob Storage and SQL Database clients

- **Microsoft Graph** - SharePoint, Teams, and Planner integration

- **SaaS Providers** - Monday.com, D-Tools, Harvest, FastField, Zendesk APIs

- **Universal Helpers** - GraphQL file loading, error handling, data parsing

  

**Configuration & Environment Management:**

- **Environment-Driven Configuration** - All IDs and secrets via environment variables

- **Unified Configuration Loading** - Consistent configuration patterns across services

- **Multi-Environment Support** - Development, staging, and production configurations

  

**Shared Utilities:**

- **Program Lifecycle Management** - Standardized startup, logging, and shutdown

- **Data Processing** - Parsing, formatting, and validation utilities

- **User Interface Components** - GUI applications and input handlers

- **Mathematical & Date Utilities** - Common calculation and date manipulation functions

  

## Package Structure

The `jobe_shared` package is organized to house core modules and utilities necessary for API operations across various services.

```
packages/jobe_shared/
├── setup.py                   # Package configuration and dependencies
├── requirements.txt           # Package-specific requirements
├── README.md                  # Documentation template
├── jobe_shared/               # Main package source
│   ├── api/                   # API clients and integrations
│   │   ├── azure/             # Azure service clients
│   │   ├── helper/            # Universal utilities
│   │   ├── msoft_graph/       # Microsoft Graph API integration
│   │   ├── saas/              # SaaS provider integrations
│   ├── config/                # Configuration management
│   ├── models/                # Data models and schemas
│   ├── ui/                    # User interface components
│   └── utils/                 # Shared utilities
└── jobe_shared.egg-info/    # Package metadata
```

The following table outlines the key components of the package:

**Component** | **Description**
------------- | ---------------
`api`         | Contains API clients for integration with Azure, Graph, and SaaS services like Monday.com, D-Tools, etc.
`config`      | Manages configuration and environment settings, utilizes `base_client.py` for client configurations.
`models`      | Data models specific to Azure, D-Tools, etc.
`sql`         | SQL utilities including migrations, optimized queries, and connection management.
`ui`          | GUI applications and input handlers.
`utils`       | Common utilities including API helpers, logging, date manipulation, and startup/shutdown processes.

This structure allows for organized contributions, efficient maintenance, and straightforward integration with Jobe Systems' services.

## Installation & Setup

  

### Package Installation

  

The jobe_shared package is installed as an editable development dependency in Azure Functions:

  

```bash

# In your Azure Function's requirements.txt

-e ../../packages/jobe_shared

```

  

### Environment Configuration

  

Ensure your environment has the required variables configured:

  

```bash

# Monday.com Configuration

MONDAY_API_TOKEN=your_monday_api_token

MONDAY_WORKSPACE_CRM=workspace_id

MONDAY_BOARD_OPPORTUNITY=board_id

  

# Azure Configuration

AZURE_STORAGE_CONNECTION_STRING=connection_string

AZURE_SQL_CONNECTION_STRING=connection_string

  

# D-Tools Configuration

DTOOLS_CLOUD_API_KEY=api_key

DTOOLS_SI_USERNAME=username

DTOOLS_SI_PASSWORD=password

```

  

## Usage Examples

  

### Standardized Program Initialization

  

```python

from jobe_shared.utils.startup import program_start, program_end

  

def main():

    logger = program_start(

        program_name="CRM Sync Service",

        version="1.2.0",

        last_updated="2025-06-20",

        creator="Nathan"

    )

    try:

        logger.info("Starting CRM synchronization process")

        # Your service logic here

        logger.info("CRM synchronization completed successfully")

    except Exception as e:

        logger.error(f"CRM synchronization failed: {str(e)}", exc_info=True)

        raise

    finally:

        program_end(logger, "CRM Sync Service")

  

if __name__ == "__main__":

    main()

```

  

### Monday.com API Integration

  

```python

from jobe_shared.api.saas.monday.config.monday_client import MondayAPIClient

from jobe_shared.config.monday_config import MondayConfig

from jobe_shared.api.helper.graphql_loader import load_graphql_query

  

# Initialize Monday.com client

client = MondayAPIClient(MondayConfig.api_token())

  

# Load GraphQL query from file

query = load_graphql_query('saas/monday/graphql/queries/get_board_items.graphql')

  

# Execute query with environment-driven configuration

board_id = MondayConfig.board_id("opportunity")

response = client.make_request(query, {"board_id": board_id})

```

  

### Azure Blob Storage Operations

  

```python

from jobe_shared.api.azure.blob_client import BlobStorageClient

  

# Initialize blob client

blob_client = BlobStorageClient()

  

# Upload data to blob storage

blob_client.upload_blob(

    container_name="crm-data",

    blob_name="opportunities.json",

    data=json_data

)

  

# Download blob data

data = blob_client.download_blob(

    container_name="crm-data",

    blob_name="opportunities.json"

)

```

  

### D-Tools Cloud Integration

```python
from jobe_shared.api.saas.cloud.queries.get_cloud_projects import get_cloud_projects
from jobe_shared.api.saas.cloud.parse.format_cloud_items import format_cloud_items

# Get D-Tools Cloud projects
projects = get_cloud_projects()

# Format project data for processing
formatted_items = format_cloud_items(projects)
```

### SQL Utilities Usage

```python
from jobe_shared.sql.utils.connection_manager import ConnectionManager
from jobe_shared.sql.queries.base_queries import BaseQueries
from jobe_shared.sql.queries.analytics_queries import AnalyticsQueries

# Initialize connection manager
connection_manager = ConnectionManager()

# Execute base queries
base_queries = BaseQueries(connection_manager)
opportunities = base_queries.get_opportunities()

# Execute analytics queries
analytics_queries = AnalyticsQueries(connection_manager)
metrics = analytics_queries.get_performance_metrics()

# Use optimized search queries
from jobe_shared.sql.queries.search_queries import SearchQueries
search_queries = SearchQueries(connection_manager)
results = search_queries.search_opportunities("project_name")
```

  

## API Modules

  

### Azure Services (`/api/azure/`)

  

**Blob Storage Client** (`blob_client.py`)

- Upload/download blob data

- Container management

- Blob metadata operations

  

**SQL Database Client** (`sql_client.py`)

- Database connection management

- Query execution utilities

- Transaction handling

  

### SQL Utilities (`/sql/`)

**Database Management**

- **Migrations** - Database schema migration scripts
- **Queries** - Optimized SQL queries for analytics, search, and detailed operations
- **Utils** - Connection management and performance monitoring

**Key Components:**

```python
# Connection management
from jobe_shared.sql.utils.connection_manager import ConnectionManager

# Query execution
from jobe_shared.sql.queries.base_queries import BaseQueries
from jobe_shared.sql.queries.analytics_queries import AnalyticsQueries

# Performance monitoring
from jobe_shared.sql.utils.performance_monitor import PerformanceMonitor
```

---

### Microsoft Graph (`/api/msoft_graph/`)

**SharePoint Integration**

- Document library operations
- Site and list management
- File upload/download capabilities

**Teams & Planner Integration**

- Team creation and management
- Planner task operations
- Calendar integration

  

### SaaS Provider APIs (`/api/saas/`)

  

#### Monday.com (`/saas/monday/`)

**Most comprehensive integration with:**

- **Extensive GraphQL Library** - 100+ pre-built queries and mutations

- **Configuration Management** - Environment-driven board and workspace IDs

- **Data Processing** - Specialized formatters for CRM and project data

- **Real-time Operations** - Activity log monitoring and webhook support

  

#### D-Tools Integration (`/saas/cloud/` & `/saas/si/`)

- **Cloud API Client** - Project and item management

- **System Integrator API** - Legacy system integration

- **Data Parsing** - Brand analysis, model counting, and change order processing

  

#### Other SaaS Providers

- **Harvest** (`/saas/harvest/`) - Time tracking and project management

- **FastField** (`/saas/fastfield/`) - Mobile data collection and field operations

- **Zendesk** (`/saas/zendesk/`) - Support ticket management and customer service

  

## Configuration Management

  

### Environment-Driven Configuration

  

All configuration is managed through environment variables, eliminating hardcoded values:

  

```python

from jobe_shared.config.monday_config import MondayConfig

  

# Access configuration values

board_id = MondayConfig.board_id("opportunity")  # Gets MONDAY_BOARD_OPPORTUNITY

workspace_id = MondayConfig.workspace_id("crm")  # Gets MONDAY_WORKSPACE_CRM

api_token = MondayConfig.api_token()              # Gets MONDAY_API_TOKEN

```

  

### Multi-Environment Support

  

Configuration adapts automatically based on environment:

  

```bash

# Development Environment

MONDAY_BOARD_OPPORTUNITY=4493285981

  

# Production Environment  

MONDAY_BOARD_OPPORTUNITY=5123456789

```

  

## Development Guidelines

  

### Import Standards

  

**Use full module path imports** (recommended approach):

  

```python

# Preferred - explicit and clear

from jobe_shared.api.saas.monday.config.monday_client import MondayAPIClient

from jobe_shared.api.helper.graphql_loader import load_graphql_query

from jobe_shared.utils.startup import program_start, program_end

  

# Avoid relative imports

from ....helper.graphql_loader import load_graphql_query  # DON'T DO THIS

```

  

### Adding New Functionality

  

1. **Identify the correct module** - Place new functions in appropriate directories

2. **Follow existing patterns** - Use established naming conventions and structure

3. **Add comprehensive docstrings** - Include Args, Returns, and Examples

4. **Update package version** - Increment version in setup.py for new releases

  

### SaaS Provider Integration Pattern

  

When adding new SaaS providers, follow the established structure:

  

```

api/saas/[provider]/

├── config/                    # Client setup and configuration

│   ├── [provider]_client.py

│   ├── [provider]_config.py

│   └── [provider]_settings.py

└── functions/                 # API operations

    ├── mutations/             # Create, update, delete operations

    ├── queries/               # Data retrieval operations

    └── parse/                 # Data parsing and transformation

```

  

## Technical Details

  

### Dependencies

  

The package includes these core dependencies:

  

```python

install_requires=[

    "python-dotenv>=1.0.0",      # Environment variable management

    "requests>=2.28.2",          # HTTP client library

    "python-dateutil>=2.8.2",    # Date parsing and manipulation

    "azure-storage-blob>=12.19.0", # Azure Blob Storage client

    "azure-functions>=1.18.0",   # Azure Functions runtime

    "azure-keyvault-secrets>=4.7.0", # Azure Key Vault integration

    "azure-identity>=1.15.0",    # Azure authentication

]

```

  

### Package Distribution

  

The package is distributed as an installable Python package:

  

- **Development Mode**: Installed with `-e` flag for live editing

- **Production**: Can be pinned to specific versions for stability

- **Cross-Service Usage**: Single package installation across all Azure Functions

  

### GraphQL Integration

  

Special support for GraphQL operations with file-based query management:

  

```python

# Load GraphQL queries from organized file structure

query = load_graphql_query('saas/monday/graphql/queries/items.graphql')

mutation = load_graphql_query('saas/monday/graphql/mutations/create_workspace.graphql')

```

  

### Error Handling & Logging

  

Standardized error handling and logging across all modules:

  

```python

from jobe_shared.utils.centralized_logging import setup_logging

  

logger = setup_logging("service_name")

logger.info("Operation completed successfully")

logger.error("Operation failed", exc_info=True)

```

  

---

  

## Related Documentation

  

- **[Monday.com API Integration Guide](./jobe_shared/api/saas/monday/README.md)** - Comprehensive Monday.com integration documentation

- **[Environment Configuration Guide](../../infrastructure/environments/README.md)** - Environment variable setup and management

- **[LLM Development Guide](../../resources/docs/archive/js-llm-projectknowledge.md)** - Overall codebase development guidelines

- **[Package Development Best Practices](../../resources/docs/warp/import_approach_comparison.md)** - Import patterns and package development standards

  

---

  

The jobe_shared package serves as the foundation for all Jobe Systems API integrations, providing reliable, maintainable, and consistent functionality across the entire codebase. Its package-based architecture eliminates import issues while ensuring all services benefit from shared improvements and bug fixes.