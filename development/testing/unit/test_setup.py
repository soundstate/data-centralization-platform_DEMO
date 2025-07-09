"""Test setup verification for Data Centralization Platform."""

import sys
from pathlib import Path

import pytest


class TestSetup:
    """Test basic setup and configuration."""

    def test_python_version(self):
        """Test that Python version is 3.11 or higher."""
        assert sys.version_info >= (3, 11), f"Python 3.11+ required, got {sys.version}"

    def test_virtual_environment(self):
        """Test that we're running in a virtual environment."""
        assert hasattr(sys, "real_prefix") or (
            hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
        ), "Virtual environment not detected"

    def test_project_structure(self):
        """Test that key project directories exist."""
        project_root = Path.cwd()
        
        # Check core directories
        assert (project_root / "packages").exists(), "packages directory missing"
        assert (project_root / "services").exists(), "services directory missing"
        assert (project_root / "flows").exists(), "flows directory missing"
        assert (project_root / "data").exists(), "data directory missing"
        assert (project_root / "infrastructure").exists(), "infrastructure directory missing"
        
        # Check configuration files
        assert (project_root / "requirements.txt").exists(), "requirements.txt missing"
        assert (project_root / ".env.example").exists(), ".env.example missing"
        assert (project_root / "pyproject.toml").exists(), "pyproject.toml missing"
        assert (project_root / "pytest.ini").exists(), "pytest.ini missing"

    def test_core_imports(self):
        """Test that core dependencies can be imported."""
        try:
            import fastapi
            import pydantic
            import sqlalchemy
            import alembic
            import psycopg2
            import httpx
            import black
            import mypy
        except ImportError as e:
            pytest.fail(f"Core dependency import failed: {e}")

    def test_shared_core_structure(self):
        """Test that shared_core package structure exists."""
        project_root = Path.cwd()
        shared_core = project_root / "packages" / "shared_core"
        
        assert shared_core.exists(), "shared_core package missing"
        assert (shared_core / "shared_core").exists(), "shared_core/shared_core missing"
        assert (shared_core / "shared_core" / "api").exists(), "api directory missing"
        assert (shared_core / "shared_core" / "models").exists(), "models directory missing"
        assert (shared_core / "shared_core" / "config").exists(), "config directory missing"
        assert (shared_core / "shared_core" / "utils").exists(), "utils directory missing"

    def test_services_structure(self):
        """Test that services directory structure exists."""
        project_root = Path.cwd()
        services = project_root / "services"
        
        # Check service categories
        assert (services / "data_collection").exists(), "data_collection services missing"
        assert (services / "data_processing").exists(), "data_processing services missing"
        assert (services / "insights").exists(), "insights services missing"
        assert (services / "delivery").exists(), "delivery services missing"
        assert (services / "llm_integration").exists(), "llm_integration services missing"

    def test_data_directories(self):
        """Test that data directories exist."""
        project_root = Path.cwd()
        data = project_root / "data"
        
        # Check data subdirectories
        assert (data / "raw").exists(), "data/raw missing"
        assert (data / "processed").exists(), "data/processed missing"
        assert (data / "correlations").exists(), "data/correlations missing"
        assert (data / "embeddings").exists(), "data/embeddings missing"
        assert (data / "visualizations").exists(), "data/visualizations missing"
        assert (data / "insights").exists(), "data/insights missing"

    @pytest.mark.slow
    def test_environment_configuration(self):
        """Test environment configuration setup."""
        from dotenv import load_dotenv
        import os
        
        project_root = Path.cwd()
        env_example = project_root / ".env.example"
        
        # Test .env.example exists and has required sections
        assert env_example.exists(), ".env.example file missing"
        
        content = env_example.read_text()
        required_sections = [
            "Database Configuration",
            "API Keys - External Services",
            "LLM Configuration",
            "Application Configuration",
        ]
        
        for section in required_sections:
            assert section in content, f"Missing section: {section}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
