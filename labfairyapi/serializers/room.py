from rest_framework import serializers
from labfairyapi.models import Building, Room


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = "__all__"


class RoomSerializer(serializers.ModelSerializer):
    building = BuildingSerializer(many=False)

    class Meta:
        model = Room
        fields = "__all__"
