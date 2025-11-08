import pytest
from playwright.sync_api import Page

from src.main.ui.pages.login_page import LoginPage
from src.main.api.classes.session_storage import SessionStorage
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.fixture(autouse=True, scope="function")
def user_session_extension(request, page, user_factory):
    SessionStorage.clear()
    mark = request.node.get_closest_marker("user_session")
    if not mark:
        return

    count: int = max(int(mark.args[0]), 1)
    auth_index: int = int(mark.kwargs.get("auth", 0))

    users: list[CreateUserRequest] = [user_factory() for _ in range(count)]
    SessionStorage.add_users(users)
    LoginPage(page).auth_as_user(users[auth_index])


@pytest.fixture(autouse=True)
def admin_session_autologin(
    request: pytest.FixtureRequest, 
    page: Page, 
    admin_user_request: CreateUserRequest
):
    mark = request.node.get_closest_marker("admin_session")
    if not mark:
        return

    LoginPage(page).auth_as_user(admin_user_request)


@pytest.fixture(autouse=True)
def browser_match_guard(request):
    def norm(n: str) -> str:
        n = n.strip().lower()
        return {"chrome": "chromium", "ff": "firefox"}.get(n, n)

    mark = request.node.get_closest_marker("browsers")
    if not mark:
        return

    allowed = {norm(str(x)) for x in (mark.args or ())}
    if not allowed:
        return

    try:
        current = request.getfixturevalue("browser_name")
        print(current)
    except Exception:
        return

    if norm(str(current)) not in allowed:
        pytest.skip(f"Пропущен: текущий браузер '{current}' не в {sorted(allowed)}")