from enum import Enum
from dataclasses import dataclass
from typing import Type
from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.models.create_account_response import CreateAccountResponse


@dataclass(frozen=True)
class EndpointConfig:
    url: str
    request_model: Type[BaseModel]
    response_model: Type[BaseModel]


class Endpoint(Enum):
    ADMIN_USER = EndpointConfig(
        url="/admin/users",
        request_model=CreateUserRequest,
        response_model=CreateUserResponse,
    )

    LOGIN = EndpointConfig(
        url="/auth/login",
        request_model=LoginUserRequest,
        response_model=LoginUserResponse,
    )

    ACCOUNTS = EndpointConfig(
        url="/accounts",
        request_model=BaseModel,
        response_model=CreateAccountResponse,
    )

    @property
    def url(self) -> str:
        return self.value.url

    @property
    def request_model(self) -> Type[BaseModel]:
        return self.value.request_model

    @property
    def response_model(self) -> Type[BaseModel]:
        return self.value.response_model
