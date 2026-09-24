import requests
import allure


class BaseApi:
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