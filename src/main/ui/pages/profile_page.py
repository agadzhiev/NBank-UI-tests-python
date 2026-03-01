from playwright.sync_api import expect

from src.main.ui.pages.base_page import BasePage


class ProfilePage(BasePage):
    @property
    def page_title(self):
        return self.page.get_by_text("✏️ Edit Profile")

    @property
    def name_input(self):
        return self.page.get_by_placeholder("Enter new name")

    @property
    def save_changes_button(self):
        return self.page.get_by_role("button", name="💾 Save Changes")

    def url(self):
        return "/profile/edit"

    def check_page_is_visible(self):
        expect(self.page_title).to_be_visible()
        return self

    def update_name(self, new_name: str):
        self.name_input.fill(new_name)
        self.save_changes_button.click()
        self.page.wait_for_load_state("networkidle")
        return self