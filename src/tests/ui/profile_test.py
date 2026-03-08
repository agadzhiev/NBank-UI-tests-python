import pytest
from playwright.sync_api import Page

from src.main.api.generators.random_data import RandomData
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.ui.pages.login_page import LoginPage
from src.main.ui.pages.profile_page import ProfilePage


@pytest.mark.ui
@pytest.mark.usefixtures("browser_match_guard")
class TestProfile:
    @pytest.mark.prepare_users(number=1)
    @pytest.mark.parametrize("new_name", [RandomData.get_username(10)])
    @pytest.mark.check_profile_field_change(
        user_source="prepared_users[0]",
        profile_field="name",
        expected_value_source="new_name",
        xfail_if_none=True,
        xfail_reason="System bug: profile name is not persisted after UI update.",
    )
    def test_user_canchange_profile_name(
        self,
        page: Page,
        prepared_users: list[CreateUserRequest],
        new_name: str,
    ):
        prepared = prepared_users[0]

        LoginPage(page).auth_as_user(prepared) \
            .go_to(ProfilePage(page)) \
            .check_page_is_visible() \
            .update_name(new_name)
        
