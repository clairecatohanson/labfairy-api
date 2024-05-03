from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from labfairyapi.models import Room
from labfairyapi.serializers import RoomSerializer


class RoomViewSet(ViewSet):
    def list(self, request):
        # Get all rooms
        rooms = Room.objects.all()

        # Get optional query_params and filter
        building_id = request.query_params.get("building")
        if building_id is not None:
            rooms = rooms.filter(building__pk=building_id)

        serializer = RoomSerializer(rooms, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
