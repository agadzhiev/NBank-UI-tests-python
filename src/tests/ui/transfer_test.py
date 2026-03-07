from decimal import Decimal
import time
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

        sender_before_balance = None
        for _ in range(10):
            sender_before_balance = api_manager.database_steps.get_account_balance_by_account_number(
                sender.account.accountNumber
            )
            if sender_before_balance == Decimal("1000.0"):
                break
            time.sleep(0.3)

        receiver_before_balance = api_manager.database_steps.get_account_balance_by_account_number(
            receiver.account.accountNumber
        )

        receiver_dao = api_manager.database_steps.get_user_by_username(receiver.user.username)
        recipient_name = receiver_dao.name or "noname"

        LoginPage(page).go_to(TransferPage(page)) \
            .check_page_is_visible() \
            .make_transfer(
                sender_account_id=sender.account.id,
                recipient_name=recipient_name,
                recipient_account_number=receiver.account.accountNumber,
                amount=transfer_amount,
            )

        expected_sender_after = sender_before_balance - Decimal(str(transfer_amount))
        expected_receiver_after = receiver_before_balance + Decimal(str(transfer_amount))
        sender_after_balance = None
        receiver_after_balance = None
        for _ in range(10):
            sender_after_balance = api_manager.database_steps.get_account_balance_by_account_number(
                sender.account.accountNumber
            )
            receiver_after_balance = api_manager.database_steps.get_account_balance_by_account_number(
                receiver.account.accountNumber
            )
            if sender_after_balance == expected_sender_after and receiver_after_balance == expected_receiver_after:
                break
            time.sleep(0.3)

        assert sender_after_balance == expected_sender_after
        assert receiver_after_balance == expected_receiver_after
        
