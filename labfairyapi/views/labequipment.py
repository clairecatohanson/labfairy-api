from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from labfairyapi.models import Lab, Equipment, LabEquipment
from labfairyapi.serializers import LabEquipmentSerializer


class LabEquipmentViewSet(ViewSet):
    def create(self, request):
        # Check if the user is a superuser
        user = request.auth.user
        if not user.is_superuser:
            return Response(
                {"error": "You are not authorized to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Check for required keys in the request body
        try:
            lab_id = request.data["lab_id"]
            equipment_id = request.data["equipment_id"]
        except KeyError:
            return Response(
                {"error": "Missing required fields: lab_id and/or equipment_id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Try to get lab and equipment instances
        try:
            lab = Lab.objects.get(pk=lab_id)
            equipment = Equipment.objects.get(pk=equipment_id)
        except Lab.DoesNotExist:
            return Response(
                {"error": "Lab not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Equipment.DoesNotExist:
            return Response(
                {"error": "Equipment not found"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Check for duplicate instance
        found_lab_equipment = LabEquipment.objects.filter(lab=lab, equipment=equipment)
        count = len(found_lab_equipment)
        if len(found_lab_equipment):
            return Response(
                {"error": "The provided LabEquipment already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Try to create a new LabEquipment instance
        try:
            new_lab_equipment = LabEquipment.objects.create(
                lab=lab, equipment=equipment
            )
            new_lab_equipment.save()
        except ValidationError as e:
            return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize the LabEquipment
        serializer = LabEquipmentSerializer(new_lab_equipment, many=False)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
