from django.db import models


class Maintenance(models.Model):
    name = models.CharField(max_length=125)
    description = models.TextField()
    days_interval = models.IntegerField(null=True)

    def __str__(self):
        return self.name
