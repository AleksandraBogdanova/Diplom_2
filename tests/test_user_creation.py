import requests

from helpers import random_email, random_password, random_name, build_user_payload


class TestUserCreation:
    def test_create_unique_user(self, base_url, unique_user):
        response = requests.post(
            f"{base_url}/auth/register",
            json=unique_user,
            timeout=10,
        )
        assert response.status_code == 200, response.text

        data = response.json()
        assert data["success"] is True
        assert "accessToken" in data and data["accessToken"].startswith("Bearer ")
        assert "refreshToken" in data and data["refreshToken"]
        assert data["user"]["email"] == unique_user["email"]
        assert data["user"]["name"] == unique_user["name"]

    def test_create_existing_user_returns_403(self, base_url, registered_user):
        """1.2 Создать пользователя, который уже зарегистрирован."""
        response = requests.post(
            f"{base_url}/auth/register",
            json=registered_user["user_data"],
            timeout=10,
        )
        assert response.status_code == 403, response.text

        data = response.json()
        assert data["success"] is False
        assert data["message"] == "User already exists"

    def test_create_user_without_email_returns_403(self, base_url):
        payload = build_user_payload(
            email=None,
            password=random_password(),
            name=random_name(),
        )
        response = requests.post(
            f"{base_url}/auth/register", json=payload, timeout=10
        )
        assert response.status_code == 403, response.text
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "Email, password and name are required fields"

    def test_create_user_without_password_returns_403(self, base_url):
        payload = build_user_payload(
            email=random_email(),
            password=None,
            name=random_name(),
        )
        response = requests.post(
            f"{base_url}/auth/register", json=payload, timeout=10
        )
        assert response.status_code == 403, response.text
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "Email, password and name are required fields"

    def test_create_user_without_name_returns_403(self, base_url):
        payload = build_user_payload(
            email=random_email(),
            password=random_password(),
            name=None,
        )
        response = requests.post(
            f"{base_url}/auth/register", json=payload, timeout=10
        )
        assert response.status_code == 403, response.text
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "Email, password and name are required fields"