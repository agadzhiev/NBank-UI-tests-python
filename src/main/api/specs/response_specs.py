class ResponseSpecs:
    @staticmethod
    def entity_was_created(response):
        assert response.status_code == 201
        return response

    @staticmethod
    def response_status_code_is_200(response):
        assert response.status_code == 200
        return response
