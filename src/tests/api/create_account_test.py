import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.comparison.model_assertions import ModelAssertions


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self, api_manager: ApiManager, user_request: CreateUserRequest):
        all_accounts_before = api_manager.user_steps.get_all_accounts(user_request)
        created_account = api_manager.user_steps.create_account(user_request)
        all_accounts_after = api_manager.user_steps.get_all_accounts(user_request)
        get_account = next((acc for acc in all_accounts_after if acc.id == created_account.id), None)

        assert len(all_accounts_after) == len(all_accounts_before) + 1
        ModelAssertions(get_account, created_account).match()
