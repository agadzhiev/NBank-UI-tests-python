import pytest

from src.main.api.generators.random_data import RandomData
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.user_role import UserRole
from src.main.api.models.delete_user_request import DeleteUserRequest
from src.main.api.requests.admin_user_requester import AdminUserRequester
from src.tests.base_api_test import BaseTest


@pytest.mark.test
class TestCreateUser(BaseTest):
    def test_admin_can_create_user_with_correct_data(self):
        create_user_request = CreateUserRequest(
            username=RandomData.get_username(),
            password=RandomData.get_password(),
            role=UserRole.USER
        )

        create_user_response = AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.entity_was_created()
        ).post(create_user_request)

        self.soft_assert(self.assertTrue, create_user_request.username == create_user_response.username)
        self.soft_assert(self.assertTrue, create_user_request.password == create_user_response.password)
        self.soft_assert(self.assertTrue, create_user_request.role == create_user_response.role)
        
        AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.entity_was_deleted()
        ).delete(DeleteUserRequest(id=create_user_response.id))

    @pytest.mark.parametrize(
        'username, password, role, error_key, error_value',
        [
            ("   ", "Password33$", "USER", "username", "Username cannot be blank"),
            ("ab", "Password33$", "USER", "username", "Username must be between 3 and 15 characters"),
            ("abc$", "Password33$", "USER", "username", "Username must contain only letters, digits, dashes, underscores, and dots"),
            ("abc%", "Password33$", "USER", "username", "Username must contain only letters, digits, dashes, underscores, and dots"),
        ]
    )
    def admin_can_not_create_user_with_invalid_data(
        self, username: str, password: str, role: str, error_key: str, error_value: str
    ):
        create_user_request = CreateUserRequest(
            username=username,
            password=password,
            role=role
        )

        create_user_response = AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.request_returns_bad_request(error_key, error_value)
        ).post(create_user_request)

        AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.entity_was_deleted()
        ).delete(DeleteUserRequest(id=create_user_response.id))
