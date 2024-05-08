from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from labfairyapi.models import Inventory, Consumable, ConsumableInventory, Researcher
from labfairyapi.serializers import (
    ConsumableInventoryListSerializer,
    ConsumableInventoryDetailSerializer,
)


class ConsumableInventoryViewSet(ViewSet):
    def list(self, request):
        # Get required query_param
        inventory_id = request.query_params.get("inventory_id", None)

        if inventory_id is None:
            return Response(
                {"error": "Missing required query parameter: inventory_id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        inventory = get_object_or_404(Inventory, pk=inventory_id)

        inventory_consumables = ConsumableInventory.objects.filter(inventory=inventory)

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

            inventory_consumables = inventory_consumables.filter(
                inventory__lab_inventories__lab__researchers=researcher
            )

        serializer = ConsumableInventoryListSerializer(inventory_consumables, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        stocked_consumable = get_object_or_404(ConsumableInventory, pk=pk)

        user = request.auth.user
        if not user.is_superuser:
            # Check whether user has access to the item
            researcher = Researcher.objects.get(user=user)
            available_consumables = ConsumableInventory.objects.filter(
                inventory__lab_inventories__lab__researchers=researcher
            )
            allowed = available_consumables.filter(pk=stocked_consumable.pk).exists()
            if not allowed:
                return Response(
                    {"error": "You are not authorized to perform this action."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        serializer = ConsumableInventoryDetailSerializer(stocked_consumable, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        # Get instance
        item = get_object_or_404(ConsumableInventory, pk=pk)

        # Check that user has access to the instance
        user = request.auth.user
        if not user.is_superuser:
            researcher = Researcher.objects.get(user=user)
            available_consumables = ConsumableInventory.objects.filter(
                inventory__lab_inventories__lab__researchers=researcher
            )
            allowed = available_consumables.filter(pk=item.pk).exists()
            if not allowed:
                return Response(
                    {"error": "You are not authorized to perform this action."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        # Get optional keys
        depleted = request.data.get("depleted", None)

        if depleted is not None:
            if depleted == True:
                item.depleted = True
            if depleted == False:
                item.depleted = False

        item.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
