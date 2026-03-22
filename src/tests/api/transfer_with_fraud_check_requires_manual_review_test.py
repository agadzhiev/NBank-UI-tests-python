import random

import allure
import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.prepare_data_fixtures import PreparedUserAccount
from src.main.api.models.comparison.model_assertions import ModelAssertions
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.models.transfer_response import TransferResponse


FRAUD_MANUAL_REVIEW_REQUIRED_MOCK = {
    "status": "MANUAL_REVIEW_REQUIRED",
    "decision": "MANUAL_REVIEW_REQUIRED",
    "riskScore": 0.2,
    "reason": "Transfer requires manual review",
    "requiresManualReview": True,
    "additionalVerificationRequired": False,
}

FRAUD_MANUAL_REVIEW_REQUIRED_EXPECTED = {
    "fraudRiskScore": FRAUD_MANUAL_REVIEW_REQUIRED_MOCK["riskScore"],
    "fraudReason": FRAUD_MANUAL_REVIEW_REQUIRED_MOCK["reason"],
    "requiresManualReview": True,
    "requiresVerification": False,
}

TRANSFER_MANUAL_REVIEW_REQUIRED_EXPECTED = {
    "status": "MANUAL_REVIEW_REQUIRED",
    "message": "Transfer requires manual review",
    **FRAUD_MANUAL_REVIEW_REQUIRED_EXPECTED,
}


@pytest.mark.api
@pytest.mark.api_version("with_fraud_check")
@pytest.mark.prepare_users(number=2)
@pytest.mark.prepare_accounts(number=2, deposit=5000)
class TestTransferWithFraudCheckManualReview:
    @pytest.mark.fraud_check_mock(
        port=8080,
        endpoint=r"/.*",
        **FRAUD_MANUAL_REVIEW_REQUIRED_MOCK,
    )
    def test_transfer_with_fraud_check_requires_manual_review(
        self,
        api_manager: ApiManager,
        prepared_user_accounts: list[PreparedUserAccount],
        fraud_check_mock_server,
    ):
        with allure.step("Prepare sender/receiver accounts (2 accounts with deposit=5000)"):
            sender = prepared_user_accounts[0]
            receiver = prepared_user_accounts[1]
            before_sender_balance = api_manager.database_steps.get_balance_by_account_number(
                sender.account.accountNumber
            )
            before_receiver_balance = api_manager.database_steps.get_balance_by_account_number(
                receiver.account.accountNumber
            )

        with allure.step("Transfer with fraud check"):
            transfer_amount = round(random.uniform(0.1, 4999.9), 2)
            transfer_request = TransferRequest(
                senderAccountId=sender.account.id,
                receiverAccountId=receiver.account.id,
                amount=transfer_amount,
            )
            transfer_response = api_manager.user_steps.transfer_with_fraud_check(
                sender.user,
                transfer_request,
            )

        with allure.step("Validate transfer response matches mocked fraud decision"):
            expected = TransferResponse(
                amount=transfer_amount,
                senderAccountId=sender.account.id,
                receiverAccountId=receiver.account.id,
                **TRANSFER_MANUAL_REVIEW_REQUIRED_EXPECTED,
            )
            ModelAssertions(expected, transfer_response).match()

        with allure.step("Validate balances were not changed"):
            after_sender_balance = api_manager.database_steps.get_balance_by_account_number(
                sender.account.accountNumber
            )
            after_receiver_balance = api_manager.database_steps.get_balance_by_account_number(
                receiver.account.accountNumber
            )

            assert after_sender_balance == before_sender_balance
            assert after_receiver_balance == before_receiver_balance
