import requests


class TestUserOrders:
    def test_get_user_orders_authorized(self, base_url, auth_headers):
        response = requests.get(
            f"{base_url}/orders",
            headers=auth_headers,
            timeout=10,
        )
        assert response.status_code == 200, response.text

        data = response.json()
        assert data["success"] is True
        assert "orders" in data and isinstance(data["orders"], list)
        assert "total" in data
        assert "totalToday" in data

    def test_get_user_orders_unauthorized_returns_401(self, base_url):
        response = requests.get(f"{base_url}/orders", timeout=10)
        assert response.status_code == 401, response.text

        data = response.json()
        assert data["success"] is False
        assert data["message"] == "You should be authorised"