from rest_framework import serializers
from labfairyapi.models import SupplyRequest, Researcher, Consumable, Order
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name")


class ResearcherSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Researcher
        fields = "__all__"


class ConsumableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumable
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class SupplyRequestSerializer(serializers.ModelSerializer):
    researcher = ResearcherSerializer(many=False)
    consumable = ConsumableSerializer(many=False)
    order = OrderSerializer(many=False)

    class Meta:
        model = SupplyRequest
        fields = "__all__"
