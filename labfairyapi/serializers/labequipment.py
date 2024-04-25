from rest_framework import serializers
from labfairyapi.models import Lab, Equipment, LabEquipment


class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = (
            "id",
            "name",
        )


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ("id", "name")


class LabEquipmentSerializer(serializers.ModelSerializer):
    lab = LabSerializer(many=False)
    equipment = EquipmentSerializer(many=False)

    class Meta:
        model = LabEquipment
        fields = ("lab", "equipment")
