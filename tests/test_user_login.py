import requests


class TestUserLogin:
    def test_login_existing_user(self, base_url, registered_user):
        response = requests.post(
            f"{base_url}/auth/login",
            json={
                "email": registered_user["user_data"]["email"],
                "password": registered_user["user_data"]["password"],
            },
            timeout=10,
        )
        assert response.status_code == 200, response.text

        data = response.json()
        assert data["success"] is True
        assert data["accessToken"].startswith("Bearer ")
        assert data["refreshToken"]
        assert data["user"]["email"] == registered_user["user_data"]["email"]

    def test_login_with_wrong_credentials_returns_401(self, base_url, registered_user):
        response = requests.post(
            f"{base_url}/auth/login",
            json={
                "email": "wrong_" + registered_user["user_data"]["email"],
                "password": "wrong_password_123",
            },
            timeout=10,
        )
        assert response.status_code == 401, response.text

        data = response.json()
        assert data["success"] is False
        assert data["message"] == "email or password are incorrect"