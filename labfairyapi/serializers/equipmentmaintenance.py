from rest_framework import serializers
from labfairyapi.models import Equipment, Maintenance, EquipmentMaintenance


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ("id", "name")


class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = ("id", "name", "days_interval")


class EquipmentMaintenanceSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer(many=False)
    maintenance = MaintenanceSerializer(many=False)

    class Meta:
        model = EquipmentMaintenance
        fields = ("id", "equipment", "maintenance", "date_needed", "date_scheduled")
