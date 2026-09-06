"""Модели гостиничных номеров и связанных с ними бронирований."""

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F


class Room(models.Model):
    """Гостиничный номер с описанием, стоимостью за ночь и датой создания."""

    description = models.TextField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(price__gte=0),
                name="room_price_non_negative",
            )
        ]


class Booking(models.Model):
    """Период бронирования конкретного номера.

    Даты задают полуоткрытый интервал: номер доступен в дату окончания
    бронирования для следующего гостя.
    """

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()  # с какого по какое снимают жилье
    finish_date = models.DateField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(start_date__lt=F("finish_date")),
                name="booking_dates_valid",
            )
        ]
