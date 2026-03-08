import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.prepare_data_fixtures import PreparedUserAccount
from src.main.api.generators.random_data import RandomData
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.requests.skeleton.endpoint import Endpoint
from src.main.api.requests.skeleton.requesters.crud_requester import CrudRequester
from src.main.api.specs.request_specs import RequestSpecs


@pytest.mark.api
@pytest.mark.api_version("with_database")
@pytest.mark.prepare_users(number=2)
@pytest.mark.prepare_accounts(number=2, deposit=5000)
class TestTransfer:
    @pytest.mark.parametrize("transfer_amount", [RandomData.get_amount(min_value=0.01, max_value=4999.99)])
    @pytest.mark.check_transfer_balance_change(
        sender_account_source="prepared_user_accounts[0].account.accountNumber",
        receiver_account_source="prepared_user_accounts[1].account.accountNumber",
        amount_source="transfer_amount",
    )
    def test_transfer_between_accounts(
        self,
        prepared_user_accounts: list[PreparedUserAccount],
        transfer_amount: float,
    ):
        sender, receiver = prepared_user_accounts

        transfer_request = TransferRequest(
            senderAccountId=sender.account.id,
            receiverAccountId=receiver.account.id,
            amount=transfer_amount,
        )

        transfer_response = CrudRequester(
            RequestSpecs.auth_as_user(sender.user.username, sender.user.password),
            Endpoint.TRANSFER,
            lambda response: None,
        ).post(transfer_request).json()

        assert transfer_response["senderAccountId"] == sender.account.id
        assert transfer_response["receiverAccountId"] == receiver.account.id
        assert transfer_response["amount"] == transfer_amount

    @pytest.mark.parametrize("transfer_amount", [6000.0])
    @pytest.mark.check_transfer_balance_change(
        sender_account_source="prepared_user_accounts[0].account.accountNumber",
        receiver_account_source="prepared_user_accounts[1].account.accountNumber",
        amount_source="transfer_amount",
        should_change=False,
    )
    def test_user_cannot_transfer_more_than_available_balance(
        self,
        prepared_user_accounts: list[PreparedUserAccount],
        transfer_amount: float,
    ):
        sender, receiver = prepared_user_accounts

        response = CrudRequester(
            RequestSpecs.auth_as_user(sender.user.username, sender.user.password),
            Endpoint.TRANSFER,
            lambda response: None,
        ).post(
            TransferRequest(
                senderAccountId=sender.account.id,
                receiverAccountId=receiver.account.id,
                amount=transfer_amount,
            )
        )

        assert response.status_code == 400, (
            f"Expected 400 for transfer with insufficient funds, got {response.status_code}. "
            f"Response body: {response.text}"
        )
        assert "insufficient funds" in response.text.lower(), (
            f"Expected insufficient funds error, got: {response.text}"
        )
