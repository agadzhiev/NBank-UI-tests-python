import pytest
import softest

from src.fixtures.object_fixtures import *
from src.fixtures.user_fixtures import *
from src.fixtures.api_fixtures import *


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_teardown(item):
    """Automatically call softest.assert_all() after each test if the instance is softest.TestCase"""
    outcome = yield
    test_instance = getattr(item, 'instance', None)

    if isinstance(test_instance, softest.TestCase):
        try:
            test_instance.assert_all()
        except AssertionError as e:
            raise e
        except Exception:
            pass
