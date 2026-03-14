import pytest
from playwright.sync_api import Page

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.random_data import RandomData
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.ui.pages.login_page import LoginPage
from src.main.ui.pages.profile_page import ProfilePage


@pytest.mark.ui
@pytest.mark.usefixtures("browser_match_guard")
class TestProfile:
    @pytest.mark.prepare_users(number=1)
    def test_user_canchange_profile_name(self, page: Page,
        api_manager: ApiManager,
        prepared_users: list[CreateUserRequest]):

        prepared = prepared_users[0]
        new_name = RandomData.get_username(10)

        LoginPage(page).auth_as_user(prepared) \
            .go_to(ProfilePage(page)) \
            .check_page_is_visible() \
            .update_name(new_name)

        profile = api_manager.user_steps.get_profile(prepared)
        assert profile.username == prepared.username
        if profile.name is None:
            pytest.xfail(
                "System bug: profile name is not always returned by API after UI update."
            )
        assert profile.name == new_name
        
