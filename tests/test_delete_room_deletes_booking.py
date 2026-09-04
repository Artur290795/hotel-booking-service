import pytest
from bookings.models import Booking

@pytest.mark.django_db
def test_delete_room_deletes_booking(client, add_room_to_db, booking_factory):
    room = add_room_to_db()
    booking_data1 = booking_factory(room_id=room.id, start_date="2026-01-01", finish_date="2026-01-02")
    response = client.post("/bookings/", data=booking_data1)
    assert response.status_code == 201
    booking_data2 = booking_factory(room_id=room.id, start_date="2026-01-02", finish_date="2026-01-03")
    response = client.post("/bookings/", data=booking_data2)
    assert response.status_code == 201
    response = client.delete(f"/rooms/{room.id}/")
    assert response.status_code == 204
    assert not Booking.objects.filter(room_id=room.id).exists()