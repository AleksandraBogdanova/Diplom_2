import allure
from tests.api_client import AuthApi
from tests.messages import (
    USER_ALREADY_EXISTS_MESSAGE,
    REQUIRED_FIELDS_MESSAGE,
)
from helpers import (
    random_email,
    random_password,
    random_name,
    build_user_payload,
)


@allure.feature("Создание пользователя")
class TestUserCreation:

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, base_url, unique_user):
        auth_api = AuthApi(base_url)
        response = auth_api.register(unique_user)

        assert response.status_code == 200, response.text

        data = response.json()
        assert data["success"] is True
        assert data["accessToken"].startswith("Bearer ")
        assert data["refreshToken"]
        assert data["user"]["email"] == unique_user["email"]
        assert data["user"]["name"] == unique_user["name"]

    @allure.title("Создание уже зарегистрированного пользователя — 403")
    def test_create_existing_user_returns_403(
        self, base_url, registered_user
    ):
        auth_api = AuthApi(base_url)
        response = auth_api.register(registered_user["user_data"])

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