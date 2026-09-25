import allure
from api.auth_api import AuthApi
from config import BASE_URL
from data.messages import INVALID_CREDENTIALS_MESSAGE


@allure.feature("Авторизация пользователя")
class TestUserLogin:

    @allure.title("Авторизация существующего пользователя")
    def test_login_existing_user(self, registered_user_for_login):
        user_data, _ = registered_user_for_login

        auth_api = AuthApi(BASE_URL)
        response = auth_api.login(user_data["email"], user_data["password"])

        assert response.status_code == 200, response.text

        data = response.json()
        assert data["success"] is True
        assert data["accessToken"].startswith("Bearer ")
        assert data["refreshToken"]
        assert data["user"]["email"] == user_data["email"]

    @allure.title("Авторизация с неверными данными — 401")
    def test_login_with_wrong_credentials_returns_401(
        self, registered_user_for_login
    ):
        user_data, _ = registered_user_for_login

        auth_api = AuthApi(BASE_URL)
        response = auth_api.login(
            "wrong_" + user_data["email"],
            "wrong_password_123",
        )

        assert response.status_code == 401, response.text

        data = response.json()
        assert data["success"] is False
        assert data["message"] == INVALID_CREDENTIALS_MESSAGE