import requests


class TestOrderCreation:
    def test_create_order_authorized_with_ingredients(
        self, base_url, auth_headers, ingredients
    ):
        response = requests.post(
            f"{base_url}/orders",
            headers=auth_headers,
            json={"ingredients": ingredients},
            timeout=10,
        )
        assert response.status_code == 200, response.text

        data = response.json()
        assert data["success"] is True
        assert "name" in data and data["name"]
        assert "order" in data and "number" in data["order"]

    def test_create_order_unauthorized_returns_401(self, base_url, ingredients):
        response = requests.post(
            f"{base_url}/orders",
            json={"ingredients": ingredients},
            timeout=10,
        )
        assert response.status_code == 401, response.text

        data = response.json()
        assert data["success"] is False
        assert data["message"] == "You should be authorised"

    def test_create_order_without_ingredients_returns_400(
        self, base_url, auth_headers
    ):
        response = requests.post(
            f"{base_url}/orders",
            headers=auth_headers,
            json={"ingredients": []},
            timeout=10,
        )
        assert response.status_code == 400, response.text

        data = response.json()
        assert data["success"] is False
        assert data["message"] == "Ingredient ids must be provided"

    def test_create_order_with_invalid_hash_returns_500(
        self, base_url, auth_headers
    ):
        response = requests.post(
            f"{base_url}/orders",
            headers=auth_headers,
            json={"ingredients": ["invalid_hash_0000000000000000000000"]},
            timeout=10,
        )
        assert response.status_code == 500, response.text