from src.main.api.classes.api_manager import ApiManager

from decimal import Decimal


def _get_balance(api_manager: ApiManager, account_number: str) -> Decimal:
    return api_manager.database_steps.get_account_balance_by_account_number(account_number)


def _assert_balance_changed(before_balance: Decimal,
    after_balance: Decimal,
    delta_value: Decimal,
    account_number: str,):
    assert after_balance == before_balance + delta_value, (
        f"Expected balance change {delta_value} for account '{account_number}', "
        f"but before={before_balance}, after={after_balance}"
    )