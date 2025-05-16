from typing import TypeVar, Type, Optional, Generic, Dict, Callable

from src.main.api.models.base_model import BaseModel
from src.main.api.requests.skeleton.endpoint import Endpoint
from src.main.api.requests.skeleton.http_request import HttpRequest
from src.main.api.requests.skeleton.requesters.crud_requester import CrudRequester


T = TypeVar("T", bound=BaseModel)

class ValidatedCrudRequester(HttpRequest, Generic[T]):
    def __init__(
        self,
        request_spec: Dict[str, str],
        endpoint: Endpoint,
        response_spec: Callable
    ):
        super().__init__(request_spec, endpoint, response_spec)
        self.crud_requester = CrudRequester(
            request_spec=request_spec,
            endpoint=endpoint,
            response_spec=response_spec
        )

    def post(self, model: BaseModel) -> T:
        response = self.crud_requester.post(model)
        model_class: Type[T] = self.endpoint.response_model
        return model_class.model_validate(response.json())

    def get(self, id: int) -> Optional[T]: ...

    def update(self, id: int, model: BaseModel) -> Optional[T]: ...

    def delete(self, id: int) -> bool: ...