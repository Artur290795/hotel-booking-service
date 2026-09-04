import pytest
from rest_framework.test import APIClient

from bookings.models import Room


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


@pytest.fixture
def add_room_to_db(room_factory):
    def add_room(without_description=False, without_price=False, **kwargs):
        room_data = room_factory(
            without_description=without_description,
            without_price=without_price,
            **kwargs,
        )
        room = Room.objects.create(**room_data)
        return room

    return add_room


@pytest.fixture
def booking_factory():
    def make_booking_data(
        without_room=False,
        without_start_date=False,
        without_finish_date=False,
        **kwargs,
    ):
        defaults = {
            "room_id": 1,
            "start_date": "2026-01-01",
            "finish_date": "2026-01-02",
        }
        defaults.update(kwargs)
        if without_room:
            del defaults["room_id"]
        if without_start_date:
            del defaults["start_date"]
        if without_finish_date:
            del defaults["finish_date"]
        return defaults

    return make_booking_data
