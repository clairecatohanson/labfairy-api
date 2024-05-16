from rest_framework import serializers
from labfairyapi.models import (
    Inventory,
    Consumable,
    ConsumableInventory,
    Location,
    SupplyRequest,
    Order,
)


class ConsumableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumable
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("id", "name")


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = "__all__"


class ConsumableInventoryListSerializer(serializers.ModelSerializer):
    consumable = ConsumableSerializer(many=False)
    location = LocationSerializer(many=False)

    class Meta:
        model = ConsumableInventory
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class SupplyRequestSerializer(serializers.ModelSerializer):
    inventory = InventorySerializer(many=False)
    order = OrderSerializer(many=False)

    class Meta:
        model = SupplyRequest
        fields = "__all__"


class ConsumableDetailSerializer(serializers.ModelSerializer):
    supply_requests = SupplyRequestSerializer(many=True)

    class Meta:
        model = Consumable
        fields = ("id", "name", "supply_requests")


class ConsumableInventoryDetailSerializer(serializers.ModelSerializer):
    consumable = ConsumableDetailSerializer(many=False)
    location = LocationSerializer(many=False)
    inventory = InventorySerializer(many=False)

    class Meta:
        model = ConsumableInventory
        fields = "__all__"
