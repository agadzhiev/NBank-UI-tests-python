import pytest
import requests


@pytest.fixture
def login():
    login_url = "http://localhost:4111/api/v1/auth/login"
    login_payload = {
        "username": "admin",
        "password": "admin"
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    response = requests.post(login_url, json=login_payload, headers=headers)
    response.raise_for_status() 
    return response.headers["Authorization"]


class TestSimple:
    def test_user_can_generate_token(self, login):
        url = "http://localhost:4111/api/v1/auth/login"
        payload = {
            "username": "admin",
            "password": "admin"
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)

        assert response.status_code == 200
        assert "Authorization" in response.headers
        assert response.headers["Authorization"] == login


    def test_admin_can_create_user(self, login):
        url = "http://localhost:4111/api/v1/admin/users"
        payload = {
            "username": "newuser1234567",
            "password": "password123",
            "role": "USER"
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": login
        }

        response = requests.post(url, json=payload, headers=headers)

        assert response.status_code == 201


    def test_user_can_create_account(self, login):
        login_url = "http://localhost:4111/api/v1/auth/login"
        login_payload = {
            "username": "newuser1234567",
            "password": "password123"
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        login_response = requests.post(login_url, json=login_payload, headers=headers)
        user_auth_header = login_response.headers["Authorization"]

        account_url = "http://localhost:4111/api/v1/accounts"
        account_headers = {
            "Content-Type": "application/json",
            "Authorization": user_auth_header
        }

        account_response = requests.post(account_url, headers=account_headers)

        assert account_response.status_code == 201
        account_number = account_response.json()["accountNumber"]
        print(f"Account Number: {account_number}")


