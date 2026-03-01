from playwright.sync_api import expect

from src.main.ui.pages.base_page import BasePage


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

    def check_page_is_visible(self):
        expect(self.page_title).to_be_visible()
        return self

    def deposit_to_account(self, account_id: int, amount: float):
        self.account_selector.select_option(str(account_id))
        self.amount_input.fill(str(amount))
        self.deposit_button.click()
        self.page.wait_for_load_state("networkidle")
        return self