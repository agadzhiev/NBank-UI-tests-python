import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.update_profile_request import UpdateProfileRequest
from src.main.api.requests.skeleton.endpoint import Endpoint
from src.main.api.requests.skeleton.requesters.crud_requester import CrudRequester
from src.main.api.specs.request_specs import RequestSpecs


@pytest.mark.api
@pytest.mark.api_version("with_database")
class TestUpdateProfile:
    @pytest.mark.parametrize("update_profile_request", [RandomModelGenerator.generate(UpdateProfileRequest)])
    @pytest.mark.check_profile_field_change(
        user_source="user_request",
        profile_field="name",
        expected_value_source="update_profile_request.name",
    )
    def test_update_profile_name(
        self,
        api_manager: ApiManager,
        user_request: CreateUserRequest,
        update_profile_request: UpdateProfileRequest,
    ):
        api_manager.user_steps.update_profile(user_request, update_profile_request)

    @pytest.mark.parametrize("update_profile_request", [UpdateProfileRequest(name="")])
    @pytest.mark.check_profile_field_change(
        user_source="user_request",
        profile_field="name",
        expect_unchanged=True,
    )
    def test_user_cannot_update_profile_with_empty_name(
        self,
        user_request: CreateUserRequest,
        update_profile_request: UpdateProfileRequest,
    ):
        response = CrudRequester(
            RequestSpecs.auth_as_user(user_request.username, user_request.password),
            Endpoint.UPDATE_CUSTOMER_PROFILE,
            lambda response: None,
        ).post(update_profile_request)

        assert response.status_code == 405, (
            f"Expected 405 for empty profile name, got {response.status_code}. "
            f"Response body: {response.text}"
        )
