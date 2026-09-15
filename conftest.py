import pytest
import requests

from helpers import (
    random_email,
    random_password,
    random_name,
    build_user_payload,
)

BASE_URL = "https://stellarburgers.education-services.ru/api"


@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL


@pytest.fixture
def unique_user() -> dict:
    return build_user_payload(
        email=random_email(),
        password=random_password(),
        name=random_name(),
    )


@pytest.fixture
def registered_user(unique_user):
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json=unique_user,
        timeout=10,
    )
    assert response.status_code == 200, (
        f"Не удалось создать пользователя: {response.status_code} {response.text}"
    )
    data = response.json()
    yield {
        "user_data": unique_user,
        "access_token": data["accessToken"],
        "refresh_token": data["refreshToken"],
    }


@pytest.fixture
def auth_headers(registered_user) -> dict:
    return {"Authorization": registered_user["access_token"]}


@pytest.fixture
def ingredients() -> list[str]:
    response = requests.get(f"{BASE_URL}/ingredients", timeout=10)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    ids = [item["_id"] for item in data["data"]]
    return ids[:2]