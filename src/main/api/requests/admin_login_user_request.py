import requests

from src.main.api.requests.request import Request


class AdminLoginUserRequest(Request):
    def post(self, login_user_request):
        url = f"{self.base_url}/auth/login"
        response = requests.post(url, json=login_user_request, headers=self.headers)
        return response
