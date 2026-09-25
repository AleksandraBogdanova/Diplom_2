import allure
from api.auth_api import AuthApi
from api.user_api import UserApi
from config import BASE_URL
from data.messages import UNAUTHORIZED_MESSAGE
from utils.generators import random_email, random_password, random_name


@allure.feature("Изменение данных пользователя")
class TestUserUpdate:

    @allure.title("Изменение email авторизованным пользователем")
    def test_update_email_authorized(self, registered_user_for_update):
        _, headers = registered_user_for_update
        new_email = random_email()

        user_api = UserApi(BASE_URL)
        response = user_api.update_email(new_email, headers)

        assert response.status_code == 200, response.text

        data = response.json()
        assert data["success"] is True
        assert data["user"]["email"] == new_email

    @allure.title("Изменение имени авторизованным пользователем")
    def test_update_name_authorized(self, registered_user_for_update):
        _, headers = registered_user_for_update
        new_name = random_name()

        user_api = UserApi(BASE_URL)
        response = user_api.update_name(new_name, headers)

        assert response.status_code == 200, response.text

        data = response.json()
        assert data["success"] is True
        assert data["user"]["name"] == new_name

    @allure.title("Изменение пароля авторизованным пользователем")
    def test_update_password_authorized(self, registered_user_for_update):
        user_data, headers = registered_user_for_update
        new_password = random_password()

        user_api = UserApi(BASE_URL)
        response = user_api.update_password(new_password, headers)

        assert response.status_code == 200, response.text

        data = response.json()
        assert data["success"] is True

        auth_api = AuthApi(BASE_URL)
        login_response = auth_api.login(user_data["email"], new_password)
        assert login_response.status_code == 200, login_response.text

    @allure.title("Изменение email без авторизации — 401")
    def test_update_email_unauthorized_returns_401(
        self, registered_user_for_update
    ):
        user_api = UserApi(BASE_URL)
        response = user_api.update_email(random_email())

        assert response.status_code == 401, response.text

        data = response.json()
        assert data["success"] is False
        assert data["message"] == UNAUTHORIZED_MESSAGE

    @allure.title("Изменение имени без авторизации — 401")
    def test_update_name_unauthorized_returns_401(
        self, registered_user_for_update
    ):
        user_api = UserApi(BASE_URL)
        response = user_api.update_name(random_name())

        assert response.status_code == 401, response.text

        data = response.json()
        assert data["success"] is False
        assert data["message"] == UNAUTHORIZED_MESSAGE

    @allure.title("Изменение пароля без авторизации — 401")
    def test_update_password_unauthorized_returns_401(
        self, registered_user_for_update
    ):
        user_api = UserApi(BASE_URL)
        response = user_api.update_password(random_password())

        assert response.status_code == 401, response.text

        data = response.json()
        assert data["success"] is False
        assert data["message"] == UNAUTHORIZED_MESSAGE