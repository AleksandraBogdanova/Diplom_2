import allure
from tests.api_client import AuthApi
from tests.messages import INVALID_CREDENTIALS_MESSAGE


@allure.feature("Авторизация пользователя")
class TestUserLogin:

    @allure.title("Авторизация существующего пользователя")
    def test_login_existing_user(self, base_url, registered_user):
        auth_api = AuthApi(base_url)
        response = auth_api.login(
            registered_user["user_data"]["email"],
            registered_user["user_data"]["password"],
        )

        assert response.status_code == 200, response.text

        data = response.json()
        assert data["success"] is True
        assert data["accessToken"].startswith("Bearer ")
        assert data["refreshToken"]
        assert data["user"]["email"] == registered_user["user_data"]["email"]

    @allure.title("Авторизация с неверными данными — 401")
    def test_login_with_wrong_credentials_returns_401(
        self, base_url, registered_user
    ):
        auth_api = AuthApi(base_url)
        response = auth_api.login(
            "wrong_" + registered_user["user_data"]["email"],
            "wrong_password_123",
        )

        assert response.status_code == 401, response.text

        data = response.json()
        assert data["success"] is False
        assert data["message"] == INVALID_CREDENTIALS_MESSAGE