from django.db import models


class ConsumableInventory(models.Model):
    consumable = models.ForeignKey(
        "Consumable", on_delete=models.CASCADE, related_name="consumable_inventories"
    )
    inventory = models.ForeignKey(
        "Inventory",
        on_delete=models.SET_NULL,
        null=True,
        related_name="inventory_consumables",
    )
    location = models.ForeignKey(
        "Location",
        on_delete=models.SET_NULL,
        null=True,
        related_name="inventory_consumables",
    )
    depleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.inventory.name} - {self.consumable.name}"
