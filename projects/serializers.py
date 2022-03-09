from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


from .models import Comment, Contributor, Issue, Project
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

    def save(self, **kwargs):
        project_instance = super().save(**kwargs)
        author = project_instance.author
        # This saves us headaches with permissions.
        Contributor.objects.create(user=author, project=project_instance)
        return project_instance


class ProjectCreateFormSerializer(serializers.ModelSerializer):
    """
    This is used to pimp the browser API interface.
    """

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
    """
    This is used to pimp the browser API interface.
    """

    user_id = serializers.IntegerField(min_value=1)


class IssueSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(min_value=0, source="author.id")
    project_id = serializers.IntegerField(min_value=0, source="project.id")
    assignee_id = serializers.IntegerField(min_value=0, source="assignee.id")

    class Meta:
        model = Issue
        exclude = ("author", "project", "assignee")

    def create(self, validated_data):
        # We want the validation step to run,
        # but we don't want the nested field representation from source.
        assert hasattr(
            self, "_errors"
        ), "You must call `.is_valid()` before calling `.save()`."
        return Issue.objects.create(**self.initial_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get(
            "description", instance.description
        )
        instance.tag = validated_data.get("tag", instance.tag)
        instance.priority = validated_data.get("priority", instance.priority)
        instance.status = validated_data.get("status", instance.status)
        instance.assignee_id = validated_data.get("assignee", {}).get(
            "id", instance.assignee_id
        )
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
        source="author.id",
        required=False,
    )
    issue_id = serializers.PrimaryKeyRelatedField(
        queryset=Issue.objects.all(), source="issue.id", required=False
    )

    class Meta:
        model = Comment
        exclude = ["author", "issue"]

    def create(self, validated_data):
        # We want the validation step to run,
        # but we don't want the nested field representation from source.
        assert hasattr(
            self, "_errors"
        ), "You must call `.is_valid()` before calling `.save()`."
        return Comment.objects.create(**self.initial_data)

    def update(self, instance, validated_data):
        instance.description = validated_data.get(
            "description", instance.description
        )
        instance.save()
        return instance
