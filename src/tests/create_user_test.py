import pytest

from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.random_data import RandomData
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestCreateUser:
    @pytest.mark.usefixtures('api_manager')
    @pytest.mark.parametrize('create_user_request', [RandomModelGenerator.generate(CreateUserRequest)])
    def test_create_valid_user(self, api_manager: ApiManager, create_user_request: CreateUserRequest):
        api_manager.admin_steps.create_user(create_user_request)
    
    @pytest.mark.parametrize(
        'username, password, role, error_key, error_value',
        [
            ("   ", "Password33$", "USER", "username", "Username cannot be blank"),
            ("ab", "Password33$", "USER", "username", "Username must be between 3 and 15 characters"),
            ("abc$", "Password33$", "USER", "username", "Username must contain only letters, digits, dashes, underscores, and dots"),
            ("abc%", "Password33$", "USER", "username", "Username must contain only letters, digits, dashes, underscores, and dots"),
        ]
    )
    @pytest.mark.usefixtures('api_manager')
    def test_create_invalid_user(self, api_manager: ApiManager, username: str, password: str, role: str, error_key: str, error_value: str):
        create_user_request = CreateUserRequest(username=username, password=password, role=role)
        api_manager.admin_steps.create_invalid_user(create_user_request, error_key, error_value)
    