from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from labfairyapi.models import Maintenance
from labfairyapi.serializers import MaintenanceSerializer


class MaintenanceViewSet(ViewSet):
    def list(self, request):
        # Get all maintenance types
        maintenance_types = Maintenance.objects.all()

        # Serialize the data
        serializer = MaintenanceSerializer(maintenance_types, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
