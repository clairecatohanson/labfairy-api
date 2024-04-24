from django.db import models


class Location(models.Model):
    room = models.ForeignKey(
        "Room", on_delete=models.SET_NULL, null=True, related_name="locations"
    )
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} ({self.room})"
