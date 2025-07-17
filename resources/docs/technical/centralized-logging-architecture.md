# Centralized Logging Architecture

**Technical Documentation - Demo Codebase Data Platform**

*Version: 2.0*  
*Created: June 30, 2025*  
*Last Updated: July 17, 2025*  
*Status: Implemented*

---

## Executive Summary

This document outlines the implementation of a centralized logging system for all services in the Demo Codebase Data Platform. The solution leverages existing infrastructure patterns while providing unified log management, consistent formatting, and seamless Azure integration.

**Key Objectives:**
- Centralize all service logs in the root `/logs` directory
- Standardize logging patterns across all services
- Integrate with existing `shared_core` utilities
- Ensure Azure Functions and Container Apps compatibility
- Provide consistent log formatting and rotation

---

## Current State Analysis

### Existing Logging Infrastructure
The codebase currently implements:
- **Root logs directory**: `/logs/` with existing files:
  - `spotify_*.log`
  - `data_processing.log`
  - `correlation_analysis.log`
  - `github_collector.log`
- **Shared startup utilities**: `shared_core.utils.startup.program_start()` and `program_end()`
- **Package-based architecture**: Services use shared logging via `shared_core`
- **Environment-driven configuration**: All settings managed via environment variables

### Services Requiring Logging Integration
```
services/
â”œâ”€â”€ data_collection/              # API data collection services
â”œâ”€â”€ data_processing/              # Data transformation and ETL
â”œâ”€â”€ insights/                     # Correlation analysis and insights
â”œâ”€â”€ delivery/                     # API gateway and export services
â”œâ”€â”€ llm_integration/              # LLM and embedding services
flows/
â”œâ”€â”€ data_ingestion_flow/          # Data collection workflows
â”œâ”€â”€ processing_flow/              # Data processing workflows
â”œâ”€â”€ correlation_flow/             # Statistical analysis workflows
â””â”€â”€ notion_sync_flow/             # Notion integration workflows
```

---

## Implementation Architecture

### Core Design Principles

1. **Centralized Storage**: All logs written to `/logs` directory at repository root
2. **Shared Utilities**: Leverage existing `shared_core.utils.startup` patterns
3. **Consistent Naming**: Standardized file naming with date rotation
4. **Environment Flexibility**: Support local development and Azure deployment
5. **Package Integration**: Seamless integration with existing shared package architecture

### Logging Flow Architecture

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚   Service       â”‚â”€â”€â”€â–¶â”‚   shared_core   â”‚â”€â”€â”€â–¶â”‚   Centralized   â”‚
â”‚   Instance      â”‚    â”‚   Logging       â”‚    â”‚   /logs         â”‚
â”‚                 â”‚    â”‚   Utilities     â”‚    â”‚   Directory     â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                              â”‚
                              â–¼
                       â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                       â”‚   Azure         â”‚
                       â”‚   Monitor/      â”‚
                       â”‚   App Insights  â”‚
                       â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## Technical Specifications

### File Structure and Naming Convention

#### Primary Log Directory Structure
```
/logs/
â”œâ”€â”€ services/                            # Service-specific logs
â”‚   â”œâ”€â”€ data_collection_20250630.log    # Data collection services
â”‚   â”œâ”€â”€ spotify_client_20250630.log     # Spotify API client
â”‚   â”œâ”€â”€ github_client_20250630.log      # GitHub API client
â”‚   â”œâ”€â”€ data_processing_20250630.log    # Data transformation
â”‚   â”œâ”€â”€ correlation_analysis_20250630.log # Statistical analysis
â”‚   â”œâ”€â”€ llm_integration_20250630.log    # LLM and embeddings
â”‚   â””â”€â”€ notion_sync_20250630.log        # Notion integration
â”œâ”€â”€ flows/                               # Workflow logs
â”‚   â”œâ”€â”€ data_ingestion_20250630.log     # Data collection workflows
â”‚   â”œâ”€â”€ processing_flow_20250630.log    # Processing workflows
â”‚   â””â”€â”€ correlation_flow_20250630.log   # Analysis workflows
â”œâ”€â”€ system/                              # System-level logs
â”‚   â”œâ”€â”€ startup_20250630.log            # Application startup logs
â”‚   â”œâ”€â”€ errors_20250630.log             # Error aggregation
â”‚   â””â”€â”€ performance_20250630.log        # Performance metrics
â””â”€â”€ archive/                             # Archived logs (optional)
    â”œâ”€â”€ 2025-06/                        # Monthly archives
    â””â”€â”€ 2025-05/
```

#### Naming Convention Rules
- **Format**: `{service_name}_{YYYYMMDD}.log`
- **Service Name**: Lowercase, underscores for spaces
- **Date Format**: YYYYMMDD for daily rotation
- **Extensions**: Always `.log`
- **Special Cases**: 
  - System logs: `system_{type}_{YYYYMMDD}.log`
  - Error logs: `errors_{YYYYMMDD}.log`

### Shared Logging Utilities Enhancement

#### Enhanced Startup Utility
**Location**: `packages/shared_core/shared_core/utils/startup.py`

```python
# Enhanced program_start function signature
def program_start(
    program_name: str,
    version: str = "1.0.0",
    last_updated: str = None,
    creator: str = "System",
    log_level: str = "INFO",
    log_to_file: bool = True,
    centralized_logs: bool = True,
    azure_integration: bool = None
) -> logging.Logger:
```

#### New Logging Configuration Module
**Location**: `packages/shared_core/shared_core/utils/logging_config.py`

```python
class CentralizedLogger:
    """Centralized logging configuration for all services"""
    
    @staticmethod
    def get_logger(service_name: str, **kwargs) -> logging.Logger:
        """Get configured logger for a service"""
        
    @staticmethod
    def get_log_file_path(service_name: str) -> Path:
        """Generate standardized log file path"""
        
    @staticmethod
    def setup_log_rotation(service_name: str, max_files: int = 7):
        """Configure log rotation for service"""
```

### Environment Configuration

#### Required Environment Variables
```bash
# Logging Configuration
LOG_LEVEL=INFO                          # DEBUG, INFO, WARNING, ERROR, CRITICAL
CENTRALIZED_LOGGING=true                # Enable centralized logging
LOG_ROTATION_DAYS=7                     # Days to keep logs
AZURE_LOG_INTEGRATION=true              # Enable Azure Monitor integration

# Azure-Specific (Production)
APPLICATIONINSIGHTS_CONNECTION_STRING=your_connection_string
AZURE_LOG_STREAM=true                   # Stream to Azure Monitor

# Development-Specific
LOG_TO_CONSOLE=true                     # Also log to console
LOG_FILE_MAX_SIZE=10MB                  # Max size before rotation
```

---

## Implementation Plan

### Phase 1: Shared Package Enhancement (Week 1)

#### Deliverables:
1. **Enhanced `startup.py`**
   - Add centralized logging parameters
   - Implement automatic log file path resolution
   - Add Azure integration hooks

2. **New `logging_config.py` Module**
   - Centralized logger factory
   - Standardized formatting
   - Log rotation management
   - Environment-based configuration

3. **Configuration Classes**
   - LoggingConfig class in `shared_core.config`
   - Environment variable management
   - Azure integration settings

#### Code Implementation:

**Enhanced startup.py**:
```python
def program_start(
    program_name: str,
    version: str = "1.0.0",
    last_updated: str = None,
    creator: str = "System",
    **logging_kwargs
) -> logging.Logger:
    """Enhanced startup with centralized logging"""
    
    # Initialize centralized logger
    logger = CentralizedLogger.get_logger(
        service_name=program_name.lower().replace(" ", "_"),
        **logging_kwargs
    )
    
    # Log startup information
    logger.info(f"=== {program_name} Starting ===")
    logger.info(f"Version: {version}")
    logger.info(f"Last Updated: {last_updated}")
    logger.info(f"Creator: {creator}")
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    
    return logger
```

**New logging_config.py**:
```python
import logging
import os
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

class CentralizedLogger:
    """Centralized logging configuration"""
    
    @staticmethod
    def get_logs_directory() -> Path:
        """Get the centralized logs directory path"""
        # Find the repository root (contains packages/ and services/)
        current_path = Path(__file__)
        repo_root = current_path
        
        # Navigate up to find repo root
        while repo_root.parent != repo_root:
            if (repo_root / "packages").exists() and (repo_root / "functions").exists():
                break
            repo_root = repo_root.parent
        
        logs" / "services"
        logs_dir.mkdir(parents=True, exist_ok=True)
        return logs_dir
    
    @classmethod
    def get_logger(
        cls,
        service_name: str,
        log_level: str = None,
        azure_integration: bool = None
    ) -> logging.Logger:
        """Get configured logger for a function"""
        
        # Configuration from environment
        log_level = log_level or os.getenv("LOG_LEVEL", "INFO")
        azure_integration = azure_integration or os.getenv("AZURE_LOG_INTEGRATION", "false").lower() == "true"
        
        # Create logger
        logger = logging.getLogger(service_name)
        logger.setLevel(getattr(logging, log_level.upper()))
        
        # Clear existing handlers
        logger.handlers.clear()
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        
        # File handler (centralized)
        if os.getenv("CENTRALIZED_LOGGING", "true").lower() == "true":
            log_file = cls.get_log_file_path(service_name)
            file_handler = TimedRotatingFileHandler(
                log_file,
                when='midnight',
                interval=1,
                backupCount=int(os.getenv("LOG_ROTATION_DAYS", "7"))
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        # Console handler
        if os.getenv("LOG_TO_CONSOLE", "true").lower() == "true":
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        
        # Azure handler (if configured)
        if azure_integration:
            cls._add_azure_handler(logger, formatter)
        
        return logger
    
    @classmethod
    def get_log_file_path(cls, service_name: str) -> Path:
        """Generate standardized log file path"""
        logs_dir = cls.get_logs_directory()
        date_str = datetime.now().strftime("%Y%m%d")
        return logs_dir / f"{function_name}_{date_str}.log"
    
    @staticmethod
    def _add_azure_handler(logger: logging.Logger, formatter: logging.Formatter):
        """Add Azure Application Insights handler if available"""
        try:
            from azure.monitor.opentelemetry import configure_azure_monitor
            # Configure Azure Monitor integration
            configure_azure_monitor()
        except ImportError:
            # Azure SDK not available, skip
            pass
```

### Phase 2: Service Migration (Week 2)

#### Migration Strategy for Each Service:

**Template for Service Conversion**:
```python
# Before (example)
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# After (standardized)
from shared_core.utils.startup import program_start, program_end

def main():
    logger = program_start(
        program_name="Data Collection Service",
        version="2.1.0",
        last_updated="2025-07-17",
        creator="System"
    )
    
    try:
        # Function logic here
        logger.info("Starting data collection process")
        
        # ... function implementation ...
        
        logger.info("Data collection completed successfully")
        
    except Exception as e:
        logger.error(f"Data collection failed: {str(e)}", exc_info=True)
        raise
    finally:
        program_end(logger, "Data Collection Service")

if __name__ == "__main__":
    main()
```

#### Services to Migrate:
1. **data_collection â†’ `data_collection_20250717.log``
2. **spotify_client â†’ `spotify_client_20250717.log``
3. **github_client â†’ `github_client_20250717.log``
4. **data_processing â†’ `data_processing_20250717.log``
5. **correlation_analysis â†’ `correlation_analysis_20250717.log``
6. **llm_integration â†’ `llm_integration_20250717.log``
7. **notion_sync â†’ `notion_sync_20250717.log``

### Phase 3: Azure Integration (Week 3)

#### Azure Functions Configuration
```python
# In function app settings or Bicep templates
{
    "CENTRALIZED_LOGGING": "true",
    "LOG_LEVEL": "INFO",
    "AZURE_LOG_INTEGRATION": "true",
    "APPLICATIONINSIGHTS_CONNECTION_STRING": "@Microsoft.KeyVault(SecretUri=...)",
    "LOG_ROTATION_DAYS": "7"
}
```

#### Container Apps Integration
```yaml
# In container app configuration
env:
  - name: CENTRALIZED_LOGGING
    value: "true"
  - name: LOG_LEVEL
    value: "INFO"
  - name: AZURE_LOG_INTEGRATION
    value: "true"
volumeMounts:
  - name: logs-volume
    mountPath: /app/logs
```

### Phase 4: Monitoring and Maintenance (Week 4)

#### Log Management Features:
1. **Automated Cleanup**
   - Daily log rotation
   - Automatic archival after retention period
   - Storage space monitoring

2. **Monitoring Integration**
   - Azure Monitor dashboards
   - Log Analytics queries
   - Alert configuration for errors

3. **Development Tools**
   - Log viewer utility
   - Log analysis scripts
   - Performance monitoring

---

## Testing Strategy

### Unit Tests
```python
# Test centralized logger creation
def test_centralized_logger_creation():
    logger = CentralizedLogger.get_logger("test_service")
    assert logger.name == "test_service"
    assert len(logger.handlers) > 0

# Test log file path generation
def test_log_file_path_generation():
    path = CentralizedLogger.get_log_file_path("test_service")
    assert "test_service" in str(path)
    assert datetime.now().strftime("%Y%m%d") in str(path)
```

### Integration Tests
```python
# Test full logging workflow
def test_service_logging_workflow():
    logger = program_start("Test Service", version="1.0.0")
    logger.info("Test message")
    program_end(logger, "Test Service")
    
    # Verify log file was created
    log_file = CentralizedLogger.get_log_file_path("test_service")
    assert log_file.exists()
    
    # Verify log content
    with open(log_file, 'r') as f:
        content = f.read()
        assert "Test Service Starting" in content
        assert "Test message" in content
```

---

## Final Deliverables

### Code Artifacts
1. **Enhanced `packages/shared_core/shared_core/utils/startup.py`**
2. **New `packages/shared_core/shared_core/utils/logging_config.py`**
3. **Updated `packages/shared_core/shared_core/config/logging_config.py`**
4. **Migrated service files (7 services total)
5. **Azure deployment templates** with logging configuration

### Documentation
1. **Logging Standards Guide** - Developer documentation
2. **Azure Integration Guide** - Deployment documentation
3. **Troubleshooting Guide** - Operations documentation
4. **Migration Checklist** - Implementation verification

### Infrastructure
1. **Updated Bicep templates** with logging environment variables
2. **Azure Monitor configuration** for log aggregation
3. **Log retention policies** and automated cleanup
4. **Performance monitoring dashboards**

### Expected Log Output Structure
```
/logs/services/
â”œâ”€â”€ data_collection_20250717.log       # ~500KB daily
â”œâ”€â”€ spotify_client_20250717.log        # ~200KB daily
â”œâ”€â”€ github_client_20250717.log         # ~300KB daily
â”œâ”€â”€ data_processing_20250717.log       # ~150KB daily
â”œâ”€â”€ correlation_analysis_20250717.log  # ~100KB daily
â”œâ”€â”€ llm_integration_20250717.log       # ~250KB daily
â””â”€â”€ notion_sync_20250717.log           # ~50KB daily
```

---

## Success Metrics

### Technical Metrics
- **100% service coverage - All services using centralized logging
- **Zero logging errors** - No logging-related exceptions
- **Consistent formatting** - All logs follow standard format
- **Azure integration** - Logs visible in Azure Monitor

### Operational Metrics
- **Reduced troubleshooting time** - Centralized log location
- **Improved monitoring** - Standardized error tracking
- **Simplified maintenance** - Automated rotation and cleanup
- **Enhanced visibility** - Unified log aggregation

### Performance Metrics
- **Minimal overhead** - <5ms logging performance impact
- **Efficient storage** - Compressed and rotated logs
- **Fast searchability** - Indexed logs in Azure Monitor
- **Scalable architecture** - Supports service scaling

---

## Implementation Timeline

| Week | Phase | Deliverables | Status |
|------|-------|-------------|---------|
| 1 | Shared Package Enhancement | Enhanced utilities, logging config | Ready |
| 2 | Service Migration | 7 services converted | Ready |
| 3 | Azure Integration | Cloud configuration, monitoring | Ready |
| 4 | Testing & Validation | Tests, documentation, monitoring | Ready |

**Total Implementation Time**: 4 weeks  
**Development Effort**: ~40 hours  
**Testing Effort**: ~16 hours  
**Documentation Effort**: ~8 hours

---

*This specification provides a complete implementation roadmap for centralized logging in the Demo Codebase Data Platform. All code examples and configurations align with existing project patterns and Azure deployment requirements.*
