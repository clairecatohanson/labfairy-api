from rest_framework import serializers
from labfairyapi.models import Order, SupplyRequest, Consumable


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class ConsumableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumable
        fields = "__all__"


class SupplyRequestSerializer(serializers.ModelSerializer):
    consumable = ConsumableSerializer(many=False)

    class Meta:
        model = SupplyRequest
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    lineitems = SupplyRequestSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id", "lineitems", "date_completed")
