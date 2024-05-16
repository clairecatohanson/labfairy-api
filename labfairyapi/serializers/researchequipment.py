from rest_framework import serializers
from labfairyapi.models import Researcher, Equipment, ResearcherEquipment
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name")


class ResearcherSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Researcher
        fields = ("id", "user")


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ("id", "name")


class ResearcherEquipmentSerializer(serializers.ModelSerializer):
    researcher = ResearcherSerializer(many=False)
    equipment = EquipmentSerializer(many=False)

    class Meta:
        model = ResearcherEquipment
        fields = "__all__"
