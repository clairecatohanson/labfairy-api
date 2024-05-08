from django.db import models


class Order(models.Model):
    date_completed = models.DateTimeField(null=True, blank=True)
