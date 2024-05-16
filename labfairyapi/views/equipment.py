from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
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
        if "archived" in request.data:
            equipment.archived = request.data["archived"]

        equipment.save()

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
        equipment = get_object_or_404(Equipment, pk=pk)

        equipment.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        # Check user
        user = request.auth.user
        if user.is_superuser:
            equipment = Equipment.objects.all()
        else:
            researcher = Researcher.objects.get(user=user)
            restricted = request.query_params.get("restricted")
            if restricted == "access":
                has_lab_access = Q(equipment_labs__lab__researchers=researcher)
                has_requested_access = Q(access_requests__researcher=researcher)
                has_approved_access = Q(access_requests__approved=True)

                # equipment = Equipment.objects.filter(equipment_labs__lab=researcher.lab)
                equipment = Equipment.objects.filter(
                    has_lab_access | (has_requested_access & has_approved_access)
                ).distinct()
            else:
                equipment = Equipment.objects.all()

        # Get optional query params
        availability = request.query_params.get("status")
        lab_id = request.query_params.get("lab_id")
        search_name = request.query_params.get("name")

        # Filter by status
        if availability is not None:
            if availability == "archived":
                equipment = equipment.filter(archived=True)
            if availability == "active":
                equipment = equipment.filter(archived=False)

        # Filter by lab
        if lab_id is not None:
            equipment = equipment.filter(equipment_labs__lab__id=lab_id)

        # Filter by name
        if search_name is not None:
            equipment = equipment.filter(name__icontains=search_name)

        # Create a serializer instance with the queryset
        serializer = EquipmentListSerializer(
            equipment, context={"request": request}, many=True
        )

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

            # Get list of equipment that the researcher has access to
            has_lab_access = Q(equipment_labs__lab__researchers=researcher)
            has_requested_access = Q(access_requests__researcher=researcher)
            has_approved_access = Q(access_requests__approved=True)

            available_equipment = Equipment.objects.filter(
                has_lab_access | (has_requested_access & has_approved_access)
            ).distinct()

            # Check if the equipment instance is in the queryset of allowed equipment
            allowed = available_equipment.filter(pk=equipment.pk).exists()

            # If not allowed, return error. Otherwise, return equipment details.
            if not allowed:
                return Response(
                    {"error": "You are not authorized to perform this action."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        serializer = EquipmentFullSerializer(equipment, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)
