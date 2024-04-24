from django.db import models


class Building(models.Model):
    name = models.CharField(max_length=80)
    short_name = models.CharField(max_length=6)

    def __str__(self):
        return self.name
