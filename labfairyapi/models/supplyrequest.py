from django.db import models
from django.core.validators import MinValueValidator


class SupplyRequest(models.Model):
    researcher = models.ForeignKey(
        "Researcher",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="supply_requests",
    )
    consumable = models.ForeignKey(
        "Consumable",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="supply_requests",
    )
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    date_requested = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(
        "Order",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lineitems",
    )
    date_received = models.DateTimeField(null=True, blank=True)
