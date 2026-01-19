from typing import Any

from src.main.api.models.comparison.model_comparator import ModelComparator
from src.main.api.models.comparison.model_comparison_configuration import ModelComparisonConfigLoader


def models_match(request: Any, response: Any):
    config_loader = ModelComparisonConfigLoader('model-comparison.properties')
    rule = config_loader.get_rule_for(request)

    if rule is not None:
        result = ModelComparator.compare_fields(
            request, response, rule.field_mapping
        )

        if not result.is_success():
            raise AssertionError(f'Model comparison failed with mismatches fields: \n{result.mismatches}')
        
    else:
        raise AssertionError(f'No comparion rule found for class {request.__class__.__name__}')


class ModelAssertions:
    """
    Backward-compatible wrapper used by some tests.
    Convention in tests: ModelAssertions(actual_response, expected_request).match()
    Internally, comparison rules are defined for request -> response mapping, so we swap args.
    """

    def __init__(self, actual: Any, expected: Any):
        self.actual = actual
        self.expected = expected

    def match(self) -> None:
        models_match(self.expected, self.actual)