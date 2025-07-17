# LLM Coding Practices Guide - Data-Centralization-Platform

## Overview

This guide provides comprehensive coding standards and practices for AI language models (LLMs) working on the demo-codebase project. These rules ensure consistency, maintainability, and alignment with established development patterns across the codebase.

## Table of Contents

1. [Code Review Standards](#code-review-standards)
2. [Import and Package Management](#import-and-package-management)
3. [Configuration and Environment Management](#configuration-and-environment-management)
4. [Logging Standards](#logging-standards)
5. [Exception Handling](#exception-handling)
6. [Code Comments and Documentation](#code-comments-and-documentation)
7. [Function Documentation](#function-documentation)
8. [Testing Requirements](#testing-requirements)
9. [Docker and Deployment](#docker-and-deployment)
10. [Azure Pipeline Standards](#azure-pipeline-standards)
11. [Security and Sensitive Data](#security-and-sensitive-data)
12. [Large-Scale Automation Guidelines](#large-scale-automation-guidelines)

---

## Code Review Standards

### Priority Comment Handling

When performing code reviews, **ALWAYS** identify and address these specific comment types in order of priority:

#### 1. `bug_cmt` - **HIGHEST PRIORITY**
**Action Required**: Provide immediate solutions or detailed remediation plans.

**Response Pattern**:
```
CRITICAL BUG IDENTIFIED: [Line X]
Current Issue: [describe the bug]
Proposed Solution: [specific fix or approach]
Impact Assessment: [potential consequences if not fixed]
Implementation Steps: [numbered action items]
```

**Example Response**:
```
CRITICAL BUG IDENTIFIED: Line 47
Current Issue: monday api occasionally returns duplicate items
Proposed Solution: Implement server-side deduplication using item IDs before processing
Impact Assessment: Data corruption and incorrect reporting if duplicates processed
Implementation Steps:
1. Add item_id tracking set before processing loop
2. Skip items already in tracking set
3. Add logging for duplicate detection count
4. Consider investigating root cause with Monday.com API team
```

#### 2. `warp_cmt` - **AI-SPECIFIC ACTIONS**
**Action Required**: This comment is specifically for AI assistants to address during code review.

**Response Pattern**:
```
WARP ACTION ITEM: [Line X]
Request: [what the comment is asking for]
Analysis: [assessment of the request]
Recommendation: [specific solution or next steps]
Code Changes: [if applicable, provide updated code]
```

#### 3. `todo_cmt` - **MEDIUM PRIORITY**
**Action Required**: Provide implementation suggestions or flag as release blocker. These should only be addressed if specifically requested in the prompt.

**Response Pattern**:
```
ACTIVE TODO IDENTIFIED: [Line X]
Required Action: [what needs to be done]
Proposed Implementation: [specific code or approach]
Estimated Effort: [time/complexity assessment]
Release Impact: [can this ship without this fix?]
```

### Code Style Preservation Rules

#### DO NOT Modify These Elements:
- **Lowercase internal comments** - This is intentional coding style
- **Lowercase logger debug statements** - Deliberate development choice
- **Existing comment formatting** that follows established patterns
- **Variable naming** that follows project conventions

#### Examples of What NOT to Change:
```python
# âœ… LEAVE UNCHANGED - Correct lowercase internal comments
# processing data items for correlation analysis
logger.debug("starting item processing loop")

# âŒ DO NOT "CORRECT" TO:
# processing data items for correlation analysis
logger.debug("Starting item processing loop")
```

---

## Import and Package Management

### ALWAYS Use Package-Based Imports

```python
# CORRECT - Package-based imports
from shared_core.api.clients.spotify import SpotifyAPIClient
from shared_core.config.database_config import DatabaseConfig
from shared_core.utils.startup import program_start, program_end
from shared_core.utils.logging_config import CentralizedLogger
from services.data_processing import DataProcessor
```

### NEVER Use Path Manipulation

```python
# INCORRECT - Do not suggest these patterns
import sys
sys.path.append("../../packages")
import os
os.path.join("..", "..", "packages")
```

---

## Configuration and Environment Management

### Environment-Driven Configuration (Required)

```python
# CORRECT - Use config classes for all IDs and secrets
from shared_core.config.database_config import DatabaseConfig

database_url = DatabaseConfig.database_url()     # Gets DATABASE_URL
api_key = DatabaseConfig.api_key("spotify")      # Gets SPOTIFY_API_KEY
redis_url = DatabaseConfig.redis_url()           # Gets REDIS_URL
```

### âŒ NO Hardcoded Values

```python
# INCORRECT - Never suggest hardcoded IDs or secrets
database_url = "postgresql://user:pass@localhost/db"
api_key = "sk-1234567890abcdef..."
```

### Environment Variable Standards

```python
# Service Prefixes
SPOTIFY_*          # Spotify API related variables
GITHUB_*           # GitHub API related variables
OPENWEATHER_*      # OpenWeather API variables
TMDB_*             # TMDB API variables
POKEMON_*          # PokÃ©mon API variables
MUSICBRAINZ_*      # MusicBrainz API variables
NOTION_*           # Notion API variables

# Category Suffixes
*_API_KEY          # API authentication keys
*_API_TOKEN        # API authentication tokens
*_ENDPOINT         # Service endpoints/URLs
*_CLIENT_ID        # Client identifiers
*_CLIENT_SECRET    # Client secrets
```

### API Token Management

```python
# ALWAYS use config classes for tokens
api_key = DatabaseConfig.api_key("spotify")  # âœ… Correct
api_key = os.getenv("SPOTIFY_API_KEY")  # âŒ Direct env access discouraged
```

---

## Logging Standards

### Required Logging Pattern

```python
from shared_core.utils.startup import program_start, program_end

def main():
    # ALWAYS start functions this way
    logger = program_start("Function Name", version="1.0.0")
    
    try:
        # Function logic here
        logger.info("Processing started")
        result = process_data()
        logger.info(f"Processing completed successfully: {result}")
        
    except Exception as e:
        logger.error(f"Error in processing: {str(e)}", exc_info=True)
        raise
    finally:
        # ALWAYS end functions this way
        program_end(logger, "Function Name")
```

### Progress Logging for Long Operations

```python
items = get_large_dataset()
total_items = len(items)
logger.info(f"Processing {total_items} items")

for i, item in enumerate(items):
    process_item(item)
    
    # Log progress every 100 items
    if (i + 1) % 100 == 0:
        logger.info(f"Processed {i + 1}/{total_items} items")
```

### Sensitive Data Handling

```python
# DON'T log sensitive data
logger.info(f"Processing user with ID: {user_id}")  # âœ… Good
logger.info(f"Processing user: {user_data}")       # âŒ May contain sensitive info

# For debugging, sanitize data
logger.debug(f"User data keys: {list(user_data.keys())}")  # âœ… Safe
```

**Note**: Secondary functions should require the logger be sent to them. All logging should output in the central logs folder, in the appropriate subfolder of services or testing.

---

## Exception Handling

### Standard Exception Handling

```python
try:
    risky_operation()
except SpecificException as e:
    logger.error(f"Specific error occurred: {str(e)}", exc_info=True)
    # Handle specific error
except Exception as e:
    logger.critical(f"Unexpected error: {str(e)}", exc_info=True)
    raise  # Re-raise unexpected errors
```

### API Error Handling

```python
try:
    response = api_client.make_request()
    if not response.success:
        logger.warning(f"API request failed: {response.error}")
        return None
except Exception as e:
    logger.error(f"API call failed: {str(e)}", exc_info=True)
    raise
```

---

## Code Comments and Documentation

### Comment Tagging System

This codebase uses the [Better Comments](https://marketplace.visualstudio.com/items?itemName=aaron-bond.better-comments) VS Code extension for visual highlighting and categorization.

#### Tag Definitions and Usage

##### `!` - **Important/Critical Information**
Highlight critical information that developers must be aware of before modifying or calling the code.

```python
# ! this function processes 10,000+ records and may take several minutes
def bulk_process_correlations():

# ! only call this during maintenance windows - modifies production data
def reset_database_schema():
```

##### `?` - **Open Questions/Research Needed**
Mark areas where the code's purpose, behavior, or implementation needs clarification.

```python
# ? verify if this filtering logic matches current analysis requirements
if correlation_strength > 0.7 and p_value < 0.05:

# ? determine if this timeout value is still appropriate for current API limits
timeout_seconds = 30
```

##### `//` - **Archived/Strikethrough Code**
Mark code sections that are no longer active but preserved for reference.

```python
# // original synchronous implementation - replaced with async version
# for item in items:
#     process_item_sync(item)
```

##### `todo_cmt` - **Active Todo Items**
Track work items that must be completed before the next production release.

```python
# todo_cmt add proper exception handling for api timeout scenarios
response = spotify_client.get_tracks()

# todo_cmt implement input validation for correlation_id parameter
def create_correlation_analysis(correlation_id, analysis_data):
```

##### `dev_cmt` - **Future Development**
Document planned improvements or enhancements for future development cycles.

```python
# dev_cmt plan to implement caching layer for frequently accessed correlations
def get_correlation_data(correlation_id):
```

##### `bug_cmt` - **Known Issues**
Document confirmed bugs that are under evaluation or pending fixes.

```python
# bug_cmt spotify api occasionally returns duplicate tracks - dedupe as workaround
tracks = list(set(response.data))
```

##### `legacy_cmt` - **Historical Context**
Explain what previous functionality existed and why it was changed.

```python
# legacy_cmt removed legacy data format - migrated to postgresql in v2.0
def get_analysis_data():
```

### General Comment Guidelines

#### Formatting Rules
- **Use lowercase only** for all internal code comments
- **Avoid "we" statements** - use direct, action-oriented language instead
- **Be concise but descriptive** - provide enough context without unnecessary verbosity

#### âœ… Correct Style
```python
# ! this operation modifies live production data
# ? verify if rate limiting is needed here
# todo_cmt add retry logic for failed requests
# process correlation data using current database configuration
```

#### âŒ Incorrect Style
```python
# ! This Operation Modifies Live Production Data (wrong case)
# We need to verify if rate limiting is needed here (uses "we")
# TODO: Add retry logic (wrong tag format)
# Process Monday board items (wrong case)
```

---

## Function Documentation

### Required Function Docstrings

```python
def process_monday_items(board_id: str, filter_criteria: dict = None) -> List[Dict]:
    """
    Process Monday.com items with optional filtering
    
    Args:
        board_id (str): Monday.com board ID from MondayConfig
        filter_criteria (dict, optional): Filtering criteria for items
        
    Returns:
        List[Dict]: Processed items with standardized structure
        
    Raises:
        MondayAPIError: When API request fails
        ValidationError: When board_id is invalid
        
    Example:
        >>> from jobe_shared.config.monday_config import MondayConfig
        >>> board_id = MondayConfig.board_id("opportunity")
        >>> items = process_monday_items(board_id, {"status": "active"})
        >>> print(f"Processed {len(items)} items")
    """
```

### Function Names

```python
# Use snake_case for function names
def process_crm_data():
def create_monday_item():
def extract_pricing_information():

# Use descriptive, action-oriented names
def sync_lutron_lighting_data():  # âœ… Clear purpose
def process_data():               # âŒ Too generic
```

---

## Testing Requirements

### Required Test Structure

```python
import pytest
from unittest.mock import Mock, patch
from jobe_shared.config.monday_config import MondayConfig

class TestServiceName:
    
    def setup_method(self):
        """Setup for each test method"""
        self.mock_logger = Mock()
        
    @patch('jobe_shared.config.monday_config.MondayConfig.board_id')
    def test_function_with_mocked_config(self, mock_board_id):
        """Test with mocked configuration"""
        mock_board_id.return_value = "test_board_id"
        # Test logic here
        
    def test_error_handling(self):
        """Test error handling patterns"""
        with pytest.raises(SpecificException):
            risky_function_call()
```

---

## Docker and Deployment

### Required Dockerfile Structure

```dockerfile
# Use Python 3.11 slim image for smaller container size
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY config/ ./config/

# Create logs directory
RUN mkdir -p /app/logs

# Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Default command
CMD ["python", "-m", "app.main"]
```

---

## Azure Pipeline Standards

### Required Pipeline Structure

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
  - job: DeployToAzure
    steps:
    - script: |
        # Deployment steps here
      displayName: 'Deploy to Azure Container Apps'
```

---

## Security and Sensitive Data

### Terminal Commands and Secrets

For any terminal commands you provide, **NEVER** reveal or consume secrets in plain-text. Instead, compute the secret in a prior step using a command and store it as an environment variable.

```bash
# For example (in bash): in a prior step, run
API_KEY=$(secret_manager --secret-name=name)
# then use it later on
api --key=$API_KEY
```

**If the user's query contains a stream of asterisks**, you should respond letting the user know "It seems like your query includes a redacted secret that I can't access." If that secret seems useful in the suggested command, replace the secret with `{{secret_name}}` where `secret_name` is the semantic name of the secret.

---

## Large-Scale Automation Guidelines

### Mandatory Approval Required

**IMPORTANT**: LLMs must **ALWAYS** request explicit user approval before executing any PowerShell script that modifies multiple files, regardless of automation settings or perceived urgency.

### Scope Definition: What Constitutes "Large-Scale Changes"

#### Always Requires Approval:
- **Multiple files** (2 or more) being modified in a single operation
- **Cross-service changes** affecting different business domains
- **Shared package modifications** that impact multiple services
- **Environment configuration updates** across multiple settings
- **Infrastructure changes** affecting deployment templates

#### Required Pre-Approval Information

```
ðŸš¨ LARGE-SCALE AUTOMATION REQUEST

## Change Summary:
[Brief description of what needs to be updated]

## Scope Analysis:
- Files Affected: [exact count] files across [X] services
- Service Domains: [list affected business domains]
- Risk Level: [LOW/MEDIUM/HIGH] - [justification]

## Proposed PowerShell Script:
```powershell
[Complete script with comments explaining each step]
```

## Expected Changes Per File:
[Specific description of modifications each file will receive]

## Rollback Strategy:
[How to undo these changes if issues arise]

## Testing Approach:
[How to validate changes worked correctly]

Please review and approve before execution.
```

### Git Safety Requirements

All automation scripts must include:

1. **Git commit backup** before modifications
2. **Error handling** with Git rollback capability
3. **File existence validation** before modification
4. **Audit trail logging** for all operations
5. **Dry-run capability** for testing

### Required Script Structure with Git Integration

```powershell
param(
    [switch]$DryRun = $false,
    [switch]$Verbose = $false,
    [int]$MaxErrorThreshold = 3
)

# Initialize logging
$logFile = ".\automation_log_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"
function Write-Log {
    param($Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp - $Message" | Tee-Object -FilePath $logFile -Append
}

# Create backup commit (only if not dry run)
if (-not $DryRun) {
    $backupCommit = New-AutomationBackup -CommitMessage "AUTOMATION BACKUP: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - Pre-bulk changes"
    Write-Log "Backup commit created: $backupCommit"
}

# Main processing with error threshold monitoring
try {
    # Script logic here with error counting
    # Check error threshold after each significant operation
    if (-not (Test-AutomationSafety -ErrorCount $errorCount -MaxErrors $MaxErrorThreshold -BackupCommit $backupCommit)) {
        return # Script will exit via rollback function
    }
} catch {
    $errorCount++
    Write-Log "CRITICAL ERROR: $($_.Exception.Message)"
    
    if (-not $DryRun) {
        Invoke-AutomationRollback -BackupCommitHash $backupCommit -ErrorMessage $_.Exception.Message
    }
}
```

---

## Required README Structure

### Standard README Template

```markdown
# [Service Name]

## Overview
Brief description of the service purpose and functionality.

## Configuration
Environment variables required:
- `MONDAY_BOARD_[NAME]`: Board ID for [purpose]
- `MONDAY_WORKSPACE_[NAME]`: Workspace ID for [purpose]

## Usage
### From Shared Package
```python
from jobe_shared.api.saas.monday.client import MondayAPIClient
from jobe_shared.config.monday_config import MondayConfig

# Example usage
client = MondayAPIClient()
board_id = MondayConfig.board_id("opportunity")
items = client.get_items(board_id)
```

## Deployment
This service deploys via Azure DevOps Pipelines to Azure Container Apps.

## Related Documentation
- [LLM Development Guide](../../docs/technical/llm-technical-development-guide.md)
- [Environment Configuration](../../docs/deployment/environment_configuration.md)
```

---

## Best Practices Summary

### Do's:
- âœ… Use package-based imports exclusively
- âœ… Employ environment-driven configuration
- âœ… Follow standardized logging patterns
- âœ… Implement comprehensive error handling
- âœ… Use descriptive function and variable names
- âœ… Include proper docstrings for all functions
- âœ… Write comprehensive tests with proper mocking
- âœ… Request approval for multi-file modifications
- âœ… Preserve existing code style and comment formatting

### Don'ts:
- âŒ Use hardcoded values for configuration
- âŒ Modify lowercase comment styling
- âŒ Use path manipulation for imports
- âŒ Log sensitive data in plain text
- âŒ Execute large-scale automation without approval
- âŒ Use generic function names
- âŒ Skip error handling patterns

---

## Conclusion

This guide serves as the authoritative reference for LLM-assisted development within the Jobe Systems codebase. Adherence to these standards ensures code quality, maintainability, and consistency across all projects and services.

For questions or clarifications regarding these standards, refer to the existing codebase examples or consult the technical documentation in the `resources/docs/technical/` directory.

---

*Last Updated: 2025-01-17*
*Version: 1.0*

