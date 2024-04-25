from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from labfairyapi.models import Equipment, Maintenance, EquipmentMaintenance
from labfairyapi.serializers import EquipmentMaintenanceSerializer


class EquipmentMaintenanceViewSet(ViewSet):
    def create(self, request):
        current_user = request.auth.user

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
            user=current_user,
        )

        # Check for optional keys in the request body
        date_scheduled = request.data.get("date_scheduled")
        notes = request.data.get("notes")

        if date_scheduled is not None:
            # Only allow superuser to complete scheduling
            if current_user.is_superuser:
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
