# Development Directory

This directory contains all development-related files organized logically to separate demo, testing, tools, and example code from the production codebase.

## 📁 Directory Structure

```
development/
├── README.md                    # This file - development guide
├── demos/                       # Demo scripts and interactive demonstrations
│   ├── data/                   # Demo data files and generators
│   ├── interactive/            # Interactive demos (Streamlit, Dash, etc.)
│   ├── outputs/                # Generated visualization files and results
│   ├── visualization/          # Visualization testing and demos
│   ├── correlation_analysis_demo.py
│   ├── create_demo_scenarios.py
│   └── create_demo_video_guide.py
├── testing/                     # All test files and testing utilities
│   ├── functional/             # End-to-end functional tests
│   ├── integration/            # Integration tests
│   ├── oauth/                  # OAuth authentication tests
│   └── unit/                   # Unit tests
├── tools/                       # Development tools and utilities
│   ├── generators/             # Code and structure generators
│   ├── scripts/                # Development scripts
│   └── utilities/              # Utility functions and helpers
├── examples/                    # Example implementations
│   ├── api_clients/            # API client examples
│   ├── data_collection/        # Data collection examples
│   └── visualization/          # Visualization examples
└── docs/                       # Development-specific documentation
```

## 🎯 Quick Navigation

### 🎬 Demos & Visualizations

**Location**: `development/demos/`

Run interactive demonstrations and generate visualizations:

```bash
# Run correlation analysis demo
cd development/demos
python correlation_analysis_demo.py

# Run interactive Streamlit dashboard
cd development/demos/interactive
streamlit run streamlit_dashboard.py

# Generate demo data
cd development/demos/data
python generate_demo_data.py

# Test visualization components
cd development/demos/visualization
python test_visualizations.py
```

**Key Files:**
- `correlation_analysis_demo.py` - Comprehensive correlation analysis demonstration
- `create_demo_scenarios.py` - Generate demo scenarios for presentations
- `create_demo_video_guide.py` - Create video content guides
- `interactive/streamlit_dashboard.py` - Interactive web dashboard
- `data/` - Contains demo data files and generators
- `outputs/` - Generated visualizations and HTML reports

### 🧪 Testing

**Location**: `development/testing/`

Run different types of tests:

```bash
# Run unit tests
cd development/testing/unit
python -m pytest

# Run integration tests
cd development/testing/integration
python -m pytest test_pokemon_*.py

# Run functional tests (like MusicBrainz API)
cd development/testing/functional
python test_musicbrainz_basic.py

# Test OAuth flow
cd development/testing/oauth
python test_oauth_flow.py
```

**Test Categories:**
- **unit/** - Fast, isolated unit tests
- **integration/** - Service integration tests (Pokemon GraphQL, etc.)
- **functional/** - End-to-end functionality tests
- **oauth/** - OAuth authentication flow tests

### 🔧 Development Tools

**Location**: `development/tools/`

Utility scripts and generators:

```bash
# Generate folder structure documentation
cd development/tools/generators
./generate_folder_structure.ps1

# Create presentation materials
cd development/tools/utilities
python create_presentation_materials.py

# Generate competitive analysis
python create_competitive_analysis.py
```

**Tool Categories:**
- **generators/** - Code and documentation generators
- **utilities/** - Business and presentation utilities
- **scripts/** - General development scripts

### 📚 Examples

**Location**: `development/examples/`

Reference implementations and code examples:

- **api_clients/** - Example API client implementations
- **data_collection/** - Data collection workflow examples
- **visualization/** - Chart and graph generation examples

## 🚀 Getting Started

### Prerequisites

1. **Python Environment**: Ensure you have Python 3.11+ with virtual environment activated
2. **Dependencies**: Install shared_core package in development mode:
   ```bash
   pip install -e packages/shared_core
   ```
3. **Environment Variables**: Set up your `.env` file from `infrastructure/environments/.env.example`

### Running Your First Demo

1. **Basic Setup Test**:
   ```bash
   cd development/testing/functional
   python test_musicbrainz_basic.py
   ```

2. **Interactive Dashboard**:
   ```bash
   cd development/demos/interactive
   pip install streamlit
   streamlit run streamlit_dashboard.py
   ```

3. **Correlation Analysis**:
   ```bash
   cd development/demos
   python correlation_analysis_demo.py
   ```

### Testing Workflow

1. **Unit Tests** - Test individual components:
   ```bash
   cd development/testing/unit
   python -m pytest test_setup.py -v
   ```

2. **Integration Tests** - Test service interactions:
   ```bash
   cd development/testing/integration
   python -m pytest test_pokemon_graphql.py -v
   ```

3. **Functional Tests** - Test complete workflows:
   ```bash
   cd development/testing/functional
   python test_musicbrainz_basic.py
   ```

## 📊 Demo Scenarios

The demos are organized by complexity and purpose:

### Level 1: Basic API Testing
- `testing/functional/test_musicbrainz_basic.py` - Basic API connectivity
- `testing/integration/test_pokemon_simple.py` - Simple GraphQL queries

### Level 2: Data Collection
- `demos/data/generate_demo_data.py` - Generate sample datasets
- Data collection service examples in `services/data_collection/`

### Level 3: Analysis & Visualization
- `demos/correlation_analysis_demo.py` - Statistical analysis
- `demos/visualization/test_visualizations.py` - Chart generation
- `demos/interactive/streamlit_dashboard.py` - Interactive web interface

### Level 4: Complete Workflows
- OAuth authentication flows
- End-to-end data pipeline demonstrations
- Business intelligence reporting

## 🔐 Authentication Testing

### MusicBrainz OAuth 2.0

1. **Setup**: Configure OAuth credentials in `.env`
2. **Test Basic Flow**:
   ```bash
   cd development/testing/oauth
   python test_oauth_flow.py
   ```
3. **Interactive Testing**:
   ```bash
   cd services/auth/musicbrainz_auth_service
   python main.py
   # Visit http://localhost:8000/auth/musicbrainz/login
   ```

## 🛠️ Development Tools Usage

### Structure Generation

Generate documentation for the current folder structure:

```bash
cd development/tools/generators
./generate_folder_structure.ps1 -OutputPath "current_structure.md"
```

### Presentation Materials

Create business presentation materials:

```bash
cd development/tools/utilities
python create_presentation_materials.py
python create_competitive_analysis.py
```

### Demo Content Creation

Generate demo scenarios and content:

```bash
cd development/demos
python create_demo_scenarios.py
python create_demo_video_guide.py
```

## 📈 Data Flow Examples

### 1. API Data Collection
```
API Client → Data Validation → Database Storage → Correlation Analysis
```

### 2. Visualization Pipeline
```
Raw Data → Processing → Statistical Analysis → Chart Generation → Interactive Dashboard
```

### 3. OAuth Authentication
```
User Request → Authorization Server → Token Exchange → Authenticated API Calls
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**:
   ```bash
   # Make sure shared_core is installed in development mode
   cd packages/shared_core
   pip install -e .
   ```

2. **Environment Variables**:
   ```bash
   # Copy example environment file
   cp infrastructure/environments/.env.example .env
   # Edit .env with your actual values
   ```

3. **Database Connections**:
   ```bash
   # Start required services
   make docker-up
   ```

4. **OAuth Issues**:
   ```bash
   # Verify Redis is running
   redis-cli ping
   # Check OAuth credentials
   python -c "from shared_core.config.musicbrainz_config import MusicBrainzConfig; print(MusicBrainzConfig.get_oauth_config())"
   ```

### Debug Mode

Enable debug logging for detailed output:

```bash
export DEBUG_MODE=true
export LOG_LEVEL=DEBUG
python your_demo_script.py
```

## 📋 Development Checklist

When adding new features:

- [ ] Add unit tests in `testing/unit/`
- [ ] Add integration tests if applicable in `testing/integration/`
- [ ] Create demo script in `demos/`
- [ ] Add documentation in `docs/` if needed
- [ ] Test with OAuth authentication if applicable
- [ ] Update this README if new directories are added

## 🤝 Contributing

When contributing to the development directory:

1. **Keep separation** - Production code stays in main directories
2. **Organize logically** - Use appropriate subdirectories
3. **Document examples** - Add clear documentation for demo code
4. **Test thoroughly** - Ensure demos and tests work reliably
5. **Update imports** - Fix any broken import statements after moving files

## 📚 Additional Resources

- **Main Project README**: `../README.md`
- **API Documentation**: `packages/shared_core/shared_core/api/clients/*/README.md`
- **MusicBrainz Setup Guide**: `packages/shared_core/shared_core/api/clients/musicbrainz/MUSICBRAINZ_OAUTH_SETUP.md`
- **Technical Documentation**: `resources/docs/technical/`
- **AI Development Guide**: `resources/docs/ai/`

---

**Happy Development! 🎉**

This organized structure helps maintain clean separation between production code and development/testing materials while making everything easily discoverable and runnable.
