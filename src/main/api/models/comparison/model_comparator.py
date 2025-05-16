from typing import Any, Dict, List


class Mismatch:
    def __init__(self, field_name: str, expected: Any, actual: Any):
        self.field_name = field_name
        self.expected = expected
        self.actual = actual

    def __str__(self) -> str:
        return f"{self.field_name}: expected={self.expected}, actual={self.actual}"


class ComparisonResult:
    def __init__(self, mismatches: List[Mismatch]):
        self.mismatches = mismatches

    def is_success(self) -> bool:
        return not self.mismatches

    def get_mismatches(self) -> List[Mismatch]:
        return self.mismatches

    def __str__(self) -> str:
        if self.is_success():
            return "All fields match."
        return "Mismatched fields:\n" + "\n".join(f"- {m}" for m in self.mismatches)


class ModelComparator:
    @staticmethod
    def compare_fields(
        request: Any,
        response: Any,
        field_mappings: Dict[str, str]
    ) -> ComparisonResult:

        mismatches: List[Mismatch] = []

        for request_field, response_field in field_mappings.items():
            value1 = ModelComparator._get_field_value(request, request_field)
            value2 = ModelComparator._get_field_value(response, response_field)

            if str(value1) != str(value2):
                mismatches.append(
                    Mismatch(f"{request_field} -> {response_field}", value1, value2)
                )

        return ComparisonResult(mismatches)

    @staticmethod
    def _get_field_value(obj: Any, field_name: str) -> Any:
        current_class = obj.__class__

        while current_class:
            if hasattr(obj, field_name):
                return getattr(obj, field_name)
            current_class = current_class.__base__

        raise AttributeError(
            f"Field '{field_name}' not found in class {obj.__class__.__name__}"
        )
