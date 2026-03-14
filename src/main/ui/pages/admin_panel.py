from typing import List
from playwright.sync_api import Locator

from src.main.ui.pages.base_page import BasePage
from src.main.ui.elements.user_badge import UserBadge
from src.main.ui.utils.ui_waits import UiWaits


class AdminPanel(BasePage):
    @property
    def admin_panel_text(self):
        return self.page.get_by_text("Admin Panel")
    
    @property
    def add_user_button(self):
        return self.page.get_by_role("button", name="Add User")
    
    def url(self):
        return "/admin"
    
    def create_user(self, username: str, password: str):
        self.wait_until_loaded()
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.add_user_button.click()
        return self
    
    def get_all_users_locator(self) -> Locator:
        return self.page.locator(".card.shadow-custom:has(:has-text('All Users'))")
    
    def get_all_users(self) -> List[UserBadge]:
        return self._generate_page_elements(self.get_all_users_locator(), UserBadge)

    def get_user_locator(self, username: str) -> Locator:
        return self.get_all_users_locator().get_by_text(username, exact=True)

    def wait_until_loaded(self):
        UiWaits.visible(self.admin_panel_text)
        UiWaits.visible(self.username_input)
        UiWaits.visible(self.password_input)
        UiWaits.enabled(self.add_user_button)
        UiWaits.visible(self.get_all_users_locator())
        return self

    def wait_user_present(self, username: str):
        UiWaits.contains_text(self.get_all_users_locator(), username)
        return self

    def wait_user_absent(self, username: str):
        UiWaits.has_count(self.get_user_locator(username), 0)
        return self
    
    def wait_for_username(self, username: str):
        return self.wait_user_present(username)

    def check_page_is_visible(self):
        return self.wait_until_loaded()

    def check_user_is_visible(self, username: str):
        return self.wait_user_present(username)

    def check_user_is_not_visible(self, username: str):
        return self.wait_user_absent(username)
