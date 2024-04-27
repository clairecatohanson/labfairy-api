from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from labfairyapi.models import Location
from labfairyapi.serializers import LocationSerializer


class LocationViewSet(ViewSet):
    def list(self, request):
        # Get all locations
        locations = Location.objects.all()

        # Get optional query_params and filter
        room_id = request.query_params.get("room")
        if room_id is not None:
            locations = locations.filter(room__pk=room_id)

        serializer = LocationSerializer(locations, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
