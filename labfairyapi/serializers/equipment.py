from rest_framework import serializers
from labfairyapi.models import Location, Equipment


class EquipmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Equipment
        fields = ("id", "name", "description", "location", "archived")
        depth = 3
