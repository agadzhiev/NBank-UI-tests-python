import os
from pathlib import Path


class Config:
    _instance = None
    _properties = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            config_path = Path(__file__).parent / 'config.properties'
            if not config_path.exists():
                raise RuntimeError("config.properties not found in resources")
            with open(config_path, 'r') as f:
                for line in f:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        cls._properties[key] = value
        return cls._instance

    @staticmethod
    def get(key):
        return Config()._properties.get(key)

    @staticmethod
    def get_or_default(key, default_value):
        return Config()._properties.get(key, default_value)
