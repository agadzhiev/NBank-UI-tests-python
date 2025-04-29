import abc

from src.main.api.models.base_model import BaseModel
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class Request(abc.ABC):
    def __init__(self, base_url: str, response_spec: ResponseSpecs, headers: dict = None):
        self.base_url = base_url
        self.headers = headers if headers else {}
        self.response_spec = response_spec

    @abc.abstractmethod
    def post(self, model):
        pass