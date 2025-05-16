from src.main.api.models.comparison.model_comparison_config_loader import ModelComparisonConfigLoader
from src.main.api.models.comparison.model_comparator import ModelComparator
from typing import Any


class ModelAssertions:
    def __init__(self, request: Any, response: Any):
        self.request = request
        self.response = response

    @staticmethod
    def assert_that_models(request: Any, response: Any) -> "ModelAssertions":
        return ModelAssertions(request, response)

    def match(self) -> "ModelAssertions":
        config_loader = ModelComparisonConfigLoader("model-comparison.properties")
        rule = config_loader.get_rule_for(self.request.__class__)

        if rule is not None:
            result = ModelComparator.compare_fields(
                self.request,
                self.response,
                rule.get_field_mappings()
            )

            if not result.is_success():
                raise AssertionError(
                    f"Model comparison failed with mismatched fields:\n{result}"
                )
        else:
            raise AssertionError(
                f"No comparison rule found for class {self.request.__class__.__name__}"
            )

        return self
