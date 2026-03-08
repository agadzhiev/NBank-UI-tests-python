from decimal import Decimal

import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.prepare_data_fixtures import PreparedUserAccount
from src.main.api.generators.random_data import RandomData
from src.main.api.models.comparison.dao_and_model_assertions import DaoAndModelAssertions
from src.main.api.models.deposit_response import DepositResponse


@pytest.mark.api
@pytest.mark.api_version("with_database")
@pytest.mark.prepare_users(number=1)
@pytest.mark.prepare_accounts(number=1)
class TestDeposit:
    def test_deposit_to_account(self, api_manager: ApiManager, prepared_user_accounts: list[PreparedUserAccount]):
        account = prepared_user_accounts[0].account
        user = prepared_user_accounts[0].user
        deposit_amount = RandomData.get_amount(min_value=0.01, max_value=5000.0)

        before_balance = api_manager.database_steps.get_account_balance_by_account_number(account.accountNumber)

        deposit_response = api_manager.user_steps.deposit_to_account(
            user,
            account.id,
            deposit_amount,
        )

        account_dao = api_manager.database_steps.get_account_by_account_number(account.accountNumber)

        expected_deposit_response = DepositResponse(
            id=account.id,
            accountNumber=account.accountNumber,
            balance=float(before_balance + Decimal(str(deposit_amount))),
        )

        DaoAndModelAssertions.assert_that(expected_deposit_response, account_dao).match()
        DaoAndModelAssertions.assert_that(deposit_response, account_dao).match()
