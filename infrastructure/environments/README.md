# Environment Configuration Management

This directory contains the complete environment management system for the Data Centralization Platform. It provides a structured, secure, and maintainable approach to handling configuration and secrets across development, staging, and production environments.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Directory Structure](#directory-structure)
- [Configuration Hierarchy](#configuration-hierarchy)
- [Environment Files](#environment-files)
- [Usage Instructions](#usage-instructions)
- [Security Guidelines](#security-guidelines)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Architecture Overview

The environment system follows a hierarchical structure where:

1. **Shared Configuration** provides common settings across all environments
2. **Environment-Specific Configuration** overrides shared settings with environment-specific values
3. **Secrets** are separated from configuration and managed securely
4. **PowerShell Scripts** provide automation for loading and validating environments

### Key Features

- **Environment-Driven Configuration** - All settings use environment variables
- **Secure Secret Management** - Separation of secrets from configuration
- **Configuration Inheritance** - Shared settings with environment-specific overrides
- **Validation & Loading Automation** - PowerShell scripts for environment management
- **Git-Safe Structure** - Placeholder values prevent accidental secret commits

## Directory Structure

```
infrastructure/environments/
├── README.md                           # This documentation
├── .env.example                        # Example environment file template
├── powershell/                         # Environment management scripts
│   └── load_environment.ps1           # Environment loading and validation script
├── shared/                             # Shared across all environments
│   ├── config/
│   │   └── .env.shared                # Common configuration settings
│   └── secrets/
│       └── .env.secrets.shared        # Shared secrets template
├── development/                        # Development environment
│   ├── config/
│   │   └── .env.development           # Development-specific configuration
│   └── secrets/
│       └── .env.secrets.development   # Development secrets (local only)
├── staging/                            # Staging environment
│   ├── config/
│   │   └── .env.staging              # Staging-specific configuration
│   └── secrets/
│       └── .env.secrets.staging      # Staging secrets (local only)
└── production/                        # Production environment
    ├── config/
    │   └── .env.production           # Production-specific configuration
    └── secrets/
        └── .env.secrets.production   # Production secrets (local only)
```

## Configuration Hierarchy

Environment variables are loaded in the following order (later values override earlier ones):

1. **Shared Configuration** (`shared/config/.env.shared`)
2. **Environment Configuration** (`{environment}/config/.env.{environment}`)
3. **Shared Secrets** (`shared/secrets/.env.secrets.shared`) - Template only
4. **Environment Secrets** (`{environment}/secrets/.env.secrets.{environment}`)

### Configuration Categories

#### Shared Configuration
- Application metadata (name, version)
- API rate limits and timeouts
- Default pagination settings
- Common correlation analysis thresholds
- Universal API endpoints

#### Environment-Specific Configuration
- Environment identification (`development`, `staging`, `production`)
- Debug and logging settings
- Database connection parameters
- API base URLs and endpoints
- Development features and flags

#### Secrets Management
- API keys and tokens
- Database credentials
- JWT secrets and encryption keys
- OAuth client credentials

## Environment Files

### Configuration Files (`.env.{environment}`)

These files contain non-sensitive configuration values that can be safely committed to version control.

**Key Sections:**
- Environment Identification
- Application Configuration
- Logging Configuration
- Database Configuration
- Data Processing Configuration
- Redis Configuration
- LLM Configuration
- Workflow Configuration
- Security Configuration
- External API Configuration
- Development Features

### Secrets Files (`.env.secrets.{environment}`)

These files contain sensitive information and should **NEVER** be committed to version control.

**Key Sections:**
- Database Credentials
- External API Keys (Music & Entertainment)
- External API Keys (AI & Language Models)
- External API Keys (Developer Tools)
- External API Keys (Weather & Location)
- External API Keys (Productivity & Collaboration)
- Security & Encryption Keys

## Usage Instructions

### 1. Loading Environment Variables

#### Using PowerShell Script (Recommended)

```powershell
# Load development environment
.\infrastructure\environments\powershell\load_environment.ps1 -Environment development

# Load with verbose output
.\infrastructure\environments\powershell\load_environment.ps1 -Environment development -Verbose

# Validate environment without loading
.\infrastructure\environments\powershell\load_environment.ps1 -Environment development -ValidateOnly

# Show secrets during loading (use carefully)
.\infrastructure\environments\powershell\load_environment.ps1 -Environment development -ShowSecrets
```

#### Using Python (UnifiedEnvironmentLoader)

```python
from shared_core.config.unified_environment_loader import UnifiedEnvironmentLoader

# Automatically detect and load environment
UnifiedEnvironmentLoader.ensure_environment_loaded()

# Load specific environment
UnifiedEnvironmentLoader.load_environment("development")
```

### 2. Configuration Management

#### Using Configuration Classes

```python
from shared_core.config.database_config import DatabaseConfig
from shared_core.config.spotify_config import SpotifyConfig

# Database configuration
db_url = DatabaseConfig.database_url()
redis_url = DatabaseConfig.redis_url()

# API configuration
spotify_client_id = SpotifyConfig.client_id()
spotify_secret = SpotifyConfig.client_secret()
```

#### Direct Environment Variable Access

```python
import os

# Get configuration values
environment = os.getenv("ENVIRONMENT", "development")
debug_mode = os.getenv("DEBUG", "false").lower() == "true"
api_key = os.getenv("SPOTIFY_CLIENT_ID")
```

### 3. Setting Up New Environment

#### For Development
1. Copy secrets template: `cp shared/secrets/.env.secrets.shared development/secrets/.env.secrets.development`
2. Update secret values in `development/secrets/.env.secrets.development`
3. Customize configuration in `development/config/.env.development` if needed
4. Load and validate: `.\powershell\load_environment.ps1 -Environment development -ValidateOnly`

#### For Production
1. Set up Azure Key Vault for secret management
2. Configure Application Settings in Azure Functions/Container Apps
3. Reference Key Vault secrets using `@Microsoft.KeyVault(...)` syntax
4. Validate configuration before deployment

## Security Guidelines

### Git Security

**Files that MUST be in `.gitignore`:**
```gitignore
# Environment secrets (never commit!)
**/.env.secrets.*
!**/.env.secrets.shared  # Template only
.env.local
.env.*.local

# Environment logs
environment_load_log_*.txt
```

### Secret Management Best Practices

1. **Development Environment**
   - Use placeholder/dummy secrets for initial setup
   - Store real development secrets in password manager
   - Never commit actual API keys to version control

2. **Staging/Production Environments**
   - Use Azure Key Vault for all production secrets
   - Implement proper access controls and auditing
   - Rotate secrets regularly
   - Use managed identities where possible

3. **API Key Security**
   - Generate environment-specific API keys when possible
   - Use least-privilege principles for API access
   - Monitor API usage for anomalies
   - Implement proper error handling to avoid secret exposure

### Configuration Validation

Required environment variables by category:

#### Application (Always Required)
- `APP_NAME` - Application identifier
- `APP_VERSION` - Current version
- `ENVIRONMENT` - Environment identifier (development/staging/production)

#### Database (Always Required)
- `POSTGRES_HOST` - Database server hostname
- `POSTGRES_PORT` - Database server port
- `POSTGRES_DB` - Database name
- `POSTGRES_USER` - Database username
- `POSTGRES_PASSWORD` - Database password

#### External APIs (Required for Functionality)
- `SPOTIFY_CLIENT_ID` - Spotify API client ID
- `SPOTIFY_CLIENT_SECRET` - Spotify API client secret
- `OPENAI_API_KEY` - OpenAI API key
- `GITHUB_TOKEN` - GitHub personal access token

## Best Practices

### 1. Environment Variable Naming

Follow the established naming conventions:

```bash
# Service Prefixes
SPOTIFY_*          # Spotify API related
GITHUB_*           # GitHub API related
OPENAI_*           # OpenAI API related
TMDB_*             # The Movie Database API
OPENWEATHER_*      # OpenWeatherMap API
MUSICBRAINZ_*      # MusicBrainz API
NOTION_*           # Notion API
POKEMON_*          # Pokémon API

# Category Suffixes
*_API_KEY          # API authentication keys
*_API_TOKEN        # API authentication tokens
*_CLIENT_ID        # OAuth client identifiers
*_CLIENT_SECRET    # OAuth client secrets
*_BASE_URL         # Service base URLs
*_RATE_LIMIT       # API rate limits
*_TIMEOUT          # Request timeouts
```

### 2. Configuration Management

- **Use Configuration Classes**: Always use shared configuration classes instead of direct `os.getenv()` calls
- **Provide Defaults**: Include sensible defaults for non-critical settings
- **Validate Configuration**: Implement validation for required configuration values
- **Document Changes**: Update this README when adding new configuration categories

### 3. Secret Management

- **Separate Secrets from Configuration**: Keep sensitive data in dedicated secrets files
- **Use Templates**: Maintain secret templates to document required values
- **Environment-Specific Secrets**: Use different secrets for each environment
- **Regular Rotation**: Implement regular secret rotation procedures

### 4. Development Workflow

- **Load Environment First**: Always load environment configuration before running applications
- **Validate Before Deploy**: Use validation scripts before deploying to staging/production
- **Test Configuration Changes**: Test configuration changes in development before promoting
- **Document Dependencies**: Document any new environment variable requirements

## Troubleshooting

### Common Issues

#### 1. Missing Environment Variables

**Symptoms:**
- Application fails to start
- Configuration validation errors
- API authentication failures

**Solutions:**
```powershell
# Check which variables are missing
.\powershell\load_environment.ps1 -Environment development -ValidateOnly

# Load environment with verbose output to see what's loaded
.\powershell\load_environment.ps1 -Environment development -Verbose
```

#### 2. Configuration Not Loading

**Symptoms:**
- Environment variables not set
- Using default values instead of configured values

**Solutions:**
1. Verify file paths and naming conventions
2. Check for syntax errors in `.env` files
3. Ensure proper file encoding (UTF-8)
4. Verify environment detection logic

#### 3. API Authentication Failures

**Symptoms:**
- 401 Unauthorized responses from external APIs
- Authentication token errors

**Solutions:**
1. Verify API keys are correctly set in secrets files
2. Check API key validity and expiration
3. Ensure proper environment variable naming
4. Test API keys using direct API calls

#### 4. Database Connection Issues

**Symptoms:**
- Cannot connect to database
- Connection timeout errors

**Solutions:**
1. Verify database configuration values
2. Test database connectivity separately
3. Check network access and firewall settings
4. Validate database user permissions

### Debugging Tools

#### PowerShell Environment Loader

```powershell
# Full diagnostic run
.\powershell\load_environment.ps1 -Environment development -Verbose

# Show all loaded variables (including secrets)
.\powershell\load_environment.ps1 -Environment development -ShowSecrets

# Validate without loading
.\powershell\load_environment.ps1 -Environment development -ValidateOnly
```

#### Configuration Testing

```python
# Test configuration classes
from shared_core.config.database_config import DatabaseConfig

# Validate database configuration
if DatabaseConfig.validate_database_connection():
    print("Database configuration is valid")
    print(DatabaseConfig.get_database_info())

# Test API configurations
from shared_core.config.spotify_config import SpotifyConfig
print(SpotifyConfig.get_config_summary())
```

### Getting Help

For additional support:

1. Check the technical documentation in `resources/docs/technical/`
2. Review the AI coding practices guide in `resources/docs/ai/`
3. Examine working examples in the `services/` directory
4. Test configuration with the PowerShell validation scripts

---

## File Maintenance

This environment system should be maintained as follows:

- **Monthly**: Review and update API rate limits based on usage
- **Quarterly**: Audit and rotate development secrets
- **Semi-Annually**: Review and update configuration templates
- **Annually**: Complete security audit of environment management system

For questions about this system, refer to the project documentation or contact the development team.
