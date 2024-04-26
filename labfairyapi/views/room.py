from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from labfairyapi.models import Room
from labfairyapi.serializers import RoomSerializer


class RoomViewSet(ViewSet):
    def list(self, request):
        all_rooms = Room.objects.all()

        serializer = RoomSerializer(all_rooms, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
