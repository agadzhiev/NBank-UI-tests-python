import pytest
import requests

from src.tests.base_api_test import BaseApiTest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_account_request import CreateAccountRequest
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.requests.admin_create_user_request import AdminCreateUserRequest

BASE_URL = "http://localhost:4111/api/v1"
HEADERS = {
    "Authorization": "Basic YWRtaW46YWRtaW4=",
    "Content-Type": "application/json",
    "Accept": "application/json"
}


@pytest.mark.api
class TestSimple(BaseApiTest):
    def test_user_can_generate_token(self):
        login_request = LoginUserRequest(username="admin", password="admin")
        unauth_spec = RequestSpecs.unauth_spec()

        response = requests.post(
            f"{unauth_spec['base_url']}/auth/login", json=login_request.model_dump(), headers=unauth_spec["headers"]
        )

        assert response.status_code == 200
        assert "Authorization" in response.headers
        assert response.headers["Authorization"] == "Basic YWRtaW46YWRtaW4="

    def test_admin_can_create_user(self):
        user_request = CreateUserRequest.generate()

        response = AdminCreateUserRequest(
            response_spec=ResponseSpecs.entity_was_created,
            **RequestSpecs.admin_auth_spec()).\
            post(user_request.model_dump())

        assert response.status_code == 201
        user_response = response.json()

        assert user_request.username == user_response["username"]
        assert user_request.role.value == user_response["role"], f'{user_request}\n\n{user_response}'

    def test_user_can_create_account(self):
        user_request = CreateUserRequest.generate()
        admin_spec = RequestSpecs.admin_auth_spec()

        response = requests.post(
            f"{admin_spec['base_url']}/admin/users",
            json=user_request.model_dump(),
            headers=admin_spec["headers"]
        )
        assert response.status_code == 201
        user_response = response.json()

        account_request = CreateAccountRequest(username=user_request.username, password=user_request.password)
        user_spec = RequestSpecs.auth_as_user(user_request.username, user_request.password)

        account_response = requests.post(
            f"{user_spec['base_url']}/accounts",
            json=account_request.model_dump(),
            headers=user_spec["headers"]
        )

        assert account_response.status_code == 201
        account_data = account_response.json()

        assert account_data["accountNumber"] is not None
        assert account_data["balance"] == 0.0
