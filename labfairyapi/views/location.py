from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from labfairyapi.models import Location
from labfairyapi.serializers import LocationSerializer


class LocationViewSet(ViewSet):
    def list(self, request):
        all_locations = Location.objects.all()

        serializer = LocationSerializer(all_locations, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
