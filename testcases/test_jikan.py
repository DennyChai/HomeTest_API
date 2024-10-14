import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import requests
from utils.read_datas import ReadDatas
from testcases.base_test_interface import BaseTestInterface

class TestJikan(BaseTestInterface):
  read_data = ReadDatas()
  test_data_path = r"./config/jikan.yaml"
  test_data = read_data.read_yaml(test_data_path)
  BASE_URL = "https://api.jikan.moe/v4"
  
  @pytest.fixture(scope="module")
  def setup_class(self):
    super().setup_class()
    self.cookie = {}


  @pytest.fixture
  def base_url(self):
      return "https://api.jikan.moe/v4"


  def test_can_call_endpoint(self, base_url):
    url = base_url
    response = requests.get(url)
    assert response.status_code == 200


  @pytest.mark.parametrize("id", test_data["animes_incorrect_id"])
  def test_anime_id_not_exist(self, base_url, id):
    url = f"{base_url}/anime/{id}"
    response = requests.get(url)
    assert response.status_code == 404


  @pytest.mark.parametrize("id,full_data", test_data["animes_full_data"])
  def test_anime_full_data(self, base_url, id, full_data):
    url = f"{base_url}/anime/{id}/full"
    response = requests.get(url)
    assert response.status_code == 200
    assert response.headers.get('Content-Type') == 'application/json'
    response_json = response.json()
    assert response_json["data"]["title"] == full_data["title"]


  @pytest.mark.parametrize("id,full_data", test_data["animes_full_data"])
  def test_full_data_equal_short_data(self, base_url, id, full_data):
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

