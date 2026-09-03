from rest_framework import serializers
from bookings.models import Room

class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ["id", "description", "price", "created_at"]
