from decimal import Decimal
import pytest
from playwright.sync_api import Page

from main.api.classes.api_manager import ApiManager
from main.api.fixtures.prepare_data_fixtures import PreparedUserAccount
from main.api.generators.random_data import RandomData
from main.ui.pages.deposit_page import DepositPage
from main.ui.pages.login_page import LoginPage
from main.ui.pages.transfer_page import TransferPage


@pytest.mark.ui
@pytest.mark.usefixtures("browser_match_guard")
class TestTransfer:
    @pytest.mark.prepare_users(number=1)
    @pytest.mark.prepare_accounts(number=2)
    def test_user_can_transfer_money_between_accounts(self, page: Page,
        api_manager: ApiManager,
        prepared_user_accounts: list[PreparedUserAccount]):
        
        sender, receiver = prepared_user_accounts
        transfer_amount = RandomData.get_amount(min_value=0.01, max_value=500.0)

        # Ensure sender has enough money for transfer through UI flow.
        LoginPage(page).auth_as_user(sender.user) \
            .go_to(DepositPage(page)) \
            .check_page_is_visible() \
            .deposit_to_account(sender.account.id, 1000.0)

        sender_before_balance = api_manager.database_steps.get_account_balance_by_account_number(
            sender.account.accountNumber
        )
        receiver_before_balance = api_manager.database_steps.get_account_balance_by_account_number(
            receiver.account.accountNumber
        )

        user_dao = api_manager.database_steps.get_user_by_username(sender.user.username)
        recipient_name = user_dao.name or "noname"

        LoginPage(page).go_to(TransferPage(page)) \
            .check_page_is_visible() \
            .make_transfer(
                sender_account_id=sender.account.id,
                recipient_name=recipient_name,
                recipient_account_number=receiver.account.accountNumber,
                amount=transfer_amount,
            )

        sender_after_balance = api_manager.database_steps.get_account_balance_by_account_number(
            sender.account.accountNumber
        )
        receiver_after_balance = api_manager.database_steps.get_account_balance_by_account_number(
            receiver.account.accountNumber
        )

        assert sender_after_balance == sender_before_balance - Decimal(str(transfer_amount))
        assert receiver_after_balance == receiver_before_balance + Decimal(str(transfer_amount))
        
