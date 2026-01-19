import pytest
from playwright.sync_api import Page

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.ui.pages.user_dashboard import UserDashboard
from src.main.ui.pages.bank_alert import BankAlert


@pytest.mark.ui
class TestCreateAccount:
    @pytest.mark.user_session(10)
    def test_user_can_create_account(self, api_manager: ApiManager, page: Page, user_request: CreateUserRequest):
        user_accounts_before = api_manager.user_steps.get_all_accounts(user_request)

        UserDashboard(page).open() \
        .check_page_is_visible() \
        .create_new_account() \
        .check_alert_message_and_accept(BankAlert.NEW_ACCOUNT_CREATED)

        user_accounts_after = api_manager.user_steps.get_all_accounts(user_request)

        new_accounts = [acc for acc in user_accounts_after if acc.id not in {acc.id for acc in user_accounts_before}]
        assert len(new_accounts) == 1
        assert new_accounts[0].balance == 0