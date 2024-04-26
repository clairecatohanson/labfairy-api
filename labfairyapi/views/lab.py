from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from labfairyapi.models import Lab
from labfairyapi.serializers import LabSerializer


class LabViewSet(ViewSet):
    def list(self, request):
        all_labs = Lab.objects.all()

        serializer = LabSerializer(all_labs, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
