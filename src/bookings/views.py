from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RoomSerializer
from .models import Room


class RoomView(APIView):
    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        sort = request.query_params.get("sort")
        order = request.query_params.get("order")
        
        if sort and (sort not in ["price", "created_at"] or order not in ["asc", "desc"]):
            return Response({"error": "Invalid sort or order parameter"}, status=status.HTTP_400_BAD_REQUEST)
        if not sort and order:
            return Response({"error": "Sort parameter is required when order parameter is provided"}, status=status.HTTP_400_BAD_REQUEST)
        rooms = Room.objects.all()
        if sort:
            rooms = rooms.order_by(sort) if order == "asc" else rooms.order_by(f"-{sort}")
           
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, room_id: int):
        room = get_object_or_404(Room, id=room_id)
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
    def patch(self, request, room_id: int):
        room = get_object_or_404(Room, id=room_id)
        serializer = RoomSerializer(room, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
