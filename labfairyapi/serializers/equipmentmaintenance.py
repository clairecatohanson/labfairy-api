from rest_framework import serializers
from labfairyapi.models import (
    Equipment,
    Maintenance,
    EquipmentMaintenance,
    Location,
    Room,
    Building,
)
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "username")


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ("name", "short_name")


class RoomSerializer(serializers.ModelSerializer):
    building = BuildingSerializer(many=False)

    class Meta:
        model = Room
        fields = (
            "number",
            "building",
        )


class LocationSerializer(serializers.ModelSerializer):
    room = RoomSerializer(many=False)

    class Meta:
        model = Location
        fields = ("name", "room")


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ("id", "name")


class EquipmentFullSerializer(serializers.ModelSerializer):
    location = LocationSerializer(many=False)

    class Meta:
        model = Equipment
        fields = "__all__"


class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = ("id", "name", "days_interval")


class MaintenanceFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = "__all__"


class EquipmentMaintenanceSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer(many=False)
    maintenance = MaintenanceSerializer(many=False)

    class Meta:
        model = EquipmentMaintenance
        fields = (
            "id",
            "equipment",
            "maintenance",
            "date_needed",
            "date_scheduled",
            "date_completed",
        )


class EquipmentMaintenanceDetailsSerializer(serializers.ModelSerializer):
    equipment = EquipmentFullSerializer(many=False)
    maintenance = MaintenanceFullSerializer(many=False)
    user = UserSerializer(many=False)

    class Meta:
        model = EquipmentMaintenance
        fields = "__all__"
