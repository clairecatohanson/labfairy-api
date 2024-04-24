from rest_framework import serializers
from labfairyapi.models import Equipment, LabEquipment, EquipmentMaintenance


class EquipmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Equipment
        fields = ("id", "name", "description", "location", "archived")
        depth = 3


class EquipmentLabSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabEquipment
        fields = ("lab",)
        depth = 1


class EquipmentMaintenanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = EquipmentMaintenance
        fields = "__all__"


class EquipmentListSerializer(serializers.ModelSerializer):

    equipment_labs = EquipmentLabSerializer(many=True)

    class Meta:
        model = Equipment
        fields = ("id", "name", "location", "equipment_labs", "archived")


class EquipmentFullSerializer(serializers.ModelSerializer):

    equipment_labs = EquipmentLabSerializer(many=True)
    maintenance_tickets = EquipmentMaintenanceSerializer(many=True)

    class Meta:
        model = Equipment
        fields = (
            "id",
            "name",
            "location",
            "equipment_labs",
            "maintenance_tickets",
            "archived",
        )
