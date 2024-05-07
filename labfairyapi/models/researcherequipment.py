from django.db import models


class ResearcherEquipment(models.Model):
    researcher = models.ForeignKey(
        "Researcher", on_delete=models.CASCADE, related_name="equipment_requests"
    )
    equipment = models.ForeignKey(
        "Equipment", on_delete=models.CASCADE, related_name="access_requests"
    )
    training_date = models.DateField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.researcher.name} - {self.equipment.name}"
