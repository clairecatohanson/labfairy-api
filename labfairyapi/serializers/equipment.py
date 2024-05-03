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
    has_access = serializers.SerializerMethodField()

    def get_has_access(self, obj):
        request = self.context["request"]
        user = request.auth.user

        if user.is_superuser:
            return True
        if obj.equipment_labs.filter(lab=user.researcher.lab).exists():
            return True
        return False

    class Meta:
        model = Equipment
        fields = ("id", "name", "location", "equipment_labs", "archived", "has_access")


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
