import requests
import allure


class ApiClient:
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url
        self.timeout = timeout

    @allure.step("POST {endpoint}")
    def post(self, endpoint: str,
             headers: dict | None = None,
             json: dict | None = None):
        return requests.post(
            f"{self.base_url}{endpoint}",
            headers=headers,
            json=json,
            timeout=self.timeout,
        )

    @allure.step("GET {endpoint}")
    def get(self, endpoint: str,
            headers: dict | None = None,
            params: dict | None = None):
        return requests.get(
            f"{self.base_url}{endpoint}",
            headers=headers,
            params=params,
            timeout=self.timeout,
        )

    @allure.step("PATCH {endpoint}")
    def patch(self, endpoint: str,
              headers: dict | None = None,
              json: dict | None = None):
        return requests.patch(
            f"{self.base_url}{endpoint}",
            headers=headers,
            json=json,
            timeout=self.timeout,
        )

    @allure.step("DELETE {endpoint}")
    def delete(self, endpoint: str, headers: dict | None = None):
        return requests.delete(
            f"{self.base_url}{endpoint}",
            headers=headers,
            timeout=self.timeout,
        )


class AuthApi(ApiClient):

    @allure.step("Зарегистрировать пользователя")
    def register(self, payload: dict):
        return self.post("/auth/register", json=payload)

    @allure.step("Авторизоваться: {email}")
    def login(self, email: str, password: str):
        return self.post(
            "/auth/login",
            json={"email": email, "password": password},
        )


class IngredientsApi(ApiClient):

    @allure.step("Получить список ингредиентов")
    def get_all(self):
        return self.get("/ingredients")


class UserApi(ApiClient):

    @allure.step("Получить данные пользователя")
    def get_user(self, headers: dict | None = None):
        return self.get("/auth/user", headers=headers)

    @allure.step("Обновить email пользователя")
    def update_email(self, email: str, headers: dict | None = None):
        return self.patch("/auth/user", headers=headers, json={"email": email})

    @allure.step("Обновить имя пользователя")
    def update_name(self, name: str, headers: dict | None = None):
        return self.patch("/auth/user", headers=headers, json={"name": name})

    @allure.step("Обновить пароль пользователя")
    def update_password(self, password: str, headers: dict | None = None):
        return self.patch(
            "/auth/user",
            headers=headers,
            json={"password": password},
        )


class OrdersApi(ApiClient):

    @allure.step("Создать заказ с ингредиентами")
    def create_order(self, ingredients: list,
                     headers: dict | None = None):
        return self.post(
            "/orders",
            headers=headers,
            json={"ingredients": ingredients},
        )

    @allure.step("Создать заказ без ингредиентов")
    def create_order_without_ingredients(self, headers: dict | None = None):
        return self.post(
            "/orders",
            headers=headers,
            json={"ingredients": []},
        )

    @allure.step("Создать заказ с невалидным хэшем ингредиента")
    def create_order_with_invalid_hash(self, headers: dict | None = None):
        return self.post(
            "/orders",
            headers=headers,
            json={"ingredients": ["invalid_hash_0000000000000000000000"]},
        )

    @allure.step("Получить заказы пользователя")
    def get_user_orders(self, headers: dict | None = None):
        return self.get("/orders", headers=headers)