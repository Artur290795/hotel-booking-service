import pytest


class TestCreateRoom:
    @pytest.mark.django_db
    @pytest.mark.parametrize("price, expected_price", 
                            [
                                (100, "100.00"), 
                                (100.00, "100.00"), 
                                (100.000, "100.00"), 
                                (0, "0.00"), 
                                ("50.45", "50.45")
                            ]
                            )
    def test_create_room_with_valid_price(self, client, room_factory, price, expected_price):
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
    @pytest.mark.parametrize("without_price, without_description", [
        (True, False),
        (False, True),
        (True, True),
    ])
    def test_create_room_with_missing_data(self, client, room_factory, without_price, without_description):
        room_data = room_factory(without_price=without_price, without_description=without_description)
        response = client.post("/rooms/", data=room_data, format="json")
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_create_room_with_empty_description(self, client, room_factory):
        room_data = room_factory(description="")
        response = client.post("/rooms/", data=room_data,)
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