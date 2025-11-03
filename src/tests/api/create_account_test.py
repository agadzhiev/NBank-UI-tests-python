import pytest

from src.main.classes.api_manager import ApiManager
from src.main.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestCreateAccount:
    @pytest.mark.usefixtures('user_request', 'api_manager')
    def test_create_account(self, api_manager: ApiManager, user_request: CreateUserRequest):
        api_manager.user_steps.create_account(user_request)
