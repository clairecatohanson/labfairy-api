from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from labfairyapi.models import Location, Equipment, Researcher
from labfairyapi.serializers import (
    EquipmentCreatedSerializer,
    EquipmentListSerializer,
    EquipmentFullSerializer,
)


class EquipmentViewSet(ViewSet):
    def create(self, request):
        # Check if the user is a superuser
        user = request.auth.user
        if not user.is_superuser:
            return Response(
                {"error": "You are not authorized to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Get the location instance if it is provided
        try:
            location = Location.objects.get(pk=request.data["location_id"])
        except KeyError:
            location = None
        except Location.DoesNotExist:
            return Response(
                {"error": "Location not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create a new equipment instance
        try:
            new_equipment = Equipment.objects.create(
                name=request.data["name"],
                description=request.data["description"],
                location=location,
            )
            new_equipment.save()
        except ValidationError as e:
            return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize the new equipment instance
        serializer = EquipmentCreatedSerializer(new_equipment, many=False)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        # Check if the user is a superuser
        user = request.auth.user
        if not user.is_superuser:
            return Response(
                {"error": "You are not authorized to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            equipment = Equipment.objects.get(pk=pk)
        except Equipment.DoesNotExist:
            return Response(
                {"error": "Equipment not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Update the equipment fields with the provided data
        if "name" in request.data:
            equipment.name = request.data["name"]
        if "description" in request.data:
            equipment.description = request.data["description"]
        if "location_id" in request.data:
            try:
                location = Location.objects.get(pk=request.data["location_id"])
                equipment.location = location
            except Location.DoesNotExist:
                return Response(
                    {"error": "Location not found"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        equipment.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        # Retrieve all equipment instances
        all_equipment = Equipment.objects.all()

        # Create a serializer instance with the queryset
        serializer = EquipmentListSerializer(all_equipment, many=True)

        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        # Get the requested equipment instance
        try:
            equipment = Equipment.objects.get(pk=pk)
        except Equipment.DoesNotExist:
            return Response(
                {"error": "Equipment not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Check if the user is a superuser. If not, get the associated researcher.
        user = request.auth.user
        if not user.is_superuser:
            researcher = Researcher.objects.get(user=user)

            # Get the LabEquipment queryset for labs associated with this equipment instance
            lab_equipment_set = equipment.equipment_labs.all()

            # Get the lab_ids from the lab_equipment_set
            lab_ids = [labequipment.lab.id for labequipment in lab_equipment_set]

            # Determine whether the researcher is associated with one of the found lab_ids
            if researcher.lab.id not in lab_ids:
                return Response(
                    {"error": "You are not authorized to perform this action."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        serializer = EquipmentFullSerializer(equipment, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)
