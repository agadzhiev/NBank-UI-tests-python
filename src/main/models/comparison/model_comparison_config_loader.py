import configparser
from typing import Dict, List, Type
import os
from pathlib import Path


class ComparisonRule:
    def __init__(self, response_class_name: str, field_pairs: List[str]):
        self.response_class_name = response_class_name
        self.field_mappings: Dict[str, str] = {}

        for pair in field_pairs:
            parts = pair.split('=')
            if len(parts) == 2:
                self.field_mappings[parts[0].strip()] = parts[1].strip()
            else:
                self.field_mappings[pair.strip()] = pair.strip()

    def get_response_class_name(self) -> str:
        return self.response_class_name

    def get_field_mappings(self) -> Dict[str, str]:
        return self.field_mappings


class ModelComparisonConfigLoader:
    def __init__(self, config_file: str):
        self.rules: Dict[str, ComparisonRule] = {}
        self._load_config(config_file)

    def _load_config(self, config_file: str):
        path = Path(__file__).parents[5] / 'resources' / f'{config_file}'
        print(path)

        if not os.path.exists(path):
            raise FileNotFoundError(f"Config file not found: {config_file}")

        config = configparser.ConfigParser()
        config.optionxform = str 
        config.read(path)

        for key in config.defaults():
            value = config.defaults()[key]
            target = value.split(":")
            if len(target) != 2:
                continue

            response_class = target[0].strip()
            field_list = [field.strip() for field in target[1].split(",")]

            self.rules[key.strip()] = ComparisonRule(response_class, field_list)

    def get_rule_for(self, request_cls: Type) -> ComparisonRule | None:
        return self.rules.get(request_cls.__name__)
