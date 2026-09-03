from django.db import models
from django.core.validators import MinValueValidator


class Room(models.Model):
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(price__gte=0),
                name="room_price_non_negative",
            )
        ]


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()  # с какого по какое снимают жилье
    finish_date = models.DateField()
