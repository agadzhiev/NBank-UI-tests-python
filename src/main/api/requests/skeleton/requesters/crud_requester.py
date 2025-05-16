import requests
from typing import TypeVar, Optional

from src.main.api.configs.config import Config
from src.main.api.requests.skeleton.interfaces.crud_end_interface import CrudEndpointInterface
from src.main.api.models.base_model import BaseModel
from src.main.api.requests.skeleton.http_request import HttpRequest


T = TypeVar("T", bound=BaseModel)


class CrudRequester(HttpRequest, CrudEndpointInterface):

    def post(self, model: Optional[T]) -> requests.Response:
        body = model.model_dump() if model is not None else ""

        response = requests.post(
            url=f"{Config.get('server')}{Config.get('apiVersion')}{self.endpoint.url}",
            headers=self.request_spec,
            json=body
        )
        self.response_spec(response)
        return response

    def get(self, id: int) -> Optional[T]: ...

    def update(self, id: int, model: T) -> Optional[BaseModel]: ...

    def delete(self, id: int) -> bool: 
        response = requests.delete(
            url=f"{Config.get('server')}{Config.get('apiVersion')}{self.endpoint.url}/{id}",
            headers=self.request_spec
        )
        self.response_spec(response)
        return response