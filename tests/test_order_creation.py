import allure
from api.orders_api import OrdersApi
from config import BASE_URL
from data.messages import INGREDIENTS_REQUIRED_MESSAGE


@allure.feature("Создание заказа")
class TestOrderCreation:

    @allure.title("Создание заказа авторизованным пользователем "
                  "с ингредиентами")
    def test_create_order_authorized_with_ingredients(
        self, auth_headers, ingredients
    ):
        orders_api = OrdersApi(BASE_URL)
        response = orders_api.create_order(ingredients, auth_headers)

        assert response.status_code == 200, response.text

        data = response.json()
        assert data["success"] is True
        assert data.get("name")
        assert data.get("order", {}).get("number")

    @allure.title("Создание заказа без ингредиентов — 400")
    def test_create_order_without_ingredients_returns_400(self, auth_headers):
        orders_api = OrdersApi(BASE_URL)
        response = orders_api.create_order_without_ingredients(auth_headers)

        assert response.status_code == 400, response.text

        data = response.json()
        assert data["success"] is False
        assert data["message"] == INGREDIENTS_REQUIRED_MESSAGE

    @allure.title("Создание заказа с невалидным хэшем ингредиента — 500")
    def test_create_order_with_invalid_hash_returns_500(self, auth_headers):
        orders_api = OrdersApi(BASE_URL)
        response = orders_api.create_order_with_invalid_hash(auth_headers)

        assert response.status_code == 500, response.text