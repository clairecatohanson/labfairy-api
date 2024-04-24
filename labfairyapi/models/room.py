from django.db import models


class Room(models.Model):
    building = models.ForeignKey(
        "Building", on_delete=models.CASCADE, related_name="rooms"
    )
    number = models.IntegerField()

    def __str__(self):
        return f"{self.building.name} - Room {self.number}"
