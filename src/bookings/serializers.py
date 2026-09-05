from loguru import logger
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
        fields = ["id", "room_id", "start_date", "finish_date"]

    def validate(self, attrs):
        logger.info(f"Validating booking: {attrs}")
        start_date = attrs["start_date"]
        finish_date = attrs["finish_date"]
        if start_date >= finish_date:
            logger.error("Start date must be before finish date")
            raise serializers.ValidationError("Start date must be before finish date")
        all_bookings_in_room = Booking.objects.filter(room=attrs["room"])
        conflicted_bookings = all_bookings_in_room.filter(
            start_date__lt=finish_date, finish_date__gt=start_date
        ).exists()
        if conflicted_bookings:
            logger.error("Room is already booked for this period")
            raise serializers.ValidationError("Room is already booked for this period")
        logger.info(f"Booking validated: {attrs}")
        return attrs
