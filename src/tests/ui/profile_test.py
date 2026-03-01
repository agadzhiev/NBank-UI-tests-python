import pytest
from playwright.sync_api import Page, expect

from main.api.classes.api_manager import ApiManager
from main.api.generators.random_data import RandomData
from main.api.models.create_user_request import CreateUserRequest
from main.ui.pages.login_page import LoginPage
from main.ui.pages.profile_page import ProfilePage


@pytest.mark.ui
@pytest.mark.usefixtures("browser_match_guard")
class TestProfile:
    @pytest.mark.prepare_users(number=1)
    def test_user_canchange_profile_name(self, page: Page,
        api_manager: ApiManager,
        prepared_users: list[CreateUserRequest]):

        prepared = prepared_users[0]
        new_name = RandomData.get_full_name()

        LoginPage(page).auth_as_user(prepared)

        ProfilePage(page).open() \
            .check_page_is_visible() \
            .update_name(new_name)

        user_dao = api_manager.database_steps.get_user_by_username(prepared.username)
        assert user_dao.name == new_name
        