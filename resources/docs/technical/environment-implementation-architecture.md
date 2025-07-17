# Environment Implementation Architecture

**Technical Documentation - Jobe Systems API Codebase**

*Version: 1.0*  
*Created: July 17, 2025*  
*Last Updated: July 17, 2025*  
*Status: Current Implementation*

---

## Executive Summary

This document provides a comprehensive technical outline of the 3-stage environment implementation utilized in the Jobe Systems API Codebase. The architecture supports development, staging, and production environments through the `infrastructure/environments` folder structure, enabling secure, scalable, and maintainable deployment patterns for Azure Functions and Container Apps.

**Key Features:**
- Centralized environment management with shared configurations
- Secure secret management through Azure Key Vault integration
- Environment-specific variable overrides with inheritance hierarchy
- CI/CD pipeline compatibility for automated deployments
- Developer-friendly local development support

---

## Environment Architecture Overview

### Three-Stage Environment Model

The codebase implements a standard three-stage deployment model:

1. **Development** - Local development and feature testing
2. **Staging** - Pre-production testing and validation
3. **Production** - Live production environment

### Environment Hierarchy

```
Configuration Priority (highest to lowest):
1. Azure Application Settings (production)
2. Environment-specific variables (.env.development, .env.staging, .env.production)
3. Shared configuration (.env.shared)
4. Default values in code
```

---

## Current Implementation Structure

### Folder Organization

```
infrastructure/
└── environments/
    ├── README.md                           # Environment management documentation
    ├── development/                        # Development environment
    │   ├── config/
    │   │   └── .env.development           # Development-specific variables
    │   └── secrets/                       # Development secrets (local only)
    │
    ├── staging/                           # Staging environment
    │   ├── config/
    │   │   └── .env.staging              # Staging-specific variables
    │   └── secrets/                       # Staging secrets (local only)
    │
    ├── production/                        # Production environment
    │   ├── config/
    │   │   └── .env.production           # Production-specific variables
    │   └── secrets/                       # Production secrets (local only)
    │
    └── shared/                            # Shared across all environments
        ├── config/
        │   └── .env.shared               # Common configuration
        └── secrets/
            └── .env.secrets.shared       # Shared secrets template
```

### Security Implementation

- **Secrets Management**: All sensitive data stored in Azure Key Vault
- **Local Development**: `.env` files for local development (never committed)
- **Git Security**: Comprehensive `.gitignore` patterns for secret files
- **Access Control**: Environment-specific access permissions

---

## Environment Variable Strategy

### Naming Conventions

```bash
# Service Prefixes
MONDAY_*           # Monday.com related variables
AZURE_*            # Azure service variables
DTOOLS_*           # D-Tools integration variables
HARVEST_*          # Harvest time tracking variables
FASTFIELD_*        # FastField form variables
ZENDESK_*          # Zendesk support variables
SHAREPOINT_*       # SharePoint integration variables

# Category Suffixes
*_API_TOKEN        # API authentication tokens
*_ENDPOINT         # Service endpoints/URLs
*_WORKSPACE_*      # Workspace identifiers
*_BOARD_*          # Board/container identifiers
*_DATABASE_*       # Database connection information
*_STORAGE_*        # Storage account information
*_SUBSCRIPTION_*   # Azure subscription information
```

### Shared Configuration (`shared/config/.env.shared`)

```bash
# ============================================================================
# SHARED CONFIGURATION (All Environments)
# ============================================================================

# Application Information
APP_NAME=jobe-systems-api
APP_VERSION=2.0.0

# Logging Configuration
LOG_LEVEL=INFO
LOG_FORMAT=json
LOG_RETENTION_DAYS=30

# General Azure Configuration
AZURE_REGION=eastus2
AZURE_RESOURCE_GROUP_PREFIX=jobe-systems

# Common Service Endpoints
MONDAY_API_URL=https://api.monday.com/v2
DTOOLS_CLOUD_BASE_URL=https://dtcloudapi.d-tools.cloud
MONDAY_API_VERSION=2023-10
DTOOLS_API_VERSION=v2

# Default Pagination Settings
DTOOLS_CLOUD_PAGE_SIZE=1226
MONDAY_MAX_ITEMS=250

# Universal Board Types
MONDAY_WORKSPACE_TYPE=open
MONDAY_BOARD_TYPE=public
```

### Development Environment (`development/config/.env.development`)

```bash
# ============================================================================
# DEVELOPMENT ENVIRONMENT
# ============================================================================
ENVIRONMENT=development
ENVIRONMENT_SHORT=dev

# Debug Settings
DEBUG=true
LOG_LEVEL=DEBUG
AZURE_FUNCTIONS_ENVIRONMENT=development

# Azure Resources (Development)
AZURE_RESOURCE_GROUP=jobe-systems-dev
AZURE_STORAGE_ACCOUNT=jobesystemsdevdata
AZURE_SQL_DATABASE=jobe-systems-dev-db

# Monday.com Development Configuration
MONDAY_WORKSPACE_CRM=2702876
MONDAY_WORKSPACE_DESIGN_ENGINEERING=2552021
MONDAY_WORKSPACE_OPERATIONS=2552035

# Core Boards (Development)
MONDAY_BOARD_OPPORTUNITY=4493285981
MONDAY_BOARD_DEAL=4494641258
MONDAY_BOARD_PROPERTY=4733431849

# Development-specific overrides
DTOOLS_CLOUD_INCLUDE_ARCHIVED=true
MONDAY_USE_TEST_BOARDS=true
ENABLE_DETAILED_LOGGING=true
MOCK_EXTERNAL_APIS=false
```

### Staging Environment (`staging/config/.env.staging`)

```bash
# ============================================================================
# STAGING ENVIRONMENT
# ============================================================================
ENVIRONMENT=staging
ENVIRONMENT_SHORT=stg

# Staging Settings
DEBUG=false
LOG_LEVEL=INFO
AZURE_FUNCTIONS_ENVIRONMENT=staging

# Azure Resources (Staging)
AZURE_RESOURCE_GROUP=jobe-systems-staging
AZURE_STORAGE_ACCOUNT=jobesystemsstagingdata
AZURE_SQL_DATABASE=jobe-systems-staging-db

# Monday.com Staging Configuration
MONDAY_WORKSPACE_CRM=${MONDAY_STAGING_WORKSPACE_CRM}
MONDAY_WORKSPACE_DESIGN_ENGINEERING=${MONDAY_STAGING_WORKSPACE_DESIGN}
MONDAY_WORKSPACE_OPERATIONS=${MONDAY_STAGING_WORKSPACE_OPS}

# Core Boards (Staging)
MONDAY_BOARD_OPPORTUNITY=${MONDAY_STAGING_BOARD_OPPORTUNITY}
MONDAY_BOARD_DEAL=${MONDAY_STAGING_BOARD_DEAL}
MONDAY_BOARD_PROPERTY=${MONDAY_STAGING_BOARD_PROPERTY}

# Performance Testing Settings
ENABLE_PERFORMANCE_MONITORING=true
PERFORMANCE_BASELINE_ENABLED=true
```

### Production Environment (`production/config/.env.production`)

```bash
# ============================================================================
# PRODUCTION ENVIRONMENT
# ============================================================================
ENVIRONMENT=production
ENVIRONMENT_SHORT=prod

# Production Settings
DEBUG=false
LOG_LEVEL=INFO
AZURE_FUNCTIONS_ENVIRONMENT=production

# Azure Resources (Production)
AZURE_RESOURCE_GROUP=jobe-systems-prod
AZURE_STORAGE_ACCOUNT=jobesystemsproddata
AZURE_SQL_DATABASE=jobe-systems-prod-db

# Monday.com Production Configuration
MONDAY_WORKSPACE_CRM=${MONDAY_PROD_WORKSPACE_CRM}
MONDAY_WORKSPACE_DESIGN_ENGINEERING=${MONDAY_PROD_WORKSPACE_DESIGN}
MONDAY_WORKSPACE_OPERATIONS=${MONDAY_PROD_WORKSPACE_OPS}

# Core Boards (Production)
MONDAY_BOARD_OPPORTUNITY=${MONDAY_PROD_BOARD_OPPORTUNITY}
MONDAY_BOARD_DEAL=${MONDAY_PROD_BOARD_DEAL}
MONDAY_BOARD_PROPERTY=${MONDAY_PROD_BOARD_PROPERTY}

# Production Monitoring Settings
ENABLE_PERFORMANCE_MONITORING=true
ENABLE_DETAILED_LOGGING=false
AZURE_MONITOR_ENABLED=true
PRODUCTION_ALERTS_ENABLED=true
```

---

## Technical Implementation

### Environment Detection and Loading

The codebase uses enhanced configuration classes for environment detection:

```python
# Environment Management Class
class EnvironmentManager:
    @staticmethod
    def get_environment() -> str:
        """Detect current environment from environment variables"""
        return os.getenv("ENVIRONMENT", "development").lower()
    
    @staticmethod
    def is_azure_environment() -> bool:
        """Check if running in Azure Functions environment"""
        return os.getenv("AZURE_FUNCTIONS_ENVIRONMENT") is not None
    
    @staticmethod
    def load_environment_config():
        """Load environment configuration with proper hierarchy"""
        if EnvironmentManager.is_azure_environment():
            # Azure Functions: use Application Settings directly
            return
        
        # Local development: load .env files in order
        env = EnvironmentManager.get_environment()
        
        # Load in hierarchical order: shared → environment-specific
        load_dotenv(f"infrastructure/environments/shared/config/.env.shared")
        load_dotenv(f"infrastructure/environments/{env}/config/.env.{env}")
```

### Configuration Classes Integration

Enhanced configuration classes work seamlessly with the environment structure:

```python
# Updated Monday.com Configuration
class MondayConfig:
    @staticmethod
    def board_id(name: str) -> str:
        """Get Monday.com board ID by name"""
        return os.getenv(f"MONDAY_BOARD_{name.upper()}")
    
    @staticmethod
    def workspace_id(name: str) -> str:
        """Get Monday.com workspace ID by name"""
        return os.getenv(f"MONDAY_WORKSPACE_{name.upper()}")
    
    @staticmethod
    def api_token() -> str:
        """Get Monday.com API token"""
        return os.getenv("MONDAY_API_TOKEN")

# Updated Azure Configuration
class AzureConfig:
    @staticmethod
    def resource_group() -> str:
        """Get environment-specific resource group"""
        return os.getenv("AZURE_RESOURCE_GROUP")
    
    @staticmethod
    def storage_account() -> str:
        """Get environment-specific storage account"""
        return os.getenv("AZURE_STORAGE_ACCOUNT")
    
    @staticmethod
    def sql_database() -> str:
        """Get environment-specific SQL database"""
        return os.getenv("AZURE_SQL_DATABASE")
```

---

## Azure Functions Integration

### Application Settings Configuration

For Azure Functions deployment, configuration is managed through Application Settings:

```json
{
  "type": "Microsoft.Web/sites",
  "properties": {
    "siteConfig": {
      "appSettings": [
        {
          "name": "ENVIRONMENT",
          "value": "production"
        },
        {
          "name": "MONDAY_API_TOKEN",
          "value": "@Microsoft.KeyVault(SecretUri=https://jobe-systems-prod-kv.vault.azure.net/secrets/monday-api-token/)"
        },
        {
          "name": "DTOOLS_CLOUD_API_TOKEN",
          "value": "@Microsoft.KeyVault(SecretUri=https://jobe-systems-prod-kv.vault.azure.net/secrets/dtools-api-token/)"
        },
        {
          "name": "AZURE_RESOURCE_GROUP",
          "value": "jobe-systems-prod"
        }
      ]
    }
  }
}
```

### Key Vault Integration

Sensitive configuration values are stored in Azure Key Vault:

- **Development**: `jobe-systems-dev-kv`
- **Staging**: `jobe-systems-staging-kv`
- **Production**: `jobe-systems-prod-kv`

---

## CI/CD Pipeline Integration

### GitHub Actions Workflow

```yaml
name: Deploy to Azure Functions

env:
  ENVIRONMENT_PATH: infrastructure/environments

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout
      uses: actions/checkout@v3
    
    - name: Load Environment Configuration
      run: |
        python ${{ env.ENVIRONMENT_PATH }}/scripts/load_environment.py \
          --environment ${{ github.ref_name }}
    
    - name: Deploy to Azure Functions
      run: |
        az functionapp deployment source config-zip \
          --resource-group ${{ env.AZURE_RESOURCE_GROUP }} \
          --name ${{ env.AZURE_FUNCTION_APP_NAME }} \
          --src deployment.zip
    
    - name: Update Application Settings
      run: |
        az functionapp config appsettings set \
          --resource-group ${{ env.AZURE_RESOURCE_GROUP }} \
          --name ${{ env.AZURE_FUNCTION_APP_NAME }} \
          --settings @${{ env.ENVIRONMENT_PATH }}/${{ github.ref_name }}/config/appsettings.json
```

### Environment-Specific Deployment

Each environment has dedicated deployment configurations:

- **Development**: Triggered on push to `development` branch
- **Staging**: Triggered on push to `staging` branch
- **Production**: Triggered on push to `main` branch with manual approval

---

## Security Implementation

### Secret Management Strategy

1. **Local Development**: 
   - Uses `.env` files in `secrets/` folders
   - Never committed to git repository
   - Template files provided for setup

2. **Azure Environments**:
   - All secrets stored in Azure Key Vault
   - Function Apps access via managed identity
   - Automatic secret rotation where possible

3. **CI/CD Integration**:
   - GitHub secrets for deployment credentials
   - Azure DevOps variable groups for configuration
   - Secure variable substitution during deployment

### Access Control

```bash
# Environment-specific access permissions
Development:   All developers (read/write)
Staging:       Senior developers + DevOps (read/write)
Production:    DevOps team only (read/write), Others (read-only)
```

### Git Security Configuration

```gitignore
# Environment Secrets (never commit)
infrastructure/environments/*/secrets/.env.*
infrastructure/environments/*/secrets/keyvault.*

# Allow templates and documentation
!infrastructure/environments/*/secrets/*.example
!infrastructure/environments/*/secrets/README.md
```

---

## Environment-Specific Features

### Development Environment
- **Debug Mode**: Full logging and debugging enabled
- **Mock Services**: Option to mock external APIs
- **Test Data**: Uses development-specific boards and workspaces
- **Rapid Deployment**: Fast iteration with minimal validation

### Staging Environment
- **Performance Testing**: Baseline performance monitoring
- **Integration Testing**: Full system integration validation
- **User Acceptance Testing**: Production-like environment for UAT
- **Automated Testing**: Comprehensive test suite execution

### Production Environment
- **High Availability**: Multi-region deployment support
- **Performance Monitoring**: Full Azure Monitor integration
- **Alerting**: Comprehensive alerting and notification system
- **Backup & Recovery**: Automated backup and disaster recovery

---

## Local Development Setup

### Environment Setup Process

1. **Clone Repository**:
   ```bash
   git clone https://github.com/your-org/jobe-systems-api-codebase.git
   cd jobe-systems-api-codebase
   ```

2. **Create Local Environment Configuration**:
   ```bash
   # Copy shared configuration
   cp infrastructure/environments/shared/config/.env.shared .env.shared
   
   # Copy development configuration
   cp infrastructure/environments/development/config/.env.development .env.development
   
   # Create local secrets (use provided templates)
   cp infrastructure/environments/development/secrets/.env.secrets.example infrastructure/environments/development/secrets/.env.secrets
   ```

3. **Configure Environment Variables**:
   ```bash
   export ENVIRONMENT=development
   export PYTHONPATH="${PYTHONPATH}:$(pwd)/packages"
   ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -e packages/jobe_shared
   pip install -e packages/jobe_workflows
   ```

### VS Code Configuration

```json
{
  "files.associations": {
    ".env*": "dotenv",
    "*.env.*": "dotenv"
  },
  "files.exclude": {
    "**/environments/**/secrets/.env.*": true
  },
  "python.defaultInterpreterPath": ".venv/bin/python",
  "python.envFile": "${workspaceFolder}/.env.development"
}
```

---

## Monitoring and Observability

### Environment-Specific Monitoring

**Development**:
- Local logging to console and files
- Basic performance metrics
- Debug-level logging enabled

**Staging**:
- Azure Monitor integration
- Performance baseline establishment
- Integration test result tracking

**Production**:
- Full Azure Monitor and Application Insights
- Custom dashboards and alerts
- Business metrics and KPIs
- Automated incident response

### Logging Strategy

```python
# Environment-aware logging configuration
class LoggingConfig:
    @staticmethod
    def get_log_level():
        env = os.getenv("ENVIRONMENT", "development")
        return {
            "development": "DEBUG",
            "staging": "INFO", 
            "production": "WARNING"
        }.get(env, "INFO")
    
    @staticmethod
    def get_log_format():
        env = os.getenv("ENVIRONMENT", "development")
        if env == "production":
            return "json"
        return "text"
```

---

## Troubleshooting Guide

### Common Issues and Solutions

1. **Environment Variables Not Loading**:
   - Check `ENVIRONMENT` variable is set correctly
   - Verify file paths in `infrastructure/environments/`
   - Ensure proper file permissions

2. **Azure Function Configuration Issues**:
   - Verify Application Settings in Azure portal
   - Check Key Vault access permissions
   - Validate managed identity configuration

3. **Local Development Issues**:
   - Ensure `.env` files are not committed to git
   - Check Python path includes packages directory
   - Verify virtual environment is activated

### Debug Commands

```bash
# Check current environment
python -c "import os; print(f'Environment: {os.getenv(\"ENVIRONMENT\", \"not set\")}')"

# List all environment variables
python -c "import os; [print(f'{k}={v}') for k,v in os.environ.items() if k.startswith(('MONDAY_', 'AZURE_', 'DTOOLS_'))]"

# Test configuration loading
python -c "from jobe_shared.config import MondayConfig; print(f'CRM Workspace: {MondayConfig.workspace_id(\"CRM\")}')"
```

---

## Future Enhancements

### Planned Improvements

1. **Environment Automation**:
   - Automated environment provisioning
   - Infrastructure as Code (IaC) templates
   - Environment lifecycle management

2. **Advanced Monitoring**:
   - Business process monitoring
   - Predictive alerting
   - Performance optimization recommendations

3. **Enhanced Security**:
   - Certificate-based authentication
   - Network security groups
   - Advanced threat protection

4. **Developer Experience**:
   - One-click environment setup
   - Integrated development tooling
   - Automated testing frameworks

---

## Conclusion

The 3-stage environment implementation provides a robust, secure, and scalable foundation for the Jobe Systems API Codebase. The architecture supports modern DevOps practices while maintaining developer productivity and operational excellence.

The implementation leverages Azure's native capabilities for configuration management, security, and monitoring while providing flexibility for local development and testing. This approach ensures consistent behavior across environments while allowing for environment-specific optimizations and configurations.

---

*This document serves as the definitive technical reference for understanding and working with the environment implementation architecture in the Jobe Systems API Codebase.*
