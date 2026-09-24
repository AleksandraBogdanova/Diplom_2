import allure
import pytest
from api.auth_api import AuthApi
from api.user_api import UserApi
from data.messages import INVALID_CREDENTIALS_MESSAGE
from utils.generators import random_email, random_password, random_name


@pytest.fixture
def registered_user_for_login(base_url):
    auth_api = AuthApi(base_url)
    user_api = UserApi(base_url)

    user_data = {
        "email": random_email(),
        "password": random_password(),
        "name": random_name(),
    }

    response = auth_api.register(user_data)
    token = response.json()["accessToken"]
    headers = {"Authorization": token}

    yield user_data, headers

    user_api.delete_user(headers)


@allure.feature("Авторизация пользователя")
class TestUserLogin:

    @allure.title("Авторизация существующего пользователя")
    def test_login_existing_user(self, base_url, registered_user_for_login):
        user_data, _ = registered_user_for_login

        auth_api = AuthApi(base_url)
        response = auth_api.login(user_data["email"], user_data["password"])

        assert response.status_code == 200, response.text

        data = response.json()
        assert data["success"] is True
        assert data["accessToken"].startswith("Bearer ")
        assert data["refreshToken"]
        assert data["user"]["email"] == user_data["email"]

    @allure.title("Авторизация с неверными данными — 401")
    def test_login_with_wrong_credentials_returns_401(
        self, base_url, registered_user_for_login
    ):
        user_data, _ = registered_user_for_login

        auth_api = AuthApi(base_url)
        response = auth_api.login(
            "wrong_" + user_data["email"],
            "wrong_password_123",
        )

        assert response.status_code == 401, response.text

        data = response.json()
        assert data["success"] is False
        assert data["message"] == INVALID_CREDENTIALS_MESSAGE