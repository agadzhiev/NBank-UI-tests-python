from src.main.ui.pages.base_page import BasePage
from src.main.ui.utils.ui_waits import UiWaits


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
        return "/edit-profile"

    def wait_until_loaded(self):
        UiWaits.visible(self.page_title)
        UiWaits.visible(self.name_input)
        UiWaits.enabled(self.save_changes_button)
        return self

    def wait_profile_form_ready(self):
        return self.wait_until_loaded()

    def wait_profile_saved(self):
        self.page.wait_for_load_state("networkidle")
        return self.wait_profile_form_ready()

    def check_page_is_visible(self):
        return self.wait_until_loaded()

    def update_name(self, new_name: str):
        self.wait_profile_form_ready()
        self.name_input.fill(new_name)
        self.save_changes_button.click()
        return self.wait_profile_saved()
