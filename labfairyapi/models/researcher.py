from django.db import models
from django.contrib.auth.models import User


class Researcher(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="researcher"
    )
    lab = models.ForeignKey(
        "Lab", on_delete=models.SET_DEFAULT, default=1, related_name="researchers"
    )

    def __str__(self):
        return f"{self.user.username} ({self.lab.name})"
