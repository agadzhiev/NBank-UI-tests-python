import pytest
import requests


class TestValidation:
    @pytest.mark.parametrize(
        "username, password, role",
        [
            ("newuser12", "password123!", "USER"),
            ("john_doe", "Password!23", "USER"),
            ("jane.doe", "Pass1234$", "USER")
        ] 
    )
    def test_admin_can_create_user_with_correct_data(self, username, password, role):
        url = "http://localhost:4111/api/v1/admin/users"
        request_body = {
            "username": username,
            "password": password,
            "role": role
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Basic YWRtaW46YWRtaW4="
        }

        response = requests.post(url, json=request_body, headers=headers)

        assert response.status_code == 201
        response_json = response.json()
        assert response_json["username"] == username
        assert response_json["role"] == role

        # Assuming the password is not returned or is hashed
        assert "password" not in response_json


    def test_admin_cannot_create_user_with_existing_username(self):
        existing_username = "existinguser"
        url = "http://localhost:4111/api/v1/admin/users"
        request_body = {
            "username": existing_username,
            "password": "newPassword!123",
            "role": "USER"
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Basic YWRtaW46YWRtaW4="
        }

        response = requests.post(url, json=request_body, headers=headers)

        assert response.status_code == 400
        assert response.text == f"Error: Username '{existing_username}' already exists."

