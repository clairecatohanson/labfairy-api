from django.db import models


class Equipment(models.Model):
    name = models.CharField(max_length=125)
    description = models.TextField()
    location = models.ForeignKey(
        "Location", on_delete=models.SET_NULL, null=True, related_name="equipment"
    )
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name
