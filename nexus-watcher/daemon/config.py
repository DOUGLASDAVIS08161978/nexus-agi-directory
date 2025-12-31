"""Configuration management for Nexus Watcher daemon."""

import os
import yaml
from pathlib import Path
from typing import Any, Dict
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration manager for the daemon."""

    def __init__(self, config_path: str = None):
        """
        Initialize configuration.

        Args:
            config_path: Path to config.yaml file
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config.yaml"

        self.config_path = Path(config_path)
        self._config: Dict[str, Any] = {}
        self.load()

    def load(self):
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path, 'r') as f:
            self._config = yaml.safe_load(f)

        # Override with environment variables
        self._apply_env_overrides()

    def _apply_env_overrides(self):
        """Apply environment variable overrides."""
        # GitHub token
        if os.getenv('GITHUB_TOKEN'):
            self._config['discovery_scout']['github_token'] = os.getenv('GITHUB_TOKEN')

        # Database path
        if os.getenv('STATE_DB'):
            self._config['daemon']['state_db'] = os.getenv('STATE_DB')

        # Log level
        if os.getenv('LOG_LEVEL'):
            self._config['daemon']['log_level'] = os.getenv('LOG_LEVEL')

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.

        Args:
            key_path: Dot-separated path (e.g., 'daemon.log_level')
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        keys = key_path.split('.')
        value = self._config

        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
                if value is None:
                    return default
            else:
                return default

        return value

    def set(self, key_path: str, value: Any):
        """
        Set configuration value using dot notation.

        Args:
            key_path: Dot-separated path
            value: Value to set
        """
        keys = key_path.split('.')
        config = self._config

        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]

        config[keys[-1]] = value

    @property
    def all(self) -> Dict[str, Any]:
        """Get all configuration as dictionary."""
        return self._config.copy()
