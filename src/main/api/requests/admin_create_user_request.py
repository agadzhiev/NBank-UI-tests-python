import requests

from src.main.api.requests.request import Request


class AdminCreateUserRequest(Request):
    def post(self, create_user_request):
        url = f"{self.base_url}/admin/users"
        response = requests.post(url, json=create_user_request, headers=self.headers)
        self.response_spec(response)
        return response
