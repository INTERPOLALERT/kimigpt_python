"""
Configuration Manager for WebsiteNow
Handles loading and saving of configuration and API keys
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any


class ConfigManager:
    """Manage application configuration"""

    def __init__(self):
        # Use fixed base directory Z:\websitenow
        self.base_dir = Path("Z:/websitenow")

        self.config_dir = self.base_dir / "config"
        self.config_file = self.config_dir / "config.json"
        self.ensure_config_dir()

    def ensure_config_dir(self):
        """Ensure configuration directory exists"""
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if not self.config_file.exists():
            return self.get_default_config()

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.get_default_config()

    def save_config(self, config: Dict[str, Any]):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            'api_keys': {},
            'preferences': {
                'theme': 'light',
                'default_style': 'modern',
                'default_color': 'blue',
                'default_complexity': 'moderate',
                'default_framework': 'vanilla'
            },
            'output_dir': str(self.base_dir / 'output'),
            'upload_dir': str(self.base_dir / 'uploads'),
            'version': '1.0.0'
        }

    def save_api_keys(self, api_keys: Dict[str, str]):
        """Save API keys to configuration"""
        config = self.load_config()
        config['api_keys'] = api_keys
        self.save_config(config)

    def get_api_key(self, provider: str) -> str:
        """Get API key for a specific provider"""
        config = self.load_config()
        return config.get('api_keys', {}).get(provider, '')

    def has_api_keys(self) -> bool:
        """Check if any API keys are configured"""
        config = self.load_config()
        api_keys = config.get('api_keys', {})
        return bool(api_keys)

    def get_all_api_keys(self) -> Dict[str, str]:
        """Get all API keys"""
        config = self.load_config()
        return config.get('api_keys', {})

    def update_preference(self, key: str, value: Any):
        """Update a single preference"""
        config = self.load_config()
        if 'preferences' not in config:
            config['preferences'] = {}
        config['preferences'][key] = value
        self.save_config(config)

    def get_preference(self, key: str, default=None):
        """Get a single preference"""
        config = self.load_config()
        return config.get('preferences', {}).get(key, default)

    def get_output_dir(self) -> str:
        """Get output directory"""
        config = self.load_config()
        output_dir = config.get('output_dir', str(self.base_dir / 'output'))
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        return output_dir

    def get_upload_dir(self) -> str:
        """Get upload directory"""
        config = self.load_config()
        upload_dir = config.get('upload_dir', str(self.base_dir / 'uploads'))
        Path(upload_dir).mkdir(parents=True, exist_ok=True)
        return upload_dir
