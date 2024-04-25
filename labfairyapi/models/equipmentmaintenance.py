from django.db import models
from django.contrib.auth.models import User


class EquipmentMaintenance(models.Model):
    equipment = models.ForeignKey(
        "Equipment", on_delete=models.CASCADE, related_name="maintenance_tickets"
    )
    maintenance = models.ForeignKey(
        "Maintenance", on_delete=models.CASCADE, related_name="tickets"
    )
    date_request_completed = models.DateTimeField(auto_now_add=True)
    date_needed = models.DateField()
    date_scheduled = models.DateField(null=True)
    date_completed = models.DateTimeField(null=True)
    notes = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1)

    def __str__(self):
        return f"{self.maintenance.name} ({self.equipment.name})"
