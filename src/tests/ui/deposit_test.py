import pytest
from playwright.sync_api import Page

from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.prepare_data_fixtures import PreparedUserAccount
from src.main.api.generators.random_data import RandomData
from src.main.ui.pages.deposit_page import DepositPage
from src.main.ui.pages.login_page import LoginPage


@pytest.mark.ui
@pytest.mark.usefixtures("browser_match_guard")
class TestDeposit:
    @pytest.mark.prepare_users(number=1)
    @pytest.mark.prepare_accounts(number=1)
    @pytest.mark.parametrize("deposit_amount", [RandomData.get_amount(min_value=0.01, max_value=5000.0)])
    @pytest.mark.check_account_balance_change(
        account_source="prepared_user_accounts[0].account.accountNumber",
        delta_source="deposit_amount",
    )
    def test_user_can_deposit_money(
        self,
        page: Page,
        prepared_user_accounts: list[PreparedUserAccount],
        deposit_amount: float,
    ):
        prepared = prepared_user_accounts[0]

        LoginPage(page).auth_as_user(prepared.user) \
            .go_to(DepositPage(page)) \
            .check_page_is_visible() \
            .deposit_to_account(prepared.account.id, deposit_amount)
        
