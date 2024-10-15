from http import HTTPStatus
import read_data
import requests
import pytest
import json


test_data = read_data.load_test_data(r"./config/basket_data.yaml")


class TestBasket:
    @pytest.mark.parametrize("name", test_data["unknown_basket_name"])
    def test_read_unregistered_basket_content(self, basket_url, headers, name):
        basket_url = basket_url + name
        response = requests.get(basket_url, headers=headers)
        response_text = response.text
        assert "text/html" in response.headers["content-type"]
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert f"Could not get basket: {name} does not exist" in response_text

    @pytest.mark.parametrize("name,data", test_data["basket_content"])
    def test_create_basket(self, basket_url, headers, name, data):
        basket_url = basket_url + name
        response = requests.post(
            basket_url, headers=headers, data=json.dumps(data))
        assert "text/html" in response.headers["content-type"]
        assert response.status_code == HTTPStatus.OK
        assert f"Your Pantry was updated with basket: {name}!"

    @pytest.mark.parametrize("name", test_data["basket_name"])
    def test_read_basket_content(self, basket_url, headers, name):
        basket_url = basket_url + name
        response = requests.get(basket_url, headers=headers)
        assert "application/json" in response.headers["content-type"]
        assert response.status_code == HTTPStatus.OK

    @pytest.mark.parametrize("name,data", test_data["basket_addition_content"])
    def test_update_basket_content(self, basket_url, headers, name, data):
        basket_url = basket_url + name
        response = requests.put(
            basket_url, headers=headers, data=json.dumps(data))
        response_json = response.json()
        assert "application/json" in response.headers["content-type"]
        assert response.status_code == HTTPStatus.OK
        for k, v in data.items():
            assert k in response_json
            assert response_json[k] == v
        current_content = requests.get(basket_url, headers=headers)
        current_content_json = current_content.json()
        assert current_content_json == response_json

    @pytest.mark.parametrize("name", test_data["basket_name"])
    def test_delete_entire_basket(self, basket_url, headers, name):
        basket_url = basket_url + name
        response_delete_basket = requests.delete(basket_url, headers=headers)
        assert "text/html" in response_delete_basket.headers["content-type"]
        assert response_delete_basket.status_code == HTTPStatus.OK
        response_text = response_delete_basket.text
        assert f"{name} was removed from your Pantry" in response_text

        response_get_basket = requests.get(basket_url, headers=headers)
        response_get_basket_text = response_get_basket.text
        assert "text/html" in response_get_basket.headers["content-type"]
        assert response_get_basket.status_code == HTTPStatus.BAD_REQUEST
        assert f"Could not get basket: {name} does not exist" in response_get_basket_text

    @pytest.mark.parametrize("name", test_data["unknown_basket_name"])
    def test_delete_unregistered_basket(self, basket_url, headers, name):
        basket_url = basket_url + name
        response = requests.delete(basket_url, headers=headers)
        response_text = response.text
        assert "text/html" in response.headers["content-type"]
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert f"Could not delete basket: {name} does not exist" in response_text
