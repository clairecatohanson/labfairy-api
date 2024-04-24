from django.db import models


class Lab(models.Model):
    name = models.CharField(max_length=125)
    description = models.TextField()

    def __str__(self):
        return self.name
