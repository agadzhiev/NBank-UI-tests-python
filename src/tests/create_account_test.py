import pytest

from src.main.api.generators.random_data import RandomData
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.user_role import UserRole
from src.main.api.models.delete_user_request import DeleteUserRequest
from src.main.api.requests.admin_user_requester import AdminUserRequester
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.tests.base_api_test import BaseTest


@pytest.mark.test
class TestCreateAccount(BaseTest):
    def test_user_can_create_account(self):
        user_request = CreateUserRequest(
            username=RandomData.get_username(),
            password=RandomData.get_password(),
            role=UserRole.USER
        )

        create_user_response = AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.entity_was_created()
        ).post(user_request)

        CreateAccountRequester(
            RequestSpecs.auth_as_user(user_request.username,
                                      user_request.password),
            ResponseSpecs.entity_was_created()
        ).post(None)

        get_customer_accounts = CreateAccountRequester(
            RequestSpecs.auth_as_user(user_request.username,
                                      user_request.password),
            ResponseSpecs.request_returns_OK()
        ).get()

        self.soft_assert(
            self.assertTrue,
            get_customer_accounts.accounts
        )

        AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.entity_was_deleted()
        ).delete(DeleteUserRequest(id=create_user_response.id))


