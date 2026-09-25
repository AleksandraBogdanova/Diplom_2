import allure
from api.base_api import BaseApi
from data.urls import INGREDIENTS


class IngredientsApi(BaseApi):

    @allure.step("Получить список ингредиентов")
    def get_all(self):
        return self.get(INGREDIENTS)