import pytest
from playwright.sync_api import Page, expect

from src.main.ui.pages.bank_alert import BankAlert
from src.main.api.classes.api_manager import ApiManager
from src.main.ui.pages.user_dashboard import UserDashboard
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.ui
class TestCreateAccount:
    @pytest.mark.user_session(1)
    @pytest.mark.usefixtures("user_request", "api_manager")
    def test_user_can_create_account(self, page: Page, api_manager: ApiManager, user_request: CreateUserRequest):
        dashboard_page = UserDashboard(page).open()\
            .create_new_account()\
            .check_alert_message_and_accept(BankAlert.NEW_ACCOUNT_CREATED)
        expect(dashboard_page.welcome_text).to_be_visible()

        created_accounts = api_manager.user_steps.get_all_accounts(user_request)
        assert len(created_accounts) == 1
        assert created_accounts[0] and created_accounts[0].balance == 0