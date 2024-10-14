import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import requests
from utils.read_datas import read_test_datas

TEST_DATA_NAME = "jikan"
TEST_DATA = read_test_datas(TEST_DATA_NAME)

@pytest.fixture(scope="module")
def base_url():
    return "https://api.jikan.moe/v4"


@pytest.mark.parametrize("id", TEST_DATA["animes_id"])
def test_can_call_endpoint(base_url, id):
  url = base_url
  response = requests.get(url)
  assert response.status_code == 200

@pytest.mark.parametrize("id", TEST_DATA["animes_incorrect_id"])
def test_anime_id_not_exist(base_url, id):
  url = f"{base_url}/anime/{id}"
  response = requests.get(url)
  assert response.status_code == 404

@pytest.mark.parametrize("id,full_data", TEST_DATA["animes_full_data"])
def test_anime_full_data(base_url, id, full_data):
  url = f"{base_url}/anime/{id}/full"
  response = requests.get(url)
  assert response.status_code == 200
  assert response.headers.get('Content-Type') == 'application/json'
  response_json = response.json()
  assert response_json["data"]["title"] == full_data["title"]

@pytest.mark.parametrize("id,full_data", TEST_DATA["animes_full_data"])
def test_full_data_equal_short_data(base_url, id, full_data):
  short_data_url = f"{base_url}/anime/{id}"
  full_data_url = f"{base_url}/anime/{id}/full"
  short_data_response = requests.get(short_data_url)
  full_data_response = requests.get(full_data_url)

  assert short_data_response.status_code == 200
  assert short_data_response.headers.get('Content-Type') == 'application/json'
  short_response_json = short_data_response.json()
  full_response_json = full_data_response.json()
  assert short_response_json["data"]["title"] == full_response_json["data"]["title"] == full_data["title"]
  assert short_response_json["data"]["episodes"] == full_response_json["data"]["episodes"] == full_data["episodes"]

