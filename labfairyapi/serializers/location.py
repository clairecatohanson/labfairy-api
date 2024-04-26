from rest_framework import serializers
from labfairyapi.models import Building, Room, Location


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = "__all__"


class RoomSerializer(serializers.ModelSerializer):
    building = BuildingSerializer(many=False)

    class Meta:
        model = Room
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    room = RoomSerializer(many=False)

    class Meta:
        model = Location
        fields = "__all__"
