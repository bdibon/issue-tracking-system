from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, mixins, status, renderers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

from .serializers import (
    CommentSerializer,
    ContributorRetrieveSerializer,
    ContributorCreateSerializer,
    IssueSerializer,
    ProjectCreateSerializer,
    ProjectSerializer,
)
from .models import Comment, Issue, Project, Contributor
from .permissions import (
    IsAuthorOrReadOnly,
    IsProjectContributor,
    IsProjectManager,
)
from .renderers import ProjectContributorListRenderer, ProjectCreateRenderer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    A ViewSet to perform CRUD operations on projects.
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    renderer_classes = [renderers.JSONRenderer, ProjectCreateRenderer]

    def create(self, request, *args, **kwargs):
        project_author = request.user
        serializer = ProjectCreateSerializer(
            data={
                "author": project_author.id,
                "title": request.data["title"],
                "description": request.data["description"],
                "type": request.data["type"],
            }
        )

        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # This is not consistent with REST conventions,
    # however as I have been playing with custom renderers
    # I'll allow myself this fantasy.
    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)


class ContributorsListCreateView(generics.ListCreateAPIView):
    """
    List and add contributors to a specific project.
    """

    serializer_class = ContributorRetrieveSerializer
    renderer_classes = [renderers.JSONRenderer, ProjectContributorListRenderer]
    permission_classes = [IsAuthenticated, IsProjectManager]

    def get_queryset(self):
        project_id = self.kwargs.get(self.lookup_field)
        return Contributor.objects.filter(
            project__id__iexact=project_id
        ).prefetch_related("user")

    def create(self, request, *args, **kwargs):
        user_id = request.data["user_id"]
        project_id = kwargs["pk"]
        serializer = ContributorCreateSerializer(
            data={"user": user_id, "project": project_id}
        )

        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContributorRetrieveDeleteView(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """
    Retrieve or destroy a project's contributor.
    """

    serializer_class = ContributorRetrieveSerializer
    permission_classes = [IsAuthenticated, IsProjectManager]

    def get_object(self):
        obj = get_object_or_404(self.get_queryset())
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        project_id = self.kwargs.get("project_id")
        contributor_id = self.kwargs.get("contributor_id")

        return Contributor.objects.filter(
            pk=contributor_id, project__id=project_id
        )

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class IssueListCreateView(generics.ListCreateAPIView):
    """
    List and add issues to a project.
    """

    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor]
    lookup_field = "project_id"

    def get_queryset(self):
        project_id = self.kwargs.get(self.lookup_field)
        return Issue.objects.filter(project__id=project_id)

    def create(self, request, *args, **kwargs):
        project_id = self.kwargs.get(self.lookup_field)
        data = {
            **request.data,
            "project_id": project_id,
            "author_id": request.user.id,
        }
        serializer = IssueSerializer(data=data)

        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update and destroy a project's issues.
    """

    serializer_class = IssueSerializer
    permission_classes = [
        IsAuthenticated,
        IsProjectContributor,
        IsAuthorOrReadOnly,
    ]

    def get_object(self):
        project_id = self.kwargs.get("project_id")
        issue_id = self.kwargs.get("issue_id")
        query_set = Issue.objects.filter(pk=issue_id, project_id=project_id)
        issue = get_object_or_404(query_set)

        self.check_object_permissions(self.request, issue)

        return issue


class CommentListCreateView(generics.ListCreateAPIView):
    """
    List and add comments to an issue.
    """

    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticated,
        IsProjectContributor,
    ]

    def get_queryset(self):
        project_id = self.kwargs.get("project_id")
        issue_id = self.kwargs.get("issue_id")
        issue = Issue.objects.filter(pk=issue_id, project_id=project_id)[:1]
        return Comment.objects.filter(issue=issue)

    def create(self, request, *args, **kwargs):
        if not self.get_queryset().exists():
            raise serializers.ValidationError()

        issue_id = self.kwargs.get("issue_id")
        serializer = CommentSerializer(
            data={
                "author_id": request.user.id,
                "issue_id": issue_id,
                "description": request.data["description"],
            }
        )

        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a commment.
    """

    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticated,
        IsProjectContributor,
        IsAuthorOrReadOnly,
    ]

    def get_object(self):
        project_id = self.kwargs.get("project_id")
        issue_id = self.kwargs.get("issue_id")
        comment_id = self.kwargs.get("comment_id")

        issue_query_set = Issue.objects.filter(
            pk=issue_id, project_id=project_id
        )[:1]
        comment_query_set = Comment.objects.filter(
            pk=comment_id, issue=issue_query_set
        )

        comment = get_object_or_404(comment_query_set)
        self.check_object_permissions(self.request, comment)

        return comment
