from http import HTTPStatus
from requests import Response


class ResponseSpecs:
    @staticmethod
    def request_returns_OK():
        def check(response: Response):
            assert response.status_code == HTTPStatus.OK, response.text
        return check

    @staticmethod
    def entity_was_created():
        def check(response: Response):
            assert response.status_code == HTTPStatus.CREATED, response.text
        return check
    
    @staticmethod
    def entity_was_deleted():
        def check(response: Response):
            assert response.status_code in [HTTPStatus.OK, HTTPStatus.NO_CONTENT], response.text
        return check

    @staticmethod
    def request_returns_bad_request(
        error_key: str,
        error_value: str
    ):  
        def check(response: Response):
            assert response.status_code == HTTPStatus.BAD_REQUEST
            assert response.json().get(error_key) == error_value
        return check
