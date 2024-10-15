from http import HTTPStatus
import read_data
import requests
import pytest
import json

test_data = read_data.load_test_data(r"./config/pantry_data.yaml")


class TestPantry:
    def test_can_call_server_with_token(self, pantry_url):
        response = requests.get(pantry_url)
        assert response.status_code == HTTPStatus.OK
        assert "application/json" in response.headers["content-type"]
        response_json = response.json()
        assert all([title in response_json
                    for title in ["name", "description", "errors", "notifications", "percentFull", "baskets"]])

    @pytest.mark.parametrize("unregistered_id", test_data["unregistered_id"])
    def test_call_server_with_unregistered_token(self, base_url, unregistered_id):
        unregistered_id_url = base_url + unregistered_id
        response = requests.get(unregistered_id_url)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert "text/html" in response.headers["content-type"]
        response_text = response.text
        assert "Could not get pantry" in response_text
        assert f"{unregistered_id} not found" in response_text

    @pytest.mark.parametrize("symbol_id", test_data["symbol_id"])
    def test_call_server_with_symbols_token(self, base_url, symbol_id):
        symbol_id_url = base_url + symbol_id
        response = requests.get(symbol_id_url)
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert "text/html" in response.headers["content-type"]
        response_text = response.text
        assert "Cannot GET" in response_text
        assert "<title>Error</title>" in response_text

    @pytest.mark.parametrize("data", test_data["data_to_update"])
    def test_update_pantry_information(self, pantry_url, headers, data):
        update_response = requests.put(
            pantry_url, headers=headers, data=json.dumps(data))
        assert update_response.status_code == HTTPStatus.OK
        assert "application/json" in update_response.headers["content-type"]
        update_result = update_response.json()

        current_response = requests.get(pantry_url)
        current_result = current_response.json()
        assert current_result == update_result

    @pytest.mark.parametrize("data", test_data["wrong_key_to_update"])
    def test_update_pantry_information_with_wrong_key(self, pantry_url, headers, data):
        original_response = requests.get(pantry_url)
        original_result = original_response.json()
        update_response = requests.put(
            pantry_url, headers=headers, data=json.dumps(data))

        assert update_response.status_code == HTTPStatus.OK  # Even not exists
        assert "application/json" in update_response.headers["content-type"]
        update_result = update_response.json()
        assert original_result == update_result
