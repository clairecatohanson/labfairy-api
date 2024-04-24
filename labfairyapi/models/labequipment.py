from django.db import models


class LabEquipment(models.Model):
    lab = models.ForeignKey(
        "Lab", on_delete=models.SET_DEFAULT, default=1, related_name="lab_equipment"
    )
    equipment = models.ForeignKey(
        "Equipment", on_delete=models.CASCADE, related_name="equipment_labs"
    )

    def __str__(self):
        return f"{self.equipment.name} ({self.lab.name})"
