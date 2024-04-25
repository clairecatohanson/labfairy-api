from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from labfairyapi.models import Lab, Equipment, LabEquipment
from labfairyapi.serializers import LabEquipmentSerializer


class LabEquipmentViewSet(ViewSet):
    # Check if the user is a superuser
    permission_classes = [IsAdminUser]

    def create(self, request):
        # Check for required keys in the request body
        lab_id = request.data.get("lab_id")
        equipment_id = request.data.get("equipment_id")

        if not lab_id or not equipment_id:
            return Response(
                {"error": "Missing required fields: lab_id and/or equipment_id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Try to lab and equipment instances
        lab = get_object_or_404(Lab, pk=lab_id)
        equipment = get_object_or_404(Equipment, pk=equipment_id)

        # Check for duplicate LabEquipment instance
        try:
            found_lab_equipment = LabEquipment.objects.get(lab=lab, equipment=equipment)
            return Response(
                {"error": "The provided LabEquipment already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except LabEquipment.DoesNotExist:
            # Try to create a new LabEquipment instance
            try:
                new_lab_equipment = LabEquipment.objects.create(
                    lab=lab, equipment=equipment
                )
                new_lab_equipment.save()
            except ValidationError as e:
                return Response(
                    {"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST
                )

            # Serialize the LabEquipment
            serializer = LabEquipmentSerializer(new_lab_equipment, many=False)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        # Check for required keys in the request body
        lab_id = request.data.get("lab_id")
        equipment_id = request.data.get("equipment_id")

        if not lab_id or not equipment_id:
            return Response(
                {"error": "Missing required fields: lab_id and/or equipment_id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Try to lab and equipment instances
        lab = get_object_or_404(Lab, pk=lab_id)
        equipment = get_object_or_404(Equipment, pk=equipment_id)

        # Try to find the requested LabEquipment instance
        try:
            found_instance = LabEquipment.objects.get(lab=lab, equipment=equipment)
            found_instance.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except LabEquipment.DoesNotExist:
            return Response(
                {"error": "LabEquipment not found"}, status=status.HTTP_404_NOT_FOUND
            )
