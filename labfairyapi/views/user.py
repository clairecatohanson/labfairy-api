from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from labfairyapi.models import Researcher
from labfairyapi.serializers import UserResearcherSerializer, SuperUserSerializer


class UserViewSet(ViewSet):
    def list(self, request):
        # Get current user
        current_user = request.auth.user

        # If not superuser, get associated Researcher
        if not current_user.is_superuser:
            researcher = Researcher.objects.get(user=current_user)
            current_user.researcher = researcher
            serializer = UserResearcherSerializer(current_user, many=False)
        else:
            serializer = SuperUserSerializer(current_user, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)
