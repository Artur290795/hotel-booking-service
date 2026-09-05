from django.shortcuts import get_object_or_404
from loguru import logger
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Booking, Room
from .serializers import BookingSerializer, RoomSerializer


class RoomView(APIView):
    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f"Room created: {serializer.data}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        sort = request.query_params.get("sort")
        order = request.query_params.get("order")
        if not sort and order:
            logger.error("Sort parameter is required when order parameter is provided")
            return Response(
                {
                    "error": "Sort parameter is required when order parameter is provided"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if sort:
            if sort not in ["price", "created_at"]:
                logger.error(f"Invalid sort parameter: {sort}")
                return Response(
                    {"error": "Invalid sort parameter"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            order = order or "asc"
            if order not in ("asc", "desc"):
                logger.error(f"Invalid order parameter: {order}")
                return Response(
                    {"error": "Invalid order parameter"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        rooms = Room.objects.all()
        if sort:
            rooms = (
                rooms.order_by(sort) if order == "asc" else rooms.order_by(f"-{sort}")
            )
        logger.info(f"Rooms sorted: {rooms}")
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, room_id: int):
        room = get_object_or_404(Room, id=room_id)
        room.delete()
        logger.info(f"Room deleted: {room_id}")
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, room_id: int):
        room = get_object_or_404(Room, id=room_id)
        serializer = RoomSerializer(room, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f"Room updated: {room_id}")
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookingView(APIView):
    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()
        result = {"id": booking.id}
        logger.info(f"Booking created: {result}")
        return Response(result, status=status.HTTP_201_CREATED)

    def get(self, request):
        room_id = request.query_params.get("room_id")
        if not room_id or not room_id.isdigit():
            return Response(
                {"error": "Invalid room ID"}, status=status.HTTP_400_BAD_REQUEST
            )
        get_object_or_404(Room, id=room_id)
        bookings = Booking.objects.filter(room_id=room_id).order_by("start_date")
        serializer = BookingSerializer(bookings, many=True)
        logger.info(f"Bookings found: {serializer.data}")
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, booking_id: int):
        booking = get_object_or_404(Booking, id=booking_id)
        booking.delete()
        logger.info(f"Booking deleted: {booking_id}")
        return Response(status=status.HTTP_204_NO_CONTENT)
