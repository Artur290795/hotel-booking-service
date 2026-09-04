from time import sleep

import pytest

from bookings.models import Room


class TestCreateRoom:
    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "price, expected_price",
        [
            (100, "100.00"),
            (150.00, "150.00"),
            (200.00, "200.00"),
            (0, "0.00"),
            ("50.45", "50.45"),
        ],
    )
    def test_create_room_with_valid_price(
        self, client, room_factory, price, expected_price
    ):
        room_data = room_factory(price=price)
        response = client.post("/rooms/", data=room_data)
        assert response.status_code == 201
        assert response.json()["price"] == expected_price
        assert response.json()["description"] == "test room"

    @pytest.mark.django_db
    @pytest.mark.parametrize("price", [-1, -100, "-5", "50,45"])
    def test_create_room_with_invalid_price(self, client, room_factory, price):
        room_data = room_factory(price=price)
        response = client.post("/rooms/", data=room_data)
        assert response.status_code == 400

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "without_price, without_description",
        [
            (True, False),
            (False, True),
            (True, True),
        ],
    )
    def test_create_room_with_missing_data(
        self, client, room_factory, without_price, without_description
    ):
        room_data = room_factory(
            without_price=without_price, without_description=without_description
        )
        response = client.post("/rooms/", data=room_data, format="json")
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_create_room_with_empty_description(self, client, room_factory):
        room_data = room_factory(description="")
        response = client.post(
            "/rooms/",
            data=room_data,
        )
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_create_room_with_empty_price(self, client, room_factory):
        room_data = room_factory(price="")
        response = client.post("/rooms/", data=room_data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_create_room_with_none_price(self, client, room_factory):
        room_data = room_factory(price=None)
        response = client.post("/rooms/", data=room_data, format="json")
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_create_room_with_none_description(self, client, room_factory):
        room_data = room_factory(description=None)
        response = client.post("/rooms/", data=room_data, format="json")
        assert response.status_code == 400


class TestGetRoom:
    @pytest.mark.django_db
    def test_get_all_rooms(self, client, add_room_to_db):
        add_room_to_db(description="test room 1", price=100)
        add_room_to_db(description="test room 2", price=200)
        add_room_to_db(description="test room 3", price=300)
        response = client.get("/rooms/")
        assert response.status_code == 200
        assert len(response.json()) == 3
        descriptions = [room["description"] for room in response.json()]
        assert sorted(descriptions) == sorted(
            ["test room 1", "test room 2", "test room 3"]
        )

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "order, result",
        [
            ("asc", ["100.00", "200.00", "300.00"]),
            ("desc", ["300.00", "200.00", "100.00"]),
        ],
    )
    def test_get_all_rooms_with_sort_price(self, client, add_room_to_db, order, result):
        add_room_to_db(description="test room 3", price=300)
        add_room_to_db(description="test room 1", price=100)
        add_room_to_db(description="test room 2", price=200)

        response = client.get(f"/rooms/?sort=price&order={order}")
        assert response.status_code == 200
        assert len(response.json()) == 3
        prices = [room["price"] for room in response.json()]
        assert prices == result

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "order, result",
        [
            ("asc", ["test room 3", "test room 1", "test room 2"]),
            ("desc", ["test room 2", "test room 1", "test room 3"]),
        ],
    )
    def test_get_all_rooms_with_sort_created_at(
        self, client, add_room_to_db, order, result
    ):
        add_room_to_db(description="test room 3", price=300)
        sleep(0.5)
        add_room_to_db(description="test room 1", price=100)
        sleep(0.5)
        add_room_to_db(description="test room 2", price=200)
        response = client.get(f"/rooms/?sort=created_at&order={order}")
        assert response.status_code == 200
        assert len(response.json()) == 3
        created_descriptions = [room["description"] for room in response.json()]
        assert created_descriptions == result

    @pytest.mark.django_db
    @pytest.mark.parametrize("sort, order", [("invalid", "asc"), ("price", "invalid")])
    def test_get_all_rooms_with_invalid_sort_and_order_parameter(
        self, client, add_room_to_db, sort, order
    ):
        add_room_to_db(description="test room 3", price=300)
        add_room_to_db(description="test room 1", price=100)
        add_room_to_db(description="test room 2", price=200)
        response = client.get(f"/rooms/?sort={sort}&order={order}")
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_order_without_sort(self, client, add_room_to_db):
        add_room_to_db(description="test room 3", price=300)
        add_room_to_db(description="test room 1", price=100)
        add_room_to_db(description="test room 2", price=200)
        response = client.get("/rooms/?order=asc")
        assert response.status_code == 400


class TestDeleteRoom:
    @pytest.mark.django_db
    def test_delete_room(self, client, add_room_to_db):
        room = add_room_to_db(description="test room", price=100)
        add_room_to_db(description="test room 2", price=200)
        add_room_to_db(description="test room 3", price=300)
        response = client.delete(f"/rooms/{room.id}/")
        assert response.status_code == 204
        assert Room.objects.count() == 2

    @pytest.mark.django_db
    def test_delete_non_existing_room(self, client):
        response = client.delete("/rooms/9999/")
        assert response.status_code == 404


class TestPatchRoom:
    @pytest.mark.django_db
    def test_patch_change_description(self, client, add_room_to_db):
        room = add_room_to_db(description="test room", price=100)
        response = client.patch(
            f"/rooms/{room.id}/", data={"description": "test room updated"}
        )
        assert response.status_code == 200
        assert Room.objects.get(id=room.id).description == "test room updated"
        assert Room.objects.get(id=room.id).price == 100

    @pytest.mark.django_db
    def test_patch_change_price(self, client, add_room_to_db):
        room = add_room_to_db(description="test room", price=100)
        response = client.patch(f"/rooms/{room.id}/", data={"price": 200})
        assert response.status_code == 200
        assert Room.objects.get(id=room.id).price == 200
        assert Room.objects.get(id=room.id).description == "test room"

    @pytest.mark.django_db
    def test_patch_not_existing_room(self, client):
        response = client.patch("/rooms/5/", data={"description": "test room updated"})
        assert response.status_code == 404

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "data",
        [
            {"price": "45,45"},
            {"price": "invalid"},
            {"price": -200},
        ],
    )
    def test_patch_invalid_data(self, client, add_room_to_db, data):
        room = add_room_to_db(description="test room", price=100)
        response = client.patch(f"/rooms/{room.id}/", data=data)
        assert response.status_code == 400
