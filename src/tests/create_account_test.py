import pytest

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.classes.api_manager import ApiManager
from src.tests.base_api_test import BaseTestWithoutSoftAsserts


@pytest.mark.test
class TestCreateAccount(BaseTestWithoutSoftAsserts):

    @pytest.mark.usefixtures('user_request')
    def test_user_can_create_account(self, api_manager: ApiManager, user_request: CreateUserRequest):
        api_manager.user_steps.create_account(user_request)
