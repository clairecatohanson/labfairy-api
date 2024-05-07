from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from labfairyapi.models import Researcher, Equipment, ResearcherEquipment
from labfairyapi.serializers import ResearcherEquipmentSerializer


class ResearcherEquipmentViewSet(ViewSet):
    def create(self, request):
        # Get researcher
        researcher = Researcher.objects.get(user=request.auth.user)

        # Check for required keys in the request body
        equipment_id = request.data.get("equipment_id")
        training_date = request.data.get("training_date")

        if not equipment_id or not training_date:
            return Response(
                {"error": "Missing required fields: equipment_id and/or training_date"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Try to get equipment instance
        equipment = get_object_or_404(Equipment, pk=equipment_id)

        # Check for duplicate ResearcherEquipment instance
        try:
            found_researcher_equipment = ResearcherEquipment.objects.get(
                researcher=researcher, equipment=equipment
            )
            return Response(
                {"error": "The provided researcher equipment request already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ResearcherEquipment.DoesNotExist:
            # Try to create a new ResearcherEquipment instance
            try:
                new_researcher_equipment = ResearcherEquipment.objects.create(
                    researcher=researcher,
                    equipment=equipment,
                    training_date=training_date,
                )
                new_researcher_equipment.save()
            except ValidationError as e:
                return Response(
                    {"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST
                )

            # Serialize the ResearcherEquipment
            serializer = ResearcherEquipmentSerializer(
                new_researcher_equipment, many=False
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        # Get user
        user = request.auth.user

        # Get ResearcherEquipment instances available to the user
        if user.is_superuser:
            requests = ResearcherEquipment.objects.all()

        else:
            researcher = Researcher.objects.get(user=user)
            requests = ResearcherEquipment.objects.filter(researcher=researcher)

        # Get optional query params and filter
        progress = request.query_params.get("progress", None)

        if progress is not None:
            if progress == "pending":
                requests = requests.filter(approved=False)
            if progress == "approved":
                requests = requests.filter(approved=True)

        # Order by training date
        requests = requests.order_by("training_date")

        # Serialize the ResearcherEquipment
        serializer = ResearcherEquipmentSerializer(requests, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        # Try to find the requested instance
        researcher_equipment = get_object_or_404(ResearcherEquipment, pk=pk)

        # Get the user
        user = request.auth.user

        if not user.is_superuser:
            researcher = Researcher.objects.get(user=user)
            if researcher_equipment.researcher != researcher:
                return Response(
                    {"error": "You are not authorized to perform this action."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        researcher_equipment.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None):
        # admin only
        user = request.auth.user
        if not user.is_superuser:
            return Response(
                {"error": "You are not authorized to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Check for required keys in the request body
        approved = request.data.get("approved", None)

        if approved == None or approved == "":
            return Response(
                {"error": "Missing required fields: approved"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Try to find the requested instance
        researcher_equipment = get_object_or_404(ResearcherEquipment, pk=pk)

        # Update the instance
        researcher_equipment.approved = approved
        researcher_equipment.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
