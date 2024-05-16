from django.db import models


class Consumable(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    vendor = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
