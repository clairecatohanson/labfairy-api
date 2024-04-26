from django.db import models


class Room(models.Model):
    building = models.ForeignKey(
        "Building", on_delete=models.CASCADE, related_name="rooms"
    )
    name = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.building.name} - Room {self.name}"
