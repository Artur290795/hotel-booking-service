import pytest
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def room_factory():
    def make_room_data(without_description=False, without_price=False, **kwargs):
        defaults = {
            "description": "test room",
            "price": 100,
        }
        defaults.update(kwargs)
        if without_description:
            del defaults["description"]
        if without_price:
            del defaults["price"]
        
        return defaults
    return make_room_data