from src.main.ui.pages.base_page import BasePage
from src.main.ui.utils.ui_waits import UiWaits


class TransferPage(BasePage):
    @property
    def page_title(self):
        return self.page.get_by_text("🔄 Make a Transfer")

    @property
    def account_selector(self):
        return self.page.locator("select.account-selector")

    @property
    def recipient_name_input(self):
        return self.page.get_by_placeholder("Enter recipient name")

    @property
    def recipient_account_number_input(self):
        return self.page.get_by_placeholder("Enter recipient account number")

    @property
    def amount_input(self):
        return self.page.get_by_placeholder("Enter amount")

    @property
    def confirm_checkbox(self):
        return self.page.locator("#confirmCheck")

    @property
    def send_transfer_button(self):
        return self.page.get_by_role("button", name="🚀 Send Transfer")

    def url(self):
        return "/transfer"

    def wait_until_loaded(self):
        UiWaits.visible(self.page_title)
        UiWaits.visible(self.account_selector)
        UiWaits.visible(self.recipient_name_input)
        UiWaits.visible(self.recipient_account_number_input)
        UiWaits.visible(self.amount_input)
        UiWaits.visible(self.confirm_checkbox)
        UiWaits.enabled(self.send_transfer_button)
        return self

    def wait_transfer_form_ready(self):
        return self.wait_until_loaded()

    def wait_transfer_completed(self):
        self.page.wait_for_load_state("networkidle")
        return self.wait_transfer_form_ready()

    def check_page_is_visible(self):
        return self.wait_until_loaded()

    def make_transfer(
        self,
        sender_account_id: int,
        recipient_name: str,
        recipient_account_number: str,
        amount: float,
    ):
        self.wait_transfer_form_ready()
        self.account_selector.select_option(str(sender_account_id))
        self.recipient_name_input.fill(recipient_name)
        self.recipient_account_number_input.fill(recipient_account_number)
        self.amount_input.fill(str(amount))
        self.confirm_checkbox.check()
        self.send_transfer_button.click()
        return self.wait_transfer_completed()
