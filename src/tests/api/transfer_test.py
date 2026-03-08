from decimal import Decimal

import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.prepare_data_fixtures import PreparedUserAccount
from src.main.api.generators.random_data import RandomData
from src.main.api.models.comparison.dao_and_model_assertions import DaoAndModelAssertions
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.transfer_request import TransferRequest


@pytest.mark.api
@pytest.mark.api_version("with_database")
@pytest.mark.prepare_users(number=2)
@pytest.mark.prepare_accounts(number=2, deposit=5000)
class TestTransfer:
    def test_transfer_between_accounts(
        self,
        api_manager: ApiManager,
        prepared_user_accounts: list[PreparedUserAccount],
    ):
        sender, receiver = prepared_user_accounts
        transfer_amount = RandomData.get_amount(min_value=0.01, max_value=4999.99)

        sender_before_balance = api_manager.database_steps.get_account_balance_by_account_number(
            sender.account.accountNumber
        )
        receiver_before_balance = api_manager.database_steps.get_account_balance_by_account_number(
            receiver.account.accountNumber
        )

        transfer_request = TransferRequest(
            senderAccountId=sender.account.id,
            receiverAccountId=receiver.account.id,
            amount=transfer_amount,
        )

        api_manager.user_steps.transfer(sender.user, transfer_request)

        sender_after = api_manager.database_steps.get_account_by_account_number(sender.account.accountNumber)
        receiver_after = api_manager.database_steps.get_account_by_account_number(receiver.account.accountNumber)

        expected_sender = CreateAccountResponse(
            id=sender.account.id,
            accountNumber=sender.account.accountNumber,
            balance=float(sender_before_balance - Decimal(str(transfer_amount))),
        )
        expected_receiver = CreateAccountResponse(
            id=receiver.account.id,
            accountNumber=receiver.account.accountNumber,
            balance=float(receiver_before_balance + Decimal(str(transfer_amount))),
        )

        DaoAndModelAssertions.assert_that(expected_sender, sender_after).match()
        DaoAndModelAssertions.assert_that(expected_receiver, receiver_after).match()
