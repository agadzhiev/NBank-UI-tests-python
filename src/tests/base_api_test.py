import softest


class BaseTestWithoutSoftAsserts: ...


class BaseTest(softest.TestCase, BaseTestWithoutSoftAsserts): ...