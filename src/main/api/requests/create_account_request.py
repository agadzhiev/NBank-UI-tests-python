import requests

from src.main.api.requests.request import Request


class CreateAccountRequest(Request):
    def post(self, model):
        url = f"{self.base_url}/accounts"
        response = requests.post(url, json=model, headers=self.headers)
        return response
