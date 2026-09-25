import allure
from api.base_api import BaseApi
from data.urls import USER


class UserApi(BaseApi):

    @allure.step("Получить данные пользователя")
    def get_user(self, headers: dict | None = None):
        return self.get(USER, headers=headers)

    @allure.step("Обновить email пользователя")
    def update_email(self, email: str, headers: dict | None = None):
        return self.patch(USER, headers=headers, json={"email": email})

    @allure.step("Обновить имя пользователя")
    def update_name(self, name: str, headers: dict | None = None):
        return self.patch(USER, headers=headers, json={"name": name})

    @allure.step("Обновить пароль пользователя")
    def update_password(self, password: str, headers: dict | None = None):
        return self.patch(USER, headers=headers, json={"password": password})

    @allure.step("Удалить пользователя")
    def delete_user(self, headers: dict | None = None):
        return self.delete(USER, headers=headers)