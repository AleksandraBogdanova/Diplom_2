import allure
from api.base_api import BaseApi
from data.urls import ORDERS


class OrdersApi(BaseApi):

    @allure.step("Создать заказ с ингредиентами")
    def create_order(self, ingredients: list,
                     headers: dict | None = None):
        return self.post(
            ORDERS,
            headers=headers,
            json={"ingredients": ingredients},
        )

    @allure.step("Создать заказ без ингредиентов")
    def create_order_without_ingredients(self, headers: dict | None = None):
        return self.post(
            ORDERS,
            headers=headers,
            json={"ingredients": []},
        )

    @allure.step("Создать заказ с невалидным хэшем ингредиента")
    def create_order_with_invalid_hash(self, headers: dict | None = None):
        return self.post(
            ORDERS,
            headers=headers,
            json={"ingredients": ["invalid_hash_0000000000000000000000"]},
        )

    @allure.step("Получить заказы пользователя")
    def get_user_orders(self, headers: dict | None = None):
        return self.get(ORDERS, headers=headers)