import requests

from src.main.api.requests.requester import Requester
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.get_customer_accounts_response import GetCustomerAccountsResponse

class CreateAccountRequester(Requester):
    def post(self, model) -> CreateAccountResponse:
        url = f"{self.base_url}/accounts"
        response = requests.post(url, json=model, headers=self.headers)
        self.response_spec(response)
        return CreateAccountResponse(**response.json())

    def get(self) -> GetCustomerAccountsResponse:
        url = f"{self.base_url}/customer/accounts"
        response = requests.get(url, headers=self.headers)
        self.response_spec(response)
        accounts_list = response.json()
        return GetCustomerAccountsResponse(accounts=[CreateAccountResponse(**account) for account in accounts_list])