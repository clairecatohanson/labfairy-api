from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework import permissions
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from labfairyapi.models import Consumable, SupplyRequest, Researcher, Order
from labfairyapi.serializers import OrderSerializer, OrderDetailSerializer


class OrderViewSet(ViewSet):
    permission_classes = [permissions.IsAdminUser]

    def create(self, request):
        annotated = Order.objects.annotate(num_lineitems=Count("lineitems"))
        open_order = annotated.filter(num_lineitems=0).exists()
        if open_order:
            return Response(
                {"error": "An open order already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        new_order = Order.objects.create()
        serializer = OrderSerializer(new_order, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderDetailSerializer(order, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
