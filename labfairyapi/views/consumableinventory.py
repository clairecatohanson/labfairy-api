from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from rest_framework import status
from django.shortcuts import get_object_or_404
from labfairyapi.models import (
    Inventory,
    Consumable,
    ConsumableInventory,
    Researcher,
    Location,
)
from labfairyapi.serializers import (
    ConsumableInventoryListSerializer,
    ConsumableInventoryDetailSerializer,
    ConsumableInventoryBasicSerializer,
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

        # Get optional query params
        availability = request.query_params.get("status", None)
        searchName = request.query_params.get("name", None)

        if availability is not None:
            if availability == "available":
                inventory_consumables = inventory_consumables.filter(depleted=False)
            if availability == "depleted":
                inventory_consumables = inventory_consumables.filter(depleted=True)

        if searchName is not None:
            inventory_consumables = inventory_consumables.filter(
                consumable__name__icontains=searchName
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

    def create(self, request):
        # Get keys from request body
        consumable_id = request.data.get("consumable_id", None)
        inventory_id = request.data.get("inventory_id", None)
        location_id = request.data.get("location_id", None)

        if not consumable_id or not inventory_id:
            return Response(
                {"error": "Missing required fields: consumable_id, inventory_id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        consumable = get_object_or_404(Consumable, pk=consumable_id)
        inventory = get_object_or_404(Inventory, pk=inventory_id)
        if location_id is not None:
            location = get_object_or_404(Location, pk=location_id)

        try:
            new_inventory_item = ConsumableInventory.objects.create(
                consumable=consumable,
                inventory=inventory,
                depleted=False,
            )

            if location_id is not None:
                new_inventory_item.location = location
            new_inventory_item.save()
        except ValidationError as e:
            return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ConsumableInventoryBasicSerializer(new_inventory_item, many=False)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
