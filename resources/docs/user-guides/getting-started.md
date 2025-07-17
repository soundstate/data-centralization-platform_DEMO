# Getting Started Guide

**User Guide - Jobe Systems API Codebase**

*Version: 1.0*  
*Created: July 17, 2025*  
*Last Updated: July 17, 2025*  
*Status: Current Implementation*

---

## Welcome to the Jobe Systems API Codebase

This guide will help new developers get up and running with the Jobe Systems API Codebase. The codebase consolidates data from multiple SaaS platforms (Monday.com, D-Tools, Harvest, FastField, Zendesk, SharePoint) into a centralized Azure environment, providing unified access through Power Apps and automated workflows.

## Required Proficiencies

Before working with the Jobe Systems API Codebase, developers should have a solid understanding of the following languages and technologies:

### Programming Languages
- **Python** - Core language for Azure Functions and shared packages
- **YAML** - Configuration files, Power App, and CI/CD pipelines
- **JSON** - Data interchange and configuration
- **Markdown** - Documentation and README files
- **SQL** - Database queries and data manipulation
- **REST/GraphQL APIs** - API integration and consumption

### Technologies and Concepts
- **Azure Functions** - Serverless compute platform
- **Azure Container Apps** - Containerized application hosting
- **CI/CD Pipelines** - Automated deployment workflows
- **Power Platform** - Low-code application development (Power Apps, Power Automate)
- **Shared Packages** - Modular code architecture for reusable components
- **Centralized Logging** - Unified logging system for monitoring and debugging
- **Environment Management** - Configuration and deployment strategies for different environments (development, staging, production)

### Tools

- **GitHub** - Version control and collaboration
- **VS Code** - Primary development environment
- **Power Apps** - Low-code application development
- **Power Automate** - Workflow automation
- **PowerShell** - Command-line interface and scripting
- **Azure DevOps** - CI/CD and project management
- **Postman** - API testing and development

### Recommended Learning Path

**Phase 1: Foundation (Complete First)**
1. **Python Fundamentals** - Review syntax, data structures, functions
2. **Git/GitHub** - Version control, branching, pull requests
3. **Virtual Environments** - Python package management
4. **PowerShell** - Command-line proficiency
5. **VS Code** - IDE configuration and extensions

**Phase 2: Core Technologies**
1. **Azure Functions** - Serverless development patterns
2. **REST/GraphQL APIs** - API consumption and integration
3. **SQL** - Database querying and optimization
4. **JSON/YAML** - Data formats and configuration
5. **Logging** - Centralized logging practices

**Phase 3: Advanced Concepts**
1. **CI/CD Pipelines** - Automated deployment
2. **Azure Container Apps** - Container orchestration
3. **Power Platform** - Low-code development
4. **Shared Packages** - Package architecture patterns
5. **Environment Management** - Configuration strategies

### Codebase Implementation Examples

**Where to find these concepts in the codebase:**
- **Python**: `functions/*/`, `packages/jobe_shared/`
- **Azure Functions**: `functions/*/main.py`, `infrastructure/`
- **SQL**: `packages/jobe_shared/sql/`, `resources/sql/`
- **REST/GraphQL**: `packages/jobe_shared/api/saas/`
- **CI/CD**: `infrastructure/pipelines/`
- **Power Apps**: `app/environments/`
- **Logging**: `packages/jobe_shared/utils/centralized_logging.py`
- **Shared Packages**: `packages/jobe_shared/`
- **Configuration**: `infrastructure/environments/`

### Additional Technologies

Developers should also familiarize themselves with:
- **Azure CLI** - Azure resource management
- **Docker** - Containerization (for Container Apps)
- **Monday.com API** - Primary CRM integration
- **Microsoft Graph API** - Office 365 integration
- **D-Tools API** - Industry-specific integrations

---

---

## Quick Start Checklist

- [ ] Install required development tools
- [ ] Set up Azure DevOps access
- [ ] Clone the repository
- [ ] Configure local environment
- [ ] Install Python packages
- [ ] Set up authentication
- [ ] Run first test
- [ ] Review documentation

---

## Required Software Installation

### Core Development Tools

#### **Python Environment**
```bash
# Install Python 3.11 or later
# Download from: https://www.python.org/downloads/
python --version  # Should be 3.11+

# Install pip (usually included with Python)
pip --version
```

#### **Git Version Control**
```bash
# Install Git
# Download from: https://git-scm.com/downloads
git --version

# Configure Git (replace with your information)
git config --global user.name "Your Name"
git config --global user.email "your.email@company.com"
```

#### **Visual Studio Code**

**Important: Set PowerShell as Default Terminal**

Before proceeding, ensure your terminal is set to use PowerShell as the default. This is the standard for this codebase.

1. **Download and install VS Code**: https://code.visualstudio.com/
2. **Configure PowerShell as default terminal**:
   - Open VS Code
   - Press `Ctrl + Shift + P` to open Command Palette
   - Type "Terminal: Select Default Profile"
   - Select "PowerShell"

**Required Extensions:**

Install these essential extensions for optimal development experience:

- **Prettier** - Code formatting
- **Better Comments** - Enhanced comment highlighting
- **Peacock** - Workspace color themes
- **Black Formatter** - Python code formatting
- **Error Lens** - Inline error display
- **GitLens** - Enhanced Git integration
- **Python** - Core Python development
- **Azure Tools** - Azure development support
- **Azure Functions** - Azure Functions development

**Configure Standard Settings:**

1. **Import VS Code Standard Settings**:
   - Press `Ctrl + Shift + P`
   - Type "Preferences: Open User Settings (JSON)"
   - Copy the contents from `resources\setup\vs-code-standard-settings-DEFAULT.json`
   - Paste into your user settings file

2. **Install VS Code Profiles**:
   - Navigate to `resources\setup\vs-code-profiles\`
   - Import the following profiles based on your development focus:
     - `code.code-profile` - General development
     - `data.code-profile` - Data science and analytics
     - `ui.code-profile` - User interface development
     - `web.code-profile` - Web development
     - `docs.code-profile` - Documentation writing
     - `cad.code-profile` - CAD and design work

**PowerShell Terminal Commands:**

All terminal commands in this guide use PowerShell syntax. Examples:

```powershell
# PowerShell commands (use these)
Get-Location
Set-Location "C:\path\to\directory"
Get-ChildItem

# NOT bash commands
pwd
cd /path/to/directory
ls
```

#### **Azure CLI**
```bash
# Install Azure CLI
# Download from: https://learn.microsoft.com/en-us/cli/azure/install-azure-cli
az --version

# Login to Azure (will be configured later)
az login
```

#### **Azure Functions Core Tools**
```bash
# Install Azure Functions Core Tools
npm install -g azure-functions-core-tools@4 --unsafe-perm true

# Verify installation
func --version
```

#### **Power Platform CLI (for Power Apps development)**
```bash
# Install Power Platform CLI
npm install -g @microsoft/powerapps-cli

# Verify installation
pac --version
```

---

## Access Requirements and Authentication

### Required Access Permissions

To work with this codebase, you'll need access to the following systems:

#### **Azure DevOps Access**
- **Organization**: `jobe-systems`
- **Project**: `js-codebase`
- **Repository**: `js-codebase`
- **Required Permissions**: 
  - Repository: Read, Contribute
  - Pipelines: Read, Execute
  - Variable Groups: Read

**To Request Access:**
1. Contact Jarrod K. for access permissions and general guidance
2. Provide your Microsoft work account email
3. Specify required permissions level

#### **Azure Subscription Access**
- **Subscription**: Azure Jobe Systems Subscription
- **Required Permissions**:
  - **Development Environment**: Contributor access to development resource group
  - **Staging Environment**: Reader access (unless specifically assigned)
  - **Production Environment**: Reader access only (DevOps team manages)

**To Request Access:**
1. Contact Jarrod K. for Azure access
2. Specify which environments you need access to
3. Justify access level required

#### **SaaS Platform Access (for development/testing)**
- **Monday.com**: Developer workspace access
- **D-Tools Cloud**: Development environment API access
- **Power Platform**: Development environment access

**To Request Access:**
1. Contact Jarrod K. for SaaS platform access
2. Request development/testing environment access
3. Obtain API tokens and workspace IDs

---

## Repository Setup

### Clone the Repository

```powershell
# Clone from Azure DevOps (primary repository)
git clone https://jobe-systems@dev.azure.com/jobe-systems/js-codebase/_git/js-codebase

# Navigate to project directory
Set-Location js-codebase

# Verify repository structure
Get-ChildItem
```

### Set Up Development Branch

```powershell
# Create and switch to your development branch
git checkout -b feature/your-name-getting-started

# Set up remote tracking
git push -u origin feature/your-name-getting-started
```

---

## Local Environment Configuration

### Python Virtual Environment

```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment (PowerShell)
.venv\Scripts\Activate.ps1

# Verify activation
Get-Command python  # Should point to .venv directory
```

### Install Shared Packages

```powershell
# Install shared packages in development mode
pip install -e packages/jobe_shared
pip install -e packages/jobe_workflows

# Install additional development dependencies
pip install -r requirements.txt

# Verify installations
pip list | Select-String "jobe"
```

### Environment Variables Setup

#### **Create Local Environment Files**

1. **Copy shared configuration**:
```powershell
Copy-Item infrastructure/environments/shared/config/.env.shared .env.shared
```

2. **Copy development configuration**:
```powershell
Copy-Item infrastructure/environments/development/config/.env.development .env.development
```

3. **Create local secrets file**:
```powershell
# Copy template (never commit this file)
Copy-Item infrastructure/environments/development/secrets/.env.secrets.example infrastructure/environments/development/secrets/.env.secrets
```

4. **Edit secrets file with your credentials**:
```powershell
# Edit the secrets file with your API tokens
code infrastructure/environments/development/secrets/.env.secrets
```

#### **Required Environment Variables**

You'll need to obtain and configure the following:

```bash
# Monday.com API
MONDAY_API_TOKEN=your_monday_api_token_here

# Azure Configuration
AZURE_SUBSCRIPTION_ID=your_azure_subscription_id
AZURE_TENANT_ID=your_azure_tenant_id

# D-Tools API (if working with D-Tools integration)
DTOOLS_CLOUD_API_TOKEN=your_dtools_api_token

# Database connections (development)
AZURE_SQL_CONNECTION_STRING=your_dev_database_connection
```

**To Obtain API Tokens:**
1. **Monday.com**: Go to Admin → API → Generate new token
2. **D-Tools**: Contact your D-Tools administrator
3. **Azure**: Use Azure CLI: `az account show`

---

## Authentication Setup

### Azure Authentication

```bash
# Login to Azure CLI
az login

# Set default subscription (use your development subscription)
az account set --subscription "your-dev-subscription-id"

# Verify access
az account show
```

### Power Platform Authentication

```bash
# Authenticate to Power Platform (development environment)
pac auth create --url https://jobedev.crm.dynamics.com

# Verify connection
pac org who

# List available environments
pac env list
```

### Azure DevOps Authentication

```bash
# Install Azure DevOps extension for Azure CLI
az extension add --name azure-devops

# Configure Azure DevOps
az devops configure --defaults organization=https://dev.azure.com/jobe-systems project=js-codebase

# Verify access
az repos list
```

---

## Verify Your Setup

### Test Environment Configuration

```bash
# Test environment variable loading
python -c "import os; print(f'Environment: {os.getenv(\"ENVIRONMENT\", \"not set\")}')")

# Test shared package imports
python -c "from jobe_shared.config.monday_config import MondayConfig; print('Package import successful')"

# Test configuration access
python -c "from jobe_shared.config.monday_config import MondayConfig; print(f'API Token configured: {\"Yes\" if MondayConfig.api_token() else \"No\"}')"
```

### Run a Simple Test Function

Create a test file to verify everything is working:

```python
# Create test_setup.py
from jobe_shared.utils.startup import program_start, program_end
from jobe_shared.config.monday_config import MondayConfig

def test_setup():
    logger = program_start(
        program_name="Setup Test",
        version="1.0.0",
        creator="Your Name"
    )
    
    try:
        # Test configuration
        logger.info("Testing configuration access...")
        api_token = MondayConfig.api_token()
        
        if api_token:
            logger.info("✅ Monday.com API token configured")
        else:
            logger.warning("⚠️ Monday.com API token not configured")
            
        logger.info("✅ Setup test completed successfully")
        
    except Exception as e:
        logger.error(f"❌ Setup test failed: {str(e)}")
        raise
    finally:
        program_end(logger, "Setup Test")

if __name__ == "__main__":
    test_setup()
```

```bash
# Run the test
python test_setup.py
```

---

## Essential Documentation to Review

After completing the setup, review these documents in order:

### **1. Architecture Understanding**
- **[Repository Structure Guide](../processes/repository-structure-guide.md)** - Folder organization
- **[Environment Implementation Architecture](../technical/environment_implementation_architecture.md)** - Environment configuration

### **2. Development Workflows**
- **[Git Usage Guide](../processes/git-usage-guide.md)** - Development standards and workflows
- **[AI Development Workflow](../processes/ai-development-workflow.md)** - AI-assisted development patterns

### **3. Technical Implementation**
- **[Centralized Logging Architecture](../technical/centralized_logging_architecture.md)** - Logging implementation
- **Shared Package Documentation** - Review `packages/jobe_shared/` structure
- **Function Examples** - Examine existing functions in `functions/` directory

### **4. Business Context**
- **[Jobe Systems Internal Project Process](../processes/jobe-systems-project-process.md)** - Business workflow understanding
- **[Power Apps Extraction Guide](../processes/power-apps-extraction-guide.md)** - Power Platform development

---

## Your First Development Task

### Create a Simple "Hello World" Function

1. **Create a new function directory**:
```powershell
New-Item -ItemType Directory -Path functions/hello_world_yourname
Set-Location functions/hello_world_yourname
```

2. **Create basic structure**:
```powershell
# Create main.py
New-Item -ItemType File -Name main.py

# Create requirements.txt
Set-Content -Path requirements.txt -Value "-e ../../packages/jobe_shared"

# Create app directory
New-Item -ItemType Directory -Path app/src -Force
```

3. **Implement a simple HTTP function**:
```python
# main.py
import azure.functions as func
import json
from datetime import datetime
from jobe_shared.utils.startup import program_start, program_end

app = func.FunctionApp()

@app.function_name("hello_world_http")
@app.route(route="hello", auth_level=func.AuthLevel.FUNCTION)
def hello_world_http(req: func.HttpRequest) -> func.HttpResponse:
    logger = program_start(
        program_name="Hello World Function",
        version="1.0.0",
        creator="Your Name"
    )
    
    try:
        name = req.params.get('name') or 'World'
        logger.info(f"Hello World function called with name: {name}")
        
        response_data = {
            "message": f"Hello, {name}!",
            "timestamp": datetime.now().isoformat(),
            "function": "hello_world_http",
            "developer": "Your Name"
        }
        
        logger.info("Hello World function completed successfully")
        
        return func.HttpResponse(
            json.dumps(response_data),
            status_code=200,
            headers={"Content-Type": "application/json"}
        )
        
    except Exception as e:
        logger.error(f"Hello World function failed: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            headers={"Content-Type": "application/json"}
        )
    finally:
        program_end(logger, "Hello World Function")
```

4. **Test locally**:
```powershell
# Install dependencies
pip install -r requirements.txt

# Start local Azure Functions host
func start

# Test in another terminal
Invoke-WebRequest -Uri "http://localhost:7071/api/hello?name=YourName"
```

5. **Commit your changes**:
```powershell
git add .
git commit -m "feat(hello-world): add hello world function for new developer setup"
git push origin feature/your-name-getting-started
```

---

## Common Issues and Solutions

### **Python Import Errors**
**Issue**: `ModuleNotFoundError: No module named 'jobe_shared'`  
**Solution**: 
```powershell
# Ensure you're in the virtual environment
.venv\Scripts\Activate.ps1

# Reinstall packages in development mode
pip install -e packages/jobe_shared
pip install -e packages/jobe_workflows
```

### **Environment Variable Issues**
**Issue**: Configuration not loading properly  
**Solution**: 
```powershell
# Check environment variable setup
python -c "import os; print(os.getenv('ENVIRONMENT', 'not set'))"

# Verify .env files exist and are properly formatted
Get-ChildItem infrastructure/environments/development/config/
```

### **Azure Authentication Issues**
**Issue**: Azure CLI authentication failures  
**Solution**: 
```bash
# Clear existing authentication
az logout

# Re-authenticate
az login

# Verify account and subscription
az account show
```

### **API Token Issues**
**Issue**: API calls failing with authentication errors  
**Solution**: 
1. Verify API tokens are correct and not expired
2. Check token permissions in the respective platforms
3. Ensure tokens are properly set in environment files

---

## Getting Help

### **Internal Resources**
- **Jarrod K.**: For access permissions, questions, and general guidance
- **DevOps Team**: For Azure and deployment issues
- **Senior Developers**: For code review and architecture questions

### **Documentation Resources**
- **Technical Documentation**: `resources/docs/technical/`
- **Process Documentation**: `resources/docs/processes/`
- **User Guides**: `resources/docs/user-guides/`

### **External Resources**
- **Azure Functions Documentation**: https://docs.microsoft.com/en-us/azure/azure-functions/
- **Monday.com API Documentation**: https://developer.monday.com/
- **Power Platform Documentation**: https://docs.microsoft.com/en-us/power-platform/

---

## Next Steps

After completing this setup:

1. **Complete the hello world function** and test it thoroughly
2. **Review the technical documentation** listed above
3. **Examine existing functions** in the `functions/` directory
4. **Understand the business processes** by reviewing the project process documentation
5. **Practice using the Git workflow** with a simple feature branch
6. **Set up your development environment** for ongoing work
7. **Connect with your team** to understand current priorities and projects

---

You're now ready to start contributing to the Jobe Systems API Codebase. This platform plays a crucial role in automating business processes and integrating multiple systems to improve operational efficiency.

Remember to:
- Follow the established development patterns
- Use the centralized logging system
- Test thoroughly in the development environment
- Document your code and processes
- Ask Jarrod K. questions when you need help

---

*This guide covers the essential setup for new developers. For specific implementation details, always reference the linked technical documentation.*
