import pytest
import time


@pytest.fixture(scope="session")
def auth_token():
    return "1fc9e061-edad-4bdf-b6e4-ca0d1c174aff"


@pytest.fixture(scope="session")
def base_url():
    return "https://getpantry.cloud/apiv1/pantry/"


@pytest.fixture(scope="session")
def pantry_url(base_url, auth_token):
    return f"{base_url}{auth_token}"


@pytest.fixture(scope="session")
def basket_url(pantry_url):
    return f"{pantry_url}/basket/"


@pytest.fixture(scope="session")
def headers():
    return {
        "Content-Type": "application/json"
    }


@pytest.fixture(autouse=True)
def sleep_after_test():
    yield
    time.sleep(3)
