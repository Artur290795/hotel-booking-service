from django.db import models


class Room(models.Model):
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)  # когда создали комнату(для инфы)


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()  # с какого по какое снимают жилье
    finish_date = models.DateField()
