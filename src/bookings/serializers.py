import random
from rest_framework import serializers
from bookings.models import Booking, Room


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ["id", "description", "price", "created_at"]


class BookingSerializer(serializers.ModelSerializer):
    room_id = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(), source="room"
    )

    class Meta:
        model = Booking
        fields = ["room_id", "start_date", "finish_date"]

    def validate(self, attrs):
        start_date = attrs["start_date"]
        finish_date = attrs["finish_date"]
        if start_date >= finish_date:
            raise serializers.ValidationError("Start date must be before finish date")
        all_bookings_in_room = Booking.objects.filter(room=attrs["room"])
        conflicted_bookings = all_bookings_in_room.filter(start_date__lt=finish_date, finish_date__gt=start_date).exists()
        if conflicted_bookings:
            raise serializers.ValidationError("Room is already booked for this period")
        return attrs
