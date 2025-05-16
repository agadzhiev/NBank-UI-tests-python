from typing import get_type_hints, get_args, get_origin, Annotated, Any
from src.main.api.generators.generating_rule import GeneratingRule
import rstr
import uuid
import random
from datetime import datetime, timedelta


class RandomModelGenerator:
    @staticmethod
    def generate(cls: type) -> Any:
        type_hints = get_type_hints(cls, include_extras=True)
        init_data = {}

        for field_name, annotated_type in type_hints.items():
            rule = None
            actual_type = annotated_type

            if get_origin(annotated_type) is Annotated:
                actual_type, *annotations = get_args(annotated_type)
                for ann in annotations:
                    if isinstance(ann, GeneratingRule):
                        rule = ann

            if rule:
                value = RandomModelGenerator._generate_from_regex(rule.regex, actual_type)
            else:
                value = RandomModelGenerator._generate_value(actual_type)

            init_data[field_name] = value

        return cls(**init_data)

    @staticmethod
    def _generate_from_regex(regex: str, field_type: type) -> Any:
        generated = rstr.xeger(regex)
        if field_type is int:
            return int(generated)
        elif field_type is float:
            return float(generated)
        else:
            return generated

    @staticmethod
    def _generate_value(field_type: type) -> Any:
        if field_type is str:
            return str(uuid.uuid4())[:8]
        elif field_type is int:
            return random.randint(0, 1000)
        elif field_type is float:
            return round(random.uniform(0, 100.0), 2)
        elif field_type is bool:
            return random.choice([True, False])
        elif field_type is datetime:
            return datetime.now() - timedelta(seconds=random.randint(0, 100000))
        elif get_origin(field_type) is list:
            return RandomModelGenerator._generate_list(field_type)
        elif isinstance(field_type, type):
            return RandomModelGenerator.generate(field_type)
        else:
            return None

    @staticmethod
    def _generate_list(field_type: Any) -> list:
        args = get_args(field_type)
        if args and args[0] == str:
            return [str(uuid.uuid4())[:5] for _ in range(2)]
        return []
