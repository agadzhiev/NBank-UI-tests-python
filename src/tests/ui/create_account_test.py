import pytest
from playwright.sync_api import Page, expect

from src.tests.ui.base_test import BaseUITest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.ui.pages.user_dashboard import UserDashboard
from src.main.ui.pages.bank_alert import BankAlert


@pytest.mark.ui
class TestCreateAccount(BaseUITest):
    @pytest.mark.usefixtures("user_request", "api_manager")
    def test_user_can_create_account(self, api_manager: ApiManager, page: Page, user_request: CreateUserRequest):
        # ШАГ 1: юзер логинится в банке
        self.auth_as_user(page, user_request)

        # ШАГ 2: юзер создает аккаунт
        dashboard_page = UserDashboard(page).open()\
            .create_new_account()\
            .check_alert_message_and_accept(BankAlert.NEW_ACCOUNT_CREATED)
        expect(dashboard_page.welcome_text).to_be_visible()
        
        # ШАГ 3: проверка, что аккаунт был создан на API
        user_accounts = api_manager.user_steps.get_all_accounts(user_request)

        assert len(user_accounts) == 1
        assert user_accounts[0] and user_accounts[0].balance == 0