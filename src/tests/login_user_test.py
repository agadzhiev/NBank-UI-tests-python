import pytest

from src.main.api.generators.random_data import RandomData
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.user_role import UserRole
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.delete_user_request import DeleteUserRequest
from src.main.api.requests.login_user_requester import LoginUserRequester
from src.main.api.requests.admin_user_requester import AdminUserRequester
from src.tests.base_api_test import BaseTest


@pytest.mark.test
class TestLoginUser(BaseTest):
    def test_admin_can_generate_auth_token_test(self):
        login_user_request = LoginUserRequest(
            username='admin',
            password='admin'
        )

        create_user_response = LoginUserRequester(
            RequestSpecs.unauth_spec(),
            ResponseSpecs.request_returns_OK()
        ).post(login_user_request)

        self.soft_assert(self.assertTrue, login_user_request.username == create_user_response.username)
        self.soft_assert(self.assertTrue, "ADMIN" == create_user_response.role)

    def test_user_can_generate_auth_token(self):
        create_user_request = CreateUserRequest(
            username=RandomData.get_username(),
            password=RandomData.get_password(),
            role=UserRole.USER
        )

        create_user_response = AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.entity_was_created()
        ).post(create_user_request)

        login_user_response = LoginUserRequester(
            RequestSpecs.unauth_spec(),
            ResponseSpecs.request_returns_OK()
        ).post(LoginUserRequest(
            username=create_user_request.username,
            password=create_user_request.password))
        
        self.soft_assert(
            self.assertTrue, 
            create_user_request.username == create_user_response.username == login_user_response.username
        )
        self.soft_assert(self.assertTrue, create_user_request.password == create_user_response.password)
        self.soft_assert(self.assertTrue, create_user_request.role == login_user_response.role)

        AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.entity_was_deleted()
        ).delete(DeleteUserRequest(id=create_user_response.id))
