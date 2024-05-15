from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from labfairyapi.models import Researcher, Lab


class ResearcherViewSet(ViewSet):
    def update(self, request, pk=None):
        researcher = get_object_or_404(Researcher, pk=pk)

        lab_id = request.data.get("lab_id", None)

        if not lab_id:
            return Response(
                {"error": "Missing required fields: lab_id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        lab = get_object_or_404(Lab, pk=lab_id)

        researcher.lab = lab
        researcher.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
