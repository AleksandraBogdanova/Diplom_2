import requests

from helpers import random_email, random_password, random_name


class TestUserUpdate:
    def test_update_email_authorized(self, base_url, registered_user, auth_headers):
        new_email = random_email()
        response = requests.patch(
            f"{base_url}/auth/user",
            headers=auth_headers,
            json={"email": new_email},
            timeout=10,
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["success"] is True
        assert data["user"]["email"] == new_email

    def test_update_name_authorized(self, base_url, registered_user, auth_headers):
        new_name = random_name()
        response = requests.patch(
            f"{base_url}/auth/user",
            headers=auth_headers,
            json={"name": new_name},
            timeout=10,
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["success"] is True
        assert data["user"]["name"] == new_name

    def test_update_password_authorized(self, base_url, registered_user, auth_headers):
        new_password = random_password()
        response = requests.patch(
            f"{base_url}/auth/user",
            headers=auth_headers,
            json={"password": new_password},
            timeout=10,
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["success"] is True

        login_response = requests.post(
            f"{base_url}/auth/login",
            json={
                "email": registered_user["user_data"]["email"],
                "password": new_password,
            },
            timeout=10,
        )
        assert login_response.status_code == 200

    # ---------- Без авторизации ----------

    def test_update_email_unauthorized_returns_401(self, base_url, registered_user):
        response = requests.patch(
            f"{base_url}/auth/user",
            json={"email": random_email()},
            timeout=10,
        )
        assert response.status_code == 401, response.text
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "You should be authorised"

    def test_update_name_unauthorized_returns_401(self, base_url, registered_user):
        response = requests.patch(
            f"{base_url}/auth/user",
            json={"name": random_name()},
            timeout=10,
        )
        assert response.status_code == 401, response.text
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "You should be authorised"

    def test_update_password_unauthorized_returns_401(self, base_url, registered_user):
        response = requests.patch(
            f"{base_url}/auth/user",
            json={"password": random_password()},
            timeout=10,
        )
        assert response.status_code == 401, response.text
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "You should be authorised"