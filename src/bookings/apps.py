"""Конфигурация Django-приложения бронирований."""

from django.apps import AppConfig


class BookingsConfig(AppConfig):
    """Регистрирует приложение бронирований в Django."""

    name = "bookings"
