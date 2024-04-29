from rest_framework import serializers
from labfairyapi.models import (
    Equipment,
    LabEquipment,
    EquipmentMaintenance,
    Location,
    Room,
    Building,
)


class EquipmentLabSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabEquipment
        fields = ("lab",)
        depth = 1


class EquipmentMaintenanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = EquipmentMaintenance
        fields = "__all__"


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        exclude = ("id",)


class RoomSerializer(serializers.ModelSerializer):
    building = BuildingSerializer(many=False)

    class Meta:
        model = Room
        fields = ("name", "building")


class LocationSerializer(serializers.ModelSerializer):

    room = RoomSerializer(many=False)

    class Meta:
        model = Location
        fields = (
            "name",
            "room",
        )


class EquipmentListSerializer(serializers.ModelSerializer):

    equipment_labs = EquipmentLabSerializer(many=True)
    location = LocationSerializer(many=False)

    class Meta:
        model = Equipment
        fields = ("id", "name", "location", "equipment_labs", "archived")


class EquipmentFullSerializer(serializers.ModelSerializer):

    equipment_labs = EquipmentLabSerializer(many=True)
    maintenance_tickets = EquipmentMaintenanceSerializer(many=True)
    location = LocationSerializer(many=False)

    class Meta:
        model = Equipment
        fields = (
            "id",
            "name",
            "description",
            "location",
            "equipment_labs",
            "maintenance_tickets",
            "archived",
        )


class EquipmentCreatedSerializer(serializers.ModelSerializer):

    location = LocationSerializer(many=False)

    class Meta:
        model = Equipment
        fields = ("id", "name", "description", "location", "archived")
