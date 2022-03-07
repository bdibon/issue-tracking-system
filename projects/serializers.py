from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


from .models import Contributor, Project
from accounts.serializers import CustomUserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class ProjectCreateSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all()
    )

    class Meta:
        model = Project
        fields = ["title", "description", "type", "author"]


class ProjectCreateFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["title", "description", "type"]


class ContributorRetrieveSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    project = ProjectSerializer()

    class Meta:
        model = Contributor
        fields = ["id", "user", "project"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        new_representation = {}

        for field in representation["user"]:
            new_field = "user_id" if field == "id" else field
            new_representation[new_field] = representation["user"][field]

        new_representation["contributor_id"] = representation["id"]
        new_representation["project_id"] = representation["project"]["id"]

        return new_representation


class ContributorCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all()
    )
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all()
    )

    class Meta:
        model = Contributor
        fields = ["user", "project"]
        validators = [
            UniqueTogetherValidator(
                queryset=Contributor.objects.all(), fields=["user", "project"]
            )
        ]


class ContributorCreateFormSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(min_value=1)
