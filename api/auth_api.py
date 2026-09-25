import allure
from api.base_api import BaseApi
from data.urls import LOGIN, REGISTER


class AuthApi(BaseApi):

    @allure.step("Зарегистрировать пользователя")
    def register(self, payload: dict):
        return self.post(REGISTER, json=payload)

    @allure.step("Авторизоваться: {email}")
    def login(self, email: str, password: str):
        return self.post(
            LOGIN,
            json={"email": email, "password": password},
        )