"""
Unified Environment Configuration Loader

This module provides a single, consolidated environment loading system that combines
the functionality of both EnvironmentManager and EnvironmentLoader. It ensures
consistent environment variable loading across all applications and packages.

Features:
- Single source of truth for environment configuration
- Support for shared and environment-specific settings
- Azure Functions and local development compatibility
- Proper loading order: shared → environment → secrets
- Validation of required variables
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..utils.centralized_logging import CentralizedLogger

# Initialize logger
logger = CentralizedLogger.get_logger("unified_environment_loader")

# Try to import python-dotenv
try:
    from dotenv import load_dotenv

    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    logger.warning(
        "python-dotenv not available. Environment files will not be loaded in local development."
    )


class UnifiedEnvironmentLoader:
    """
    Unified environment configuration loader that consolidates all environment
    management functionality into a single, comprehensive system.
    """

    _instance: Optional["UnifiedEnvironmentLoader"] = None
    _initialized: bool = False

    def __new__(cls, *args, **kwargs):
        """Singleton pattern to ensure single instance"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, environment: Optional[str] = None, force_reload: bool = False):
        """
        Initialize the unified environment loader

        Args:
            environment: Target environment (development/staging/production)
            force_reload: Force reload even if already initialized
        """
        if self._initialized and not force_reload:
            return

        self.environment = self._determine_environment(environment)
        self.is_azure = self._detect_azure_environment()
        self.environment_root = self._find_environment_root()
        self.loaded_files: List[str] = []
        self.failed_files: List[str] = []
        self.config_loaded = False

        # Auto-load configuration
        self.load_configuration()
        self._initialized = True

    def _determine_environment(self, environment: Optional[str]) -> str:
        """Determine the target environment"""
        if environment:
            env = environment.lower()
        else:
            env = (
                os.getenv("ENVIRONMENT", "").lower()
                or os.getenv("ENV", "").lower()
                or os.getenv("DEPLOYMENT_STAGE", "").lower()
                or os.getenv("AZURE_FUNCTIONS_ENVIRONMENT", "").lower()
                or "development"
            )

        # Normalize environment names
        env_mapping = {
            "dev": "development",
            "develop": "development",
            "stage": "staging",
            "prod": "production",
        }
        env = env_mapping.get(env, env)

        # Validate environment
        valid_environments = ["development", "staging", "production"]
        if env not in valid_environments:
            logger.warning(f"Unknown environment '{env}', defaulting to 'development'")
            env = "development"

        return env

    def _detect_azure_environment(self) -> bool:
        """Detect if running in Azure Functions environment"""
        return any(
            [
                os.getenv("AZURE_FUNCTIONS_ENVIRONMENT"),
                os.getenv("FUNCTIONS_WORKER_RUNTIME"),
                os.getenv("AzureWebJobsStorage"),
                os.getenv("WEBSITE_SITE_NAME"),
            ]
        )

    def _find_environment_root(self) -> Optional[Path]:
        """Find the root directory containing environment configuration files"""
        # Start from current working directory and search upward
        current_path = Path.cwd()

        # Try various search patterns
        search_patterns = [
            "infrastructure/environments",
            "environments",
            "../infrastructure/environments",
            "../../infrastructure/environments",
        ]

        for pattern in search_patterns:
            env_path = current_path / pattern
            if env_path.exists() and env_path.is_dir():
                logger.debug(f"Found environment root: {env_path}")
                return env_path.resolve()

        # If running from a package, try to find js-codebase root
        if "packages" in str(current_path) or "jobe_shared" in str(current_path):
            parts = current_path.parts
            try:
                # Find js-codebase in the path
                for i, part in enumerate(parts):
                    if "js-codebase" in part:
                        root_path = Path(*parts[: i + 1])
                        env_path = root_path / "infrastructure" / "environments"
                        if env_path.exists():
                            logger.debug(
                                f"Found environment root via js-codebase: {env_path}"
                            )
                            return env_path
            except (IndexError, ValueError):
                pass

        logger.warning("Environment configuration directory not found")
        return None

    def _load_env_file(self, file_path: Path, description: str = "") -> bool:
        """Load a single environment file"""
        if not file_path.exists():
            logger.debug(f"Environment file not found: {file_path}")
            return False

        if not DOTENV_AVAILABLE:
            logger.warning("Cannot load .env files - python-dotenv not available")
            return False

        try:
            success = load_dotenv(file_path, override=True)
            if success:
                self.loaded_files.append(str(file_path))
                logger.info(f"Loaded {description}: {file_path.name}")
                return True
            else:
                self.failed_files.append(str(file_path))
                logger.warning(f"Failed to load {description}: {file_path}")
                return False
        except Exception as e:
            self.failed_files.append(str(file_path))
            logger.error(f"Error loading {description} {file_path}: {e}")
            return False

    def load_configuration(self) -> bool:
        """Load all environment configuration in the proper order"""
        if self.is_azure:
            logger.info("Running in Azure Functions - using Application Settings")
            self.config_loaded = True
            return True

        if not self.environment_root:
            logger.error("Cannot load environment files - environment root not found")
            self.config_loaded = False
            return False

        logger.info(f"Loading environment configuration for: {self.environment}")

        # Define loading order (later files override earlier ones)
        env_files = [
            # 1. Shared configuration (base settings)
            (
                self.environment_root / "shared" / "config" / ".env.shared",
                "shared config",
            ),
            # 2. Shared secrets (base secrets)
            (
                self.environment_root / "shared" / "secrets" / ".env.secrets.shared",
                "shared secrets",
            ),
            # 3. Environment-specific configuration (highest priority)
            (
                self.environment_root
                / self.environment
                / "config"
                / f".env.{self.environment}",
                f"{self.environment} config",
            ),
        ]

        # Load each file in order
        success_count = 0
        for file_path, description in env_files:
            if self._load_env_file(file_path, description):
                success_count += 1

        # Log summary
        logger.info(
            f"Environment loading complete: {success_count}/{len(env_files)} files loaded"
        )

        if self.loaded_files:
            logger.debug(
                f"Successfully loaded: {[Path(f).name for f in self.loaded_files]}"
            )

        if self.failed_files:
            logger.debug(f"Failed to load: {[Path(f).name for f in self.failed_files]}")

        self.config_loaded = True
        return success_count > 0

    def validate_required_variables(self, required_vars: List[str]) -> List[str]:
        """
        Validate that required environment variables are set

        Args:
            required_vars: List of required environment variable names

        Returns:
            List of missing variable names
        """
        missing_vars = []
        for var in required_vars:
            value = os.getenv(var)
            if not value or value.strip() == "":
                missing_vars.append(var)

        if missing_vars:
            logger.error(f"Missing required environment variables: {missing_vars}")
        else:
            logger.info("All required environment variables are set")

        return missing_vars

    def get_environment_info(self) -> Dict[str, Any]:
        """Get comprehensive environment information for debugging"""
        return {
            "environment": self.environment,
            "is_azure": self.is_azure,
            "is_local": not self.is_azure,
            "config_loaded": self.config_loaded,
            "environment_root": (
                str(self.environment_root) if self.environment_root else None
            ),
            "dotenv_available": DOTENV_AVAILABLE,
            "loaded_files": [Path(f).name for f in self.loaded_files],
            "failed_files": [Path(f).name for f in self.failed_files],
            "key_variables": {
                "ENVIRONMENT": os.getenv("ENVIRONMENT"),
                "MONDAY_API_TOKEN": (
                    "***SET***" if os.getenv("MONDAY_API_TOKEN") else "NOT SET"
                ),
                "AZURE_STORAGE_CONNECTION_STRING": (
                    "***SET***"
                    if os.getenv("AZURE_STORAGE_CONNECTION_STRING")
                    else "NOT SET"
                ),
                "AZURE_RESOURCE_GROUP": os.getenv("AZURE_RESOURCE_GROUP"),
                "DEBUG": os.getenv("DEBUG"),
                "LOG_LEVEL": os.getenv("LOG_LEVEL"),
            },
        }

    @classmethod
    def get_instance(
        cls, environment: Optional[str] = None, force_reload: bool = False
    ) -> "UnifiedEnvironmentLoader":
        """Get the singleton instance of the environment loader"""
        return cls(environment=environment, force_reload=force_reload)

    @classmethod
    def ensure_environment_loaded(
        cls, required_vars: Optional[List[str]] = None
    ) -> bool:
        """
        Ensure environment configuration is loaded and validate required variables

        Args:
            required_vars: Optional list of required environment variables

        Returns:
            True if environment is properly loaded and all required vars are set
        """
        loader = cls.get_instance()

        if not loader.config_loaded:
            logger.error("Environment configuration not loaded")
            return False

        if required_vars:
            missing_vars = loader.validate_required_variables(required_vars)
            if missing_vars:
                logger.error(f"Missing required variables: {missing_vars}")
                return False

        return True


# Convenience functions for backward compatibility
def load_environment(environment: Optional[str] = None) -> Dict[str, str]:
    """Load environment configuration and return environment variables"""
    loader = UnifiedEnvironmentLoader.get_instance(environment=environment)
    return dict(os.environ)


def get_current_environment() -> str:
    """Get the current environment name"""
    loader = UnifiedEnvironmentLoader.get_instance()
    return loader.environment


def is_azure_environment() -> bool:
    """Check if running in Azure Functions environment"""
    loader = UnifiedEnvironmentLoader.get_instance()
    return loader.is_azure


def validate_environment(required_vars: List[str]) -> bool:
    """Validate that required environment variables are set"""
    return UnifiedEnvironmentLoader.ensure_environment_loaded(required_vars)


# Initialize environment on module import
_loader = UnifiedEnvironmentLoader.get_instance()
logger.info(f"Environment loader initialized for {_loader.environment} environment")
