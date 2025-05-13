import requests

from src.main.api.requests.requester import Requester


class AdminLoginUserRequester(Requester):
    def post(self, login_user_request):
        url = f"{self.base_url}/auth/login"
        response = requests.post(url, json=login_user_request, headers=self.headers)
        self.response_spec(response)
        return response
