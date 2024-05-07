from django.db import models


class LabInventory(models.Model):
    lab = models.ForeignKey(
        "Lab", on_delete=models.CASCADE, related_name="lab_inventories"
    )
    inventory = models.ForeignKey(
        "Inventory", on_delete=models.CASCADE, related_name="lab_inventories"
    )

    def __str__(self):
        return f"{self.lab.name} - {self.inventory.name}"
