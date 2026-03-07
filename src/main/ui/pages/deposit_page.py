from src.main.ui.pages.base_page import BasePage
from src.main.ui.pages.user_dashboard import UserDashboard
from src.main.ui.utils.ui_waits import UiWaits


class DepositPage(BasePage):
    @property
    def page_title(self):
        return self.page.get_by_text("💰 Deposit Money")

    @property
    def account_selector(self):
        return self.page.locator("select.account-selector")

    @property
    def amount_input(self):
        return self.page.get_by_placeholder("Enter amount")

    @property
    def deposit_button(self):
        return self.page.get_by_role("button", name="💵 Deposit")

    def url(self):
        return "/deposit"

    def wait_until_loaded(self):
        UiWaits.visible(self.page_title)
        UiWaits.visible(self.account_selector)
        UiWaits.visible(self.amount_input)
        UiWaits.enabled(self.deposit_button)
        return self

    def wait_form_ready(self):
        return self.wait_until_loaded()

    def wait_deposit_completed(self):
        self.page.wait_for_load_state("networkidle")
        UserDashboard(self.page).check_page_is_visible()
        return self

    def check_page_is_visible(self):
        return self.wait_until_loaded()

    def deposit_to_account(self, account_id: int, amount: float):
        self.wait_form_ready()
        self.account_selector.select_option(str(account_id))
        self.amount_input.fill(str(amount))
        self.deposit_button.click()
        return self.wait_deposit_completed()
