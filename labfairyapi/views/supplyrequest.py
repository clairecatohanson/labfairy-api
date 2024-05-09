from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from labfairyapi.models import Consumable, SupplyRequest, Researcher, Order
from labfairyapi.serializers import SupplyRequestSerializer


class SupplyRequestViewSet(ViewSet):
    def create(self, request):
        user = request.auth.user

        # Check for required keys in the request body
        consumable_id = request.data.get("consumable_id")
        quantity = request.data.get("quantity")

        if not consumable_id or not quantity:
            return Response(
                {"error": "Missing required fields: consumable_id and/or quantity"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        consumable = get_object_or_404(Consumable, pk=consumable_id)

        if user.is_superuser:
            # Create a new SupplyRequest instance in memory (i.e. as opposed to create) with the required keys
            supply_request = SupplyRequest(consumable=consumable, quantity=quantity)
        else:
            researcher = Researcher.objects.get(user=user)
            supply_request = SupplyRequest(
                researcher=researcher, consumable=consumable, quantity=quantity
            )
        # Run through model validators before saving the in-memory instance to the database
        try:
            supply_request.full_clean()
            supply_request.save()
        except ValidationError as e:
            return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize and return
        serializer = SupplyRequestSerializer(supply_request, many=False)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        user = request.auth.user
        supply_requests = SupplyRequest.objects.all()

        if not user.is_superuser:
            researcher = Researcher.objects.get(user=user)
            supply_requests = supply_requests.filter(researcher=researcher)

        # Get optional query_params
        request_status = request.query_params.get("status")
        limit = request.query_params.get("limit")

        if request_status is not None:
            if request_status == "requested":
                supply_requests = supply_requests.filter(order__isnull=True)

            if request_status == "ordered":
                supply_requests = supply_requests.filter(
                    order__isnull=False, date_received__isnull=True
                )

        supply_requests = supply_requests.order_by("date_requested")

        if limit is not None:
            limit = int(limit)
            supply_requests = supply_requests[:limit]

        serializer = SupplyRequestSerializer(supply_requests, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        user = request.auth.user
        supply_request = get_object_or_404(SupplyRequest, pk=pk)

        # Get data from body
        order_id = request.data.get("order_id", None)
        date_received = request.data.get("date_received", None)

        if order_id is not None:
            if not user.is_superuser:
                return Response(
                    {"error": "You are not authorized to perform this action."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            order = get_object_or_404(Order, pk=order_id)
            supply_request.order = order

        if date_received is not None:
            supply_request.date_received = date_received

        supply_request.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
