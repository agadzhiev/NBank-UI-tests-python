import abc
from typing import Callable, Dict


class Requester(abc.ABC):
    def __init__(
            self, 
            request_spec: Dict[str, str], 
            response_spec: Callable, 
    ):
        self.headers = request_spec.get('headers')
        self.base_url = request_spec.get('base_url', 'http://localhost:4111')
        self.response_spec = response_spec

    @abc.abstractmethod
    def post(self, model):
        pass