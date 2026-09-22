import pytest
import allure
from tests.api_client import AuthApi, IngredientsApi
from tests.config import BASE_URL, TEST_EMAIL, TEST_PASSWORD


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def auth_headers(base_url):
    auth_api = AuthApi(base_url)
    response = auth_api.login(TEST_EMAIL, TEST_PASSWORD)
    assert response.status_code == 200, response.text
    return {"Authorization": response.json()["accessToken"]}


@pytest.fixture(scope="session")
def ingredients(base_url):
    ingredients_api = IngredientsApi(base_url)
    response = ingredients_api.get_all()
    assert response.status_code == 200, response.text
    data = response.json()["data"]
    return [data[0]["_id"], data[1]["_id"]]


@pytest.fixture
def unique_user():
    from helpers import random_email, random_password, random_name
    return {
        "email": random_email(),
        "password": random_password(),
        "name": random_name(),
    }


@pytest.fixture
def registered_user(base_url, unique_user):
    auth_api = AuthApi(base_url)

    register_response = auth_api.register(unique_user)
    assert register_response.status_code == 200, register_response.text

    login_response = auth_api.login(
        unique_user["email"],
        unique_user["password"],
    )
    assert login_response.status_code == 200, login_response.text

    return {
        "user_data": unique_user,
        "response": register_response.json(),
        "headers": {
            "Authorization": login_response.json()["accessToken"]
        },
    }


@pytest.fixture
def auth_api(base_url):
    return AuthApi(base_url)


@pytest.fixture
def user_api(base_url):
    from tests.api_client import UserApi
    return UserApi(base_url)


@pytest.fixture
def orders_api(base_url):
    from tests.api_client import OrdersApi
    return OrdersApi(base_url)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(autouse=True)
def screenshot_on_failure(request):
    yield
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        driver = request.node.funcargs.get("driver") or \
                 request.node.funcargs.get("authorized_driver")
        if driver is not None:
            allure.attach(
                driver.get_screenshot_as_png(),
                name=f"failure_{request.node.name}",
                attachment_type=allure.attachment_type.PNG,
            )