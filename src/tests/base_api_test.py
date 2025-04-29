import requests
from pytest import fixture


class BaseApiTest:
    @fixture(autouse=True)
    def setup_api_tests(self):
        self.softly = []

    def add_soft_assertion(self, assertion):
        self.softly.append(assertion)

    def assert_all(self):
        for assertion in self.softly:
            assertion()