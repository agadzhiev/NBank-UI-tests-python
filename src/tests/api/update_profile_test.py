import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.random_model_generator import RandomModelGenerator
from src.main.api.models.comparison.dao_and_model_assertions import DaoAndModelAssertions
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.update_profile_request import UpdateProfileRequest
from src.main.api.models.user_profile_response import UserProfileResponse


@pytest.mark.api
@pytest.mark.api_version("with_database")
class TestUpdateProfile:
    @pytest.mark.parametrize("update_profile_request", [RandomModelGenerator.generate(UpdateProfileRequest)])
    def test_update_profile_name(
        self,
        api_manager: ApiManager,
        user_request: CreateUserRequest,
        update_profile_request: UpdateProfileRequest,
    ):
        profile_before = api_manager.user_steps.get_profile(user_request)

        api_manager.user_steps.update_profile(user_request, update_profile_request)

        user_dao = api_manager.database_steps.get_user_by_username(user_request.username)
        expected_profile = UserProfileResponse(
            id=profile_before.id,
            username=profile_before.username,
            name=update_profile_request.name,
            role=profile_before.role,
        )
        DaoAndModelAssertions.assert_that(expected_profile, user_dao).match()
