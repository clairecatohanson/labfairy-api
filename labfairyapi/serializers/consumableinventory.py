from rest_framework import serializers
from labfairyapi.models import Inventory, Consumable, ConsumableInventory, Location


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


class ConsumableInventoryDetailSerializer(serializers.ModelSerializer):
    consumable = ConsumableSerializer(many=False)
    location = LocationSerializer(many=False)
    inventory = InventorySerializer(many=False)

    class Meta:
        model = ConsumableInventory
        fields = "__all__"
