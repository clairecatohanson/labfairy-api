from rest_framework import serializers
from django.contrib.auth.models import User
from labfairyapi.models import Researcher


class SuperUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "is_superuser",
            "is_staff",
        )


class ResearcherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Researcher
        fields = "__all__"


class UserResearcherSerializer(serializers.ModelSerializer):
    researcher = ResearcherSerializer(many=False)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "is_superuser",
            "is_staff",
            "researcher",
        )
