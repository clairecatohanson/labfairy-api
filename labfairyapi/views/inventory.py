from django.shortcuts import get_object_or_404
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

    def retrieve(self, request, pk=None):
        inventory = get_object_or_404(Inventory, pk=pk)

        user = request.auth.user
        if not user.is_superuser:
            researcher = Researcher.objects.get(user=user)
            available_inventories = Inventory.objects.filter(
                lab_inventories__lab__researchers=researcher
            )
            allowed = available_inventories.filter(pk=inventory.pk).exists()
            if not allowed:
                return Response(
                    {"error": "You are not authorized to perform this action."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        serializer = InventorySerializer(inventory, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)
