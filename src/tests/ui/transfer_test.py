import pytest
from playwright.sync_api import Page

from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.prepare_data_fixtures import PreparedUserAccount
from src.main.api.generators.random_data import RandomData
from src.main.ui.pages.login_page import LoginPage
from src.main.ui.pages.transfer_page import TransferPage


@pytest.mark.ui
@pytest.mark.usefixtures("browser_match_guard")
class TestTransfer:
    @pytest.mark.prepare_users(number=2)
    @pytest.mark.prepare_accounts(number=2, deposit=1000)
    @pytest.mark.parametrize("transfer_amount", [RandomData.get_amount(min_value=0.01, max_value=500.0)])
    @pytest.mark.check_transfer_balance_change(
        sender_account_source="prepared_user_accounts[0].account.accountNumber",
        receiver_account_source="prepared_user_accounts[1].account.accountNumber",
        amount_source="transfer_amount",
    )
    def test_user_can_transfer_money_between_accounts(
        self,
        page: Page,
        api_manager: ApiManager,
        prepared_user_accounts: list[PreparedUserAccount],
        transfer_amount: float,
    ):
        sender, receiver = prepared_user_accounts

        recipient_name = receiver.user.username

        LoginPage(page).auth_as_user(sender.user) \
            .go_to(TransferPage(page)) \
            .check_page_is_visible() \
            .make_transfer(
                sender_account_id=sender.account.id,
                recipient_name=recipient_name,
                recipient_account_number=receiver.account.accountNumber,
                amount=transfer_amount,
            )
        
