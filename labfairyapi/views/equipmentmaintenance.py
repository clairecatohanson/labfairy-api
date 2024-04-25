from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from labfairyapi.models import Equipment, Maintenance, EquipmentMaintenance
from labfairyapi.serializers import EquipmentMaintenanceSerializer


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

        if date_scheduled is not None:
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
        date_needed = request.data.get("date_needed")
        date_scheduled = request.data.get("date_scheduled")
        completed = request.data.get("completed")
        date_completed = request.data.get("date_completed")

        if (
            not date_needed
            and not date_scheduled
            and not completed
            and not date_completed
        ):
            return Response(
                {
                    "error": "Missing required fields. Please include at least one of the following: date_needed, date_scheduled, completed, date_completed."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if date_needed is not None:
            maintenance_ticket.date_needed = date_needed

        if date_scheduled is not None:
            maintenance_ticket.date_scheduled = date_scheduled

        if completed == True:
            maintenance_ticket.date_completed = timezone.now().date()

        if date_completed is not None:
            maintenance_ticket.date_completed = date_completed
        try:
            maintenance_ticket.full_clean()
            maintenance_ticket.save()
        except ValidationError as e:
            return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        return Response({}, status=status.HTTP_204_NO_CONTENT)
