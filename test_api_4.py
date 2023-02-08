import requests

def test_url_status_code(url, status_code):
    response_code = requests.get(url).status_code
    assert response_code == status_code
