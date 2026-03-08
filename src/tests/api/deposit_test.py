import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.prepare_data_fixtures import PreparedUserAccount
from src.main.api.generators.random_data import RandomData
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.requests.skeleton.endpoint import Endpoint
from src.main.api.requests.skeleton.requesters.crud_requester import CrudRequester
from src.main.api.specs.request_specs import RequestSpecs


@pytest.mark.api
@pytest.mark.api_version("with_database")
@pytest.mark.prepare_users(number=1)
@pytest.mark.prepare_accounts(number=1)
class TestDeposit:
    @pytest.mark.parametrize("deposit_amount", [RandomData.get_amount(min_value=0.01, max_value=5000.0)])
    @pytest.mark.check_account_balance_change(
        account_source="prepared_user_accounts[0].account.accountNumber",
        delta_source="deposit_amount",
    )
    def test_deposit_to_account(
        self,
        api_manager: ApiManager,
        prepared_user_accounts: list[PreparedUserAccount],
        deposit_amount: float,
    ):
        account = prepared_user_accounts[0].account
        user = prepared_user_accounts[0].user

        deposit_response = api_manager.user_steps.deposit_to_account(
            user,
            account.id,
            deposit_amount,
        )

        assert deposit_response.id == account.id
        assert deposit_response.accountNumber == account.accountNumber
        assert deposit_response.balance >= deposit_amount

    @pytest.mark.parametrize("deposit_amount, expected_delta", [(-1.0, 0.0)])
    @pytest.mark.check_account_balance_change(
        account_source="prepared_user_accounts[0].account.accountNumber",
        delta_source="expected_delta",
    )
    def test_user_cannot_deposit_negative_amount(
        self,
        prepared_user_accounts: list[PreparedUserAccount],
        deposit_amount: float,
        expected_delta: float,
    ):
        account = prepared_user_accounts[0].account
        user = prepared_user_accounts[0].user

        response = CrudRequester(
            RequestSpecs.auth_as_user(user.username, user.password),
            Endpoint.DEPOSIT_TO_ACCOUNT,
            lambda response: None,
        ).post(DepositRequest(accountId=account.id, amount=deposit_amount))

        assert response.status_code == 500, (
            f"Expected 500 for negative deposit amount, got {response.status_code}. "
            f"Response body: {response.text}"
        )
