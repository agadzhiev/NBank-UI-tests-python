from typing import Dict

from src.main.api.configs.config import Config
from src.main.api.requests.skeleton.endpoint import Endpoint
from src.main.api.requests.skeleton.requesters.crud_requester import CrudRequester
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.specs.response_specs import ResponseSpecs


auth_headers: Dict[str, str] = {
    "admin": "Basic YWRtaW46YWRtaW4="
}

class RequestSpecs:
    @staticmethod
    def _base_url() -> str:
        return f"{Config.get('server')}{Config.get('apiVersion')}"

    @staticmethod
    def _default_headers() -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    @staticmethod
    def unauth_spec() -> Dict[str, str]:
        return RequestSpecs._default_headers()

    @staticmethod
    def admin_spec() -> Dict[str, str]:
        headers = RequestSpecs._default_headers()
        headers["Authorization"] = auth_headers["admin"]
        return headers

    @staticmethod
    def auth_as_user(username: str, password: str) -> Dict[str, str]:
        if username not in auth_headers:
            request = LoginUserRequest(username=username, password=password)
            crud = CrudRequester(
                request_spec=RequestSpecs.unauth_spec(),
                endpoint=Endpoint.LOGIN,
                response_spec=ResponseSpecs.request_returns_ok()
            )
            response = crud.post(request)
            auth_header = response.headers.get("Authorization")
            if not auth_header:
                raise ValueError("Authorization header not found in response")
            auth_headers[username] = auth_header

        headers = RequestSpecs._default_headers()
        headers["Authorization"] = auth_headers[username]
        return headers
