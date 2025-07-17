# Git Usage Guide

**Process Documentation - Data Centralization Platform Demo**

*Version: 1.0*  
*Created: January 17, 2025*  
*Last Updated: January 17, 2025*  
*Status: Current Implementation*

---

## Executive Summary

This document establishes standardized Git workflows and practices for the Data Centralization Platform demonstration repository. As a public showcase of professional development skills, this repository maintains the highest standards for commit history, branching strategy, and code organization while serving as a technical portfolio piece.

**Key Standards:**
- Conventional Commits format optimized for AI agent training
- Solo developer branching strategy with public visibility focus
- Professional commit history demonstrating technical expertise
- AI agent-friendly documentation and workflow patterns
- Strategic commits that showcase incremental development progress

---

## 📝 Commit Message Standards

This project uses the **Conventional Commits** format to ensure clean, readable commit history and compatibility with changelog generators and CI tools.

## ✅ Format

<type>(optional-scope): short summary

- `type`: the kind of change being made (see below)
- `scope`: optional, describes the area of the code affected (e.g., `auth`, `api`, `ui`)
- `summary`: a concise, imperative description (e.g., `add login validation`, not `added` or `adds`)

---

## 📦 Commit Types

| Type       | Description                                                         | Demo Platform Context |
| ---------- | ------------------------------------------------------------------- | --------------------- |
| `feat`     | A new feature                                                       | New API integrations, correlation analysis features |
| `fix`      | A bug fix                                                           | Data processing issues, API client fixes |
| `docs`     | Documentation changes only                                          | LLM knowledge base updates, README improvements |
| `style`    | Code style updates (e.g., formatting, spacing, no logic changes)    | Code formatting, linting fixes |
| `refactor` | Code restructuring that doesn't change behavior (e.g., DRYing code) | Microservices reorganization, code optimization |
| `perf`     | Performance improvements                                            | Database query optimization, API response improvements |
| `test`     | Adding or updating tests                                            | Unit tests, integration tests, correlation validation |
| `chore`    | Miscellaneous tasks like dependency bumps, cleanup, config updates  | Dependency updates, configuration changes |
| `build`    | Changes that affect the build system or external dependencies       | Docker configuration, CI/CD pipeline updates |
| `data`     | Changes to data collection, processing, or storage                  | New data sources, ETL pipeline modifications |
| `analysis` | Statistical analysis and correlation discovery                      | Correlation algorithms, significance testing |
| `llm`      | LLM integration and embedding-related changes                       | RAG pipeline, embedding generation, prompt engineering |
| `viz`      | Data visualization and dashboard updates                            | Plotly charts, interactive dashboards, Notion reports |
| `ai`       | AI agent training and knowledge base updates                        | Training data, agent behavior modifications |

---

## 🔍 Examples

**Core Platform Development:**
```bash
feat(spotify): add audio feature correlation analysis
fix(postgres): resolve pgvector index performance issue
docs(llm): update embedding generation guide
style: format correlation analysis with Black and isort
refactor(api): simplify multi-domain data linking logic
perf: optimize vector similarity search queries
test(correlation): add significance testing validation
chore: bump scipy to 1.12.0 for statistical analysis
build: update Docker compose for pgvector extension
```

**Data-Specific Examples:**
```bash
data(weather): integrate OpenWeatherMap historical data
analysis(music): implement weather-mood correlation detection
llm(embeddings): generate semantic vectors for correlation insights
viz(dashboard): create interactive correlation heatmaps
ai(training): update agent knowledge base with new correlations
```

**AI Agent Training Examples:**
```bash
ai(knowledge): add statistical significance interpretation guide
llm(rag): implement correlation context enrichment pipeline
ai(prompt): optimize causation warning generation
llm(search): improve semantic similarity for insights
```

---

## 🛠 Commit Best Practices

- Limit the summary to **72 characters or fewer**
- Use **present tense** and **imperative mood** (e.g., "add", not "added")
- Capitalization: lowercase after the colon unless it's a proper noun
- Keep your commit history clean and focused—**one purpose per commit**
- Reference issues when applicable: `fix(auth): resolve login timeout #123`
- Use conventional scopes consistently across the project

---

## 🌿 Branching Strategy

### Solo Developer Public Repository Strategy

#### **Primary Branches**
- **`main`** - Production-ready code, showcases completed features
- **`development`** - Active development branch for ongoing work
- **`experiments`** - Experimental features and proof-of-concepts

#### **Feature Development Branches**
```bash
# Format: feature/domain-specific-description
feature/spotify-audio-analysis
feature/weather-correlation-engine
feature/llm-embedding-pipeline
feature/notion-report-automation
feature/statistical-significance-testing
```

#### **Data Source Integration Branches**
```bash
# Format: data/source-integration
data/github-activity-collector
data/tmdb-entertainment-pipeline
data/pokemon-cultural-patterns
data/musicbrainz-metadata-enrichment
```

#### **Analysis Feature Branches**
```bash
# Format: analysis/correlation-type
analysis/cross-domain-temporal-patterns
analysis/weather-music-mood-correlation
analysis/entertainment-developer-productivity
analysis/cultural-environmental-connections
```

#### **LLM Integration Branches**
```bash
# Format: llm/functionality-description
llm/rag-correlation-context
llm/embedding-similarity-search
llm/statistical-narrative-generation
llm/causation-warning-system
```

#### **Visualization Branches**
```bash
# Format: viz/dashboard-component
viz/correlation-heatmap-dashboard
viz/interactive-time-series-charts
viz/geographic-correlation-maps
viz/notion-embedded-visualizations
```

### Solo Development Workflow

#### **For New Features (Public Portfolio Approach)**

1. **Create Feature Branch**:
   ```bash
   git checkout development
   git pull origin development
   git checkout -b feature/correlation-discovery-engine
   ```

2. **Incremental Development with Strategic Commits**:
   ```bash
   # Initial structure
   git add .
   git commit -m "feat(analysis): initialize correlation discovery framework"
   
   # Add statistical foundation
   git add .
   git commit -m "feat(analysis): implement statistical significance testing"
   
   # Add cross-domain linking
   git add .
   git commit -m "feat(analysis): add temporal alignment for correlation analysis"
   
   # Add causation evaluation
   git add .
   git commit -m "feat(analysis): implement causation likelihood assessment"
   ```

3. **Test and Validate**:
   ```bash
   # Add comprehensive tests
   git add .
   git commit -m "test(analysis): add correlation significance validation tests"
   
   # Add documentation
   git add .
   git commit -m "docs(analysis): document correlation discovery methodology"
   ```

4. **Merge to Development**:
   ```bash
   git checkout development
   git merge feature/correlation-discovery-engine
   git push origin development
   ```

5. **Promote to Main (Production Demo)**:
   ```bash
   git checkout main
   git merge development
   git push origin main
   git tag -a v1.2.0 -m "Release: Advanced correlation discovery engine"
   git push origin v1.2.0
   ```

#### **For AI Agent Training Updates**

1. **Quick AI Knowledge Updates**:
   ```bash
   git checkout development
   git add .
   git commit -m "ai(knowledge): update statistical interpretation guidelines"
   git push origin development
   ```

2. **LLM Pipeline Improvements**:
   ```bash
   git checkout -b llm/embedding-optimization
   git add .
   git commit -m "llm(embeddings): optimize vector similarity search performance"
   git push origin llm/embedding-optimization
   ```

---

## 🤖 AI Agent Integration Workflow

### AI-Assisted Development Process

This repository serves as a training ground for AI agents, with specific workflows designed to facilitate AI understanding and contribution.

#### **AI Agent Setup Commands**
```bash
# Initialize AI development environment
cd D:\repo\codebase\demo-codebase
code demo-codebase  # Opens VS Code with project settings

# Activate AI agent context
source .ai/agent-context.sh
```

#### **AI Knowledge Base Updates**

1. **Before AI Agent Work**:
   ```bash
   # Ensure latest AI knowledge base
   git pull origin main
   
   # Review current correlation insights
   python -m tools.ai.knowledge_sync
   ```

2. **During AI Development**:
   ```bash
   # AI-guided commits with detailed context
   git add .
   git commit -m "llm(embeddings): implement multi-domain correlation embedding generation
   
   - Added semantic vector generation for weather-music correlations
   - Implemented statistical context enrichment for embedding quality
   - Added causation evaluation features for responsible AI responses
   
   Context: This enhances AI agent ability to understand cross-domain relationships
   while maintaining statistical rigor and avoiding correlation-causation confusion."
   ```

3. **AI Agent Validation**:
   ```bash
   # Validate AI agent understanding
   python -m tools.ai.validate_agent_knowledge
   
   # Test correlation interpretation
   python -m tools.ai.test_correlation_responses
   ```

### Portfolio Development Strategy

#### **Public Repository Considerations**
- **Professional Commit History**: Every commit demonstrates technical expertise
- **Clear Progress Documentation**: Commits tell the story of feature development
- **AI Training Transparency**: Show how AI agents learn from structured data
- **Statistical Rigor**: Emphasize responsible data science practices

#### **Strategic Commit Patterns**
```bash
# Show architectural thinking
feat(architecture): implement microservices pattern for data collection

# Demonstrate statistical expertise
analysis(statistics): add rigorous significance testing with confidence intervals

# Show AI integration skills
llm(integration): implement RAG pipeline with pgvector semantic search

# Demonstrate business value
viz(insights): create interactive correlation dashboard for business intelligence
```

---

## 🧠 AI Agent Review Process

### AI-Assisted Code Review Standards

As a solo developer with AI agent assistance, the review process focuses on training AI agents to understand and validate code quality.

#### **AI Agent Review Checklist**
```python
# AI Agent Review Criteria
review_criteria = {
    "statistical_rigor": {
        "correlation_analysis": "Includes significance testing and confidence intervals",
        "causation_warnings": "Explicitly warns against correlation-causation confusion",
        "sample_size_validation": "Validates minimum sample size for statistical power"
    },
    "code_quality": {
        "type_safety": "All functions include proper type hints",
        "error_handling": "Comprehensive exception handling with logging",
        "documentation": "Docstrings explain statistical methodology"
    },
    "ai_integration": {
        "embedding_quality": "Vector embeddings capture semantic meaning",
        "rag_pipeline": "Retrieval provides relevant statistical context",
        "response_validation": "AI responses include uncertainty quantification"
    },
    "portfolio_value": {
        "technical_demonstration": "Code showcases advanced technical skills",
        "business_relevance": "Features address real-world data integration needs",
        "innovation_showcase": "Implementation demonstrates creative problem-solving"
    }
}
```

#### **Self-Review Process with AI Assistance**

1. **Statistical Review**:
   ```bash
   # Validate correlation analysis
   python -m tools.validation.statistical_review
   
   # Check significance testing
   python -m tools.validation.significance_check
   
   # Verify causation warnings
   python -m tools.validation.causation_compliance
   ```

2. **AI Agent Response Testing**:
   ```bash
   # Test AI correlation interpretation
   python -m services.llm_integration.test_correlation_responses
   
   # Validate embedding quality
   python -m services.llm_integration.test_embedding_similarity
   
   # Check RAG pipeline accuracy
   python -m services.llm_integration.test_rag_relevance
   ```

3. **Code Quality Validation**:
   ```bash
   # Type checking
   mypy packages/shared_core/
   
   # Statistical analysis validation
   pytest development/testing/statistical_tests/
   
   # Integration testing
   pytest development/testing/integration_tests/
   ```

### Professional Portfolio Standards

#### **Public Repository Excellence**
- **Code Quality**: Every commit demonstrates professional development practices
- **Technical Depth**: Features showcase advanced data science and AI integration skills
- **Documentation**: Clear explanations of complex statistical and AI concepts
- **Innovation**: Creative approaches to cross-domain data correlation
- **Responsibility**: Emphasis on ethical AI and statistical interpretation

#### **AI Agent Training Value**
- **Statistical Education**: Code teaches proper correlation vs. causation interpretation
- **Technical Integration**: Demonstrates how to integrate LLMs with data science workflows
- **Quality Assurance**: Shows how AI agents can validate statistical methodology
- **Business Context**: Connects technical implementation to real-world business value

---

## 🚀 Deployment Workflows

### Environment-Specific Deployment

#### **Development Environment**
- **Trigger**: Push to `development` branch
- **Auto-Deploy**: Yes
- **Approval**: Not required
- **Testing**: Unit tests + integration tests

#### **Staging Environment**
- **Trigger**: Push to `staging` branch
- **Auto-Deploy**: Yes
- **Approval**: Not required
- **Testing**: Full test suite + performance tests

#### **Production Environment**
- **Trigger**: Push to `main` branch
- **Auto-Deploy**: No
- **Approval**: Required (DevOps team)
- **Testing**: All tests + manual validation

### Deployment Commands

```bash
# Deploy to development
git checkout development
git merge feature/your-feature
git push origin development

# Deploy to staging
git checkout staging
git merge development
git push origin staging

# Deploy to production (requires PR and approval)
git checkout main
# Create PR from staging to main
# Wait for approval and merge
```

---

## 🛡️ Security and Compliance

### Public Repository Security Standards

#### **Never Commit (Critical for Public Repos)**:
- API keys and tokens (use environment variables)
- Database credentials or connection strings
- Personal information or private data
- Temporary debugging files with sensitive data
- Real production data (use synthetic/anonymized data)
- Private API responses (sanitize before committing)

#### **Demo-Safe .gitignore**:
```gitignore
# Environment files
.env
.env.local
.env.*.local
.env.production
.env.development

# API keys and secrets
api_keys/
secrets/
*.key
*.pem
*.p12

# Database files
*.db
*.sqlite
*.sqlite3
data/raw/personal/

# Temporary files
*.tmp
*.log
*.cache
.DS_Store
Thumbs.db

# AI model files (too large for git)
models/
*.model
*.pkl
*.joblib

# IDE and OS files
.vscode/settings.json
.idea/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# Data analysis outputs
outputs/
results/
*.ipynb_checkpoints

# Vector embeddings (regenerate as needed)
data/embeddings/vectors/
*.npy
*.npz
```

### AI Agent Security Considerations

#### **Safe AI Training Data**:
```python
# Sanitize data before AI training
def sanitize_for_ai_training(data: Dict) -> Dict:
    """
    Remove sensitive information from data before AI processing
    """
    sanitized = data.copy()
    
    # Remove personal identifiers
    sensitive_fields = ['user_id', 'email', 'phone', 'address']
    for field in sensitive_fields:
        if field in sanitized:
            sanitized[field] = '[REDACTED]'
    
    # Anonymize API responses
    if 'api_response' in sanitized:
        sanitized['api_response'] = anonymize_api_response(sanitized['api_response'])
    
    return sanitized
```

#### **Public Demo Data Strategy**:
- **Synthetic Correlations**: Generate realistic but artificial data patterns
- **Anonymized Samples**: Use anonymized versions of real data
- **Public APIs Only**: Exclusively use publicly available data sources
- **Statistical Demonstrations**: Focus on methodology rather than sensitive insights

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Run manually
pre-commit run --all-files
```

**Hook Configuration** (`.pre-commit-config.yaml`):
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: detect-private-key
```

---

## 📋 Git Configuration Standards

### Professional Portfolio Configuration

```bash
# Set professional identity
git config --global user.name "Jarrod Knapp"
git config --global user.email "soundstate8@gmail.com"

# Set default branch
git config --global init.defaultBranch main

# Set editor for detailed commits
git config --global core.editor "code --wait"

# Professional commit template
git config --global commit.template ~/.gitmessage.txt

# Line ending handling (Windows development)
git config --global core.autocrlf true

# Enhanced diff and merge tools
git config --global diff.tool vscode
git config --global merge.tool vscode
git config --global difftool.vscode.cmd 'code --wait --diff $LOCAL $REMOTE'
git config --global mergetool.vscode.cmd 'code --wait $MERGED'
```

### Professional Commit Message Template

Create `~/.gitmessage.txt`:
```text
# <type>(<scope>): <subject>
#
# <body>
#
# <footer>
# 
# Type: feat, fix, docs, style, refactor, perf, test, chore, data, analysis, llm, viz, ai
# Scope: component or feature area
# Subject: imperative, present tense, no period, max 50 chars
# Body: explain what and why, not how (wrap at 72 chars)
# Footer: reference issues, breaking changes
#
# Examples:
# feat(correlation): implement weather-music mood analysis
# fix(database): resolve pgvector index performance issue
# docs(ai): update LLM integration guidelines
# analysis(stats): add statistical significance testing
```

### Repository Configuration

```bash
# Set upstream tracking
git branch --set-upstream-to=origin/development development

# Configure merge strategy
git config merge.tool vscode
git config mergetool.vscode.cmd 'code --wait $MERGED'

# Set commit message template
git config commit.template .gitmessage.txt
```

### Demo-Optimized Aliases

```bash
# Core workflow aliases
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.unstage 'reset HEAD --'

# Professional development aliases
git config --global alias.last 'log -1 HEAD --stat'
git config --global alias.hist 'log --oneline --graph --decorate --all'
git config --global alias.pushf 'push --force-with-lease'
git config --global alias.visual '!gitk'

# Portfolio-specific aliases
git config --global alias.demo 'log --oneline --graph --decorate -10'
git config --global alias.features 'branch -a | grep feature'
git config --global alias.releases 'tag -l | sort -V'
git config --global alias.stats 'log --stat --oneline -5'

# AI development aliases
git config --global alias.ai-commit 'commit -m "ai(knowledge): update agent training data"'
git config --global alias.llm-branch 'checkout -b llm/'
git config --global alias.correlation-log 'log --grep="correlation" --oneline'
```

---

## 🔧 Advanced Git Operations

### Handling Large Files

```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.msapp"
git lfs track "*.zip"
git lfs track "*.pdf"

# Commit .gitattributes
git add .gitattributes
git commit -m "chore: configure Git LFS for large files"
```

### Cleaning Up History

```bash
# Interactive rebase to clean up commits
git rebase -i HEAD~3

# Squash multiple commits
git reset --soft HEAD~3
git commit -m "feat(auth): implement complete authentication system"

# Force push (use with caution)
git push --force-with-lease origin feature/your-branch
```

### Resolving Conflicts

```bash
# Start merge
git merge feature/other-branch

# Resolve conflicts manually or with tool
git mergetool

# Complete merge
git add .
git commit -m "Merge feature/other-branch into development"
```

---

## 📊 Repository Maintenance

### Regular Maintenance Tasks

#### **Weekly**:
- Review and merge approved PRs
- Clean up merged branches
- Update documentation
- Run security scans

#### **Monthly**:
- Review branch protection rules
- Update dependencies
- Analyze commit patterns
- Archive old branches

#### **Quarterly**:
- Review Git workflow effectiveness
- Update branching strategy if needed
- Team training on new Git features
- Repository performance optimization

### Cleanup Commands

```bash
# Remove merged branches
git branch --merged | grep -v "\*\|main\|development" | xargs -n 1 git branch -d

# Clean up remote tracking branches
git remote prune origin

# Garbage collection
git gc --aggressive --prune=now

# Check repository size
git count-objects -vH
```

---

## 🚨 Emergency Procedures

### Rollback Procedures

#### **Revert Last Commit**:
```bash
git revert HEAD
git push origin main
```

#### **Rollback to Specific Commit**:
```bash
git reset --hard commit-hash
git push --force-with-lease origin main
```

#### **Emergency Hotfix**:
```bash
# Create hotfix branch from main
git checkout main
git pull origin main
git checkout -b hotfix/critical-fix

# Make fix and commit
git add .
git commit -m "fix: resolve critical production issue"

# Deploy immediately
git push origin hotfix/critical-fix
# Create PR and merge immediately
```

### Recovery Procedures

#### **Recover Deleted Branch**:
```bash
# Find the commit hash
git reflog

# Recreate branch
git checkout -b recovered-branch commit-hash
```

#### **Recover Lost Commits**:
```bash
# Find lost commits
git fsck --lost-found

# Cherry-pick specific commits
git cherry-pick commit-hash
```

---

## 📈 Performance Optimization

### Repository Performance

```bash
# Check repository health
git fsck

# Optimize repository
git gc --aggressive

# Remove large files from history
git filter-branch --tree-filter 'rm -f large-file.zip' HEAD
```

### Workflow Performance

- **Shallow Clones**: Use `git clone --depth 1` for CI/CD
- **Sparse Checkout**: Clone only needed directories
- **Parallel Operations**: Use `git fetch --jobs=4` for faster operations
- **Delta Compression**: Configure `git config core.deltaBaseCacheLimit 2g`

---

## 🎯 Success Metrics

### Key Performance Indicators

- **Commit Message Compliance**: >95% conventional commits
- **Branch Naming Compliance**: >98% correct naming
- **PR Review Time**: <24 hours average
- **Merge Conflicts**: <5% of PRs
- **Hot Fixes**: <1 per month
- **Failed Deployments**: <2% of deployment attempts

### Monitoring Tools

- **GitHub Insights**: Repository activity and contribution metrics
- **CI/CD Dashboards**: Deployment success rates
- **Code Quality Tools**: SonarCloud integration
- **Security Scans**: Automated vulnerability detection

---

## 🔗 Related Documentation

- [LLM Project Knowledge Base](../ai/llm-project-knowledgebase.md)
- [Data Centralization Platform Architecture](../technical/platform-architecture.md)
- [Statistical Analysis Standards](../technical/statistical-methodology.md)
- [AI Agent Training Guidelines](../ai/agent-training-guide.md)
- [Correlation Discovery Methodology](../technical/correlation-methodology.md)

---

## 🎯 Portfolio Success Metrics

### Professional Demonstration Goals

- **Technical Expertise**: Git history demonstrates advanced data science and AI integration skills
- **Statistical Rigor**: Commits show proper statistical methodology and causation awareness
- **AI Innovation**: Repository showcases cutting-edge LLM integration techniques
- **Business Value**: Features address real-world data integration challenges
- **Code Quality**: Professional development practices throughout

### AI Agent Training Success

- **Knowledge Transfer**: AI agents learn proper statistical interpretation from commit history
- **Methodology Understanding**: Agents understand correlation vs. causation principles
- **Technical Integration**: Agents can contribute to complex data science workflows
- **Quality Assurance**: Agents validate statistical methodology in code reviews

---

*This document serves as the definitive guide for Git usage standards and practices in the Data Centralization Platform demonstration repository, optimized for professional portfolio presentation and AI agent training.*
