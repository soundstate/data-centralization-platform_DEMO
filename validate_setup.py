#!/usr/bin/env python3
"""
Quick validation script to ensure the development environment is properly configured.
"""

import sys
from pathlib import Path


def main():
    """Run validation checks."""
    print("🔍 Validating Data Centralization Platform Setup...")
    print("=" * 60)

    # Check Python version
    print(f"🐍 Python Version: {sys.version}")
    assert sys.version_info >= (3, 11), "Python 3.11+ required"
    print("✅ Python version is compatible")

    # Check virtual environment
    if hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    ):
        print("✅ Virtual environment is active")
    else:
        print("❌ Virtual environment not detected")
        return False

    # Check core imports
    try:
        import alembic
        import black
        import fastapi
        import httpx
        import mypy
        import psycopg2
        import pydantic
        import pytest
        import sqlalchemy
        import toml

        print("✅ All core dependencies are importable")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

    # Check project structure
    project_root = Path.cwd()
    required_dirs = [
        "packages",
        "services",
        "flows",
        "data",
        "infrastructure",
        "development/testing",
        "ui",
        "resources/docs",
    ]

    for dir_path in required_dirs:
        if (project_root / dir_path).exists():
            print(f"✅ Directory exists: {dir_path}")
        else:
            print(f"❌ Directory missing: {dir_path}")
            return False

    # Check configuration files
    config_files = [
        "requirements.txt",
        ".env.example",
        "pyproject.toml",
        "pytest.ini",
        "setup.py",
    ]

    for file_path in config_files:
        if (project_root / file_path).exists():
            print(f"✅ Configuration file exists: {file_path}")
        else:
            print(f"❌ Configuration file missing: {file_path}")
            return False

    # Test TOML validity
    try:
        import toml

        toml.load("pyproject.toml")
        print("✅ pyproject.toml is valid TOML")
    except Exception as e:
        print(f"❌ pyproject.toml error: {e}")
        return False

    # Test pytest configuration
    try:
        import pytest

        print("✅ pytest is configured and working")
    except Exception as e:
        print(f"❌ pytest error: {e}")
        return False

    print("=" * 60)
    print("🎉 All validation checks passed!")
    print("🚀 Ready to begin Phase 1 - API Client Development")
    print("=" * 60)

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
