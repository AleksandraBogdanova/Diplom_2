import pytest
import allure
from api.auth_api import AuthApi
from api.ingredients_api import IngredientsApi
from api.orders_api import OrdersApi
from api.user_api import UserApi
from config import BASE_URL, TEST_EMAIL, TEST_PASSWORD


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def auth_headers(base_url):
    auth_api = AuthApi(base_url)
    response = auth_api.login(TEST_EMAIL, TEST_PASSWORD)
    token = response.json()["accessToken"]
    return {"Authorization": token}


@pytest.fixture(scope="session")
def ingredients(base_url):
    ingredients_api = IngredientsApi(base_url)
    response = ingredients_api.get_all()
    data = response.json()["data"]
    return [data[0]["_id"], data[1]["_id"]]


@pytest.fixture
def auth_api(base_url):
    return AuthApi(base_url)


@pytest.fixture
def user_api(base_url):
    return UserApi(base_url)


@pytest.fixture
def orders_api(base_url):
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