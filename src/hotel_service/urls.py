"""Маршруты административной панели и REST API сервиса бронирования."""

from django.contrib import admin
from django.urls import path

from bookings.views import BookingView, RoomView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("rooms/", RoomView.as_view(), name="room"),
    path("rooms/<int:room_id>/", RoomView.as_view(), name="room-delete"),
    path("bookings/", BookingView.as_view(), name="booking"),
    path("bookings/<int:booking_id>/", BookingView.as_view(), name="booking-delete"),
]
