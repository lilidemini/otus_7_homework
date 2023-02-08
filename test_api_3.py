import pytest
import requests
import random
from jsonschema import validate

@pytest.mark.parametrize('id, expected_id',
                         [(10000, 10000),
                          (-1, -1, ),
                          (0, 0)])
@pytest.mark.parametrize('title, expected_title',
                         [('title', 'title'),
                          ('', ''),
                          (100, 100),
                          ('&', '&')])
def test_creating_resource(base_url_3, id, expected_id, title, expected_title):
    json = {'title': title, 'body': 'creating resourse', 'userId': id}
    res_json = requests.post(base_url_3 + '/posts', json=json).json()
    assert res_json['title'] == expected_title
    assert res_json['body'] == 'creating resourse'
    assert res_json['userId'] == expected_id

@pytest.mark.parametrize('body, expected_body',
                          [('updated body', 'updated body'),
                           ('тело изменено', 'тело изменено'),
                           (100, 100)],
                         ids=["latin", "cyrillic", "number_int"])
def test_updating_body(base_url_3, body, expected_body):
    random_userId = random.randint(1,20)
    json = {'body': body, 'userId': random_userId}
    res_json = requests.put(base_url_3 + '/posts/1', json=json).json()
    assert res_json['body'] == expected_body
    assert res_json['userId'] == random_userId

def test_response_headers(base_url_3):
    headers = {'User-Agent': 'new'}
    res = requests.get(base_url_3 + '/posts/1', headers=headers)
    assert res.request.headers.get('User-Agent') == headers['User-Agent']

def test_json_schema(base_url_3):
    random_userId = random.randint(1, 20)
    response = requests.get(base_url_3 + '/posts').json()[random_userId]
    print(response)
    schema = {
        "type": "object",
        "properties": {
            "id": {"type": "number"},
            "title": {"type": "string"},
            "body": {"type": "string"},
            "userId": {"type": "number"},
        },
        "required": ["id", "title", "body", "userId"]
    }

    validate(instance=response, schema=schema)

@pytest.mark.parametrize('userId', [-1, 0, 'a', 11],
                         ids=["negative", "zero", "letter", "out_of_range"])
def test_api_empty_response_on_user_id(base_url_3, userId, ):
    assert requests.get(base_url_3 + "/posts", params={'userId': userId}).json() == []

