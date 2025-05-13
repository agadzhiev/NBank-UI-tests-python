import requests

from src.main.api.requests.requester import Requester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.delete_user_request import DeleteUserRequest


class AdminUserRequester(Requester):
    def post(self, create_user_request: CreateUserRequest) -> CreateUserResponse:
        url = f"{self.base_url}/admin/users"
        response = requests.post(url, json=create_user_request.model_dump(), headers=self.headers)
        self.response_spec(response)
        return CreateUserResponse(**response.json())

    def delete(self, delete_user_request: DeleteUserRequest):
        url = f"{self.base_url}/admin/users/{delete_user_request.id}"
        response = requests.delete(url, headers=self.headers)
        self.response_spec(response)
        return response