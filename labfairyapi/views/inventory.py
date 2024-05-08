from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from labfairyapi.models import Inventory, Researcher
from labfairyapi.serializers import InventorySerializer


class InventoryViewSet(ViewSet):
    def list(self, request):
        inventories = Inventory.objects.all()

        user = request.auth.user
        if not user.is_superuser:
            researcher = Researcher.objects.get(user=user)
            inventories = inventories.filter(lab_inventories__lab=researcher.lab)

        serializer = InventorySerializer(inventories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
