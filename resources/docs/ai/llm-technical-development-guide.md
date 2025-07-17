# LLM Technical Development Guide

**Technical Documentation - Jobe Systems API Codebase**

*Version: 2.0*  
*Created: July 7, 2025*  
*Last Updated: July 17, 2025*  
*Status: Current Implementation*

---

## Executive Summary

This document serves as the primary entry point for LLMs working on the Jobe Systems API Codebase. It provides a comprehensive overview of the project architecture, key documentation locations, and implementation patterns to guide new development tasks.

**Essential Reading Order for LLMs:**
1. This document - Overall architecture and documentation map
2. [Environment Implementation Architecture](environment_implementation_architecture.md) - Environment configuration
3. [Centralized Logging Architecture](centralized_logging_architecture.md) - Logging implementation
4. [Repository Structure Guide](../processes/repository-structure-guide.md) - Folder organization
5. [Git Usage Guide](../processes/git-usage-guide.md) - Development workflows

---

## Project Architecture Overview

### Core Purpose
This codebase consolidates data from multiple SaaS platforms (Monday.com, D-Tools, Harvest, FastField, Zendesk, SharePoint) into a centralized Azure environment, providing unified access through Power Apps and Power BI interfaces, with comprehensive M365 workflow integration via Power Automate and extensive Azure Data Factory ETL processing.

### Key Architectural Principles
- **Package-Based Architecture**: Shared code distributed via installable Python packages with consistent patterns
- **Environment-Driven Configuration**: All IDs and secrets managed through environment variables with Azure DevOps Variable Groups
- **Service Isolation by Business Domain**: Services organized by functional area with shared infrastructure
- **API-First Design**: All integrations use RESTful or GraphQL APIs with HTTP endpoints for Power Automate
- **Azure DevOps-Centric**: Primary development platform with CI/CD pipelines and cross-platform support
- **Event-Driven Processing**: Azure Data Factory triggers and Power Automate workflows for comprehensive data orchestration
- **Three-Tier Environments**: Development → Staging → Production with automated promotion
- **Security by Design**: Azure RBAC, Dataverse permissions, and Azure Key Vault integration
- **Comprehensive ETL Infrastructure**: Azure Data Factory with pipelines, datasets, triggers, and integration runtimes

## Source Control and Development Platform

### **Primary Development Platform: Azure DevOps**
- **Repository**: Azure DevOps Git (`https://dev.azure.com/jobe-systems/js-codebase`)
- **CI/CD**: Azure DevOps Pipelines (primary deployment mechanism)
- **Work Items**: Azure DevOps Boards for project management
- **Artifacts**: Azure DevOps Artifacts for package management and distribution
- **Variable Groups**: Centralized environment variable and secret management

### **Backup Strategy**
- **GitHub**: Backup repository maintained as `github-backup` remote
- **Dual Remote Setup**: All local repositories maintain both Azure DevOps and GitHub remotes
- **Cross-Platform Sync**: Consistent codebase access across Windows and Mac platforms

### **Remote Configuration Pattern**:
```bash
# Primary development remote (Azure DevOps)
origin  https://jobe-systems@dev.azure.com/jobe-systems/js-codebase/_git/js-codebase

# Backup remote (GitHub)
github-backup  https://github.com/soundstate/jobe-systems-api-codebase.git
```

## Cross-Platform Development Workflow

### **Platform Strategy**
- **Windows**: Primary development platform with full Azure toolchain
- **Mac**: Secondary access for remote development and testing
- **Azure DevOps**: Single source of truth across all platforms
- **VS Code Settings Sync**: Consistent IDE experience and extensions across platforms

### **Setup Pattern**
```bash
# Both platforms - clone from Azure DevOps
git clone https://jobe-systems@dev.azure.com/jobe-systems/js-codebase/_git/js-codebase
cd js-codebase

# Platform-specific virtual environment activation
# Windows: .venv\Scripts\Activate.ps1
# Mac: source .venv/bin/activate

# Identical package installation pattern on both platforms
pip install -e packages/jobe_shared
pip install -e packages/jobe_workflows
```

### **Development Synchronization**
- **Push from either platform** → **Azure DevOps primary repository**
- **Pull on other platform** → **Continue development seamlessly**
- **Environment variables**: Platform-specific `.env` files with identical structure
- **Cross-platform testing**: Verify functionality works on both Windows and Mac

## Environment Variable Management Strategy

### **Three-Tier Environment Management**

#### **Local Development**
- **`.env` files**: Local development secrets and configuration
- **Location**: Service-specific `.env` files in function directories and shared `.env` in project root
- **Security**: Never commit `.env` files (protected by `.gitignore`)
- **Pattern**: Environment-driven configuration accessed via shared config classes

#### **Azure DevOps Pipelines**
- **Variable Groups**: Centralized secret management in Azure DevOps Library
  - `jobe-systems-secrets`: Sensitive values (API tokens, connection strings) marked as secret
  - `jobe-systems-config`: Non-sensitive configuration values and IDs
  - `jobe-systems-dev`: Development environment specific values
  - `jobe-systems-prod`: Production environment specific values
- **Pipeline Integration**: Reference variable groups in `azure-pipelines.yml` files
- **Environment Promotion**: Separate variable groups enable environment-specific deployments

#### **Azure Functions Runtime**
- **Application Settings**: Environment variables automatically configured during deployment
- **Azure Key Vault**: Production secret management with automatic rotation
- **Bicep Deployment**: Infrastructure as Code manages configuration deployment
- **Service Configuration**: Function-specific environment variables via Bicep templates

### **Configuration Access Pattern**:
```python
# Consistent configuration access across all environments
from jobe_shared.config.monday_config import MondayConfig

# Reads from .env locally, Variable Groups in pipelines, App Settings in Azure
board_id = MondayConfig.board_id("opportunity")
workspace_id = MondayConfig.workspace_id("crm")
api_token = MondayConfig.api_token()
```

## Azure Data Factory Integration Architecture

### **Comprehensive ETL Infrastructure**
**Objective**: Complete data processing and transformation infrastructure for multi-source data integration

### **Data Factory Components**:

#### **Factory Configuration** (`/factory`)
- **ITDBDataFactory.json**: Main Data Factory resource configuration
- **Processing orchestration**: Central control for all ETL operations

#### **Data Transformation Pipelines** (`/dataflow`)
- **Complex data transformation workflows**: Advanced ETL processing for cross-system data
- **Business Development item imports**: Automated processing of BD data
- **Opportunity JSON processing**: Monday.com opportunity data transformation
- **Vendor and manufacturer data transformation**: Supplier data standardization
- **Cross-system data synchronization**: Multi-source data harmonization

#### **Data Structure Definitions** (`/dataset`)
- **Employee Directory structures**: HR data schemas
- **Opportunity data formats**: CRM data structure definitions
- **Vendor/Manufacturer data models**: Supplier information schemas
- **API input/output table definitions**: Standardized data exchange formats

#### **Processing Pipelines** (`/pipeline`)
- **Base_Tables.json**: Foundational data table processing
- **BusDev_Daily.json**: Daily business development data sync
- **Directories_Daily.json**: Directory information updates
- **Request_Daily.json**: Daily request processing workflows
- **Vendors_Daily.json**: Vendor data synchronization

#### **Connection Configurations** (`/linkedService`)
- **Azure SQL Database connections**: Primary data repository connectivity
- **Azure Blob Storage connections**: Data lake and staging area access
- **GitHub integration**: Source control and configuration management
- **FileMaker ITDB integration**: Legacy system connectivity

#### **Automation Triggers** (`/trigger`)
- **Daily3am.json**: Early morning data processing trigger
- **Daily_305am.json, Daily_310am.json, Daily_315am.json**: Staggered processing triggers
- **Event-driven triggers**: Real-time data processing activation

#### **Integration Runtime** (`/integrationRuntime`)
- **FM-ITDB-Integration-Runtime.json**: FileMaker to Azure integration runtime
- **Data processing execution environments**: Scalable processing infrastructure

### **Data Factory Integration Benefits**:
- **Automated ETL Processing**: Scheduled and event-driven data transformation
- **Multi-Source Integration**: Seamless data flow between Monday.com, D-Tools, and Azure
- **Scalable Processing**: Auto-scaling data processing based on volume
- **Data Quality Assurance**: Built-in validation and error handling
- **Real-Time Synchronization**: Near real-time data updates across systems

## Power Apps Development Architecture

### **Power Apps Source Code Management**
**Objective**: Version control and deployment management for Power Apps through source extraction

### **Power Apps Structure** (`/app`):

#### **Development Environment** (`/app/dev`)
- **JS-dashboard-sources/**: Complete extracted Power Apps source code
  - **Assets/**: Power Apps assets and media files
  - **Connections/**: Data source connections and API connectors
  - **DataSources/**: External data source definitions and schemas
  - **Entropy/**: Power Apps metadata and configuration settings
  - **Other/References/**: External references and dependencies
  - **Src/Components/**: Power Apps component source code
  - **pkgs/**: Package definitions and table structures

#### **Environment Management**
- **Development**: Active development with full source extraction
- **Staging**: Pre-production testing environment
- **Archive**: Historical versions and rollback capabilities

### **Power Apps Integration Benefits**:
- **Version Control**: Full source code version control for Power Apps
- **Component Reusability**: Shared components across applications
- **Automated Deployment**: CI/CD integration for Power Apps deployment
- **Source Code Review**: Code review process for Power Apps changes
- **Environment Promotion**: Structured deployment across environments

## Power Automate and M365 Integration

### **HTTP-Triggered Functions for Power Automate**
**Objective**: Expose Python business logic as HTTP endpoints for M365 workflows and automation

### **Implementation Pattern**:
```python
import azure.functions as func
from jobe_shared.api.saas.monday.client import MondayAPIClient
from jobe_shared.config.monday_config import MondayConfig

app = func.FunctionApp()

@app.function_name("service_name_http")
@app.route(route="service-endpoint", auth_level=func.AuthLevel.FUNCTION)
def service_http_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    """HTTP endpoint optimized for Power Automate integration"""
    try:
        # Parse Power Automate request parameters
        req_body = req.get_json()
        
        # Use shared packages for business logic
        monday_client = MondayAPIClient(MondayConfig.api_token())
        result = perform_business_logic(monday_client, req_body)
        
        # Return standardized JSON response for Power Automate consumption
        return func.HttpResponse(
            json.dumps({
                "status": "success",
                "data": result,
                "timestamp": datetime.now().isoformat()
            }),
            status_code=200,
            headers={"Content-Type": "application/json"}
        )
    except Exception as e:
        # Standardized error response for Power Automate error handling
        return func.HttpResponse(
            json.dumps({"status": "error", "message": str(e)}),
            status_code=500,
            headers={"Content-Type": "application/json"}
        )
```

### **Service Exposure Strategy**
**Deployed Function Endpoints for Power Automate Integration**:
- **CRM Sync**: `https://jobe-crm-sync-function.azurewebsites.net/api/crm-sync`
- **Workspace Creator**: `https://jobe-workspace-creator-function.azurewebsites.net/api/create-workspace`
- **Financial Tools**: `https://jobe-financial-tools-function.azurewebsites.net/api/extract-pricing`
- **Auto Connector**: `https://jobe-auto-connector-function.azurewebsites.net/api/connect-items`
- **Lutron Sync**: `https://jobe-lutron-sync-function.azurewebsites.net/api/sync-lighting`
- **Product Add Request**: `https://jobe-product-request-function.azurewebsites.net/api/add-product`
- **Template Task Creator**: `https://jobe-template-creator-function.azurewebsites.net/api/create-tasks`
- **WatchGuard Renewal**: `https://jobe-watchguard-function.azurewebsites.net/api/renewal-board`

### **Power Automate Integration Benefits**:
- **M365 Workflow Triggers**: Initiate Python functions from SharePoint, Outlook, Teams, Power Apps
- **Standardized Responses**: Consistent JSON format for flow consumption and error handling
- **Scalable Processing**: Azure Functions auto-scale based on Power Automate demand
- **Cross-System Integration**: Combine multiple SaaS APIs in single Power Automate flows

## Enhanced Monday.com GraphQL Integration

### **Comprehensive GraphQL Library Structure**
**Objective**: Extensive Monday.com integration with specialized query organization

### **GraphQL Organization** (`/packages/jobe_shared/api/saas/monday/graphql/`):

#### **Core Operations**
- **activity_logs/**: Activity and audit logging queries
- **boards/**: Board management and configuration queries
- **columns/**: Column operations and data type management
- **groups/**: Board group management and organization
- **users/**: User management and permissions
- **workspaces/**: Workspace management and configuration

#### **Advanced Item Operations** (`/items/`)
- **edit_specific_item_type/**: Type-specific item editing and updates
- **filter_by_column_type/**: Advanced column-based filtering and search
- **gather_specific_item_details/**: Detailed item data extraction and analysis
- **get_specific_item_type_details/**: Type-specific item information retrieval
- **update_specific_items/**: Targeted item updates and modifications

#### **Specialized Integration**
- **connections_links/**: Item relationships and cross-board connections
- **crm_sql_sync/**: CRM synchronization and data extraction queries
- **docs/**: Document management and file operations
- **app_specific/**: Business-specific application queries
  - **auto_connector/**: Auto-connection logic queries
  - **dataverse_sync/**: Microsoft Dataverse integration
  - **product_add_request/**: Product addition workflows
  - **template_task_creator/**: Task template automation

### **Monday.com Integration Benefits**:
- **Type-Safe Operations**: Strongly typed GraphQL queries for reliable data access
- **Specialized Workflows**: Purpose-built queries for specific business operations
- **Cross-Board Integration**: Advanced relationship and connection management
- **Comprehensive Coverage**: Complete Monday.com API surface area coverage

## Backend Services Architecture

### **Current Service Portfolio** (`/functions/`):

#### **CRM and Data Synchronization**
- **crm_to_blob_storage/**: Monday.com CRM data synchronization to Azure Blob Storage
- **sync_cloud_project_number/**: D-Tools Cloud project number synchronization

#### **Financial and Business Intelligence**
- **pricing_ss_extractor/**: Pricing spreadsheet extraction and processing
- **vistage_financial/**: Vistage financial data integration and reporting

#### **Monday.com Automation Suite**
- **auto_connector/**: Automatic item linking and relationship management
- **workspace_creator/**: Automated workspace creation for new projects
- **populate_project_numbers/**: Project number automation and management
- **product_add_request/**: Product addition request processing and workflow
- **template_task_creator/**: Automated task template creation and deployment
- **watchguard_renewal_board/**: WatchGuard renewal management and tracking

#### **Integration and Synchronization**
- **create_cloud_project/**: D-Tools Cloud project creation and management
- **lutron_lighting_sync/**: Lutron lighting system synchronization and control

#### **Service Architecture Pattern**:
Each service follows a consistent structure:
```
functions/[service-name]/
├── main.py                    # Service entry point
├── requirements.txt           # Includes: -e ../../packages/jobe_shared
├── app/                       # Application structure
│   ├── config/               # Service-specific configuration
│   ├── core/                 # Core business logic
│   └── src/                  # Source code and functions
├── infrastructure/           # Bicep templates for deployment
│   └── bicep/               # Infrastructure as Code
├── tests/                    # Unit and integration tests
└── .github/workflows/        # CI/CD deployment pipelines
```

## CI/CD Pipeline Architecture

### **Azure DevOps Pipeline Standards**
**Primary Deployment Mechanism**: Azure DevOps Pipelines replace GitHub Actions as primary CI/CD

### **Pipeline Structure Pattern**:
```yaml
# azure-pipelines.yml - Standard pattern for all services
trigger:
  branches:
    include: [main]
  paths:
    include: 
    - functions/[service-name]/*
    - packages/jobe_shared/*

pool:
  vmImage: 'ubuntu-latest'

# Reference centralized Variable Groups
variables:
- group: jobe-systems-secrets    # API tokens, connection strings (secret)
- group: jobe-systems-config     # Board IDs, workspace IDs (non-secret)
- name: serviceName
  value: '[service-name]'

stages:
- stage: Build
  jobs:
  - job: BuildAndTest
    steps:
    - task: UsePythonVersion@0
      inputs:
        versionSpec: '3.11'
    
    - script: |
        # Install shared packages in development mode
        pip install -e packages/jobe_shared
        pip install -e packages/jobe_workflows
        cd functions/$(serviceName)
        pip install -r requirements.txt
      displayName: 'Install Dependencies'
    
    - script: |
        cd functions/$(serviceName)
        python -m pytest tests/ -v
      displayName: 'Run Tests'

- stage: Deploy
  dependsOn: Build
  condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
  jobs:
  - deployment: DeployFunction
    environment: 'production'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: AzureCLI@2
            inputs:
              azureSubscription: 'Azure-Jobe-Subscription'
              scriptLocation: 'inlineScript'
              inlineScript: |
                # Deploy infrastructure via Bicep
                az deployment group create \
                  --resource-group jobe-systems-rg \
                  --template-file functions/$(serviceName)/infrastructure/bicep/function_app.bicep
                
                # Configure environment variables from Variable Groups
                az functionapp config appsettings set \
                  --name jobe-$(serviceName)-function \
                  --resource-group jobe-systems-rg \
                  --settings \
                    MONDAY_API_TOKEN="$(MONDAY_API_TOKEN)" \
                    MONDAY_WORKSPACE_CRM="$(MONDAY_WORKSPACE_CRM)"
            displayName: 'Deploy Infrastructure and Configure Settings'
          
          - task: AzureFunctionApp@1
            inputs:
              azureSubscription: 'Azure-Jobe-Subscription'
              appName: 'jobe-$(serviceName)-function'
              package: 'functions/$(serviceName)'
            displayName: 'Deploy Function Code'
```

### **Pipeline Features**:
- **Variable Group Integration**: Centralized secret and configuration management
- **Multi-Stage Deployment**: Build → Test → Deploy with environment promotion
- **Infrastructure as Code**: Bicep template deployment for consistent environments
- **Function App Deployment**: Automated deployment with HTTP endpoints for Power Automate
- **Environment Variable Configuration**: Automatic application settings from Variable Groups

### **Service Infrastructure** (`functions/[service]/infrastructure/`)
**Service-Specific Deployment Configurations**:
- **Container Apps**: Service-specific container configurations for complex services
- **Function Apps**: HTTP-triggered endpoints optimized for Power Automate integration
- **Service Config**: Environment variables managed via Azure DevOps Variable Groups
- **Bicep Templates**: Infrastructure as Code deployment with parameterized environments
- **Azure Pipelines**: Automated deployment via service-specific `azure-pipelines.yml`

## Integration Workflow Updates

### **Adding New Services**
1. **Create Service Structure**: Use template from `templates/functions-folderstructure/`
2. **Add Shared Dependencies**: Include required packages in `requirements.txt`
3. **Implement Service Logic**: Build in `/app/src/` using shared packages
4. **Create Infrastructure**: Bicep templates in `infrastructure/bicep/`
5. **Set Up CI/CD**: Azure DevOps Pipeline in `azure-pipelines.yml`
6. **Configure Variables**: Add service-specific variables to Azure DevOps Variable Groups
7. **Create HTTP Endpoints**: Add Power Automate compatible HTTP triggers
8. **Test Integration**: Verify deployment and Power Automate connectivity

### **Power Automate Function Development**
1. **Design HTTP Interface**: Define JSON request/response schemas for Power Automate
2. **Implement Business Logic**: Use shared packages for SaaS API interactions
3. **Add Error Handling**: Standardized error responses for flow error handling
4. **Deploy via Pipeline**: Automatic deployment through Azure DevOps
5. **Test Power Automate Integration**: Create test flows to verify functionality
6. **Document API Contract**: Provide clear documentation for Power Automate developers

### **Azure Data Factory Integration**
1. **Define Data Sources**: Configure linkedService connections for new data sources
2. **Create Datasets**: Define data structure schemas in /dataset
3. **Build Pipelines**: Create ETL pipelines in /pipeline for data processing
4. **Configure Triggers**: Set up automation triggers for scheduled or event-driven processing
5. **Test Data Flow**: Validate data transformation and processing workflows
6. **Monitor Performance**: Set up monitoring and alerting for data pipeline health

## Essential Documentation Map for LLMs

### **Technical Architecture Documentation**

#### **Environment and Configuration**
- **[Environment Implementation Architecture](environment_implementation_architecture.md)**
  - 3-stage environment strategy (development, staging, production)
  - Environment variable management and Azure Key Vault integration
  - Local development setup and Azure Functions deployment
  - Security implementation and access control

#### **Logging and Monitoring**
- **[Centralized Logging Architecture](centralized_logging_architecture.md)**
  - Unified logging strategy across all functions
  - Log file organization in `/logs/functions/` directory
  - Azure Monitor integration and log retention policies
  - Environment-specific logging configurations

#### **Codebase Organization**
- **[Repository Structure Guide](../processes/repository-structure-guide.md)**
  - Complete folder structure explanation
  - Purpose and organization of each directory
  - Package-based architecture details
  - Azure Data Factory component organization

---

### **Process Documentation**

#### **Development Workflows**
- **[Git Usage Guide](../processes/git-usage-guide.md)**
  - Conventional commit standards and branching strategy
  - Code review and pull request processes
  - Environment-specific deployment workflows
  - Security and compliance guidelines

#### **Business Process Integration**
- **[Jobe Systems Internal Project Process](../processes/jobe-systems-project-process.md)**
  - BD/Sales, Design & Estimate, Engineering & Implementation stages
  - Integration points between Monday.com, D-Tools, and internal systems
  - Business workflow automation patterns

#### **Power Apps Development**
- **[Power Apps Extraction Guide](../processes/power-apps-extraction-guide.md)**
  - Power Platform CLI setup and authentication
  - App extraction, editing, and packaging workflows
  - Source code management for Power Apps

#### **AI Development Integration**
- **[AI Development Workflow](../processes/ai-development-workflow.md)**
  - AI-assisted development patterns and best practices
  - Integration with existing development workflows
  - Code review and quality assurance for AI-generated code

---

### **Implementation References**

#### **Shared Package Documentation**
- **Location**: `packages/jobe_shared/` and `packages/jobe_workflows/`
- **Key Components**:
  - API client implementations (`api/saas/monday/`, `api/azure/`)
  - Configuration management (`config/`)
  - Shared utilities (`utils/startup.py`, `utils/logging_config.py`)
  - Data models and schemas (`models/`)

#### **Function Implementation Examples**
- **Location**: `functions/` directory
- **Current Services**: CRM sync, workspace creation, Monday.com automation
- **Structure Pattern**: Each service includes `main.py`, `app/`, `infrastructure/`, `tests/`
- **HTTP Integration**: Power Automate compatible endpoints

#### **Infrastructure Templates**
- **Location**: `infrastructure/environments/` and individual `functions/*/infrastructure/`
- **Bicep Templates**: Infrastructure as Code for Azure Functions
- **Environment Configurations**: Development, staging, production settings
- **CI/CD Pipelines**: Azure DevOps pipeline templates

---

### **Quick Reference for New Development**

#### **Before Starting Development:**
1. Review [Environment Implementation Architecture](environment_implementation_architecture.md) for environment setup
2. Check [Repository Structure Guide](../processes/repository-structure-guide.md) for file organization
3. Understand [Git Usage Guide](../processes/git-usage-guide.md) for contribution workflow
4. Examine existing functions in `/functions/` for implementation patterns

#### **For New Function Development:**
1. Use template structure from existing functions
2. Follow shared package patterns for API integration
3. Implement centralized logging using `jobe_shared.utils.startup`
4. Create environment-specific configurations
5. Set up Bicep templates for infrastructure deployment
6. Configure CI/CD pipeline for automated deployment

#### **For Configuration Changes:**
1. Reference [Environment Implementation Architecture](environment_implementation_architecture.md)
2. Update appropriate environment files in `infrastructure/environments/`
3. Follow security guidelines for sensitive data
4. Test across all three environments (dev, staging, production)

#### **For Integration Work:**
1. Review existing API clients in `packages/jobe_shared/api/`
2. Follow established patterns for Monday.com, Azure, and SaaS integrations
3. Use shared configuration classes for consistent access patterns
4. Implement proper error handling and logging

---

## Development Standards and Patterns

### **Code Organization Standards**
- **Package-Based Architecture**: All shared code in installable Python packages
- **Environment-Driven Configuration**: All secrets and IDs via environment variables
- **Service Isolation**: Each function is independently deployable
- **Centralized Logging**: Unified logging using shared utilities
- **Infrastructure as Code**: Bicep templates for all Azure resources

### **Integration Patterns**
- **HTTP-First Design**: All services expose HTTP endpoints for Power Automate
- **Shared Package Usage**: Consistent API client patterns across services
- **Error Handling**: Standardized error responses for automation workflows
- **Security**: Azure Key Vault integration for production secrets
- **Monitoring**: Azure Monitor and Application Insights integration

---

*This guide provides the essential roadmap for LLMs to understand and contribute to the Jobe Systems API Codebase. Always reference the specific technical documentation linked above for detailed implementation guidance.*
