from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from labfairyapi.models import (
    Equipment,
    Maintenance,
    EquipmentMaintenance,
    Researcher,
    Lab,
)
from labfairyapi.serializers import (
    EquipmentMaintenanceSerializer,
    EquipmentMaintenanceDetailsSerializer,
)


class EquipmentMaintenanceViewSet(ViewSet):
    def create(self, request):
        user = request.auth.user

        # Check for required keys in the request body
        equipment_id = request.data.get("equipment_id")
        maintenance_id = request.data.get("maintenance_id")
        date_needed = request.data.get("date_needed")

        if not equipment_id or not maintenance_id or not date_needed:
            return Response(
                {
                    "error": "Missing required fields: equipment_id, maintenance_id, and/or date_needed"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        equipment = get_object_or_404(Equipment, pk=equipment_id)
        maintenance_type = get_object_or_404(Maintenance, pk=maintenance_id)

        # Create a new EquipmentMaintenance in memory (i.e. as opposed to create) with the required keys
        new_maintenance_ticket = EquipmentMaintenance(
            equipment=equipment,
            maintenance=maintenance_type,
            date_needed=date_needed,
            user=user,
        )

        # Check for optional keys in the request body
        date_scheduled = request.data.get("date_scheduled")
        notes = request.data.get("notes")

        if date_scheduled is not None and date_scheduled != "":
            # Only allow superuser to complete scheduling
            if user.is_superuser:
                new_maintenance_ticket.date_scheduled = date_scheduled

        if notes is not None:
            new_maintenance_ticket.notes = notes

        # Run through model validators before saving the in-memory instance to the database
        try:
            new_maintenance_ticket.full_clean()
            new_maintenance_ticket.save()
        except ValidationError as e:
            return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize the EquipmentMaintenance
        serializer = EquipmentMaintenanceSerializer(new_maintenance_ticket, many=False)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        # Check that the user is a superuser
        user = request.auth.user
        if not user.is_superuser:
            return Response(
                {"error": "You are not authorized to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Get the EquipmentMaintenance instance
        maintenance_ticket = get_object_or_404(EquipmentMaintenance, pk=pk)

        # Get optional keys from the request body
        date_needed = request.data.get("date_needed", None)
        date_scheduled = request.data.get("date_scheduled", None)
        completed = request.data.get("completed", None)
        cancelled = request.data.get("cancelled", None)
        date_completed = request.data.get("date_completed", None)

        if (
            not date_needed
            and not date_scheduled
            and not completed
            and not cancelled
            and not date_completed
        ):
            return Response(
                {
                    "error": "Missing required fields. Please include at least one of the following: date_needed, date_scheduled, completed, date_completed."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if date_needed is not None and date_needed != "":
            maintenance_ticket.date_needed = date_needed

        if date_scheduled is not None and date_scheduled != "":
            maintenance_ticket.date_scheduled = date_scheduled

        if completed == True:
            maintenance_ticket.date_completed = timezone.now().date()

        if cancelled == True:
            maintenance_ticket.date_scheduled = None

        if date_completed is not None and date_completed != "":
            maintenance_ticket.date_completed = date_completed
        try:
            maintenance_ticket.full_clean()
            maintenance_ticket.save()
        except ValidationError as e:
            return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk=None):
        # Check that user is_staff
        user = request.auth.user
        if not user.is_superuser:
            return Response(
                {"error": "You are not authorized to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Try to find the requested instance
        maintenance_ticket = get_object_or_404(EquipmentMaintenance, pk=pk)

        maintenance_ticket.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        # Check if the user is a superuser. If not, get the associated researcher.
        user = request.auth.user
        if user.is_superuser:
            maintenance_tickets = EquipmentMaintenance.objects.all()

        else:
            researcher = Researcher.objects.get(user=user)

            # Filter EquipmentMaintenance set for equipment that the lab has access to
            maintenance_tickets = EquipmentMaintenance.objects.filter(
                equipment__equipment_labs__lab__researchers=researcher
            )

        # Get optional query params and filter maintenance_tickets
        equipment_id = request.query_params.get("equipment_id")
        maintenance_type_id = request.query_params.get("maintenance_type_id")
        lab_id = request.query_params.get("lab_id")
        progress = request.query_params.get("progress")
        limit = request.query_params.get("limit")

        # Filter by equipment
        if equipment_id is not None:
            maintenance_tickets = maintenance_tickets.filter(equipment__id=equipment_id)

        # Filter by maintenance type
        if maintenance_type_id is not None:
            maintenance_tickets = maintenance_tickets.filter(
                maintenance__id=maintenance_type_id
            )

        # Filter by lab who has access to the equipment
        if lab_id is not None:
            lab = get_object_or_404(Lab, pk=lab_id)
            maintenance_tickets = maintenance_tickets.filter(
                equipment__equipment_labs__lab=lab
            )

        # Filter by progress (requested, scheduled, or completed)
        if progress is not None:
            if progress == "requested":
                maintenance_tickets = maintenance_tickets.filter(
                    date_scheduled__isnull=True
                )
            if progress == "scheduled":
                maintenance_tickets = maintenance_tickets.filter(
                    date_scheduled__isnull=False, date_completed__isnull=True
                )
            if progress == "completed":
                maintenance_tickets = maintenance_tickets.filter(
                    date_scheduled__isnull=False, date_completed__isnull=False
                )

        # Limit the number of maintenance tickets in the response
        if limit is not None:
            limit = int(limit)
            if progress == "requested":
                maintenance_tickets = maintenance_tickets.order_by("date_needed")[
                    :limit
                ]
            if progress == "scheduled":
                maintenance_tickets = maintenance_tickets.order_by("date_scheduled")[
                    :limit
                ]

        serializer = EquipmentMaintenanceSerializer(maintenance_tickets, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        maintenance_ticket = get_object_or_404(EquipmentMaintenance, pk=pk)

        # Check if the user is a superuser. If not, get the associated researcher.
        user = request.auth.user
        if not user.is_superuser:
            researcher = Researcher.objects.get(user=user)

            # Get researcher's equipment_ids
            lab_equipment_set = researcher.lab.lab_equipment.all()
            equipment_ids = [
                lab_equipment.equipment.id for lab_equipment in lab_equipment_set
            ]

            if maintenance_ticket.equipment.id not in equipment_ids:
                return Response(
                    {"error": "You are not authorized to perform this action."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        serializer = EquipmentMaintenanceDetailsSerializer(
            maintenance_ticket, many=False
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
