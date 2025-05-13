import pytest
import softest
import logging
import http.client as http_client


@pytest.fixture(scope="session", autouse=True)
def enable_http_logging():
    http_client.HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    requests_log = logging.getLogger("urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


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
