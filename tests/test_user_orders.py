import allure
from tests.api_client import OrdersApi
from tests.messages import UNAUTHORIZED_MESSAGE


@allure.feature("Заказы пользователя")
class TestUserOrders:

    @allure.title("Получение заказов авторизованным пользователем")
    def test_get_user_orders_authorized(self, base_url, auth_headers):
        orders_api = OrdersApi(base_url)
        response = orders_api.get_user_orders(auth_headers)

        assert response.status_code == 200, response.text

        data = response.json()
        assert data["success"] is True
        assert "orders" in data and isinstance(data["orders"], list)
        assert "total" in data
        assert "totalToday" in data

    @allure.title("Получение заказов неавторизованным — 401")
    def test_get_user_orders_unauthorized_returns_401(self, base_url):
        orders_api = OrdersApi(base_url)
        response = orders_api.get_user_orders()

        assert response.status_code == 401, response.text

        data = response.json()
        assert data["success"] is False
        assert data["message"] == UNAUTHORIZED_MESSAGE