import allure
import pytest
from api.auth_api import AuthApi
from api.user_api import UserApi
from data.messages import (
    USER_ALREADY_EXISTS_MESSAGE,
    REQUIRED_FIELDS_MESSAGE,
)
from utils.generators import (
    random_email,
    random_password,
    random_name,
    build_user_payload,
)


@pytest.fixture
def registered_user_for_test(base_url):
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


@allure.feature("Создание пользователя")
class TestUserCreation:

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, base_url, user_api):
        payload = {
            "email": random_email(),
            "password": random_password(),
            "name": random_name(),
        }

        auth_api = AuthApi(base_url)
        response = auth_api.register(payload)

        assert response.status_code == 200, response.text

        data = response.json()
        assert data["success"] is True
        assert data["accessToken"].startswith("Bearer ")
        assert data["refreshToken"]
        assert data["user"]["email"] == payload["email"]
        assert data["user"]["name"] == payload["name"]

        headers = {"Authorization": data["accessToken"]}
        user_api.delete_user(headers)

    @allure.title("Создание уже зарегистрированного пользователя — 403")
    def test_create_existing_user_returns_403(
        self, base_url, registered_user_for_test
    ):
        user_data, _ = registered_user_for_test

        auth_api = AuthApi(base_url)
        response = auth_api.register(user_data)

        assert response.status_code == 403, response.text

        data = response.json()
        assert data["success"] is False
        assert data["message"] == USER_ALREADY_EXISTS_MESSAGE

    @allure.title("Создание пользователя без email — 403")
    def test_create_user_without_email_returns_403(self, base_url):
        payload = build_user_payload(
            email=None,
            password=random_password(),
            name=random_name(),
        )
        auth_api = AuthApi(base_url)
        response = auth_api.register(payload)

        assert response.status_code == 403, response.text

        data = response.json()
        assert data["success"] is False
        assert data["message"] == REQUIRED_FIELDS_MESSAGE

    @allure.title("Создание пользователя без пароля — 403")
    def test_create_user_without_password_returns_403(self, base_url):
        payload = build_user_payload(
            email=random_email(),
            password=None,
            name=random_name(),
        )
        auth_api = AuthApi(base_url)
        response = auth_api.register(payload)

        assert response.status_code == 403, response.text

        data = response.json()
        assert data["success"] is False
        assert data["message"] == REQUIRED_FIELDS_MESSAGE

    @allure.title("Создание пользователя без имени — 403")
    def test_create_user_without_name_returns_403(self, base_url):
        payload = build_user_payload(
            email=random_email(),
            password=random_password(),
            name=None,
        )
        auth_api = AuthApi(base_url)
        response = auth_api.register(payload)

        assert response.status_code == 403, response.text

        data = response.json()
        assert data["success"] is False
        assert data["message"] == REQUIRED_FIELDS_MESSAGE