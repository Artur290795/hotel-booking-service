from rest_framework import serializers
from bookings.models import Booking, Room

class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ["id", "description", "price", "created_at"]


class BookingSerializer(serializers.ModelSerializer):
    room_id = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), source="room")

    class Meta:
        model = Booking
        fields = ["room_id", "start_date", "finish_date"]
