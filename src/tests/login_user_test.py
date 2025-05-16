import pytest

from src.tests.base_api_test import BaseTestWithoutSoftAsserts
from src.main.api.classes.api_manager import ApiManager


@pytest.mark.test
class TestLoginUser(BaseTestWithoutSoftAsserts):

    @pytest.mark.usefixtures('api_manager')
    def test_admin_can_generate_auth_token_test(self, api_manager: ApiManager):
        api_manager.admin_steps.login()

    @pytest.mark.usefixtures('api_manager')
    def test_user_can_generate_auth_token(self, api_manager: ApiManager):        
        create_user_request = api_manager.admin_steps.create_user()
        api_manager.user_steps.login(create_user_request)
