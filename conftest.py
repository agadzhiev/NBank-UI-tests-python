from src.main.api.fixtures.setup_hook import *
from src.main.api.fixtures.user_fixtures import *
from src.main.api.fixtures.api_fixtures import *
from src.main.api.fixtures.object_fixtures import *


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """
    Убираем параметризации по браузерам для НЕ-UI тестов:
    - если тест НЕ помечен @pytest.mark.ui
    - и у него есть параметр browser_name
    -> оставляем только вариант 'chromium', остальные деселектим.
    """


    def _norm_browser_name(val) -> str:
        s = str(val).strip().lower()
        return {"chrome": "chromium", "ff": "firefox"}.get(s, s)

    keep = []
    deselect = []

    for item in items:
        is_ui = bool(item.get_closest_marker("ui"))
        fixts = getattr(item, "fixturenames", ())

        if (not is_ui) and ("browser_name" in fixts):
            callspec = getattr(item, "callspec", None)
            if callspec is not None:
                bn = _norm_browser_name(callspec.params.get("browser_name"))
                if bn != "chromium":
                    deselect.append(item)
                    continue

        keep.append(item)

    if deselect:
        config.hook.pytest_deselected(items=deselect)
        items[:] = keep