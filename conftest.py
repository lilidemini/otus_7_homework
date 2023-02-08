import pytest
import requests

def pytest_addoption(parser):
    parser.addoption('--url_1', default='https://dog.ceo/api')
    parser.addoption('--url_2', default='https://api.openbrewerydb.org/breweries')
    parser.addoption('--url_3', default='https://jsonplaceholder.typicode.com')
    parser.addoption('--url', default='https://ya.ru')
    parser.addoption('--status_code', default=200)

@pytest.fixture
def base_url_1(request):
    return request.config.getoption("--url_1")

@pytest.fixture
def base_url_2(request):
    return request.config.getoption("--url_2")

@pytest.fixture
def base_url_3(request):
    return request.config.getoption("--url_3")

@pytest.fixture
def url(request):
    return request.config.getoption("--url")

@pytest.fixture
def status_code(request):
    return int(request.config.getoption("--status_code"))
