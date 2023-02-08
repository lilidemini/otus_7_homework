import pytest
import requests

def test_get_subbreed_list(base_url_1):
    response = requests.get(base_url_1 + '/breeds/list/all')
    assert response.status_code == 200
    assert response.json().get('status') == 'success'

@pytest.mark.parametrize('breed', ['sharpei', 'saluki', 'redbone'])
def test_get_breed_random_image(base_url_1, breed):
    response = requests.get(base_url_1 + f'/breed/{breed}/images/random')
    assert response.status_code == 200
    assert response.json().get('status') == 'success'
    image_name = response.json().get('message')
    assert breed in image_name, 'Unexpected breed in random image'

def test_subbreed_images_resolution(base_url_1):
    response = requests.get(base_url_1 + '/breed/hound/afghan/images').json().get('message')
    for i in response:
        assert '.jpg' in i, 'Unexpected image resolution, expected only .jpg'

@pytest.mark.parametrize('count', [0, 1, 50],
                         ids=["zero", "min_valid_value", "max_valid_value"])
def test_valid_count_returned_images_all_dogs(base_url_1, count):
    response = requests.get(base_url_1 + f'/breeds/image/random/{count}').json().get('message')
    assert len(response) == count

@pytest.mark.xfail(strict=True)
@pytest.mark.parametrize('number', [51, 1.5, 'a'],
                         ids=["out_of_range", "float", "letter"])
def test_error_count_returned_images_all_dogs(base_url_1, number):
    response = requests.get(base_url_1 + f'/breeds/image/random/{number}').json().get('message')
    assert len(response) == number
