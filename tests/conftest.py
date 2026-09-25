import pytest
import allure
from api.auth_api import AuthApi
from api.ingredients_api import IngredientsApi
from api.user_api import UserApi
from config import BASE_URL, TEST_EMAIL, TEST_PASSWORD
from utils.generators import random_email, random_password, random_name


@pytest.fixture(scope="session")
def auth_headers():
    auth_api = AuthApi(BASE_URL)
    response = auth_api.login(TEST_EMAIL, TEST_PASSWORD)
    token = response.json()["accessToken"]
    return {"Authorization": token}


@pytest.fixture(scope="session")
def ingredients():
    ingredients_api = IngredientsApi(BASE_URL)
    response = ingredients_api.get_all()
    data = response.json()["data"]
    return [data[0]["_id"], data[1]["_id"]]


@pytest.fixture
def registered_user_for_test():
    auth_api = AuthApi(BASE_URL)
    user_api = UserApi(BASE_URL)

    user_data = {
        "email": random_email(),
        "password": random_password(),
        "name": random_name(),
    }

    response = auth_api.register(user_data)
    token = response.json()["accessToken"]
    headers = {"Authorization": token}

    yield user_data, headers

    user_api.delete_user(headers)


@pytest.fixture
def registered_user_for_login():
    auth_api = AuthApi(BASE_URL)
    user_api = UserApi(BASE_URL)

    user_data = {
        "email": random_email(),
        "password": random_password(),
        "name": random_name(),
    }

    response = auth_api.register(user_data)
    token = response.json()["accessToken"]
    headers = {"Authorization": token}

    yield user_data, headers

    user_api.delete_user(headers)


@pytest.fixture
def registered_user_for_update():
    auth_api = AuthApi(BASE_URL)
    user_api = UserApi(BASE_URL)

    user_data = {
        "email": random_email(),
        "password": random_password(),
        "name": random_name(),
    }

    response = auth_api.register(user_data)
    token = response.json()["accessToken"]
    headers = {"Authorization": token}

    yield user_data, headers

    user_api.delete_user(headers)


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