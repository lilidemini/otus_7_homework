import pytest
import requests
import random

def test_get_list_breweries(base_url_2):
    random_per_page = random.randint(1, 10)
    response = requests.get(base_url_2, params={"per_page": {random_per_page}})
    assert response.status_code == 200
    assert len(response.json()) <= random_per_page, 'Unexpected number of breweries in list'

@pytest.mark.parametrize('city', ['San Diego', "Jung-gu",
                                  "Goyang-si", "Worcester"])
def test_filter_breweries_by_city(base_url_2, city):
    res_json = requests.get(base_url_2,
                            params={'by_city': city, "per_page": 5}).json()[0]
    assert res_json.get('city') == city

@pytest.mark.parametrize('state, expected', [('new_york', 'New York'),
                                             ('minnesota', 'Minnesota'),
                                             ('texas', 'Texas')])
def test_filter_breweries_by_state(base_url_2, state, expected):
    res_json = requests.get(base_url_2,
                            params={'by_state': state, "per_page": 5}).json()[0]
    assert res_json.get('state') == expected

@pytest.mark.parametrize('size', [1, 50],
                         ids=["default", "max_valid_value"])
def test_returned_number_breweries(base_url_2, size):
    response = requests.get(base_url_2 + '/random', params={'size': size}).json()
    assert len(response) == size

def test_search_brewery(base_url_2):
    params = {'query': 'brew'}
    res_json = requests.get(base_url_2 + '/search', params=params).json()
    for i in res_json:
        brewery_id = i.get('id')
        assert 'brew' in brewery_id, 'Unexpected search result'
