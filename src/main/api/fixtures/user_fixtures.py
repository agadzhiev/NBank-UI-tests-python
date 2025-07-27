import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.fixture
def user_request(api_manager: ApiManager):
    return api_manager.admin_steps.create_user()
