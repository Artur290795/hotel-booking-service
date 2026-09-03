from bookings.models import Booking
import pytest


class TestCreateBooking:
    @pytest.mark.django_db
    def test_create_booking_with_valid_data(self, client, add_room_to_db, booking_factory):
        room = add_room_to_db()
        add_room_to_db()
        add_room_to_db()
        booking_data = booking_factory(room_id=room.id)
        response = client.post("/bookings/", data=booking_data)
        assert response.status_code == 201
        assert response.json()["id"] == 1

    @pytest.mark.django_db
    @pytest.mark.parametrize("room_id, start_date, finish_date", [(1, "invalid_date", "2026-01-04"), (1, "2026-01-01", "invalid_date"), (10, "2026-01-01", "2026-01-02")])
    def test_create_booking_with_invalid_data(self, client, add_room_to_db, booking_factory, room_id, start_date, finish_date):
        add_room_to_db()
        booking_data = booking_factory(room_id=room_id, start_date=start_date, finish_date=finish_date)
        response = client.post("/bookings/", data=booking_data)
        assert response.status_code == 400

    @pytest.mark.django_db
    @pytest.mark.parametrize("without_room, without_start_date, without_finish_date", [(True, False, False), (False, True, False), (False, False, True)])
    def test_create_booking_without_data(self, client, add_room_to_db, booking_factory, without_room, without_start_date, without_finish_date):
        add_room_to_db()
        booking_data = booking_factory(without_room=True, without_start_date=without_start_date, without_finish_date=without_finish_date)
        response = client.post("/bookings/", data=booking_data)
        assert response.status_code == 400


class TestDeleteBooking:
    @pytest.mark.django_db
    def test_delete_booking(self, client, add_room_to_db, booking_factory):
        room = add_room_to_db()
        booking_data = booking_factory(room_id=room.id)
        booking = client.post("/bookings/", data=booking_data)
        response = client.delete(f"/bookings/{booking.json()['id']}/")
        assert response.status_code == 204
        assert Booking.objects.filter(id=booking.json()["id"]).count() == 0

    @pytest.mark.django_db
    def test_delete_non_existing_booking(self, client):
        response = client.delete("/bookings/9999/")
        assert response.status_code == 404


class TestGetBooking:
    @pytest.mark.django_db
    def test_get_booking_by_room_id(self, client, add_room_to_db, booking_factory):
        room = add_room_to_db()
        booking_data1 = booking_factory(room_id=room.id, start_date="2027-01-01", finish_date="2027-01-02")
        booking_data2 = booking_factory(room_id=room.id, start_date="2027-01-03", finish_date="2027-01-04")
        booking_data3 = booking_factory(room_id=room.id, start_date="2026-01-05", finish_date="2026-01-06")
    
        booking_resp1 = client.post("/bookings/", data=booking_data1)
        client.post("/bookings/", data=booking_data2)
        client.post("/bookings/", data=booking_data3)

        response = client.get(f"/bookings/?room_id={room.id}")

        assert response.status_code == 200
        assert response.json() == [booking_data3, booking_data1, booking_data2, ]

        client.delete(f"/bookings/{booking_resp1.json()['id']}/")
        
        response = client.get(f"/bookings/?room_id={room.id}")

        assert response.status_code == 200
        assert response.json() == [booking_data3, booking_data2]

    @pytest.mark.django_db
    def test_get_booking_with_no_bookings(self, client, add_room_to_db):
        room = add_room_to_db()
        response = client.get(f"/bookings/?room_id={room.id}")
        assert response.status_code == 200
        assert not response.json()

    @pytest.mark.django_db
    def test_get_booking_with_no_existing_room(self, client):
        response = client.get("/bookings/?room_id=9999")
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_get_booking_with_invalid_room_id(self, client):
        response = client.get("/bookings/?room_id=invalid")
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_get_booking_without_room_id(self, client, add_room_to_db, booking_factory):
        response = client.get("/bookings/")
        assert response.status_code == 400