from rest_framework import serializers
from labfairyapi.models import Order, SupplyRequest, Consumable, Researcher
from django.contrib.auth.models import User


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class ConsumableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumable
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name")


class ResearcherSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Researcher
        fields = "__all__"


class SupplyRequestSerializer(serializers.ModelSerializer):
    consumable = ConsumableSerializer(many=False)
    researcher = ResearcherSerializer(many=False)

    class Meta:
        model = SupplyRequest
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    lineitems = SupplyRequestSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id", "lineitems", "date_completed")
