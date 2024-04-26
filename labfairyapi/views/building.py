from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from labfairyapi.models import Building
from labfairyapi.serializers import BuildingSerializer


class BuildingViewSet(ViewSet):
    def list(self, request):
        all_buildings = Building.objects.all()

        serializer = BuildingSerializer(all_buildings, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
