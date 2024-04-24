from django.db import models


class EquipmentMaintenance(models.Model):
    equipment = models.ForeignKey(
        "Equipment", on_delete=models.CASCADE, related_name="maintenance_tickets"
    )
    maintenance = models.ForeignKey(
        "Maintenance", on_delete=models.CASCADE, related_name="tickets"
    )
    date_scheduling_completed = models.DateTimeField(auto_now_add=True)
    date_scheduled = models.DateField()
    date_completed = models.DateTimeField(null=True)
    next_date_needed = models.DateField(null=True)
    next_date_scheduled = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    notes = models.TextField(null=True)

    def __str__(self):
        return f"{self.maintenance.name} ({self.equipment.name})"
